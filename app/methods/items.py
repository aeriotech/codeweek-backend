import psycopg2
import json
from . import general

_conn_ = psycopg2.connect(dbname="main", user="postgres", password="123456789", host="192.168.0.110")
_cur_ = _conn_.cursor()

def getUserThings(user_id):
	_cur_.execute("SELECT id, ean, expiration_timestamp FROM \"itemInstances\" WHERE owner_id = %s", (user_id, ))
	r = general.mycursor_to_json(_cur_)
	return([] if r is None else r)

def insertThing(user_id, ean, exp=None):
	_cur_.execute("INSERT INTO \"itemInstances\" (owner_id, ean, expiration_timestamp) VALUES (%s, %s, %s)", (user_id, ean, "0" if exp is None else exp))
	_conn_.commit()

def deleteThing(id):
	_cur_.execute("DELETE FROM \"itemInstances\" WHERE id = %s", (id, ))
	_conn_.commit()

