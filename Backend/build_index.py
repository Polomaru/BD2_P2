import json
import math
import numpy as np
from heapq import heappop, heappush, heapify

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
                term_freq[term] = [(1 + math.log10(terms[term][0]), terms[term][1])]
            else:
                term_freq[term].append((1 + math.log10(terms[term][0]), terms[term][1]))
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

def process_query(query, k):
    ii = build_inverted_index(100)
    tp = TweetProccesor()
    tokens = tp.tokenize(query)
    norm = len(tokens)
    query_words = {}

    #Obtenemos la frecuencia de las palabras en la query
    for q in tokens:
        if query_words.get(q) == None:
            query_words[q] = 1
        else:
            query_words[q] += 1

    #Calculamos la distancia de coseno:
    tweets = {}
    for q in query_words:
        if ii.get(q) != None:
            i = ii[q]
            #Normalizamos localmente el vector de palabras en el query
            qq = (1 + math.log10(query_words[q])) * i['IDF'] / norm
            for tweet in i['TF']:
                #Sumamos a un documento el puntaje que va consiguiendo (con dist. de coseno)
                cosine = round(tweet[0] * i['IDF'] / i['N'] * qq, 4) 
                if tweets.get(tweet[1]) == None:
                    tweets[tweet[1]] = cosine
                else:
                    tweets[tweet[1]] += cosine
        else: 
            norm -= 1
    heap = []

    #Debemos hacer una segunda pasada porque los cosenos podrían haberse modificado...
    for tweet in tweets:
        heappush(heap, (-1 * tweets[tweet], tweet))

    #No queremos mostrar los 20K tweets al usuario, asi que nos quedamos solo con los K más relevantes
    retrieved = {}
    for i in range(k):
        retrieved[heap[0][1]] = -1 * heap[0][0] 
        heappop(heap)
        heapify(heap)
        
    return retrieved
    

if __name__ == "__main__":
    #BORRAR COMENTARIO: En el front, den la posibilidad de probar con k = 1,2,4,8,16,32 y 64
    print(process_query('Alemania ganará la eurocopa', 64))
    