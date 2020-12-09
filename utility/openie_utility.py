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
        # text = 'Barack Obama was born in Hawaii. Richard Manning wrote this sentence.'
        # print('Text: %s.' % sentence)
            for triple in client.annotate(sentence):
                #print('|-', triple)
                triples.append(triple)
        return triples

def main():
    input = "Human eat plants."
    text = PreprocessUtility.preprocess(input)
    aa = OpenieUtility.sentence_to_triple(text)
    print(aa)

if __name__ == "__main__":
    main()




    
        