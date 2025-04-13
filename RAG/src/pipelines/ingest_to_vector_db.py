from pathlib import Path

from zenml import pipeline

from sp_rag.settings import settings
from steps.etl import (
    add_metadata,
    chunk_docs,
    clean_docs,
    load_docs,
    load_docs_metadata,
    qdrant_load,
)


@pipeline()
def ingest_to_vector_db(
    files_path: str, qdrant_url: str, qdrant_collection: str
) -> None:
    """
    Pipeline to load data into Qdrant.
    :return: None
    """
    docs = load_and_process_docs(files_path)
    chunked_docs = chunk_docs(
        docs, chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP
    )
    qdrant_load(chunked_docs, qdrant_url, qdrant_collection)
    return


@pipeline()
def load_and_process_docs(path: str | Path):
    """
    Load and process documents.
    :param path:
    :return:
    """

    docs = load_docs(Path(path) / "pdfs")
    metadata = load_docs_metadata(Path(path) / "metadata")
    docs = add_metadata(docs, metadata)
    docs = clean_docs(docs)

    return docs
