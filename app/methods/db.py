import psycopg2
import json
import requests
from . import general

_conn_ = psycopg2.connect(dbname="main", user="postgres",
                          password="123456789", host="192.168.0.110")
_cur_ = _conn_.cursor()

def getInfoByEan(ean):
	#checks if product exists in our database
	_cur_.execute("SELECT ean, name, type FROM \"products\" WHERE ean = %s", (ean, ))
	r = general.mycursor_to_json(_cur_)
	if r is None or r == []:
		#product doesn't exist in OUR database, get it from external and add it to ours
		externalDbResult = requests.get("http://bazil.si/api/v2/search/?code="+str(ean), headers={"Authorization": "Bearer 1J0i8MmV2BQWJrgcVnGU"})
		if externalDbResult.status_code == 404:
			return None
		externalJson = json.loads(externalDbResult.content)
		_cur_.execute("INSERT INTO \"products\" (ean, name) VALUES (%s, %s)", (str(ean), externalJson[0]["NAME"]))
		_conn_.commit()
		return getInfoByEan(ean)
	else:
		#product exists with us, returns just our result, translated to JSON
		return r
