import psycopg2
import json
import requests

_conn_ = psycopg2.connect(dbname="main", user="postgres", password="123456789", host="192.168.0.110")
_cur_ = _conn_.cursor()

def _getProductDB_(ean):
	_cur_.execute("SELECT * FROM products WHERE ean = %s", (str(ean),))
	returned = _cur_.fetchall()
	return returned if len(returned)>0 else False

def _getProductAPI_(ean):
	returned = requests.get("http://bazil.si/api/v2/search/?code="+str(ean), headers={"Authorization": "Bearer 1J0i8MmV2BQWJrgcVnGU"})
	if returned.status_code == 404:
		return False
	return json.loads(returned.text)

def _addProductToCache_(ean):
	productJson = _getProductAPI_(ean)
	_cur_.execute("INSERT INTO products (ean, name) VALUES (%s, %s)", (str(ean), productJson[0]["NAME"]))
	_conn_.commit()
	return productJson

def getProduct(ean):
	#checks if the product already exists in OUR database and if no, adds it, and returns the product
	data = _getProductDB_(ean)
	if not data:
		return _addProductToCache_(ean)