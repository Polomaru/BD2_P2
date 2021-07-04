import json
import math
import numpy as np
import os
from heapq import heappop, heappush, heapify
from tw_proccesing import TweetProccesor

class InvertedIndex:

    def __init__(self):
        self.tp = TweetProccesor()
        self.lengths = {}
        self.ii = self.BSB_index_construction()

    def BSB_index_construction(self):
        block = 4
        return self.__build_inverted_index(100, block)
        
    #Deberia procesar solo un numero fijo de indices
    def __build_inverted_index(self, n, block):
        # doc_freq = {}
        
        tw_index = 1

        #Llenamos la frecuencia de documento para cada term y la frecuencia de termino para cada
        #par (term_freq, tweet).
        with open("../data/temp.json", "r") as file:
            temp = n
            for j in range(math.ceil(n/block)):
                term_freq = {}
                for i in range(block):
                    tweet_data = file.readline()
                    tweet_data = json.loads(tweet_data)
                    tokens = self.tp.tokenize(tweet_data["content"])
                    self.lengths[tw_index] = (len(tokens))
                    terms = {}
                    for token in tokens:
                        # if doc_freq.get(token) == None:
                        #     doc_freq[token] = 1
                        # else:
                        #     doc_freq[token] += 1
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
                inverted_index = {}
                for word in term_freq:
                    #Guardamos el peso IDF, los pesos TF y la norma (N) de TF
                    inverted_index[word] = {
                        "DF": len(term_freq[word]), 
                        "TF": term_freq[word]
                    }
                json_file = open('indexs/i' + str(j) +'.json', 'a', newline='\n', encoding='utf8')
                json_file.truncate(0)
                json_file.write(json.dumps(inverted_index, ensure_ascii=False, default=str))
                # print (inverted_index)
                # return inverted_index



def merge():
    path = './indexs'
    arr = os.listdir(path)
    inverted_index = {}
    for file in arr:
        with open(path+ '/'+file, "r") as index:
            i_dic = index.readline()
            i_dic = json.loads(i_dic)
            for k in i_dic.keys():
                if k not in inverted_index.keys():
                    inverted_index[k] = i_dic[k]
                else:
                    inverted_index[k]['TF']+=(i_dic[k]['TF'])
                    inverted_index[k]['DF']+=(i_dic[k]['DF'])
        os.remove(path+ '/'+file)
    json_file = open('i_index.json', 'a', newline='\n', encoding='utf8')
    json_file.truncate(0)
    json_file.write(json.dumps(inverted_index, ensure_ascii=False, default=str))


if __name__ == "__main__":
    #BORRAR COMENTARIO: En el front, den la posibilidad de probar con k = 1,2,4,8,16,32 y 64
    InvertedIndex()
    merge()
    # print(ii.process_query('covid enfermar', 2))