from typing import Annotated

from langchain_core.documents import Document
from tqdm import tqdm
from unstructured.cleaners.core import clean
from zenml import get_step_context, step


@step
def clean_docs(docs: list[Document]) -> Annotated[list[Document], "cleaned_docs"]:
    """
    Clean the documents.
    :param docs: List of documents.
    :return: None
    """
    for doc in tqdm(docs):
        doc.page_content = clean(
            doc.page_content, bullets=True, extra_whitespace=True, dashes=False
        )
    get_step_context().add_output_metadata(
        output_name="cleaned_docs", metadata={"num_docs": len(docs)}
    )
    return docs
