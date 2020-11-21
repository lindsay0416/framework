from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!" + "def"


@app.route("/twitter")
def test():
    return "connect to the database"


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
