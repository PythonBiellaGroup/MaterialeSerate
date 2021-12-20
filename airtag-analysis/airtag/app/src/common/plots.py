import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import numpy as np


def frequency_plot(df: pd.DataFrame):
    frequency_word_plot = px.bar(
        df,
        x="Frequency",
        y="Word",
        orientation="h",
        template="plotly_white",
        color="Frequency",
        range_color=[50, 600],
    )

    return frequency_word_plot


def wordcloud(word_list: list, save_file: bool = False):
    listToStr = " ".join([str(elem) for elem in word_list])
    wordcloud = WordCloud(
        width=5000, height=3000, max_words=100, background_color="white"
    ).generate(listToStr)
    plt.figure(figsize=(20, 20), facecolor=None)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.margins(x=0, y=0)

    # if save_file:
    # save image
    # wordcloud.to_file("static/images/wordcloud_airtag.jpeg")

    return plt
