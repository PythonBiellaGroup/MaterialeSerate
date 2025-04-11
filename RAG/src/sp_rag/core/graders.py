from langchain.chat_models import init_chat_model
from langchain.schema.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.prompts.chat import (
    HumanMessagePromptTemplate,
)
from pydantic import BaseModel, Field

from sp_rag import settings


class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )


class RetrievalGrader:
    """
    Grades the relevance of retrieved documents with a binary score.
    """

    def __init__(self):
        self.llm = init_chat_model(**settings.CHAT_MODEL_KWARGS)
        self.structured_llm = self.llm.with_structured_output(GradeDocuments)
        self.prompt = ChatPromptTemplate(
            [
                SystemMessage(
                    "You are a grader assessing the relevance of a retrieved document to a user question.\n"
                    "If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant.\n"
                    "The goal is to filter out erroneous retrievals.\n"
                    "Give a binary score 'yes' or 'no' to indicate whether the document is relevant."
                ),
                HumanMessagePromptTemplate(
                    prompt=PromptTemplate(
                        template="Retrieved document: \n\n {document} \n\n User question: {question}",
                        input_variables=["document", "question"],
                    ),
                ),
            ]
        )
        self.chain = self.prompt | self.structured_llm

    def grade(self, question: str, document: str) -> GradeDocuments:
        return self.chain.invoke({"question": question, "document": document})  # type: ignore


class GradeAnswer(BaseModel):
    """Binary score to assess whether an answer addresses the question."""

    binary_score: str = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )


class AnswerGrader:
    """
    Grades whether an answer adequately addresses the user's question.
    """

    def __init__(self):
        self.llm = init_chat_model(**settings.CHAT_MODEL_KWARGS)
        self.structured_llm = self.llm.with_structured_output(GradeAnswer)
        self.prompt = ChatPromptTemplate(
            [
                SystemMessage(
                    "You are a grader assessing whether an answer addresses or resolves a question.\n"
                    "Give a binary score 'yes' or 'no'. 'Yes' means that the answer resolves the question.",
                ),
                HumanMessagePromptTemplate(
                    prompt=PromptTemplate(
                        template="User question: \n\n {question} \n\n LLM generation: {generation}",
                        input_variables=["question", "generation"],
                    )
                ),
            ]
        )
        self.chain = self.prompt | self.structured_llm

    def grade(self, question: str, generation: str | None) -> GradeAnswer:
        return self.chain.invoke({"question": question, "generation": generation})  # type: ignore


class GradeHallucinations(BaseModel):
    """Binary score for assessing if an answer is grounded in facts."""

    binary_score: str = Field(
        description="Answer is grounded in the facts, 'yes' or 'no'"
    )


class HallucinationGrader:
    """
    Grades whether an answer is properly grounded in the provided documents.
    """

    def __init__(self):
        self.llm = init_chat_model(**settings.CHAT_MODEL_KWARGS)
        self.structured_llm = self.llm.with_structured_output(GradeHallucinations)
        self.prompt = ChatPromptTemplate(
            [
                SystemMessage(
                    "You are a grader assessing whether an LLM generation is grounded in or supported by a set of retrieved facts. Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in the facts."
                ),
                HumanMessagePromptTemplate(
                    prompt=PromptTemplate(
                        template="Set of facts: \n\n {documents} \n\n LLM generation: {generation}",
                        input_variables=["documents", "generation"],
                    )
                ),
            ]
        )
        self.chain = self.prompt | self.structured_llm

    def grade(self, documents: str, generation: str | None) -> GradeHallucinations:
        return self.chain.invoke({"documents": documents, "generation": generation})  # type: ignore
