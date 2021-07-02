import json
import math
import numpy as np

from nltk import tokenize
from tw_proccesing import TweetProccesor

def build_inverted_index(n):
    tp = TweetProccesor()
    doc_freq = {}
    term_freq = {}
    tw_index = 1

    ##Llenamos la frecuencia de documento para cada term y la frecuencia de termino para cada
    #par (term_freq, tweet).
    for tweet_data in open("../data/data.json").readlines():
        tweet_data = json.loads(tweet_data)
        tokens = tp.tokenize(tweet_data["content"])
        terms = {}
        for token in tokens:
            if doc_freq.get(token) == None:
                doc_freq[token] = 1
            else:
                doc_freq[token] += 1
            if terms.get(token) == None or terms.get(token)[1] != tw_index:
                terms[token] = (1, tw_index)
            else:
                terms[token] = (terms[token][0] + 1, tw_index)
        for term in terms:
            if term_freq.get(term) == None:
                term_freq[term] = [math.log10(terms[term])]
            else:
                term_freq[term].append(math.log10(terms[term]))
        tw_index += 1
    
    #Construimos el inverted index con las frecuencias acumuladas
    inverted_index = {}
    for word in doc_freq:
        #Guardamos el peso IDF, los pesos TF y la norma (N) de TF
        inverted_index[word] = {
            "IDF": round(math.log10(n/doc_freq[word]),4), 
            "TF": term_freq[word],
            "N": len(term_freq[word])
        }
    return inverted_index

def process_query(query):
    ii = build_inverted_index(100)
    tp = TweetProccesor()
    tokens = tp.tokenize(query)
    query_words = {}

    #Obtenemos la frecuencia de las palabras en la query
    for q in tokens:
        if query_words[q] is None:
            query_words[q] = 1
        else:
            query_words[q] += 1

    #Calculamos la distancia de coseno:
    tweets = {}
    for q in query_words:
        i = ii[q]
        #Normalizamos localmente el vector de palabras en el query
        qq = math.log10(query_words[q]) * i['IDF'] / len(tokens)
        for tweet in i['TF']:
            #Sumamos a un documento el puntaje que va consiguiendo (con dist. de coseno)
            tweets[tweet[1]] = sum((math.log10(tweet[0]) * i['IDF']) / i['N'] * qq)
        
    #Ordenamos segun el puntaje obtenido de cada tweet
    sorted(tweets, key=lambda x:x[0])
    return tweets
    

if __name__ == "__main__":
    build_inverted_index(100)
    