# 📚 Scientific Papers RAG

[![en](https://img.shields.io/badge/lang-en-red.svg)](./README.md)
[![it](https://img.shields.io/badge/lang-it-blue.svg)](./README.it.md)

An **Introduction to Retrieval-Augmented Generation (RAG)** for scientific papers using **LangChain**, **Qdrant**, **ZenML**, and **LangSmith**. This project demonstrates how to fetch, preprocess, embed, and retrieve scientific content from **ArXiv**, providing a streamlined RAG pipeline with both notebook and web interfaces.

---

## 🚀 Features

-   **📥 Paper Retrieval**: Automatically fetches research papers from **ArXiv**.
-   **🧹 Preprocessing Pipeline**: Cleans and chunks PDF documents using modular ZenML steps.
-   **📚 Vector Storage**: Embeds documents and stores them in **Qdrant**.
-   **🧠 RAG Variants**: Supports **simple**, **adaptive**, and **agentic** retrieval-augmented generation pipelines.
-   **🌐 Web UI**: Interact with the pipeline using a **Streamlit** app.
-   **🧪 Notebooks**: Explore and compare retrieval strategies in ready-to-run notebooks.
-   **🧑‍🔬 LangSmith**: Monitor the retrieval and generation pipeline.

---

## 🏗️ Project Structure

```
├── configs/                # YAML configs for ArXiv fetching & vector DB ingestion
├── docker-compose.yaml     # Starts Qdrant
├── notebooks/              # Jupyter notebooks to explore components
├── src/
│   ├── pipelines/          # ZenML pipeline definitions
│   ├── sp_rag/             # Core app logic
│   │   ├── core/           # Retrievers, graders
│   │   ├── rag/            # RAG implementations (simple, adaptive, agentic)
│   │   ├── utils/          # Encoders & helper utilities
│   │   ├── vectordb/       # Qdrant interaction logic
│   │   └── webapp/         # Streamlit-based UI
│   ├── steps/etl/          # ZenML steps (load, clean, chunk, ingest)
│   └── webapp/             # Webapp
├── tools/                  # Script runner & CLI entrypoints
└── pyproject.toml          # Project metadata & dependencies
```

---

## ⚡ Quickstart

### 0️⃣ Settings

Set up your environment variables in `.env`, use `.env.example` as a template.
Change the model used, and ingention parameters in `src/sp_rag/settings.py`.

### 1️⃣ Install Dependencies

```bash
uv venv .venv        # Create a virtual environment
uv sync              # Install project dependencies
```

### 2️⃣ Start Qdrant (Vector DB) and ZenML

```bash
docker-compose up -d qdrant
zenml login --local
```
or alternatively, use poe
```bash
poe start
```

### 3️⃣ Download ArXiv Papers

```bash
poe download-arxiv
```

Customize the search query in: `configs/arxiv_paper_download.yaml`

### 4️⃣ Ingest into Vector DB

```bash
poe load-to-qdrant
```

This includes cleaning, chunking, embedding, and storing in **Qdrant**.

---

## 🧪 Notebooks

Explore pipeline components and strategies:

-   `01_pdf_processing_notebook.ipynb`: End-to-end PDF loading, cleaning, and chunking
-   `02_retriever_methods_comparison.ipynb`: Compare dense, sparse, and hybrid retrievers
-   `03_query_retrieval_strategies.ipynb`: Test different query generation

---

## 🛠️ Pipeline Overview

🔹 **Crawl & Download** – Pull papers from ArXiv

🔹 **Clean & Chunk** – Convert PDFs into structured text

🔹 **Embed & Store** – Use Embeddings models (HuggingFace and FastEmbed) and load in Qdrant

🔹 **Retrieve & Generate** – LangChain + LangGraph for RAG variants

🔹 **Grade & Filter** – Use relevance graders to refine context

🔹 **Monitoring** – Use LangSmith to monitor the retrieval and generation pipeline

---

## 🎨 Web App Preview

Launch the interactive RAG interface:

```bash
poe webapp
```

🔍 Use this UI to run queries over your vector database and view retrieved paper segments and summaries.

---

## 📜 License

This project is licensed under the **GPLv3 License**.

---

🧠 Built for exploring large-scale scientific retrieval systems.
🚀 **Happy Researching!**
