import ast
import pandas as pd
from nltk.probability import FreqDist


def most_frequent_words(df: pd.DataFrame):
    words_list = []
    for _, tr in df.iterrows():
        for x in ast.literal_eval(tr["tweet_preprocessed"]):
            words_list.append(x)

    fdist = FreqDist(words_list)
    ds_freq_words = pd.DataFrame(list(fdist.items()), columns=["Word", "Frequency"])
    ds_top_50_freq_words = ds_freq_words.sort_values(by=["Frequency"], ascending=False)[
        :50
    ]
    ds_top_50_freq_words_cln = ds_top_50_freq_words.loc[
        (ds_top_50_freq_words["Word"] != "airtag")
    ]  # remove search key words
    ds_top_50_freq_words_cln.sort_values(by=["Frequency"], ascending=False)
    result = ds_top_50_freq_words_cln

    return result, words_list
