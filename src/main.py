import pandas as pd
import numpy as np
import math
from collections import defaultdict
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi  
from sklearn.metrics.pairwise import cosine_similarity


cran_all = pd.read_csv("Search Engine/Datasets/cran_all.csv")  
cran_query = pd.read_csv("Search Engine/Datasets/cran_query.csv")  
trec_data = "Search Engine/Datasets/cranqrel.trec.txt"  

cran_all['title'] = cran_all['title'].fillna('')
cran_all['author'] = cran_all['author'].fillna('')
cran_all['bib'] = cran_all['bib'].fillna('')
cran_all['text'] = cran_all['text'].fillna('')

def preprocess(text):
    text = re.sub(r'[^\w\s]', '', text.lower())
    tokens = text.split()
    return tokens

cran_all['tokens'] = cran_all['text'].apply(preprocess)
cran_query['tokens'] = cran_query['title'].apply(preprocess)

inverted_index = defaultdict(list)
for idx, row in cran_all.iterrows():
    doc_id = row['docno']
    tokens = row['tokens']
    for token in set(tokens):  
        inverted_index[token].append(doc_id)

inverted_index = dict(inverted_index)

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(cran_all['text'])
query_vectors = vectorizer.transform(cran_query['title'])

def rank_vsm(query_id):
    query_vector = query_vectors[query_id]
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    ranked_docs = np.argsort(similarities)[::-1]  
    return ranked_docs, similarities

bm25 = BM25Okapi(cran_all['tokens'])

def rank_bm25(query_id):
    query_tokens = cran_query.iloc[query_id]['tokens']
    scores = bm25.get_scores(query_tokens)
    ranked_docs = np.argsort(scores)[::-1]  
    return ranked_docs, scores

def rank_lm(query_id, lambda_param=0.5):
    query_tokens = cran_query.iloc[query_id]['tokens']
    doc_scores = []
    for doc_id, doc_tokens in zip(cran_all['docno'], cran_all['tokens']):
        score = 1.0
        for token in query_tokens:
            p_token_doc = (doc_tokens.count(token) + lambda_param) / (len(doc_tokens) + lambda_param * len(inverted_index))
            score *= p_token_doc
        doc_scores.append(score)

    ranked_docs = np.argsort(doc_scores)[::-1]  
    return ranked_docs, doc_scores

def generate_trec_output(model_name, rank_function):
    output_lines = []
    for query_id in range(len(cran_query)):
        ranked_docs, similarities = rank_function(query_id)
        for rank, doc_id in enumerate(ranked_docs[:100]):  
            line = f"{query_id + 1} Q0 {cran_all.iloc[doc_id]['docno']} {rank + 1} {similarities[doc_id]} {model_name}"
            output_lines.append(line)
   
    with open(f"{model_name}_output.txt", "w") as f:
        f.write("\n".join(output_lines))


generate_trec_output("VSM", rank_vsm)
generate_trec_output("BM25", rank_bm25)
generate_trec_output("LM", rank_lm)

