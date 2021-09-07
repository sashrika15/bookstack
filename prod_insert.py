from pymongo import MongoClient
import random

cluster = MongoClient("<YOUR URI STRING>")
db=cluster["ecommerce"]
users=db["users"]
products=db["products"]


books=["Skill It, Kill It","Home in the World","Monk in a Merc","It’s a Wonderful Life","The Bench","Elephant in the Womb"]
auths=["Ronnie Screwvala","Amartya Sen","Monk in a Merc","Ruskin Bond","Meghan Markle","Kalki Koechlin"]
i=1
for (name, author) in zip(books, auths):
    # print(name)
    # print(author)
    # print(i)
    
    item = {
        "_id":i,
        "name":name,
        "author":author,
        "price":random.randint(100,400),
        }
    products.insert_one(item)
    i=i+1


# dbResponse = products.insert_one(item)
