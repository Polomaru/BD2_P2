from flask import Flask, render_template, request
import json
from inverted_index import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index3.html")

@app.route('/search')
def search():
    return render_template("index3.html")
@app.route('/reindex')
def reindex():
    do_query()
    with open('resources/rpta.json') as file:
        return render_template("results.html",data=json.load(file))


'''
@app.route('/twets')
def read_twet():
    with open('tweets_2021-06-22.json') as file:
    data = json.load(file)
    for client in data['clients']:
        print('First name:', client['first_name'])
        print('Last name:', client['last_name'])
        print('Age:', client['age'])
        print('Amount:', client['amount'])
        print('')

@app.route('/colors')
def show_tweets():
    return render_template("index3.html")
'''

if __name__ == "__main__":
    app.run(debug=True,port=5820)