import os 
import json
io = input("Ingrese query: ")
os.system('snscrape --jsonl --max-results 200  twitter-search " ' + io + ' until:2021-06-30 lang:es "  > myjson.json') 
