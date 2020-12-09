import configparser
import os
from openie import StanfordOpenIE
import pandas as pd
import jsonlines
import json
import spacy 
from preprocess_utility import PreprocessUtility


class OpenieUtility:

    @staticmethod
    def sentence_to_triple(sentence):
        triples = []
        with StanfordOpenIE() as client:
            for triple in client.annotate(sentence):
                print('|-', triple)
                triples.append(triple)
        return triples

def main():
    # input_text = "Human eat plants."
    input_text = 'Barack Obama was born in Hawaii. Richard Manning wrote this sentence.'
    text = PreprocessUtility.preprocess(input_text)
    print(text)
    aa = OpenieUtility.sentence_to_triple(text)
    print(aa)

if __name__ == "__main__":
    main()




    
        