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
from tabulate import tabulate


class cosine_Similarity_Utility:

    
    # @staticmethod
    # def cosine_distance(model, word, target_list, num):
    #     cosine_dict ={}
    #     word_list = []
    #     a = model[word]
    #     for item in target_list :
    #         if item != word :
    #             b = model[item]
    #             cos_sim  = 1 - scipy.spatial.distance.cosine(a, b)
    #             # cos_sim = dot(a, b)/(norm(a)*norm(b))
    #             cosine_dict[item] = cos_sim
    #     dist_sort=sorted(cosine_dict.items(), key=lambda dist: dist[1],reverse = True) ## in Descedning order 
    #     for item in dist_sort:
    #         word_list.append((item[0], item[1]))
            
    #     return word_list[0:num]



    @staticmethod
    def cosine_distance(model, word, target_list):
        cosine_dict ={}
        word_list = []
        a = model[word]
        for item in target_list :
            # if item != word :
            b = model[item]
            cos_sim  = 1 - scipy.spatial.distance.cosine(a, b)
            # cos_sim = dot(a, b)/(norm(a)*norm(b))
            cosine_dict[item] = cos_sim      
        for item in cosine_dict.items():
            word_list.append((item[0], item[1]))
            
        return word_list


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
        # print(type(word_list), word_list)
        
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
        # print("sim_words of ‘intelligence’ : ",sim_words )

        ## The 5 words with the most similar meanings
        most_5 = cosine_Similarity_Utility.cosine_distance(word2vec.wv, 'intelligence',  word_list)
        # print("top 5 words: ", most_5, type(most_5))
    
        return sim_words, most_5


    @staticmethod
    def triple_Similarity(word2vec,word_list):
        score1 = []
        score2 = []
        score3 = []
        final_Score_list = []
    ## 定义输入triple。 
        inputTriple = {"entity1": "human", "entity2": "ai", "relation": "develop"}
        subj = inputTriple['entity1']
        obj = inputTriple['entity2']
        rel = inputTriple["relation"]
        # print(subj, rel, obj)

        Top_subj = cosine_Similarity_Utility.cosine_distance(word2vec.wv, subj,  word_list)
        Top_obj = cosine_Similarity_Utility.cosine_distance(word2vec.wv, obj,  word_list)
        Top_rel = cosine_Similarity_Utility.cosine_distance(word2vec.wv, rel,  word_list)


        # for x in range(len(Top_subj)):
        #     subject_score = Top_subj[x][1]
        #     object_score = Top_obj[x][1]
        #     relation_score = Top_rel[x][1]

        #     subject_name = Top_subj[x][0]
        #     object_name = Top_obj[x][0]
        #     relation_name = Top_rel[x][0]

        #     # print("subject_score: \n", subject_score, subject_name)
        #     # print("object_score: \n", object_score, object_name)
        #     # print("relation_score: \n", relation_score, relation_name)
        #     score1.append(subject_score)
        #     score2.append(object_score)
        #     score3.append(relation_score)            
       

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


        ## 这下面还没改好
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
    
        # print("Triple: ", triple, type(triple))
        # print("Max value: ", maxValue)

        # return triple

        for i in range(len(Top_subj)):
            #计算总分
            final_Score = Top_subj[i][1] * 0.3 + Top_obj[i][1] * 0.3 + Top_rel[i][1] * 0.4
            final_Score_list.append(final_Score)

        #获的最高总分triple的index
        a = np.array(final_Score_list)
        idx = np.argmax(a)
        max_triple = Top_subj[idx][0] + " | "  + Top_rel[idx][0] + " | " + Top_obj[idx][0]  
        print("Triple ",max_triple,"gaint the highest final score: ",final_Score_list[idx])
        return max_triple
        
        
            



def main():

    article_text = cosine_Similarity_Utility.getData()
    all_words = cosine_Similarity_Utility.textPreprocessing(article_text)
    # print("all words: \n", all_words)

    ## Train
    word2vec = cosine_Similarity_Utility.train_Model(all_words)


    vector_all, word_list, vocabulary = cosine_Similarity_Utility.get_wordVec(word2vec)
    sim_words, Num = cosine_Similarity_Utility.similarity_Cal(word2vec, word_list)

    triple = cosine_Similarity_Utility.triple_Similarity(word2vec, word_list)
 
if __name__ == "__main__":
    main()

