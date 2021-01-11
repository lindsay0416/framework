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
                # print('|-', triple)
                triples.append(triple)
        return triples

def main():
    input_text = "jason love cat"
    text = PreprocessUtility.preprocess(input_text)
    print(text)
    aa = OpenieUtility.sentence_to_triple(input_text)
    print(aa)


if __name__ == "__main__":
    main()