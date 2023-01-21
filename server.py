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
    return json.dumps(catalog)


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
    result = []
    for prod in catalog:
        if prod["category"].lower() == category.lower():
            result.append(prod)

    return json.dumps(result)


@app.get("/api/catalog/search/<title>")
def search_by_title(title):
    # return all products whose title CONTAINS the title variable
    result = []
    for prod in catalog:
        if title.lower() in prod["title"].lower():
            result.append(prod)

    return json.dumps(result)



@app.get('/api/product/cheaper/<price>')
def search_by_price(price):
    result = []
    for prod in catalog:
        if prod["price"] < float(price):
            result.append(prod)

    return json.dumps(result)


# create a get endpoint that returns the number of products in the catalog
@app.get("/api/product/count")
def count_products():
    count = len(catalog)
    return json.dumps(count)
    # json.dumps(len(catalog))


@app.get("/api/product/cheapest")
def get_cheapest():
    answer = catalog[0]
    for prod in catalog:
        if prod["price"] < answer["answer"]:
            answer = prod

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




