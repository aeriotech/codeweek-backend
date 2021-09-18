import uuid
import psycopg2
from psycopg2 import sql
import bcrypt

pepper = "pepper cool"
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

def getUserIdByUsername(username):
    curs.execute(sql.SQL("SELECT id FROM users WHERE username={usernameIn}").format(
        usernameIn=sql.Literal(username)
    ))
    return curs.fetchone()


def createUser(username, password):
    if userExistsByUsername(username) is True:
        return None

    userId = str(uuid.uuid4())
    passwordBytes = str(password).encode('utf-8')
    salt = bcrypt.gensalt()
    hashedPasswd = str(bcrypt.hashpw(passwordBytes, salt))
    
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