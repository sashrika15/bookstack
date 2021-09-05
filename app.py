from flask import *
import json
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'a rakasjdasd g'

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
    _id = int(request.form['id'])
    quantity = int(request.form['quantity'])
    if _id and request.method=='POST':
        ############### READ ###################
        query = {"_id": _id}
        cur = products.find_one(query)
        item = {cur['_id']:{'name':cur['name'],'author':cur['author'],'_id':cur['_id'],'price':cur['price'],'quantity':quantity,'total_price': quantity * cur['price']}}
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True

        if 'cart_item' in session:
            print("Cart item in session")
            print(session['cart_item'])
            dict = session['cart_item']
            key = str(cur['_id'])
            if key in dict:
                ############# UPDATE #################
                for idx, _ in session['cart_item'].items():
                    if key == idx:
                        old_quantity = session['cart_item'][key]['quantity']
                        total_quantity = old_quantity + quantity
                        session['cart_item'][key]['quantity'] = total_quantity
                        session['cart_item'][key]['total_price'] = total_quantity * cur['price']
                        # print(session['cart_item'])
            else:
                # print("Cart item with given id not in session")
                session['cart_item'][key]={'name':cur['name'],'author':cur['author'],'_id':cur['_id'],'price':cur['price'],'quantity':quantity,'total_price': quantity * cur['price']}
                # print(session['cart_item'])

            for key, _ in session['cart_item'].items():
                individual_quantity = int(session['cart_item'][key]['quantity'])
                individual_price = float(session['cart_item'][key]['total_price'])
                all_total_quantity = all_total_quantity + individual_quantity
                all_total_price = all_total_price + individual_price
        
        ############## CREATE ###############
        else:
            # print("Cart item not in session")
            session['cart_item'] = item
            # print(session['cart_item'])
            all_total_quantity = all_total_quantity + quantity
            all_total_price = all_total_price + quantity * cur['price']
            
        session['all_total_quantity'] = all_total_quantity
        session['all_total_price'] = all_total_price

        return redirect(url_for('cart'))
    else:
        return 'Error while adding'

@app.route('/update/<string:id>')
def updateProduct(id):
    _id = int(id)
    query = {"_id": int(_id)}
    cur = products.find_one(query)
    all_total_quantity=session['all_total_quantity']
    all_total_price=session['all_total_price']
    session.modified = True
    ############# UPDATE #################
    for idx, _ in session['cart_item'].items():
        if id == idx:
            # print("Tryna update")
            old_quantity = int(session['cart_item'][id]['quantity'])
            # print(old_quantity)
            total_quantity = old_quantity + 1
            # print(total_quantity)
            session['cart_item'][id]['quantity'] = total_quantity
            session['cart_item'][id]['total_price'] = total_quantity * int(cur['price'])
            # print(session['cart_item'][id])
    for key, _ in session['cart_item'].items():
            individual_quantity = int(session['cart_item'][key]['quantity'])
            individual_price = float(session['cart_item'][key]['total_price'])
            all_total_quantity = all_total_quantity + individual_quantity
            all_total_price = all_total_price + individual_price
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/empty')
def empty_cart():
    session.clear()
    return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def deleteProduct(id):
    _id = int(id)
    query = {"_id": int(_id)}
    cur = products.find_one(query)
    all_total_quantity=session['all_total_quantity']
    all_total_price=session['all_total_price']
    session.modified = True
    ############# DELETE ##############
    for idx, _ in session['cart_item'].items():
        if id == idx:
            print("Tryna delete")
            old_quantity = int(session['cart_item'][id]['quantity'])
            # print(old_quantity)
            total_quantity = old_quantity - 1
            # print(total_quantity)
            session['cart_item'][id]['quantity'] = total_quantity
            session['cart_item'][id]['total_price'] = total_quantity * int(cur['price'])

            session['all_total_quantity'] = all_total_quantity -1
            session['all_total_price'] = all_total_price - int(cur['price'])
    return redirect(url_for('cart'))


if (__name__ == "__main__"):
    app.run(debug=True)