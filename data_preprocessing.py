import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from spacy.lang.id import Indonesian
from nltk.tag import CRFTagger
from tqdm import tqdm
from spacy.lang.id import Indonesian
from spellchecker import correction
import pandas as pd

def preprocessing(csv='data/data.csv'):
    df = pd.read_csv(csv)
    df = df['reviews'].values

    print('--case folding...')
    # case folding
    for i in range(len(df)):
        # mengubah jadi lowercase
        df[i] = df[i].lower()
        # menghapus angka
        df[i] = re.sub(r"\d+", "", df[i])
        # menghapus tanda baca
        df[i] = df[i].translate(str.maketrans("","",string.punctuation)).strip()

    print('--remove stopwords...')
    # stopwords
    stop_factory = StopWordRemoverFactory().get_stop_words() #load defaul stopword
    more_stopword = ['mantap', 'bagus', 'kan'] #menambahkan stopword
    data = stop_factory + more_stopword #menggabungkan stopword

    dictionary = ArrayDictionary(data)
    str_ = StopWordRemover(dictionary)

    for i in range(len(df)):
        df[i] = word_tokenize(str_.remove(df[i]))

    listStopword =  set(stopwords.words('indonesian'))
    for i in range(len(df)):
        removed = []
        for token in df[i]:
            if token not in listStopword:
                removed.append(token)
        df[i] = removed   

    print('--stemming...')
    # stemming
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    for i in range(len(df)):
        tokens = []
        for kata in df[i]:
            kata_dasar = stemmer.stem(kata)
            tokens.append(kata_dasar)
        df[i] = tokens

    print('--checking spell...')
    # spell checking
    for i in range(len(df)):
        tokens = []
        for kata in df[i]:
            kata_asli = correction(kata)
            if len(kata_asli) > 2:
                tokens.append(kata_asli)
        df[i] = tokens

    print('--filtering postag...')
    # filter tag
    ct = CRFTagger()
    ct.set_model_file('data/all_indo_man_tag_corpus_model.crf.tagger')

    filters = ['NN', 'NNP', 'NNS', 'NNPS', 'JJ']
    tagged = ct.tag_sents(df)
    for i in range(len(df)):
        sent = []
        for idx, posTag in enumerate(tagged[i]):
            kata = posTag[0]
            tag = posTag[1]
            if tag in filters:
                sent.append(kata)
        df[i] = sent

    return(df)

