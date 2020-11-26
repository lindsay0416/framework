import configparser
import os
from gensim.models import Word2Vec
import bs4 as bs
import urllib.request
import re
import nltk
from nltk.corpus import stopwords
import numpy as np
from numpy import dot
from numpy.linalg import norm
import scipy
import pandas as pd


class cosine_Similarity_Utility:


    @staticmethod
    def cosine_distance(model, word, target_list, num):
        cosine_dict ={}
        word_list = []
        a = model[word]
        for item in target_list :
            if item != word :
                b = model[item]
                cos_sim  = 1 - scipy.spatial.distance.cosine(a, b)
                # cos_sim = dot(a, b)/(norm(a)*norm(b))
                cosine_dict[item] = cos_sim
        dist_sort=sorted(cosine_dict.items(), key=lambda dist: dist[1],reverse = True) ## in Descedning order 
        for item in dist_sort:
            word_list.append((item[0], item[1]))
            
        return word_list[0:num]


    @staticmethod
    def getData():
        #读取配置文件
        pro_dir = os.path.split(os.path.realpath(__file__))[0]
        config_path = os.path.join(pro_dir, "config.ini")
        #if not os.path.exists(config_path):print("无配置文件")
        config = configparser.ConfigParser()
        config.read(config_path)
        path = config.get("config","URL")
        # processing the data read from URL
        scrapped_data = urllib.request.urlopen(path)
        article = scrapped_data .read()
        parsed_article = bs.BeautifulSoup(article,'lxml')
        paragraphs = parsed_article.find_all('p')
        
        article_text = ""
        for p in paragraphs:
            article_text += p.text

        return article_text

    @staticmethod
    def textPreprocessing(article_text):

    # Cleaing the text
        processed_article = article_text.lower()
        processed_article = re.sub('[^a-zA-Z]', ' ', processed_article )
        processed_article = re.sub(r'\s+', ' ', processed_article)
        # Preparing the dataset
        all_sentences = nltk.sent_tokenize(processed_article)
        all_words = [nltk.word_tokenize(sent) for sent in all_sentences]

        # Removing Stop Words
        for i in range(len(all_words)):
            all_words[i] = [w for w in all_words[i] if w not in stopwords.words('english')]

        return all_words


    @staticmethod
    def train_Model(all_words):

        word2vec = Word2Vec(all_words, min_count=1, size= 50, workers=3, window =3, sg = 1)        
        # print("vocabulary: ", vocabulary)
        return word2vec

    @staticmethod
    def get_wordVec(word2vec):
        vocabulary = word2vec.wv.vocab.keys()  # keys() 代表每一个 unique的单词， word2vec.wv.vocab 是一个dictionary。
        word_list = list(vocabulary) # All the words
        
        ## the vector of all the words
        vector_all = word2vec.wv[vocabulary]

        #读取配置文件
        pro_dir = os.path.split(os.path.realpath(__file__))[0]
        config_path = os.path.join(pro_dir, "config.ini")
        #if not os.path.exists(config_path):print("无配置文件")
        config = configparser.ConfigParser()
        config.read(config_path)
        path = config.get("config","word_VectorPath")
        
        ## vector_all Length = 2341
        # save words and vectors into csv file
        df = pd.DataFrame({"word": word_list, "vector": list(vector_all)})   
        df.to_csv(path, index = None)
    
        return vector_all, word_list, vocabulary


    @staticmethod
    def similarity_Cal(word2vec, word_list):

        ## Most similar words 
        sim_words = word2vec.wv.most_similar('intelligence')
        print("sim_words of ‘intelligence’ : ",sim_words )

        ## The 5 words with the most similar meanings
        most_5 = cosine_Similarity_Utility.cosine_distance(word2vec.wv, 'intelligence',  word_list, 5)
        print("word list", most_5)

        return sim_words, most_5



def main():

    article_text = getData()
    all_words = textPreprocessing(article_text)

    ## Train
    word2vec = train_Model(all_words)


    vector_all, word_list, vocabulary = get_wordVec(word2vec)
    sim_words, Num = similarity_Cal(word2vec, word_list)
 
if __name__ == "__main__":
    main()

