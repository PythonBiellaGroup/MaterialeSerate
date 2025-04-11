from enum import Enum

from langchain.chains.query_constructor.schema import AttributeInfo
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate
from langchain.retrievers import SelfQueryRetriever
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.schema.messages import SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts.chat import (
    HumanMessagePromptTemplate,
)
from langchain_core.retrievers import BaseRetriever

from sp_rag import settings


class RetrievalStrategy(Enum):
    SIMPLE = "simple"
    MULTI_QUERY = "multi_query"
    SELF_QUERY = "self_query"


class SimpleRetrieverWrapper:
    def __init__(self, vectorstore):
        self.retriever = vectorstore.as_retriever()


class MultiQueryRetrieverWrapper:
    """
    Wrapper around the MultiQueryRetriever to showcase better how it functions.
    """

    def __init__(self, vectorstore, n_queries=3):
        self.prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=(
                        "You are an AI language model assistant. Your task is to generate "
                        "3 different versions of the given user question to retrieve relevant "
                        "documents from a vector database. By generating multiple perspectives on the "
                        "user question, your goal is to help the user overcome some of the limitations "
                        "of distance-based similarity search. Provide these alternative questions separated by newlines."
                    )
                ),
                HumanMessagePromptTemplate(
                    prompt=PromptTemplate(
                        template="Original question: {question}",
                        input_variables=["question"],
                    )
                ),
            ]
        )
        self.retriever = MultiQueryRetriever.from_llm(
            llm=init_chat_model(**settings.CHAT_MODEL_KWARGS),
            retriever=vectorstore.as_retriever(),
            prompt=self.prompt,
        )


class SelfQueryRetrieverWrapper:
    def __init__(self, vectorstore):
        metadata_field_info = [
            AttributeInfo(
                name="paper_id",
                description="The unique identifier of the paper",
                type="string",
            ),
            AttributeInfo(
                name="title", description="The title of the paper", type="string"
            ),
            AttributeInfo(
                name="authors",
                description="A list of authors of the paper",
                type="list of strings",
            ),
            AttributeInfo(
                name="abstract", description="The abstract of the paper", type="string"
            ),
            AttributeInfo(
                name="published_date",
                description="The publication date of the paper",
                type="string",
            ),
            AttributeInfo(
                name="pdf_url",
                description="The URL to access the paper PDF",
                type="string",
            ),
            AttributeInfo(
                name="categories",
                description="The list of Arxiv categories the paper belongs to",
                type="list of strings",
            ),
        ]
        self.retriever = SelfQueryRetriever.from_llm(
            llm=init_chat_model(**settings.CHAT_MODEL_KWARGS),
            vectorstore=vectorstore,
            document_contents="page_content",
            metadata_field_info=metadata_field_info,
        )


class RetrieverFactory:
    _strategy_map = {
        RetrievalStrategy.SIMPLE: SimpleRetrieverWrapper,
        RetrievalStrategy.MULTI_QUERY: MultiQueryRetrieverWrapper,
        RetrievalStrategy.SELF_QUERY: SelfQueryRetrieverWrapper,
    }

    @staticmethod
    def get_retriever(strategy, vectorstore) -> BaseRetriever:
        wrapper_cls = RetrieverFactory._strategy_map.get(strategy)
        if not wrapper_cls:
            raise ValueError(f"Unknown retrieval strategy: {strategy}")
        return wrapper_cls(vectorstore).retriever
