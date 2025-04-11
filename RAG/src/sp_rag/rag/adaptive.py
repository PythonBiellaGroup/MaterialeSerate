import uuid
from typing import TypedDict

from langchain import hub
from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.prompts.chat import HumanMessagePromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from loguru import logger

from sp_rag import settings
from sp_rag.core.graders import (
    AnswerGrader,
    HallucinationGrader,
    RetrievalGrader,
)
from sp_rag.core.retrievers import RetrieverFactory

from .base import BaseRAG


class AdaptiveState(TypedDict):
    question: str
    documents: list[Document]
    generation: str | None


class AdaptiveRAG(BaseRAG):
    """
    An adaptive Retrieval-Augmented Generation pipeline with multiple processing steps.
    """

    def __init__(self, vectorstore, retrieval_strategy):
        logger.info("Initializing AdaptiveRAG pipeline...")

        self.retriever = RetrieverFactory.get_retriever(retrieval_strategy, vectorstore)
        self.llm = init_chat_model(**settings.CHAT_MODEL_KWARGS)

        self.retrieval_grader = RetrievalGrader()
        self.answer_grader = AnswerGrader()
        self.hallucination_grader = HallucinationGrader()

        self.rag_prompt = hub.pull("rlm/rag-prompt")
        self.rag_chain = self.rag_prompt | self.llm | StrOutputParser()

        re_write_prompt = ChatPromptTemplate(
            [
                SystemMessage(
                    "You are a question re-writer that converts an input question to a better version optimized for vectorstore retrieval."
                    "Look at the input and try to reason about the underlying semantic intent or meaning."
                ),
                HumanMessagePromptTemplate(
                    prompt=PromptTemplate(
                        template="Here is the initial question: \n\n {question} \n Formulate an improved question.",
                        input_variables=["question"],
                    )
                ),
            ]
        )
        llm_rewriter = init_chat_model(**settings.CHAT_MODEL_KWARGS)
        self.question_rewriter = re_write_prompt | llm_rewriter | StrOutputParser()

        self.memory = MemorySaver()
        self._thread_id = str(uuid.uuid4())

        self.graph = self._build_graph()

    def retrieve(self, state: AdaptiveState):
        logger.info("Starting retrieval step.")
        question = state["question"]
        documents = self.retriever.invoke(question)
        return {"documents": documents, "question": question, "generation": None}

    def grade_documents(self, state: AdaptiveState):
        logger.info("Grading document relevance.")
        question = state["question"]
        documents = state["documents"]
        filtered_docs = []
        for d in documents:
            result = self.retrieval_grader.grade(question, d.page_content)
            if result.binary_score == "yes":
                logger.info("Document deemed relevant.")
                filtered_docs.append(d)
            else:
                logger.info("Document deemed not relevant.")
        return {"documents": filtered_docs, "question": question, "generation": None}

    def generate(self, state: AdaptiveState):
        logger.info("Generating answer.")
        question = state["question"]
        documents = state["documents"]
        generation = self.rag_chain.invoke({"context": documents, "question": question})
        return {"documents": documents, "question": question, "generation": generation}

    def transform_query(self, state: AdaptiveState):
        logger.info("Transforming query for improved retrieval.")
        question = state["question"]
        better_question = self.question_rewriter.invoke({"question": question})
        return {
            "documents": state["documents"],
            "question": better_question,
            "generation": None,
        }

    def decide_next_step(self, state: AdaptiveState):
        logger.info("Assessing documents to decide next step.")
        filtered_documents = state["documents"]
        if not filtered_documents:
            logger.info("No relevant documents found; proceeding to transform query.")
            return "transform_query"
        else:
            logger.info("Relevant documents found; proceeding to generate answer.")
            return "generate"

    def validate_generation(self, state: AdaptiveState):
        logger.info("Validating generation quality and grounding.")
        question = state["question"]
        documents = state["documents"]
        generation = state["generation"]
        docs_text = "\n\n".join([d.page_content for d in documents])
        hallucination_result = self.hallucination_grader.grade(docs_text, generation)
        if hallucination_result.binary_score == "yes":
            logger.info("Generation is well-grounded in documents.")
            answer_result = self.answer_grader.grade(question, generation)
            if answer_result.binary_score == "yes":
                logger.info("Generation adequately addresses the question.")
                return "useful"
            else:
                logger.info("Generation does not sufficiently address the question.")
                return "not useful"
        else:
            logger.info(
                "Generation is not sufficiently grounded in the documents; retrying generation."
            )
            return "not supported"

    def _build_graph(self):
        workflow = StateGraph(AdaptiveState)
        workflow.set_entry_point("retrieve")

        workflow.add_node("retrieve", self.retrieve)
        workflow.add_node("grade_documents", self.grade_documents)
        workflow.add_node("generate", self.generate)
        workflow.add_node("transform_query", self.transform_query)

        workflow.add_edge("retrieve", "grade_documents")
        workflow.add_conditional_edges(
            "grade_documents",
            self.decide_next_step,
            {
                "transform_query": "transform_query",
                "generate": "generate",
            },
        )
        workflow.add_edge("transform_query", "retrieve")
        workflow.add_conditional_edges(
            "generate",
            self.validate_generation,
            {
                "not supported": "generate",
                "useful": END,
                "not useful": "transform_query",
            },
        )

        return workflow.compile(checkpointer=self.memory)

    def invoke(self, user_input: str) -> str:
        logger.info(f"Invoking AdaptiveRAG pipeline with question: {user_input}")
        state = self.graph.invoke(
            {"question": user_input},
            config={"configurable": {"thread_id": self._thread_id}},
        )

        if "generation" in state and state["generation"]:
            return state["generation"]
        elif "documents" in state:
            return "\n".join([str(doc) for doc in state["documents"]])
        else:
            return "No generation available."
