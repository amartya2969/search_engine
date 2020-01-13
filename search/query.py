import pickle
import os
from .small_utils import tf_idf,stemming,remove_punctuation,tokenize_text 
from queue import PriorityQueue
import os
if os.path.exists('search/docf.p'):
    with open('search/docf.p', 'rb') as handle:
        docf = pickle.load(handle)
else:
    docf = {}

if os.path.exists('search/postings.p'):
    with open('search/postings.p', 'rb') as handle:
        postings = pickle.load(handle)
else:
    postings = {}

if os.path.exists('search/mag.p'):
    with open('search/mag.p', 'rb') as handle:
        mag = pickle.load(handle)
else:
    mag = {}


def calc_for_query(terms,k):
    songs_count = len(mag)
    scores = {}
    for word in terms:
        if word not in docf:
            continue
        df = docf[word]
        
        for i, info in enumerate(postings[word]):
            document_name = info[0]
            word_count = info[1]
            if document_name not in scores:
                scores[document_name] = 0
            scores[document_name] += tf_idf(word_count, df, songs_count)

    pq  = PriorityQueue()
    for document_name,score in scores.items():
        magnitude = mag[document_name]
        if magnitude == 0:
            continue
       
        final_score = score / magnitude

        if pq.qsize() < k:
            pq.put((final_score,document_name))
        else :
            top = pq.get()
            if top[0] < final_score:
                pq.put((final_score,document_name))
            else : 
                pq.put(top)
    result = []
    while not pq.empty():
        result.append(pq.get())
    result.reverse()
    return result
                 

def query(text,k):
    text = remove_punctuation(text)
    terms = tokenize_text(text)
    terms = stemming(terms)
    terms = set(terms)
    ans = calc_for_query(terms,k)
    return ans

