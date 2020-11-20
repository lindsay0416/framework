# This is a Flask Server

from flask import Flask, request, jsonify, send_from_directory
import websocket
import threading
import json

app = Flask(__name__)
new_message = None
message_available = threading.Event()
SHARED = {}


@app.route("/")
def root():
    return send_from_directory("public", "chatbot.html")


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
        SHARED['ws'].send('{"text": "'+user_input+'"}')
        # logic xxxxx
        message_available.wait()
        s = new_message
        message_available.clear()
        # s = "hello word"
        # print(s)
        return s
        # return jsonify(results)




def setup_interactive(ws):
    SHARED['ws'] = ws

def on_message(ws, message):
    """
    Prints the incoming message from the server.

    :param ws: a WebSocketApp
    :param message: json with 'text' field to be printed
    """
    incoming_message = json.loads(message)
    global new_message
    new_message = incoming_message['text']
    message_available.set()
    print(new_message)

def on_error(ws, error):
    """
    Prints an error, if occurs.

    :param ws: WebSocketApp
    :param error: An error
    """
    print(error)

def on_close(ws):
    """
    Cleanup before closing connection.

    :param ws: WebSocketApp
    """
    # Reset color formatting if necessary
    print("Connection closed")

def _run_browser():
    print("open")
    port = 10001
    print("Connecting to port: ", port)
    ws = websocket.WebSocketApp(
        "ws://localhost:{}/websocket".format(port),
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    #ws.on_open = on_open
    setup_interactive(ws)
    ws.run_forever()

def on_open(ws):
    """
    Starts a new thread that loops, taking user input and sending it to the websocket.

    :param ws: websocket.WebSocketApp that sends messages to a browser_manager
    """
    


if __name__ == '__main__':
    
    threading.Thread(target=_run_browser).start()
     
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='localhost', port=5000, debug=True)
    print('Please connect to the link: http://{}:{}/'.format("localhost", 5000))

    

    
