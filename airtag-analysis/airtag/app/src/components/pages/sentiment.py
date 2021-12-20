import streamlit as st

from app.src.common.sentiment import (
    azure_sentiment,
    text_blob_sentiment,
    vader_sentiment,
)


def app():
    st.title("PBG Airtag analysis")
    st.subheader("Sentiment Analysis Page")

    st.markdown(
        """
            ### Azure Cognitive Services
            
            this is a pay as you go service provided by Microsoft Azure. The sentiment analysis feature provides sentiment labels (such as "negative", "neutral" and "positive") based on the highest confidence score found by the service at a sentence and document-level.
            
            ### VADER
            It is a simple lexicon and rule-based model for general sentiment analysis.

            Compound:It is a ‘normalized, weighted composite score computed by summing the valence scores of each word in the lexicon, adjusted according to the rules, and then normalized to be between -1 (most extreme negative) and +1 (most extreme positive).
            
            ### TextBlob
            
            is a free library for processing textual data. It provides a simple API for diving into common natural language processing (NLP) tasks such as part-of-speech tagging, noun phrase extraction, sentiment analysis, classification, translation, and more.
            
            - **Polarity** lies between [-1,1]. 1 defines the most positive rank and -1 defines the higher values of negativity.
            - **Subjectivity** lies between [0,1]. Subjectivity quantifies the amount of personal opinion and factual information contained in the text. The higher subjectivity means that the text contains personal opinion rather than factual information.
            
            
        """
    )
    with st.expander(label="Expand me", expanded=True):
        with st.container():
            st.subheader("Sentiment Analysis Validation")
            text = st.text_area(
                "Insert text you want to score",
                value="Airtags are extremely useful and I love the design",
                key="textarea_azure",
            )
            col1, col2, col3 = st.columns(3)
            if col1.button("Launch Azure Analysis", key="button_azure"):
                score, sentiment = azure_sentiment([text])
                st.write(f"Sentiment: {sentiment} with score: {score}")

            if col2.button("Launch Vader Analysis", key="button_vader"):
                score = vader_sentiment([text])
                st.write(f"Sentiment score: {score}")

            if col3.button("Launch Text Blob Analysis", key="button_textblob"):
                score, sentiment = text_blob_sentiment([text])
                st.write(f"Sentiment: {sentiment} with score: {score}")
