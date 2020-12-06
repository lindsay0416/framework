import configparser
import os
from datetime import datetime
import jsonlines

class Utility:

    @staticmethod
    def write_input_to_file(data):
        #读取配置文件
        pro_dir = os.path.split(os.path.realpath(__file__))[0]
        config_path = os.path.join(pro_dir, "config.ini")
        #if not os.path.exists(config_path):print("无配置文件")
        config = configparser.ConfigParser()
        config.read(config_path)
        path = config.get("config","inputLogPath")
        ## Get timestamp
        # Converting datetime object to string
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        # print('Current Timestamp : ', timestampStr)
        data['timestamp'] = timestampStr
        # Write the sentences into jsonl file.
        with jsonlines.open(path,"a") as js_writer: 
            js_writer.write(data)


    @staticmethod
    def write_triple_to_file(triples):
        #读取配置文件
        pro_dir = os.path.split(os.path.realpath(__file__))[0]
        config_path = os.path.join(pro_dir, "config.ini")
        #if not os.path.exists(config_path):print("无配置文件")
        config = configparser.ConfigParser()
        config.read(config_path)
        path = config.get("config","tripleLogPath")
        #write triple to file
        with jsonlines.open(path,"a") as js_writer: 
            js_writer.write_all(triples)
        




    
        