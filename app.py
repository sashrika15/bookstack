from flask import Flask, render_template,request,json,redirect,url_for,session
import pymongo
from pymongo import MongoClient


app = Flask(__name__)
app.secret_key = 'a random string'
api_key = "5ae2e3f221c38a288asdfsfd5fbdc89d5d4039b07c283619ac27"

cluster = MongoClient("mongodb+srv://sashrika:a1l4BDHjYDX1Ciue@cluster0.uciyc.mongodb.net/bookshop?retryWrites=true&w=majority")
db=cluster["bookshop"]
users=db["users"]
products=db["products"]
cart=db["cart"]

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/fiction")
def fiction():
    return render_template('fiction.html')

@app.route("/nonfiction")
def nonfiction():
    return render_template('nonfiction.html')

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        # print(username)
        # print(password)
        query = {"username": username, "password": password}
        # print(query)
        cur = users.find_one(query)

        if cur is None:
            return 'User not found'
        else:
            return 'User Found'

    else:
        return render_template('login.html')

@app.route("/cart")
def cart():
    return render_template('cart.html')

if __name__ == "__main__":
    app.run(debug=True)