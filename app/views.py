from flask import request
from psycopg2.sql import NULL
from app import app
from app.methods import users


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