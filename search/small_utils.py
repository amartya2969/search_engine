import pandas as pd
import numpy as np
import os
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from collections import Counter
import math


def tf_transforrm(tf):
    return 1 + math.log10(tf)

def idf_transform(df, songs_count):
    return math.log10(songs_count / df)

def tf_idf(tf, df, songs_count):
    return tf_transforrm(tf) * idf_transform(df, songs_count)

def tokenize_text(text):
    stop_words = set(stopwords.words('english'))
    raw_tokens = word_tokenize(text)
    tokens = [word.lower() for word in raw_tokens]
    return [word for word in tokens if not word in stop_words]

def remove_punctuation(text):
    exclude = set(string.punctuation)
    return ''.join(ch for ch in text if ch not in exclude)


def stemming(terms):
    porter_stemmer = PorterStemmer()
    stemmed_sentence = [porter_stemmer.stem(w) for w in terms]
    return stemmed_sentence




