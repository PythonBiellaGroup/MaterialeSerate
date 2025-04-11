from langchain.chat_models import init_chat_model
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

from sp_rag import settings
from sp_rag.core.retrievers import RetrievalStrategy, RetrieverFactory

from .base import BaseRAG


class SimpleRAG(BaseRAG):
    """
    A basic Retrieval-Augmented Generation pipeline that retrieves context and generates an answer.
    """

    def __init__(self, vectorstore, retrieval_strategy: RetrievalStrategy):
        self.vectorstore = vectorstore
        self.retrieval_strategy = retrieval_strategy
        self.retriever = RetrieverFactory.get_retriever(retrieval_strategy, vectorstore)
        self.llm = init_chat_model(**settings.CHAT_MODEL_KWARGS)

        self.template = (
            "You are a helpful and knowledgeable assistant. Use the context provided below to answer the question.\n"
            'If the answer is not present in the context, please respond with "I don\'t know."\n\n'
            "Context:\n{context}\n\n"
            "Question:\n{question}\n\n"
            "Answer:\n"
        )

        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=self.template,
        )

    def invoke(self, query: str):
        chain = (
            RunnableLambda(
                lambda query: {
                    "context": self.retriever.invoke(str(query)),
                    "question": query,
                }
            )
            | self.prompt
            | self.llm
        )

        response = chain.invoke(query)
        return response
