# README #

## Requisiti

### Conda
Installazione attraverso Miniconda, [documentazione ufficiale qui](https://docs.conda.io/en/latest/miniconda.html).

## Setup ambiente

```
conda env create -f envs/jupyterlab_env.yaml -n jupyterlab 
```

```
conda env create -f envs/py39_pbg_env.yaml -n py39_pbg 
```

### Verifica ambienti
Utilizzando il comando `conda env list`, dovremmo identificare i due ambienti appena creati.


## Start

```
conda activate jupyterlab
jupyter lab
```

## Laboratori introduttivi
- [Utilizzo dei Notebooks](./notebooks/00-intro-notebooks.ipynb)
- [ETL con Pandas e Numpy](./notebooks/00-intro-data-etl.ipynb)

## Scikit Learn
- [Intro sklearn - parte 1](./notebooks/01-intro-ml-sklearn-parte1.ipynb)
- [Intro sklearn - parte 2](./notebooks/01-intro-ml-sklearn-parte2.ipynb)


## Task supervisionato: Regressione
- [Linear Regression](./notebooks/02-linear-regression.ipynb)
- [Regression Tuning](./notebooks/02-regression-tuning.ipynb)


## Task non supervisionato: Clustering



