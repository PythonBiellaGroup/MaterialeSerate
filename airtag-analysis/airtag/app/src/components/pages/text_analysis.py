import streamlit as st
from app.src.common.plots import frequency_plot, wordcloud
from app.src.common.transformations import most_frequent_words
from app.src.common.importer import read_dataframe


def app():
    st.title("PBG Airtag analysis")
    st.subheader("Text Analysis Page")
    df = read_dataframe()
    print(df.columns)
    print(df.shape)
    mfwords, word_list = most_frequent_words(df)
    print(mfwords.head())
    print(mfwords.shape)

    st.dataframe(mfwords)

    freq_plot = frequency_plot(mfwords)
    st.plotly_chart(freq_plot)

    wordcloud_plot = wordcloud(word_list)
    st.pyplot(wordcloud_plot)
