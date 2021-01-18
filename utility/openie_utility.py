import configparser
import os
from openie import StanfordOpenIE
import pandas as pd
import jsonlines
import json
import spacy 
from preprocess_utility import PreprocessUtility


class OpenieUtility:
    client =  StanfordOpenIE()
    
    @staticmethod
    def sentence_to_triple(sentence):
        triples = []
        # client =  StanfordOpenIE()
        for triple in OpenieUtility.client.annotate(sentence):
            # print('|-', triple)
            triples.append(triple)
        return triples

def main():
    input_text = "Billy‘s genre is rap music."
    aa = OpenieUtility.sentence_to_triple(input_text)
    print(aa)



if __name__ == "__main__":
    main()