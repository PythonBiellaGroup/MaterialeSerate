import pandas as pd

def frequency_plot(df: pd.DataFrame): 
    frequency_word_plot = px.bar(ds_top_50_freq_words_cln, 
             x='Frequency',
             y='Word',
             orientation = 'h', 
             template = 'plotly_white',
             color = 'Frequency',
             range_color=[50, 600])
    
    return frequency_word_plot

def wordcloud(save_file: bool = False):
    listToStr = ' '.join([str(elem) for elem in words_list])
    wordcloud = WordCloud(width=5000, height=3000, max_words= 100,background_color ='white').generate(listToStr)
    plt.figure(figsize = (20, 20), facecolor = None) 
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.margins(x=0, y=0)
    
    if save_file:
        #save image
        wordcloud.to_file("static/images/wordcloud_airtag.jpeg")
    
    return plt


    