# 📚 Scientific Papers RAG

[![en](https://img.shields.io/badge/lang-en-red.svg)](./README.md)
[![it](https://img.shields.io/badge/lang-it-blue.svg)](./README.it.md)

Un’introduzione alla **Retrieval-Augmented Generation (RAG)** per articoli scientifici utilizzando **LangChain**, **Qdrant**, **ZenML**, e **LangSmith**. Questo progetto dimostra come recuperare, preprocessare, incorporare e recuperare contenuti scientifici da **ArXiv**, fornendo una pipeline RAG semplificata con interfacce sia in notebook che web.

---

## 🚀 Funzionalità

-   **📥 Recupero Articoli**: Scarica automaticamente articoli di ricerca da **ArXiv**.
-   **🧹 Pipeline di Preprocessing**: Pulisce e suddivide i documenti PDF in chunk utilizzando step modulari di ZenML.
-   **📚 Archivio Vettoriale**: Incorpora i documenti e li salva in **Qdrant**.
-   **🧠 Varianti RAG**: Supporta pipeline RAG **semplici**, **adattive** e **agentiche**.
-   **🌐 Interfaccia Web**: Interagisci con la pipeline tramite un'app **Streamlit**.
-   **🧪 Notebook**: Esplora e confronta strategie di recupero in notebook pronti all'uso.
-   **🧑‍🔬 LangSmith**: Monitora la pipeline di recupero e generazione.

---

## 🏗️ Struttura del Progetto

```
├── configs/                # Configurazioni YAML per download ArXiv e inserimento nel DB vettoriale
├── docker-compose.yaml     # Avvia Qdrant
├── notebooks/              # Notebook Jupyter per esplorare i componenti
├── src/
│   ├── pipelines/          # Definizioni delle pipeline ZenML
│   ├── sp_rag/             # Logica principale dell'app
│   │   ├── core/           # Retriever, valutatori di rilevanza
│   │   ├── rag/            # Implementazioni RAG (semplice, adattiva, agentica)
│   │   ├── utils/          # Encoder e utility
│   │   ├── vectordb/       # Logica di interazione con Qdrant
│   │   └── webapp/         # Interfaccia Streamlit
│   ├── steps/etl/          # Step ZenML (caricamento, pulizia, chunking, ingestione)
│   └── webapp/             # Webapp
├── tools/                  # Script runner e entrypoint CLI
└── pyproject.toml          # Metadati del progetto e dipendenze
```

---

## ⚡ Avvio Rapido

### 0️⃣ Configurazione

Imposta le variabili d’ambiente in `.env`, usando `.env.example` come modello.
Modifica il modello utilizzato e i parametri di ingestione in `src/sp_rag/settings.py`.

### 1️⃣ Installa le Dipendenze

```bash
uv venv .venv        # Crea un ambiente virtuale
uv sync              # Installa le dipendenze del progetto
```

### 2️⃣ Avvia Qdrant (Database Vettoriale) e ZenML

```bash
docker-compose up -d qdrant
zenml login --local
```
oppure alternativamente, usa `poe`:

```bash
poe start
```


### 3️⃣ Scarica Articoli da ArXiv

```bash
poe download-arxiv
```

Personalizza la query di ricerca in: `configs/arxiv_paper_download.yaml`

### 4️⃣ Inserisci nel Database Vettoriale

```bash
poe load-to-qdrant
```

Questo include pulizia, suddivisione in chunk, embedding e salvataggio in **Qdrant**.

---

## 🧪 Notebook

Esplora componenti e strategie della pipeline:

-   `01_pdf_processing_notebook.ipynb`: Caricamento, pulizia e suddivisione dei PDF
-   `02_retriever_methods_comparison.ipynb`: Confronto tra retriever densi, sparsi e ibridi
-   `03_query_retrieval_strategies.ipynb`: Test di diverse strategie di generazione query

---

## 🛠️ Panoramica Pipeline

🔹 **Crawl & Download** – Scarica articoli da ArXiv

🔹 **Clean & Chunk** – Trasforma PDF in testo strutturato

🔹 **Embed & Store** – Utilizza modelli di embedding (HuggingFace e FastEmbed) e salva in Qdrant

🔹 **Retrieve & Generate** – LangChain + LangGraph per varianti RAG

🔹 **Grade & Filter** – Usa valutatori di rilevanza per affinare il contesto

🔹 **Monitoring** – Monitora la pipeline con LangSmith

---

## 🎨 Anteprima Web App

Avvia l'interfaccia RAG interattiva:

```bash
poe webapp
```

🔍 Usa questa UI per eseguire query sul tuo database vettoriale e visualizzare segmenti di articoli e riassunti.

---

## 📜 Licenza

Questo progetto è distribuito sotto licenza **GPLv3**.

---

🧠 Creato per esplorare sistemi di recupero scientifico su larga scala.
🚀 **Buona Ricerca!**
