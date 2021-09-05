from flask import *
import json
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'a random string'
api_key = "5ae2e3f221c38a288asdfsfd5fbdc89d5d4039b07c283619ac27"

cluster = MongoClient("mongodb+srv://sashrika:a1l4BDHjYDX1Ciue@cluster0.uciyc.mongodb.net/bookshop?retryWrites=true&w=majority")
db=cluster["ecommerce"]
users=db["users"]
products=db["products"]
# cart=db["cart"]

@app.route('/')
def index():
    if "user" in session:
        user=session['user']
        cur=products.find()
        prod=list(cur)
        # print(prod)
        # for i in cur:
        #     print(i)
        return render_template('index.html',products=prod)
    else:
        return render_template('index.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        user=request.form['user']
        pwd=request.form['pwd']
        session['user']=user
        query = {"username": user, "password": pwd}
        cur = users.find_one(query)
        return redirect(url_for('index')) #render home page with user
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))

@app.route('/loasfasf')
def register():
    return 'hi'

@app.route('/add',methods=['POST'])
def add():
    id = int(request.form['id'])
    quantity = int(request.form['quantity'])
    if id and request.method=='POST':
        query = {"_id": id}
        # print(query)
        cur = products.find_one(query)
        # print(cur['name'])
        item = {cur['_id']:{'name':cur['name'],'author':cur['author'],'id':cur['_id'],'price':cur['price'],'quantity':quantity,'total_price': quantity * cur['price']}}
        print(item)
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True
        if 'cart_item' in session:
            print()

        else:
            session['cart_item']=item
            print(session['cart_item'])
            all_total_price=all_total_price + quantity*cur['price']
            # print(session['total_price'])
            all_total_quantity=all_total_quantity+quantity

        session['all_total_quantity']=all_total_quantity
        session['all_total_price']=all_total_price

        return redirect(url_for('index'))
    else:
        return 'Error while adding'


@app.route('/cart')
def cart():
    return render_template('cart.html')

if (__name__ == "__main__"):
    app.run(debug=True)