import pyLDAvis
import pyLDAvis.gensim_models
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def LDAvis(LDAmodel_, corpus_t, dictionary_t):
    p = pyLDAvis.gensim_models.prepare(topic_model=LDAmodel_, corpus=corpus_t, dictionary=dictionary_t)
    pyLDAvis.save_html(p, 'static/lda.html')

def wordcloud(model, topic):
    text = {word: value for word, value in model.show_topic(topic)}
    wc = WordCloud(background_color="white", 
                   max_words=1000, 
                   width=1600, height=800)
    wc.generate_from_frequencies(text)
    plt.figure(figsize=(20,10))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(f'static/wc_topic{topic+1}.png', facecolor='k', bbox_inches='tight')