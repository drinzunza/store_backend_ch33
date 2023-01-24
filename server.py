from flask import Flask, request
import json
from mock_data import catalog
from config import db

app = Flask("server")

@app.get("/")
def home():
    return "hello from flask"

#Create an endpoint that redirects to the about page and 
#it contains your name
@app.get("/about")
def about():
    return "Sergio Inzunza"

################################################################
####################### CATALOG API  ###########################
################################################################

@app.get("/api/version")
def version():
    version = {
        "V":"V.1.0.1",
        "name":"Candy_firewall",
        "yourzip": "your",
    }
    return json.dumps(version)


@app.get("/api/catalog")
def get_catalog():
    cursor = db.products.find({})
    results = []
    for prod in cursor:
        prod["_id"] = str(prod["_id"]) # fix _id issue
        results.append(prod)

    return json.dumps(results)


# save products
@app.post("/api/catalog")
def save_product():
    product = request.get_json()
    db.products.insert_one(product)

    product["_id"] = str(product["_id"]) # clean the ObjectId('asd') from the obj

    return json.dumps(product)
    


# get all products that belong to a category
@app.get("/api/catalog/<category>")
def get_by_category(category):
    cursor = db.products.find({"category": category})
    results = []
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)
    
    return json.dumps(results)


@app.get("/api/catalog/search/<title>")
def search_by_title(title):
    cursor = db.products.find({"title": {"$regex": title, "$options": "i"} })
    results = []
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)
    
    return json.dumps(results)



@app.get('/api/product/cheaper/<price>')
def search_by_price(price):    
    cursor = db.products.find({})
    result = []
    for prod in cursor:
        if prod["price"] < float(price):
            # fix the _id
            prod["_id"] = str(prod["_id"])
            result.append(prod)

    return json.dumps(result)


# create a get endpoint that returns the number of products in the catalog
@app.get("/api/product/count")
def count_products():
    count = db.products.count_documents({})
    return json.dumps(count)
    # pymongo count the elements on a collection


@app.get("/api/product/cheapest")
def get_cheapest():
    cursor = db.products.find({})
    answer = cursor[0]
    for prod in cursor:
        if prod["price"] < answer["price"]:
            answer = prod


    answer["_id"] = str(answer["_id"])
    return json.dumps(answer)




@app.get("/test/numbers")
def get_numbers():
    # create a list with numbers from 1 to 20
    # except 13 and 17
    # and return the list as json
    # [47, 29, 50, 46, 40, 42, 63, 56, 38, 54, 52, 21]
    result = []
    for n in range(1, 21):
        if n != 13 and n != 17:
            result.append(n)
    
    return json.dumps(result)


app.run(debug=True)




