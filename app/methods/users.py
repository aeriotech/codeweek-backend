import uuid
import psycopg2
from psycopg2 import sql
import bcrypt
import base64
import json

conn = psycopg2.connect("dbname='main' user='postgres' host='192.168.0.110' password='123456789'")
curs = conn.cursor()

def userExists(userId):
    curs.execute(sql.SQL("SELECT username FROM users WHERE id={userIdIn}").format(
        userIdIn=sql.Literal(userId)
    ))
    return curs.fetchone() is not None

def userExistsByUsername(username):
    curs.execute(sql.SQL("SELECT id FROM users WHERE username={usernameIn}").format(
        usernameIn=sql.Literal(username)
    ))
    return curs.fetchone() is not None

def getUsernameById(userId):
    curs.execute(sql.SQL("SELECT username FROM users WHERE id={userIdIn}").format(
        userIdIn=sql.Literal(userId)
    ))
    return curs.fetchone()

def getUserByToken(token):
    decodedJson = json.loads(base64.b64decode(token))
    curs.execute(sql.SQL("SELECT id, username, points, has_premium FROM users WHERE id={ajdi}").format(
        ajdi=sql.Literal(decodedJson["userId"])
    ))
    return curs.fetchone()

def getUserIdByUsername(username):
    curs.execute(sql.SQL("SELECT id FROM users WHERE username={usernameIn}").format(
        usernameIn=sql.Literal(username)
    ))
    return curs.fetchone()

def confirmAccessToken(accessTokenIn):
    jsonString = base64.b64decode(accessTokenIn)
    jsonParsed = json.loads(jsonString)
    
    return userExists(jsonParsed['userId'])

def generateAccessToken(userId):
    jsonString = '{"userId": "' + userId + '"}'

    return base64.b64encode(jsonString.encode('utf-8')).decode('utf-8')


def createUser(username, password):
    if userExistsByUsername(username) is True:
        return None

    userId = str(uuid.uuid4())
    passwordBytes = str(password).encode('utf-8')
    salt = bcrypt.gensalt()
    hashedPasswd = str(bcrypt.hashpw(passwordBytes, salt))[2:-1] # hashedPasswd becomes a string like "b'dhjjhdfjhj'". By doing [2:-1] it turns into just "dhjjhdfjhj"
    
    curs.execute(sql.SQL("INSERT INTO users (id, username, password, salt) VALUES ({userIdIn}, {usernameIn}, {passwordIn}, {saltIn});").format(
        userIdIn=sql.Literal(userId),
        usernameIn=sql.Literal(username),
        passwordIn=sql.Literal(hashedPasswd),
        saltIn = sql.Literal(salt)
    ))
    conn.commit()
    return userId

def deleteUser(userId):
    if userExists(userId) is not True:
        return None

    curs.execute(sql.SQL("DELETE FROM users WHERE id={userIdIn};").format(
        userIdIn=sql.Literal(userId)
    ))
    conn.commit()
    return userId

def login(username, password):
    curs.execute(sql.SQL("SELECT password,id,salt FROM users WHERE username={usernameIn}").format(
        usernameIn=sql.Literal(username)
    ))
    passwordDB = curs.fetchone()

    if passwordDB is None:
        return None
    if not len(passwordDB)==3:
        return None

    if not bcrypt.checkpw(password.encode('utf-8'), passwordDB[0].encode('utf-8')):
        return None

    return generateAccessToken(passwordDB[1])
    