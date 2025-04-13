import json
from pathlib import Path
from typing import Annotated

import numpy as np
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_core.documents import Document
from tqdm import tqdm
from zenml import get_step_context, step


@step
def load_docs(path: str | Path) -> Annotated[list[Document], "docs"]:
    """
    Load documents from a directory using langchain.
    :param path: Path to the directory containing documents pdf.
    :return: None
    """

    files = list(Path(path).glob("*.pdf"))
    if not files:
        raise ValueError(f"No PDF files found in {path}")

    sizes = []
    docs = []
    for f in tqdm(files):
        loader = UnstructuredPDFLoader(file_path=f, mode="single")
        doc = loader.load()[0]
        docs.append(doc)
        sizes.append(len(doc.page_content))

        get_step_context().add_output_metadata(
            output_name="docs",
            metadata={
                "num_docs": len(docs),
                "path": str(path),
                "avg_doc_size": float(np.mean(sizes)),
                "std_doc_size": float(np.std(sizes)),
                "max_doc_size": float(np.max(sizes)),
                "min_doc_size": float(np.min(sizes)),
                "median_doc_size": float(np.median(sizes)),
            },
        )

    return docs


@step
def load_docs_metadata(path: str | Path) -> Annotated[dict, "paper_metadata"]:
    """
    Load docs metadata from a directory. The metadata is .json file for each document.
    :param path:
    :return:
    """
    if not isinstance(path, Path):
        path = Path(path)

    metadata = {}
    for f in path.glob("*.json"):
        with open(f) as file:
            metadata[f.stem] = json.load(file)

    get_step_context().add_output_metadata(
        output_name="paper_metadata", metadata={"num_metadata": len(metadata)}
    )
    return metadata


@step
def add_metadata(
    docs: list[Document], metadata: dict
) -> Annotated[list[Document], "docs_w_metadata"]:
    """
    Add metadata to the documents.
    :param docs: List of documents.
    :param metadata: Dict of metadata.
    :return: None
    """
    for doc in docs:
        paper_id = Path(doc.metadata["source"]).stem
        doc.metadata = doc.metadata | metadata[paper_id]
    return docs
