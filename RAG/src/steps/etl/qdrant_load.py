import logging
from uuid import uuid4

from zenml import step

from sp_rag.vectordb import QdrantVectorDB


@step
def qdrant_load(
    chunked_docs: list[dict], qdrant_url: str, qdrant_collection: str
) -> None:
    db = QdrantVectorDB(url=qdrant_url, collection=qdrant_collection)
    logging.info("Loading documents into Qdrant")
    # client = QdrantClient(location=qdrant_url)
    ids = [str(uuid4()) for _ in range(len(chunked_docs))]
    texts = [doc["page_content"] for doc in chunked_docs]
    metadata = [doc["metadata"] for doc in chunked_docs]
    # client.add(collection_name=qdrant_collection, documents=texts, metadata=metadata, ids=ids)
    db.vector_store.add_texts(texts=texts, metadatas=metadata, ids=ids)
    return
