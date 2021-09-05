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

def Merge(dict1, dict2):
    res = dict1 | dict2
    return res

@app.route('/add',methods=['POST'])
def add():
    _id = int(request.form['id'])
    quantity = int(request.form['quantity'])
    if _id and request.method=='POST':
        query = {"_id": _id}
        # print(query)
        cur = products.find_one(query)
        # print(cur['name'])
        item = {cur['_id']:{'name':cur['name'],'author':cur['author'],'_id':cur['_id'],'price':cur['price'],'quantity':quantity,'total_price': quantity * cur['price']}}
        # print(item)
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True

        if 'cart_item' in session:
            print("Cart item in session")
            dict = session['cart_item']
            key = str(cur['_id'])
            if key in dict:
                print("Cart item with id in session")
                # print(session['cart_item'][key])
                for idx, value in session['cart_item'].items():
                    if key == idx:
                        old_quantity = session['cart_item'][key]['quantity']
                        total_quantity = old_quantity + quantity
                        session['cart_item'][key]['quantity'] = total_quantity
                        session['cart_item'][key]['total_price'] = total_quantity * cur['price']
                        print(session['cart_item'])
            else:
                print("Cart item with given id not in session")

                # session['cart_item'].update(item)
                # print(session['cart_item'])
        
            for key, value in session['cart_item'].items():
                individual_quantity = int(session['cart_item'][key]['quantity'])
                individual_price = float(session['cart_item'][key]['total_price'])
                all_total_quantity = all_total_quantity + individual_quantity
                all_total_price = all_total_price + individual_price
        else:
            print("Cart item not in session")
            session['cart_item'] = item
            
            # print(session['cart_item'])
            all_total_quantity = all_total_quantity + quantity
            all_total_price = all_total_price + quantity * cur['price']
            
        session['all_total_quantity'] = all_total_quantity
        session['all_total_price'] = all_total_price

        return redirect(url_for('index'))
    else:
        return 'Error while adding'


@app.route('/cart')
def cart():
    return render_template('cart.html')

if (__name__ == "__main__"):
    app.run(debug=True)