import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud


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


def text_blob_donuts(frequency_pol, frequency_sub):
    donut_cnt = make_subplots(
        rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "domain"}]]
    )
    donut_cnt.add_trace(
        go.Pie(
            labels=frequency_pol.polarity_analysis,
            values=frequency_pol.cnt,
            marker_colors=px.colors.sequential.Plasma_r,
            textinfo="label+percent",
            title="Polarity",
        ),
        1,
        1,
    )
    donut_cnt.add_trace(
        go.Pie(
            labels=frequency_sub.subjectivity_analysis,
            values=frequency_sub.cnt,
            marker_colors=px.colors.sequential.Plasma,
            textinfo="label+percent",
            title="Subjectivity",
        ),
        1,
        2,
    )

    # Use `hole` to create a donut-like pie chart
    donut_cnt.update_traces(hole=0.5, hoverinfo="label+percent")

    donut_cnt.update_layout(
        title_text="Size of sentiments results and subjectivity results"
    )
    donut_cnt.update_layout(showlegend=False)

    return donut_cnt


def text_blob_quadrant_analysis(df: pd.DataFrame):
    df_quadrant = df.loc[
        (df["polarity_analysis"] != "Neutral")
        & (df["subjectivity_analysis"] != "Neutral")
    ]
    px.colors.named_colorscales()
    quadrant_scatter_plot = px.scatter(
        df_quadrant,
        x="polarity",
        y="subjectivity",
        color="type",
        color_discrete_sequence=px.colors.sequential.Plasma_r,
        hover_data=["tweet", "favourite_count", "retweet_count"],
        template="plotly_white",
        title="Quadrant chart focused on subjectivity and polarity (neutral excluded)",
    )

    return quadrant_scatter_plot


def text_blob_calculate_big_number(frequency_pol):
    cntPos = frequency_pol[frequency_pol["polarity_analysis"] == "Positive"]
    cntNeutral = frequency_pol[frequency_pol["polarity_analysis"] == "Neutral"]
    cntNegative = frequency_pol[frequency_pol["polarity_analysis"] == "Negative"]
    return [cntPos, cntNeutral, cntNegative]
