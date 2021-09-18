from flask import request
from api import app


@app.route("/")
def index():
    return f"{request.url}"
