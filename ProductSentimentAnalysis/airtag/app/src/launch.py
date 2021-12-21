import streamlit as st
from app.src.components.multipage import MultiPage
from app.src.components.pages import start, sentiment, text_analysis

st.set_page_config(layout="wide")

# Create an instance of the app
app = MultiPage()

# Title of the main page
try:
    col1, col2 = st.columns(2)
except Exception:
    col1, col2 = st.beta_columns(2)

col2.title("PBG App")

# Add all your applications (pages) here (remember to import first)
app.add_page("Home", start.app)
app.add_page("Text analysis", text_analysis.app)
app.add_page("Sentiment analysis", sentiment.app)
