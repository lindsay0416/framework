# This file is loading the Pre-trained GloVe word Vectors model. 
# Wikipedia 2014 + Gigaword 5 vectors (6B tokens, 400K vocab, uncased, 300d vectors, 822 MB download)
# Download link: https://github.com/stanfordnlp/GloVe
import configparser
import os
import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


class Pretrained_GloVe_Utility:


    ## Downloading and loading the pre-trained vectors
    @staticmethod
    def load_Vector():
    #读取配置文件
        pro_dir = os.path.split(os.path.realpath(__file__))[0]
        config_path = os.path.join(pro_dir, "config.ini")
        config = configparser.ConfigParser()
        config.read(config_path)
        vector_Path = config.get("GloVe_WordVec", "word_vector")

        # create a dictionary that will hold the mappings between words
        embeddings_dict = {}
        # Open the txt file contains 50d vectors
        with open(vector_Path, 'r', encoding="utf-8") as f:
            for line in f:
                # python 中 split函数，splits a string into a list。(): 根据空格分，(,): 根据逗号分。
                values = line.split() 
                # 假设words中间没有空格，所以第一个元素是word，第二个元素是 vector， 用index在values中找。
                word = values[0]  
                vector = np.asarray(values[1:], "float32")
                # 不断跟新 embeddings_dict
                embeddings_dict[word] = vector
        
        
        return embeddings_dict

    # Finding similar vectors to a given vector
    @staticmethod
    def find_closest_embeddings(embedding):
        embeddings_dict = Pretrained_GloVe_Utility.load_Vector()
        return sorted(embeddings_dict.keys(), key=lambda word: spatial.distance.euclidean(embeddings_dict[word], embedding))


    # add and subtract two words together
    # 将来可以把OpenIE跑完以后，有多个单词的 S, P, O中的所有单词的向量相加，组合成一个vector。
    @staticmethod
    def math_Words(embeddings_dict):
        # 向量相加
        math = embeddings_dict["twig"] - embeddings_dict["branch"] + embeddings_dict["hand"] 
        closest_embeddings = Pretrained_GloVe_Utility.find_closest_embeddings(math)  
        return math, closest_embeddings


    # t-SNE visualizataion， 数据可视化，越相似的单词在图中的点越相近。
    @staticmethod
    def visualize(embeddings_dict):
        # n_components=2 把多维向量降维成2维
        tsne = TSNE(n_components=2, random_state=0)
        # conert all keys of embeddings_dict into list
        words =  list(embeddings_dict.keys())
        vectors = [embeddings_dict[word] for word in words]
        # 定义Y轴的值, 只显示前 1000个
        Y = tsne.fit_transform(vectors[:1000])
        plt.scatter(Y[:, 0], Y[:, 1])
        for label, x, y in zip(words, Y[:, 0], Y[:, 1]):
            plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords="offset points")
        plt.show()

        return plt.show()



def main():
    embeddings_dict = Pretrained_GloVe_Utility.load_Vector()
    print("Vector of human: ", embeddings_dict["human"])
    math, closest_embeddings = Pretrained_GloVe_Utility.math_Words(embeddings_dict)
    print("向量相加的结果: ", math, math.shape)
    print("Closest embeddings afther word maths: ", closest_embeddings[:5])

    # 测试 find_closest_embeddings 好不好用。 
    text = "king"
    closest_words =  Pretrained_GloVe_Utility.find_closest_embeddings(embeddings_dict[text])[1:6]
    print("closest_words", closest_words)
    # Pretrained_GloVe_Utility.visualize(embeddings_dict)
    


if __name__ == "__main__":
    main()


