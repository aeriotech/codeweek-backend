from app.views import app

PORT = 5000
HOST = "0.0.0.0"
DEBUG = True

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
