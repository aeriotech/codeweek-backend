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
    return f"{userId}", 200