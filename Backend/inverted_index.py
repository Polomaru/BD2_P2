import json
import math
import numpy as np
import os
import sys
from glob import glob
sys.path.append('../data')
from tweets import creator_index
from heapq import heappop, heappush, heapify
from tw_proccesing import TweetProccesor

#Constantes
size_tweets = 20000
tp = TweetProccesor()

class InvertedIndex:
        
    #Llamamos a la funcion para llenar un bucket. Estamos definiendo tamaño de bucket = 500. 
    def __build_inverted_index(self, n, block):
        #Llenamos la frecuencia de documento para cada term y la frecuencia de termino para cada
        #par (term_freq, tweet).
        tw_index = 1
        lengths = {}
        with open("../data/data.json", "r") as file:
            for j in range(math.ceil(n/block)):
                term_freq = {}
                for i in range(block):
                    tweet_data = file.readline()
                    tweet_data = json.loads(tweet_data)
                    tokens = tp.tokenize(tweet_data["content"])
                    lengths[tw_index] = len(tokens)
                    terms = {}
                    for token in tokens:
                        if terms.get(token) == None or terms.get(token)[1] != tw_index:
                            terms[token] = (1, tw_index)
                        else:
                            terms[token] = (terms[token][0] + 1, tw_index)
                    #Podemos amortiguar el TF con el logaritmo. No podemos hacer esto con DF, ya que no
                    #tenemos la información del resto de indices en los otros bloques.
                    for term in terms:
                        if term_freq.get(term) == None:
                            term_freq[term] = [(1 + math.log10(terms[term][0]), terms[term][1])]
                        else:
                            term_freq[term].append((1 + math.log10(terms[term][0]), terms[term][1]))
                    tw_index += 1

                inverted_index = {}
                for word in term_freq:
                    #Guardamos las frecuencias de cada termino
                    inverted_index[word] = {
                        "DF": len(term_freq[word]), 
                        "TF": term_freq[word]
                    }

                json_file = open('indexs/i' + str(j) +'.json', 'a', newline='\n', encoding='utf8')
                json_file.truncate(0)
                json_file.write(json.dumps(inverted_index, ensure_ascii=False, default=str))

        lengths_file = open('resources/lengths.json', 'a', newline='\n', encoding='utf8')
        lengths_file.truncate(0)
        lengths_file.write(json.dumps(lengths, ensure_ascii=False, default=str))    
        return
    
    def __merge(self):
        inverted_index = {}

        #Leemos los índices intermedios
        for f_name in glob('./indexs/*.json'):
            with open(f_name, "r") as index:
                i_dic = index.readline()
                i_dic = json.loads(i_dic)
            #Colocamos las frecuencias. Recuerde que el IDF se calcula en la misma función de similitud
            for k in i_dic.keys():
                if k not in inverted_index.keys():
                    inverted_index[k] = i_dic[k]
                else:
                    inverted_index[k]['TF']+=(i_dic[k]['TF'])
                    inverted_index[k]['DF']+=(i_dic[k]['DF'])
            os.remove(f_name)
        
        #Escribimos el índice completo
        json_file = open('resources/i_index.json', 'a', newline='\n', encoding='utf8')
        json_file.truncate(0)
        json_file.write(json.dumps(inverted_index, ensure_ascii=False, default=str))
        return

    def BSB_index_construction(self):
        block = 500
        self.__build_inverted_index(size_tweets, block)
        self.__merge()
        return

def process_query(query, k, n):
    tokens = tp.tokenize(query)
    norm = len(tokens)

    #Obtenemos la frecuencia de las palabras en la query
    query_words = {}

    for q in tokens:
        if query_words.get(q) == None:
            query_words[q] = 1
        else:
            query_words[q] += 1

    #Leemos el index desde un archivo (memoria secundaria)
    tweets = {}
    with open('resources/i_index.json', "r") as index:
        i_dic = index.readline()
        i_dic = json.loads(i_dic)
        
    with open('resources/lengths.json', "r") as lens:
        lengths = lens.readline()
        lengths = json.loads(lengths)

    #Calculamos la distancia de coseno:
    for q in query_words:
        if i_dic.get(q) != None:
            i = i_dic[q]
            #Normalizamos localmente el vector de palabras en el query
            qq = round((1 + math.log10(query_words[q])) * (math.log10(n /i['DF'])) / norm, 4)
            for tweet in i['TF']:
                #Sumamos a un documento el puntaje que va consiguiendo (con dist. de coseno)
                cosine = round(tweet[0] * (math.log10( n /i['DF'])) / lengths[str(tweet[1])] * qq, 4) 
                if tweets.get(tweet[1]) == None:
                    tweets[tweet[1]] = cosine
                else:
                    tweets[tweet[1]] += cosine
    heap = []

    #k critico para el cual a partir de k+1 la fila de prioridades es peor que el sorting
    #Ver informe para un analisis preciso de esta situación.
    if k <= 17200:
        #Debemos hacer una segunda pasada porque los cosenos podrían haberse modificado...
        for tweet in tweets:
            heappush(heap, (-1 * tweets[tweet], tweet))

        #No queremos mostrar los 20K tweets al usuario, asi que nos quedamos solo con los K más relevantes
        retrieved = {}
        for i in range(min(k,len(tweets))):
            retrieved[heap[0][1]] = -1 * heap[0][0] 
            heappop(heap)
            heapify(heap)
        return retrieved

    else:
        return dict(sorted(tweets.items())[:k])

    
#Cambiar la temática de los tweets
def change_index_theme():
    keyword = input("Keyword: ")
    maxtweets = 20000

    index_creator = creator_index()
    index_creator.make_new_index(keyword, maxtweets)
    ii = InvertedIndex()
    ii.BSB_index_construction()
    return

#Procesar consulta    
def do_query():
    q = input("Ingrese la query que quiere obtener: ")
    qns = int(input("Ingrese cuantos tweets quiere recuperar, como máximo: "))
    rpta = process_query(q,qns,size_tweets)
    indexs = open("../data/index.txt", "r")
    tweets = open("../data/data.json", "r")
    jsonrpta = {}
    cont = 0

    for n in rpta:
        indexs.seek(0,0)
        tweets.seek(0,0)
        indexs.read((n-1)*10)
        line_tweet1 = int(indexs.read(10))
        line_tweet2 = int(indexs.read(10))
        tweets.read(line_tweet1)
        json_line = tweets.read(line_tweet2 - line_tweet1-1)
        json_line = json.loads(json_line)
        json_line['score'] = rpta[n]
        jsonrpta[cont] = json_line
        cont +=1

    json_file = open('resources/rpta.json', 'a', newline='\n', encoding='utf8')
    json_file.truncate(0)
    json_file.write(json.dumps(jsonrpta, indent = 6 , ensure_ascii=False))
    return

if __name__ == "__main__":
    do_query()