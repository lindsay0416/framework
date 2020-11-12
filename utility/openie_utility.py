import configparser
import os
from openie import StanfordOpenIE
import pandas as pd
import jsonlines
import json
import spacy 


class OpenieUtility:

    @staticmethod
    def sentence_to_triple(sentence):
        triples = []
        with StanfordOpenIE() as client:
        # text = 'Barack Obama was born in Hawaii. Richard Manning wrote this sentence.'
        # print('Text: %s.' % sentence)
            for triple in client.annotate(sentence):
                # print('|-', triple)
                triples.append(triple)
        return triples




    
        