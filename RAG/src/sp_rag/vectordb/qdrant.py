from typing import Any

from langchain_core.vectorstores import VectorStoreRetriever
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    SparseIndexParams,
    SparseVectorParams,
    VectorParams,
)

from sp_rag import settings


class QdrantVectorDB:
    def __init__(self, url: str, collection: str):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.DENSE_EMBEDDING_MODEL
        )
        self.sparse_embeddings = FastEmbedSparse(
            model_name=settings.SPARSE_EMBEDDING_MODEL
        )
        self.url = url
        self.collection = collection
        self.create()

    @property
    def vector_store(self) -> QdrantVectorStore:
        return QdrantVectorStore.from_existing_collection(
            url=self.url,
            collection_name=self.collection,
            embedding=self.embeddings,
            sparse_embedding=self.sparse_embeddings,
            sparse_vector_name="sparse_vector",
            retrieval_mode=RetrievalMode.HYBRID,
        )

    def get_retriever(self, **kwargs: Any) -> VectorStoreRetriever:
        return self.vector_store.as_retriever(**kwargs)

    @property
    def dense_embedding_size(self):
        return len(self.embeddings.embed_documents(["get_size_string"])[0])

    def create(self):
        client = QdrantClient(location=self.url)

        if not client.collection_exists(self.collection):
            client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=self.dense_embedding_size, distance=Distance.COSINE
                ),
                sparse_vectors_config={
                    "sparse_vector": SparseVectorParams(
                        index=SparseIndexParams(
                            on_disk=False,
                        )
                    )
                },
            )
