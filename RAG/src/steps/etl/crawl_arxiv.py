import datetime
import json
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Annotated

import arxiv
import pandas as pd
import requests
from loguru import logger
from zenml import get_step_context
from zenml.steps import step

from sp_rag.utils import NumpyEncoder


def _clean_categories(raw_cats: list[str]) -> list[str]:
    """Splits category strings on commas or semicolons and returns a list of cleaned category strings."""
    return [c.strip() for cat in raw_cats for c in re.split(r"[;,]", cat) if c.strip()]


def _build_metadata(
    papers: list[dict],
    categories: list[str],
    keyword: str,
    target_date: datetime.date,
    final_query: str,
) -> dict:
    """
    Build metadata for the search results.
    """
    total_papers = len(papers)
    cat_counts = Counter()
    dist_counts = Counter()
    for paper in papers:
        cats = paper.get("categories", [])
        cat_counts.update(cats)
        dist_counts[len(cats)] += 1
    return {
        "query": {
            "categories_searched": categories,
            "keyword_searched": keyword,
            "target_date": target_date.isoformat(),
            "final_query": final_query,
        },
        "retrieved": {
            "papers_found": total_papers,
            "category_counts": dict(cat_counts),
            "category_distribution": dict(dist_counts),
        },
    }


@step
def search_papers(
    categories: str | list[str],
    keyword: str = "",
    date: str = "",
    max_results: int | None = 1000,
) -> Annotated[pd.DataFrame, "papers_metadata"]:
    """
    Search for papers on arXiv and return a DataFrame of metadata (title, authors, abstract, etc.).
    """
    if not date:
        target_date = datetime.date.today()
    else:
        target_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

    if isinstance(categories, str):
        categories = [categories]

    categories_query = (
        " OR ".join(f"cat:{cat}" for cat in categories) if categories else ""
    )
    if categories_query and keyword:
        query = f"({categories_query}) AND {keyword}"
    elif categories_query:
        query = categories_query
    else:
        query = keyword

    if max_results == -1:
        max_results = None

    logger.info(f"Searching for papers from {target_date} with query: '{query}'")
    search_query = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
        sort_order=arxiv.SortOrder.Descending,
    )
    client = arxiv.Client(page_size=200, delay_seconds=10)

    papers = []
    try:
        for result in client.results(search_query):
            if result.published.date() >= target_date:
                paper_id = result.entry_id.split("/")[-1]
                pdf_url = getattr(
                    result, "pdf_url", f"http://arxiv.org/pdf/{paper_id}.pdf"
                )
                cleaned_cats = _clean_categories(result.categories or [])
                authors = [author.name for author in result.authors]
                papers.append(
                    {
                        "paper_id": paper_id,
                        "title": result.title,
                        "authors": authors,
                        "abstract": result.summary,
                        "published_date": result.published.date().strftime("%Y-%m-%d"),
                        "pdf_url": pdf_url,
                        "categories": cleaned_cats,
                    }
                )
    except arxiv.UnexpectedEmptyPageError as exc:
        logger.info(f"Cannot find more papers: {exc}")

    metadata = _build_metadata(papers, categories, keyword, target_date, query)
    logger.info(f"Found {metadata['retrieved']['papers_found']} papers.")
    df = pd.DataFrame(papers)
    get_step_context().add_output_metadata(
        output_name="papers_metadata", metadata=metadata
    )
    return df


def download_pdf(paper: dict, save_dir: Path) -> bool:
    """
    Helper to download a single paper PDF.
    """
    paper_id = paper["paper_id"]
    pdf_url = paper["pdf_url"]
    filename = f"{paper_id}.pdf"
    file_path = save_dir / filename

    if file_path.exists():
        logger.info(f"PDF '{filename}' exists; skipping download.")
        return False

    try:
        logger.info(f"Downloading PDF for paper '{paper_id}' from {pdf_url}")
        response = requests.get(pdf_url, timeout=30)
        response.raise_for_status()
        file_path.write_bytes(response.content)
        logger.info(f"Downloaded '{filename}'")
        return True
    except Exception as exc:
        logger.error(f"Failed to download paper '{paper_id}': {exc}")
        return False


@step
def download_papers(
    papers_df: pd.DataFrame, save_path: str | Path
) -> Annotated[pd.DataFrame, "download_summary"]:
    """
    Download PDFs for the papers in the DataFrame.
    :param papers_df:
    :param save_path:
    :return:
    """
    save_dir = Path(save_path)
    save_dir.mkdir(parents=True, exist_ok=True)
    downloaded_count = 0

    # Use ThreadPoolExecutor for IO-bound downloads
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_paper = {
            executor.submit(download_pdf, paper_row.to_dict(), save_dir): paper_row
            for _, paper_row in papers_df.iterrows()
        }
        for future in as_completed(future_to_paper):
            if future.result():
                downloaded_count += 1

    logger.info(f"Downloaded {downloaded_count} new paper(s) into '{save_dir}'")
    get_step_context().add_output_metadata(
        output_name="download_summary",
        metadata={
            "downloaded_count": downloaded_count,
            "save_directory": str(save_dir),
        },
    )
    return papers_df


@step
def save_paper_metadata(
    papers_df: pd.DataFrame, save_path: str | Path
) -> Annotated[None, "individual_metadata_files"]:
    """
    Save metadata for each paper in the DataFrame as a JSON file.
    :param papers_df:
    :param save_path:
    :return:
    """
    save_dir = Path(save_path)
    save_dir.mkdir(parents=True, exist_ok=True)

    for _, paper in papers_df.iterrows():
        paper_id = paper["paper_id"]
        json_filename = f"{paper_id}.json"
        json_filepath = save_dir / json_filename
        try:
            # Use built-in open with explicit string conversion for the path.
            with open(json_filepath, "w") as f:
                json.dump(
                    paper.to_dict(), f, indent=2, ensure_ascii=False, cls=NumpyEncoder
                )
            logger.info(f"Saved metadata for paper '{paper_id}' as '{json_filename}'")
        except Exception as exc:
            logger.error(f"Failed to save JSON for paper '{paper_id}': {exc}")
