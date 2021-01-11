# This is a Flask Server

from flask import Flask, request, jsonify, send_from_directory
import websocket
import threading
import json
import time
import configparser
import sys
sys.path.append(r'./utility')
sys.path.append(r'./Response_model')
from rdf_utility import rdfUtility
from preprocess_utility import PreprocessUtility
from utility import Utility
from openie_utility import OpenieUtility
from cosine_similarity import cosine_Similarity_Utility
from Load_T5_model import TextGenerationUtility

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
        #data preprocessing 
        inputList = user_input.split( )
        #切换用户命令： select<username>
        if len(inputList) == 2 and inputList[0] == "select":
            #读取配置文件
            conf = configparser.ConfigParser()
            filepath = "Config/config.ini"
            conf.read(filepath)
            node ="config"
            key = "rdfNamespace"
            value = inputList[1]
            conf.set(node,key,value)
            fh = open(filepath ,'w')
            conf.write(fh)
            fh.close()
            return "Selected user: "+inputList[1]
        elif user_input == "init":
            responseData = rdfUtility.getAlldata() # 用来显示KG的数据。
            config = configparser.ConfigParser()
            config.read("Config/config.ini")
            namespace = config.get("config","rdfNamespace")
            responseData["namespace"] = namespace
            return responseData
        else:
            responseText = ""
            # Handle user input 
            data = {}
            data['text'] = user_input
            print("User input: ", user_input)
            Utility.write_input_to_file(data)
            # OpenIE， Sentence --> triple[]
            #in this case we only focus on the first triple generate from openie
            triples = OpenieUtility.sentence_to_triple(user_input)
            triple = triples[0]

            triple["subject"] = PreprocessUtility.preprocess(triple["subject"]).strip()
            triple["relation"] = PreprocessUtility.preprocess(triple["relation"]).strip()
            triple["object"] = PreprocessUtility.preprocess(triple["object"]).strip()
            print("Triple from input: ",triple)
            # write triples to file 
            Utility.write_triple_to_file(triple)
            
            # 计算 triple 相似度，并在RDF DB中找出需要返回的triple。
            t = cosine_Similarity_Utility.triple_Similarity(triple)
            if t != None:
                # 将找出的triple generate 为 text。作为response 返回给前端。
                tokenizer, model_saved = TextGenerationUtility.load_Model() 
                responseText = TextGenerationUtility.generate(t, model_saved, tokenizer) 
                print("Text generated from finded triple: ", responseText)
            else:    
                # 如果没有在RDF DB中找到适合的Triple， 将请求转发给Parlai server.
                print("Similar triple not founed in KG, transfering request...")
                SHARED['ws'].send('{"text": "'+user_input+'"}')
                message_available.wait()
                responseText = new_message
                message_available.clear()
            #将输入的triples存入KG
            add_triple_KG(triple)
            responseData = rdfUtility.getAlldata() # 用来显示KG的数据。
            responseData["Text"] = responseText
            print(responseData)
            return responseData


def add_triple_KG(triple):
    rdfUtility.add((triple["subject"],triple["relation"],triple["object"]))
    added_triple = triple["subject"] + " | "  + triple["relation"] + " | " + triple["object"]  
    print("Triple ",added_triple,"added to KG.")

def getRDFData():
    rdfUtility.getAlldata()
        

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
    time.sleep(2)
    SHARED['ws'].send('{"text": "begin"}')
    message_available.wait()
    message_available.clear()
    SHARED['ws'].send('{"text": "begin"}')
    message_available.wait()
    message_available.clear()
     
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='localhost', port=5000, debug=False)
    print('Please connect to the link: http://{}:{}/'.format("localhost", 5000))