import uuid
import psycopg2
from psycopg2 import sql
import bcrypt

pepper = "pepper cool"
conn = psycopg2.connect("dbname='main' user='postgres' host='192.168.0.110' password='123456789'")
curs = conn.cursor()

def createUser(username, password):
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