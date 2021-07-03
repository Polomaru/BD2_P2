from flask import Flask, jsonify, render_template

app = Flask(__name__)

from list import lists
  
@app.route('/ping')
def ping():
    return jsonify ({"message":"pong!"})

@app.route('/list')
def getlists():
    return jsonify({"Lista":lists, "message":"Product's list"})

@app.route('/list/<string:username>')
def getlist(username):
    listfound = [list for list in lists if list ['username'] == username]
    if (len(listfound)>0):
        return jsonify(({"product":listfound[0]}))
    return jsonify({"message": "product nnot found"})

@app.route("/html")
def home():
    return render_template("index.html")
  

if __name__ == "__main__":
    app.run(debug=True)