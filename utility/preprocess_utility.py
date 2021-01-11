import nltk

from lxml import etree
import os
import os.path
import re
from nltk.stem import WordNetLemmatizer
from gensim import corpora, models
from gensim.models import CoherenceModel
import datetime
from numpy import *
import matplotlib.pyplot as plt


class PreprocessUtility:

    #词性还原成一般现在时
    @staticmethod
    def lemmatize_document(res_low):
        # eg. 'has'-> 'have', 'countries' -> 'country'
        word_wnl = WordNetLemmatizer()

        res_lem = []
        for word, pos_tag in res_low:  # only handle verb/nouns
            if pos_tag.startswith('NN'):
                t_word = word_wnl.lemmatize(word, pos='n')
            elif pos_tag.startswith('VB'):
                t_word = word_wnl.lemmatize(word, pos='v')
            else:
                t_word = word

            res_lem.append((t_word, pos_tag))
        return res_lem


    @staticmethod
    def preprocess(input): 

        # divide the sentence into words
        tokens = nltk.word_tokenize(input)

        # pos tagging
        tagwords = nltk.pos_tag(tokens)

        # only keep letter and number
        word_reg = "[^A-Za-z0-9]"

        # removing punctuation,
        res_punc = [(re.sub(word_reg, '', kt[0]), kt[1]) for kt in tagwords]

        res_lem = PreprocessUtility.lemmatize_document(res_punc)  # lemmatization

        output = ''
        # join words into sentence
        for word in res_lem:
            output = output + " " + word[0].lower()

        return output

def main():
    print(PreprocessUtility.preprocess("Jaosn loves cats."))


if __name__ == "__main__":
    main()






