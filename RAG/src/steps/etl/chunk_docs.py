from typing import Annotated

import numpy as np
from langchain_core.documents import Document
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)
from loguru import logger
from tqdm import tqdm
from transformers import AutoTokenizer
from zenml import get_step_context, step

from sp_rag import settings


@step
def chunk_docs(
    docs: list[Document], chunk_size: int, chunk_overlap: int
) -> Annotated[list[dict], "chunked_docs"]:
    """
    Chunk the documents into smaller pieces using RecursiveCharacterTextSplitter.
    :param docs:
    :param chunk_size:
    :param chunk_overlap:
    :return:
    """
    logger.info(f"Chunking documents with tokenizer: {settings.DENSE_EMBEDDING_MODEL}")
    text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        AutoTokenizer.from_pretrained(settings.DENSE_EMBEDDING_MODEL),
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
        strip_whitespace=True,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    split_documents = []
    sizes = []
    for doc in tqdm(docs):
        chunks = text_splitter.split_text(doc.page_content)
        for i, chunk in enumerate(chunks):
            new_metadata = doc.metadata.copy() if doc.metadata else {}
            new_metadata["chunk_index"] = i
            sizes.append(len(chunk))
            split_doc = {"page_content": chunk, "metadata": new_metadata}
            split_documents.append(split_doc)

    get_step_context().add_output_metadata(
        output_name="chunked_docs",
        metadata={
            "num_chunks": len(split_documents),
            "chunking_method": type(text_splitter).__name__,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "avg_chunk_size": float(np.mean(sizes)),
            "std_chunk_size": float(np.std(sizes)),
            "max_chunk_size": float(np.max(sizes)),
            "min_chunk_size": float(np.min(sizes)),
            "median_chunk_size": float(np.median(sizes)),
        },
    )
    logger.info(f"Chunked {len(docs)} documents into {len(split_documents)} chunks.")
    return split_documents
