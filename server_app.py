# This is a Flask Server

from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)


@app.route("/")
def root():
    return send_from_directory("public", "annotation.html")


@app.route('/<path:path>')
def send_html(path):
    return send_from_directory('./public', path)


@app.route('/give_response', methods=('POST', 'GET'))
# the function name must be the same as the URL
def give_response():
    if request.method == 'GET':
        s = "hello word - a test message - GET"
        print(s)
        return s
    if request.method == 'POST':
        user_input = request.form['user_input']
        # logic xxxxx
        s = "hello word"
        print(s)
        return s
        # return jsonify(results)


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='localhost', port=5000, debug=True)
