# Percorso Dati

Serie di 4 serate che hanno come obiettivo lo sviluppo di una semplice soluzione di analisi dei dati partendo da un dataset open source (Rome Airbnb Data).
Le serate saranno tenute da:
- Andrea Melloncelli
- Andrea Guzzo

Lo scopo della serata è quella di simulare un processo di analisi su un determinato dataset, lavorando in team partendo dalle analisi esplorative fino alla messa in produzione di una dashboard interattiva

Link al dataset e alla dashboard di riferimento:
[Inside Airbnb Rome Dataset and Dashboard](http://insideairbnb.com/rome/)

Le serate saranno divise in quattro laboratori
- **Lab1 Pandas**: revisione nozioni e implementazione manipolazione ed analisi sul dataset
- **Lab2 Data visualization**: grafici e visualizzazione del dataset
- **Lab3 Streamlit**: dai notebook ad una dashboard interattiva
- **Lab4 Messa in produzione**: papermill e concetti avanzati

# Accedere ai notebook

Per accedere ai notebook è possibile utilizzare anche Google Colab:

- **Notebook Laboratorio 1**
    - Nozioni su Pandas: [![Nozioni su Pandas](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/PythonBiellaGroup/MaterialeLezioni/blob/master/PercorsoDati/lab1/lab1-pandas-intro.ipynb)

    - Analisi Dataset 1: [![Analisi Dataset 1](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/PythonBiellaGroup/MaterialeLezioni/blob/master/PercorsoDati/lab1/lab-1-example-1.ipynb)

    - Analisi Dataset 2: [![Analisi Dataset 2](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/PythonBiellaGroup/MaterialeLezioni/blob/master/PercorsoDati/lab1/lab-1-example-2.ipynb)

    - Ingegnerizzazione del processo di Input: [![Ingegnerizzazione input](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/PythonBiellaGroup/MaterialeLezioni/blob/master/PercorsoDati/lab1/lab-1-data.ipynb)

- **Notebook Laboratorio 2**
    - Data visualization intro: [![Concetti di Data visualization](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/PythonBiellaGroup/MaterialeLezioni/blob/master/PercorsoDati/Lab2/lab-2-viz-intro.ipynb)

    - Data visualization sul dataset: [![Visualizzazione dei dati sul notebook](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/PythonBiellaGroup/MaterialeLezioni/blob/master/PercorsoDati/Lab2/lab_2_example_1.ipynb)

- **Notebook Laboratorio 3**
    - Non ancora disponibili

- **Notebook Laboratorio 4**
    - Non ancora disponibili


# Lanciare il Progetto

Il progetto è stato realizzato utilizzando `Poetry`

Per lanciare il progetto e costruire il virtualenv con le librerie necessarie consigliamo di utilizzare
- `pyenv` con python 3.8^
- `poetry`

È disponibile comunque un requirements.txt per creare il vostro virtual environment all'interno della cartella.

All'interno di questa cartella, una volta clonata sulla vostra macchina fare:
```bash
#Installare le librerie
poetry install

#Lanciare la shell con il nuovo venv
poetry shell

#Ora potete usare l'ambiente
```
