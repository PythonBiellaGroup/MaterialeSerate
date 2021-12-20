import streamlit as st


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
