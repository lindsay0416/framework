
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration,Adafactor

import warnings
warnings.filterwarnings("ignore")


class TextGenerationUtility:

    @staticmethod
    def load_Model():
        ## Load Model
        tokenizer = T5Tokenizer.from_pretrained('t5-base')

        # Epoch = 1, entire single triple WebNLG dataset
        model_saved = torch.load('/Users/lindsay/Desktop/AAMAS_Demo/Entire_model/pytoch_model.bin')

        ## Epoch = 1, test on only one file of single triple WebNLG dataset
        # model_saved = torch.load('/Users/lindsay/Desktop/AAMAS_Demo/T5_test/pytoch_model.bin')

        return tokenizer, model_saved



    @staticmethod
    def generate(text,model_saved,tokenizer):
        model_saved.eval()
        input_ids = tokenizer.encode("WebNLG:{} </s>".format(text), 
                                            return_tensors="pt")  
        # input_ids  = input_ids.to(dev)
        outputs = model_saved.generate(input_ids)
        return tokenizer.decode(outputs[0])







