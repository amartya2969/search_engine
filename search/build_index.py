import pandas as pd
import os
import pickle
from collections import Counter
from small_utils import tf_idf, tokenize_text, remove_punctuation,stemming
import math
        
if os.path.exists('docf.p'):
    with open('docf.p', 'rb') as handle:
        docf = pickle.load(handle)
else:
    docf = {}

if os.path.exists('postings.p'):
    with open('postings.p', 'rb') as handle:
        postings = pickle.load(handle)
else:
    postings = {}

if os.path.exists('mag.p'):
    with open('mag.p', 'rb') as handle:
        mag = pickle.load(handle)
else:
    mag = {}

songs_count = len(mag)


def add_document(document_name,document_text):
    if document_name in mag.keys():
        print('document exists')
        return
    global songs_count
    mag[document_name] = 0
    songs_count += 1
    
    text = remove_punctuation(document_text)
    terms = tokenize_text(text)
    terms = stemming(terms)
    frequency_dict = Counter(terms)

    for word,word_count in frequency_dict.items():
        
        if word not in postings.keys():
            postings[word] = []
        postings[word].append((document_name,word_count))
        
        if word not in docf.keys():
            docf[word] = 0
        docf[word] += 1

def calc_all_magnitudes():
    for word,posting in postings.items():
        df = docf[word]
        for i, info in enumerate(posting):
            document_name = info[0]
            word_count = info[1]
            if document_name not in mag.keys():
                mag[document_name] = 0
            mag[document_name] += tf_idf(word_count, df, songs_count) ** 2
    
    for document_name in mag.keys():
        mag[document_name] = round(math.sqrt(mag[document_name]),3)




def save_index():
    pickle.dump(postings, open('postings.p', 'wb'))
    pickle.dump(docf, open('docf.p', 'wb'))
    pickle.dump(mag, open('mag.p', 'wb'))

def create_index(filename):
    df = pd.read_csv(filename, header=0)
    for index, row in df.iterrows():
        add_document(str(row['name']),str(row['text']))
    calc_all_magnitudes()
    save_index()

create_index('songs.csv')
