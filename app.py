from flask import Flask, render_template,request,json,redirect,url_for,session


app = Flask(__name__)
app.secret_key = 'a random string'
api_key = "5ae2e3f221c38a28845f05b674ad5fbdc89d5d4039b07c283619ac27"

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/fiction")
def fiction():
    return render_template('fiction.html')

@app.route("/non-fiction")
def nonfiction():
    return render_template('nonfiction.html')

@app.route("/login")
def login():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)