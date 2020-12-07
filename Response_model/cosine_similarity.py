import configparser
import os
from gensim.models import Word2Vec
import gensim
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
from tabulate import tabulate
import sys
sys.path.append(r'./utility')
'''python import模块时， 是在sys.path里按顺序查找的。
sys.path是一个列表，里面以字符串的形式存储了许多路径。
使用A.py文件中的函数需要先将他的文件路径放到sys.path中'''
from rdf_utility import rdfUtility


class cosine_Similarity_Utility:

    
    @staticmethod
    def cosine_distance_rank(model, word, target_list, num):
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
    def cosine_distance(model, word, target_list):
        cosine_dict ={}
        word_list = []
        a = model[word]
        for i in range(len(target_list)):
            # if item != word :
            item = target_list[i]
            b = model[item]
            #cos_sim  = 1 - scipy.spatial.distance.cosine(a, b)
            cos_sim = dot(a, b)/(norm(a)*norm(b))
            word_list.append((item,cos_sim))            
        return word_list


    @staticmethod
    def getData():
        #读取配置文件
        pro_dir = os.path.split(os.path.realpath(__file__))[0]
        config_path = os.path.join(pro_dir, "config.ini")
        #if not os.path.exists(config_path):print("无配置文件")
        config = configparser.ConfigParser()
        config.read(config_path)
        print("Config sections: ", config.sections())
        # path_AI = config.get("Training_Dataset", "wiki_AI")
        # path_Food = config.get("Training_Dataset", "wiki_Food")
        path_Airport = config.get("Training_Dataset", "wiki_Airport")

        # processing the data read from URL
        # scrapped_data = urllib.request.urlopen(path_AI)
        # scrapped_data = urllib.request.urlopen(path_Food)
        scrapped_data = urllib.request.urlopen(path_Airport)
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

        #读取配置文件
        pro_dir = os.path.split(os.path.realpath(__file__))[0]
        config_path = os.path.join(pro_dir, "config.ini")
        #if not os.path.exists(config_path):print("无配置文件")
        config = configparser.ConfigParser()
        config.read(config_path)
        # path_AI = config.get("pretrained_model", "model_AI")
        # path_Food = config.get("pretrained_model", "model_Food")
        path_Airport = config.get("pretrained_model", "model_Airport")
        


        ## Train model
        word2vec = Word2Vec(all_words, min_count=1, size= 50, workers=3, window =3, sg = 1)
        # word2vec.wv.save_word2vec_format(path_AI, binary=True)
        # word2vec.wv.save_word2vec_format(path_Food, binary=True)
        word2vec.wv.save_word2vec_format(path_Airport, binary=True)
        
        ## Load model
        # word2vec = gensim.models.KeyedVectors.load_word2vec_format(model_AI, binary=True)
        # word2vec = gensim.models.KeyedVectors.load_word2vec_format(model_Food, binary=True)       
        # word2vec = gensim.models.KeyedVectors.load_word2vec_format(model_Airport, binary=True)


        return word2vec


    @staticmethod
    def get_wordVec(word2vec):
        vocabulary = word2vec.wv.vocab.keys()  # keys() 代表每一个 unique的单词， word2vec.wv.vocab 是一个dictionary。
        # print("vocabulary: ", vocabulary)
        word_list = list(vocabulary) # All the words
        # print(type(word_list), word_list)
        
        ## the vector of all the words
        vector_all = word2vec.wv[vocabulary]

        #读取配置文件
        pro_dir = os.path.split(os.path.realpath(__file__))[0]
        config_path = os.path.join(pro_dir, "config.ini")
        #if not os.path.exists(config_path):print("无配置文件")
        config = configparser.ConfigParser()
        config.read(config_path)

        # path_AI = config.get("saved_Vector", "vector_AI")
        # df = pd.DataFrame({"word": word_list, "vector": list(vector_all)})   
        # df.to_csv(path_AI, index = None)

        # path_Food = config.get("saved_Vector", "vector_Food")
        # df = pd.DataFrame({"word": word_list, "vector": list(vector_all)})   
        # df.to_csv(path_Food, index = None)

        path_Airport = config.get("saved_Vector", "vector_Airport")
        df = pd.DataFrame({"word": word_list, "vector": list(vector_all)})   
        df.to_csv(path_Airport, index = None)
        
        ## vector_all Length = 2341
        # save words and vectors into csv file
        
    
        return vector_all, word_list, vocabulary


    @staticmethod
    def similarity_Cal(word2vec, word_list):

        ## Most similar words 
        sim_words = word2vec.wv.most_similar('intelligence')
        # print("sim_words of ‘intelligence’ : ",sim_words )

        ## The 5 words with the most similar meanings
        most_5 = cosine_Similarity_Utility.cosine_distance(word2vec.wv, 'intelligence',  word_list)
        # print("top 5 words: ", most_5, type(most_5))
    
        return sim_words, most_5


    #word2vec: word embedding 模型
    #inputTriple: inputTriple from openie
    #word_lists: rdfUtility.getAlltriples(namespace)
    #return: triple gaint most similarity score
    @staticmethod
    def triple_Similarity(inputTriple):
        # try:
        # #读取配置文件
        # pro_dir = os.path.split(os.path.realpath(__file__))[0]
        # config_path = os.path.join(pro_dir, "config.ini")
        # #if not os.path.exists(config_path):print("无配置文件")
        # config = configparser.ConfigParser()
        # config.read(config_path)
        # namespace = config.get("config","rdfNamespace")
        ## prepare tranning, get data
        article_text = cosine_Similarity_Utility.getData()
        all_words = cosine_Similarity_Utility.textPreprocessing(article_text)
        ## train get the model
        word2vec = cosine_Similarity_Utility.train_Model(all_words)
        # vector_all, word_list, vocabulary = cosine_Similarity_Utility.get_wordVec(word2vec)

        score1 = []
        score2 = []
        score3 = []
        final_Score_list = []
        
        # get input subj, obj, rel
        subj = inputTriple['subject']
        obj = inputTriple['object']
        rel = inputTriple['relation']
        

        word_lists = rdfUtility.getAlltriples()
        Top_subj = cosine_Similarity_Utility.cosine_distance(word2vec.wv, subj,  word_lists[0])
        Top_obj = cosine_Similarity_Utility.cosine_distance(word2vec.wv, obj,  word_lists[1])
        Top_rel = cosine_Similarity_Utility.cosine_distance(word2vec.wv, rel,  word_lists[2])  

        for i in range(len(Top_subj)):
            #计算总分
            final_Score = Top_subj[i][1] * 0.3 + Top_obj[i][1] * 0.3 + Top_rel[i][1] * 0.4
            final_Score_list.append(final_Score)

        #获的最高总分triple的index
        a = np.array(final_Score_list)
        idx = np.argmax(a)
        max_triple = Top_subj[idx][0] + " | "  + Top_rel[idx][0] + " | " + Top_obj[idx][0]  
        print("Triple ",max_triple,"gaint the highest final score: ",final_Score_list[idx])
        #ToDo: 通过实验，修改阈值。。。
        if(final_Score_list[idx] < 0.01):
            return None  
        return max_triple  
        # except:
        #     return None  

        # #读取配置文件
        # pro_dir = os.path.split(os.path.realpath(__file__))[0]
        # config_path = os.path.join(pro_dir, "config.ini")
        # #if not os.path.exists(config_path):print("无配置文件")
        # config = configparser.ConfigParser()
        # config.read(config_path)
        # path = config.get("config","Triple_Score")

        # # WRITE TRIPLE SCORES INTO FILE 
        # df = pd.DataFrame({"subject_score":score1, "object_score": score2, "relation_score": score3})
        # #print("df.shape", df.shape)
        # df.to_csv(path, index = None)


        # # READ TRIPLE SCORES FROM FILE 
        # col_list = ["subject_score", "object_score", "relation_score"]
        # df2 = pd.read_csv(path, usecols=col_list)
        # #print(df2["subject_score"], len(df2["subject_score"]))

        # for i in range(len(df2["subject_score"])):

        #     # Calculate the final score
        #     final_Score = df2["subject_score"][i] * 0.3 + df2["object_score"][i] * 0.3 + df2["relation_score"][i] * 0.4
        #     final_Score_list.append(final_Score)
        #     maxValue = max(final_Score_list)
            
        #     data = [
        #         ('subject', subject_score, subject_name)
        #         # ('object', object_score, object_name),
        #         # ('relation', relation_score, relation_name),
        #         # ('Final Score', final_Score)
        #         ]
        #     #print (tabulate(data, headers=["", "Score", "Name"]))

        #     # 找到总体分数最高的那一组 triple， 并打印出来。
        #     if (final_Score == maxValue):
        #         triple = subject_name + " | "  + relation_name + " | " + object_name       
        
        
            
def main():

    # # Train 输入新数据训练不同Domain的模型，并且存储预训练模型在本地。
    article_text = cosine_Similarity_Utility.getData()
    all_words = cosine_Similarity_Utility.textPreprocessing(article_text)
    # # print("all words: \n", all_words)

    
    word2vec = cosine_Similarity_Utility.train_Model(all_words)
    vector_all, word_list, vocabulary = cosine_Similarity_Utility.get_wordVec(word2vec)
    print(word_list, len(word_list))
    print('Done')
    

    ## Test input Triple. 使用自定义的 input triple，测试预训练模型。 
    # inputTriple = {"subject": "human", "relation": "develop", "object": "ai"}
    # inputTriple = {"subject": "people", "relation": "eat", "object": "food"}
    # triple = cosine_Similarity_Utility.triple_Similarity(inputTriple)
    # print(triple)
 

if __name__ == "__main__":
     main()

