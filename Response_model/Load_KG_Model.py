
import pandas as pd
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration,Adafactor
import glob
import os
import re
import xml.etree.ElementTree as ET
import pandas as pd



tokenizer = T5Tokenizer.from_pretrained('t5-base')

model =T5ForConditionalGeneration.from_pretrained('/Users/lindsay/Downloads/archive_2', return_dict=True)


def generate(text,model,tokenizer):
    model.eval()
    input_ids = tokenizer.encode("WebNLG:{} </s>".format(text), 
                                return_tensors="pt")  
    outputs = model.generate(input_ids)
    return tokenizer.decode(outputs[0])

