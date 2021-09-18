from flask import request
from psycopg2.sql import NULL
from app import app
from app.methods import users, items


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
    #checks user validity and get ID
    if request.headers.get("Authorization") == None:
        return "400; invalid Authorization token", 400
    token = request.headers.get("Authorization").replace("Bearer ", "")
    user = users.getUserByToken(token)
    if user is None:
        return "404; user not found", 404
    else:
        return items.getUserThings(user[0])

@app.route("/items/new", methods=["POST"])
def newItem():
    data = request.get_json()
    try:
        ean = data["ean"]
        if ean is None:
            return "400; malformed json/invalid syntax", 400
    except KeyError:
        return "400; malformed json/invalid syntax", 400
    #checks user validity and get ID
    if request.headers.get("Authorization") == None:
        return "400; invalid Authorization token", 400
    token = request.headers.get("Authorization").replace("Bearer ", "")
    user = users.getUserByToken(token)
    if user is None:
        return "404; user not found", 404
    else:
        try:
            expiration = data["expiration"]
        except KeyError:
            items.insertThing(user[0], ean)
        else:
            items.insertThing(user[0], ean, expiration)
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
    #checks user validity and get ID
    if request.headers.get("Authorization") == None:
        return "400; invalid Authorization token", 400
    token = request.headers.get("Authorization").replace("Bearer ", "")
    user = users.getUserByToken(token)
    if user is None:
        return "404; user not found", 404
    else:
        #verifies that the user is trying to delete their own item only
        user_items = items.getUserThings(user[0])
        if len(user_items) == 0:
            return "401; You can't delete that item/Item doesn't exist!", 401
        if itemId not in [x["id"] for x in user_items]:
            return "401; You can't delete that item/Item doesn't exist!", 401
        else:
            items.deleteThing(str(itemId))
            return "200; deleted", 200
