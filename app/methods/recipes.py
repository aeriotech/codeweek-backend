import psycopg2
import json
from . import general

_conn_ = psycopg2.connect(dbname="main", user="postgres", password="123456789", host="192.168.0.110")
_cur_ = _conn_.cursor()

def getRecipes(premium):
	if premium:
		_cur_.execute("SELECT * FROM \"recipes\"")
	else:
		_cur_.execute("SELECT * FROM \"recipes\" WHERE premium = false")
	return general.mycursor_to_json(_cur_)

def getRecipe(recipeId):
	_cur_.execute("SELECT * FROM \"recipes\" WHERE id = %s", (recipeId, ))
	return general.mycursor_to_json(_cur_)

def addRecipe(name, imgUrl, ingredients, url, procedure, vegan, authorId, premium):
	_cur_.execute("INSERT INTO \"recipes\" (\"name\", \"imgUrl\", \"ingredients\", \"url\", \"procedure\", \"vegan\", \"authorId\",  \"premium\") VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (name, imgUrl, ingredients, url, procedure, vegan, authorId, premium, ))
	_conn_.commit()