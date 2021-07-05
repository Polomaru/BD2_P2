from flask import Flask, jsonify, render_template, request,Response
import json


app = Flask(__name__)

from list import lists
  
@app.route('/')
def ping():
    return render_template("index.html")



#twets
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
'''
@app.route('/colors')
def show_tweets():
    return render_template("index3.html")






if __name__ == "__main__":
    app.run(debug=True,port=5820)