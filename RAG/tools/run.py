import subprocess
import sys
from pathlib import Path
from typing import Any

import click

from src.pipelines import arxiv_paper_download, ingest_to_vector_db


@click.command()
@click.option(
    "--no_cache",
    is_flag=True,
    default=False,
    help="Disable caching for the pipeline run.",
)
@click.option(
    "--download_arxiv", is_flag=True, default=False, help="Categories to search in."
)
@click.option(
    "--load_to_qdrant",
    is_flag=True,
    default=False,
    help="Load the downloaded papers to Qdrant.",
)
@click.option(
    "--webapp", is_flag=True, default=False, help="Run the Streamlit web app."
)
def main(no_cache: bool, download_arxiv: bool, load_to_qdrant: bool, webapp: bool):
    pipeline_args: dict[str, Any] = {
        "enable_cache": not no_cache,
    }

    root_dir = Path(__file__).resolve().parent.parent
    run_args = {}

    if download_arxiv:
        pipeline_args["config_path"] = (
            root_dir / "configs" / "arxiv_paper_download.yaml"
        )
        arxiv_paper_download.with_options(**pipeline_args)(**run_args)

    if load_to_qdrant:
        pipeline_args["config_path"] = root_dir / "configs" / "ingest_to_vector_db.yaml"
        ingest_to_vector_db.with_options(**pipeline_args)(**run_args)

    if webapp:
        app_path = root_dir / "src" / "webapp" / "main.py"
        subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)])


if __name__ == "__main__":
    main()
