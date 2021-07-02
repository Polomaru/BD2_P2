import nltk
from nltk import tokenize
from nltk.tokenize import TweetTokenizer
from nltk.stem.snowball import SnowballStemmer

class TweetProccesor:
    #Crea un stemmer óptimo para el lenguaje español
    #Crea la stoplist leyendo más de 600 stopwords
    #Adicionalmente agregamos algunos caracteres frecuentes
    #Complejidad: O(K) donde K es la cantidad de palabras en la stoplist.
    def __init__(self):
        self.stemmer = stemmer = SnowballStemmer(language='spanish')
        with open('stoplist.txt') as sp:
            self.stoplist = nltk.word_tokenize(sp.read().lower())
            self.stoplist += ["<", ">", ",", "º", ":", ";", ".", "!", "¿", "?", ")", "(", "@", "'", "#",'"','\"', '.', '...']

    #Para cada palabra en el tweet: si no es una stopword, la reduce a su raíz y la añade a un contenedor
    #Al final, se retorna ese vector
    #Complejidad: O(n*K) donde K es la cantidad de palabras en la stoplist.
    def tokenize(self, tweet):
        #Remover los emojis.
        tweet = tweet.encode('ascii', 'ignore').decode('ascii')
        return [self.stemmer.stem(t) for t in nltk.word_tokenize(tweet) if t not in self.stoplist]