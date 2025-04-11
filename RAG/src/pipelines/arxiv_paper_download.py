from pathlib import Path

from zenml import pipeline

from steps.etl import download_papers, save_paper_metadata, search_papers


@pipeline(enable_cache=False)
def arxiv_paper_download(
    categories: str | list[str],
    keyword: str,
    date_since: str,
    save_path: str,
    max_results: int = 1000,
):
    """
    Pipeline to search and download papers from arXiv.
    :param categories: Categories to search in.
    :param keyword: Keyword to search for.
    :param date_since: Date since when to search for papers.
    :param save_path: Output directory to save the downloaded papers.
    :param max_results: Limit on the number of results to retrieve. Set to -1 for no limit.
    :return: None
    """
    papers_df = search_papers(
        categories=categories, keyword=keyword, date=date_since, max_results=max_results
    )
    save_paper_metadata(papers_df, save_path=Path(save_path) / "metadata")
    download_papers(papers_df, save_path=Path(save_path) / "pdfs")
