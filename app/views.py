from flask import request
from psycopg2.sql import NULL
from app import app
from app.methods import users, items, recipes, general, db
import json


@app.route("/")
def index():
    return f"{request.url}"


@app.route("/createUser", methods=['POST'])
def createUserEndpoint():
    data = request.get_json()
    try:
        username = data['username']
        password = data['password']
        if username is None or password is None:
            return "400; malformed json/invalid syntax", 400
    except KeyError:
        return "400; malformed json/invalid syntax", 400
    userId = users.createUser(username, password)
    if userId is None:
        return "400; username already taken", 400
    return f"{userId}", 200


@app.route("/deleteUser", methods=['POST'])
def deleteUserEndpoint():
    data = request.get_json()
    try:
        userId = data['userId']
        if userId is None:
            return "400; malformed json/invalid syntax", 400
    except KeyError:
        return "400; malformed json/invalid syntax", 400
    userId = users.deleteUser(userId)
    if userId is None:
        return "400; user does not exist", 400
    return f"{userId}", 200


@app.route("/login", methods=['POST'])
def loginEndpoint():
    data = request.get_json()
    try:
        username = data['username']
        password = data['password']
        if username is None or password is None:
            return "400; malformed json/invalid syntax", 400
    except KeyError:
        return "400; malformed json/invalid syntax", 400
    accessToken = users.login(username, password)
    if accessToken is None:
        return "401; invalid username/password", 401
    return f"{accessToken}", 200


@app.route("/items", methods=["GET"])
def getItems():
    # checks user validity and get ID
    if request.headers.get("Authorization") == None:
        return "400; invalid Authorization token", 400
    token = request.headers.get("Authorization").replace("Bearer ", "")
    user = users.getUserByToken(token)
    if user is None:
        return "404; user not found", 404
    else:
        return json.dumps(items.getUserThings(user[0]))


@app.route("/items/new", methods=["POST"])
def newItem():
    data = request.get_json()
    if "number" in request.args:
        number = request.args["number"]
    else:
        number = 1
    try:
        ean = data["ean"]
        if ean is None:
            return "400; malformed json/invalid syntax", 400
    except KeyError:
        return "400; malformed json/invalid syntax", 400
    # checks user validity and get ID
    if request.headers.get("Authorization") is None:
        return "400; invalid Authorization token", 400
    token = request.headers.get("Authorization").replace("Bearer ", "")
    user = users.getUserByToken(token)
    if user is None:
        return "404; user not found", 404
    try:
        expiration = data["expiration"]
    except KeyError:
        items.insertThing(user[0], ean, number=number)
    else:
        items.insertThing(user[0], ean, exp=expiration, number=number)
    return ("200; Item Added", 200)


@app.route("/items/delete", methods=["POST"])
def removeItem():
    data = request.get_json()
    try:
        itemId = data["itemId"]
        if itemId is None:
            return "400; malformed json/invalid syntax", 400
    except KeyError:
        return "400; malformed json/invalid syntax", 400
    # checks user validity and get ID
    if request.headers.get("Authorization") is None:
        return "400; invalid Authorization token", 400
    token = request.headers.get("Authorization").replace("Bearer ", "")
    user = users.getUserByToken(token)
    if user is None:
        return "404; user not found", 404
    # verifies that the user is trying to delete their own item only
    user_items = items.getUserThings(user[0])
    if len(user_items) == 0:
        return "401; You can't delete that item/Item doesn't exist!", 401
    if itemId not in [x["id"] for x in user_items]:
        return "401; You can't delete that item/Item doesn't exist!", 401
    items.deleteThing(str(itemId))
    return "200; deleted", 200


@app.route("/user/points", methods=["GET"])
def getPoints():
    # checks user validity and get ID
    if request.headers.get("Authorization") == None:
        return "400; invalid Authorization token", 400
    token = request.headers.get("Authorization").replace("Bearer ", "")
    user = users.getUserByToken(token)
    if user is None:
        return "404; user not found", 404
    else:
        return {
            "userId": user[0],
            "points": user[2]
        }


@app.route("/user/points/add/<number>", methods=["GET"])
def addPoints(number):
    # checks user validity and get ID
    if request.headers.get("Authorization") == None:
        return "400; invalid Authorization token", 400
    token = request.headers.get("Authorization").replace("Bearer ", "")
    user = users.getUserByToken(token)
    if user is None:
        return "404; user not found", 404
    else:
        return json.dumps(users.changePoints(user[0], number))


@app.route("/user/username")
def getUsername():
    # checks user validity and get ID
    if request.headers.get("Authorization") == None:
        return "400; invalid Authorization token", 400
    token = request.headers.get("Authorization").replace("Bearer ", "")
    user = users.getUserByToken(token)
    if user is None:
        return "404; user not found", 404
    else:
        return {
            "userId": user[0],
            "username": user[1]
        }


@app.route("/user/premium")
def getPremium():
    # checks user validity and get ID
    if request.headers.get("Authorization") == None:
        return "400; invalid Authorization token", 400
    token = request.headers.get("Authorization").replace("Bearer ", "")
    user = users.getUserByToken(token)
    if user is None:
        return "404; user not found", 404
    else:
        return {
            "userId": user[0],
            "premium": user[3]
        }


@app.route("/recipes")
def getRecipes():
    # checks user validity and get ID
    if request.headers.get("Authorization") == None:
        return "400; invalid Authorization token", 400
    token = request.headers.get("Authorization").replace("Bearer ", "")
    user = users.getUserByToken(token)
    if user is None:
        return "404; user not found", 404
    else:
        if "ingredients" in request.args:
            ingredients = request.args.get("ingredients").split(",")
            print(recipes.getRecipes(True))
            print(ingredients)
            return json.dumps([recept for recept in recipes.getRecipes(user[3]) if general.sublist(ingredients, json.loads(recept["ingredients"]))])
        return json.dumps(recipes.getRecipes(user[3]))


@app.route("/recipes/<id>")
def getRecipe(id):
    # checks user validity and get ID
    if request.headers.get("Authorization") == None:
        return "400; invalid Authorization token", 400
    token = request.headers.get("Authorization").replace("Bearer ", "")
    user = users.getUserByToken(token)
    if user is None:
        return "404; user not found", 404
    else:
        recipe = recipes.getRecipe(id)
        if len(recipe) == 0:
            return "404; not found", 404
        else:
            recipe = recipe[0]
        if recipe["premium"]:
            if user[3]:
                return recipe
            else:
                return "403; you can't get this recipe", 403
        else:
            return recipe


@app.route("/recipe/create", methods=["POST"])
def createRecipe():
    data = request.get_json()
    try:
        name = data["name"]
        imgUrl = data["imgUrl"]
        ingredients = data["ingredients"]
        url = data["url"]
        procedure = data["procedure"]
        vegan = data["vegan"]
        premium = data["premium"]
        if None in [name, imgUrl, ingredients, url, procedure, vegan, premium]:
            return "400; malformed json/invalid syntax", 400
    except KeyError:
        return "400; malformed json/invalid syntax", 400
    # checks user validity and get ID
    if request.headers.get("Authorization") == None:
        return "400; invalid Authorization token", 400
    token = request.headers.get("Authorization").replace("Bearer ", "")
    user = users.getUserByToken(token)
    if user is None:
        return "404; user not found", 404
    else:
        recipes.addRecipe(name, imgUrl, ingredients, url,
                          procedure, vegan, user[0], premium)
        return "200; ok", 200

@app.route("/ean/<ean>")
def getByEan(ean):
    res = db.getInfoByEan(ean)
    if res is None:
        return "404; Invalid ean code", 404
    return json.dumps(res)

@app.route("/recipe/delete/<id>")
def deleteRecipe(id):
    recipes.deleteRecipe(id)
    return("200; Ok", 200)