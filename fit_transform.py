from gensim.models import Phrases
from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel

def fit_transform(data):
    bigram_t = Phrases(data, min_count=5)
    trigram_t = Phrases(bigram_t[data], min_count=5)
    for idx, d in enumerate(data):
        for token in bigram_t[d]:
            if '_' in token:# Token is a bigram, add to document.
                data[idx].append(token)
        for token in trigram_t[d]:
            if '_' in token:# Token is a bigram, add to document.
                data[idx].append(token)

    # Create a dictionary representation of the documents.
    # Remove rare & common tokens
    dictionary_t = Dictionary(data)
    dictionary_t.filter_extremes(no_below=2, no_above=0.90)
    #Create dictionary and corpus required for Topic Modeling
    corpus_t = [dictionary_t.doc2bow(doc) for doc in data]
    corpus_t = [t for t in corpus_t if t] # remove empty corpus
    print('Number of unique tokens: %d' % len(dictionary_t))
    print('Number of documents: %d' % len(corpus_t))
    print(corpus_t[:2])

    LDAmodel_ = LdaModel(corpus=corpus_t, id2word=dictionary_t, num_topics=3)

    return LDAmodel_, corpus_t, dictionary_t