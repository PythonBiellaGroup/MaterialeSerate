# Streamlit Test App

This is a first Test app with [Streamlit](https://www.streamlit.io/) to get more comfortable with this cool library.
Also the new python [poetry](https://python-poetry.org/) package manager is used to practise with it.

# Getting Started

First install the dependencies with:

```bash
poetry install
or
pip install -r requirements.txt
```

The requirements file was generated with the poetry command:

```bash
poetry export -f requirements.txt --without-hashes --output requirements.txt
```

Then you can run the web app with:

```bash
streamlit run app.py
```
