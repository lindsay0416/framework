import configparser
import os
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration,Adafactor

import warnings
warnings.filterwarnings("ignore")


class TextGenerationUtility:

    @staticmethod
    def load_Model():
        #读取配置文件
        pro_dir = os.path.split(os.path.realpath(__file__))[0]
        config_path = os.path.join(pro_dir, "config.ini")
        #if not os.path.exists(config_path):print("无配置文件")
        config = configparser.ConfigParser()
        config.read(config_path)
        path_entireModel = config.get("config","T5_pretrained_model")
        path_testModel = config.get("config","T5_test_model")

        ## Load Model
        tokenizer = T5Tokenizer.from_pretrained('t5-base')

        # Epoch = 1, entire single triple WebNLG dataset
        model_saved = torch.load(path_entireModel)

        ## Epoch = 1, test on only one file of single triple WebNLG dataset
        # model_saved = torch.load(path_testModel)

        return tokenizer, model_saved



    @staticmethod
    def generate(text,model_saved,tokenizer):
        model_saved.eval()
        input_ids = tokenizer.encode("WebNLG:{} </s>".format(text), 
                                            return_tensors="pt")  
        # input_ids  = input_ids.to(dev)
        outputs = model_saved.generate(input_ids)
        return tokenizer.decode(outputs[0])







