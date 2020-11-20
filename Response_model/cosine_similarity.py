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


def cosine_distance (model, word, target_list, num) :
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





def main():

    scrapped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Artificial_intelligence')
    article = scrapped_data .read()

    parsed_article = bs.BeautifulSoup(article,'lxml')

    paragraphs = parsed_article.find_all('p')

    article_text = ""

    for p in paragraphs:
        article_text += p.text

        # Cleaing the text
    processed_article = article_text.lower()
    processed_article = re.sub('[^a-zA-Z]', ' ', processed_article )
    processed_article = re.sub(r'\s+', ' ', processed_article)

    # Preparing the dataset
    all_sentences = nltk.sent_tokenize(processed_article)



    all_words = [nltk.word_tokenize(sent) for sent in all_sentences]
    # print(all_words)




    # Removing Stop Words
    for i in range(len(all_words)):
        all_words[i] = [w for w in all_words[i] if w not in stopwords.words('english')]

    word2vec = Word2Vec(all_words, min_count=1, size= 50, workers=3, window =3, sg = 1)

    vocabulary = word2vec.wv.vocab.keys()  # keys() 代表每一个 unique的单词， word2vec.wv.vocab 是一个dictionary。

    word_list = list(vocabulary)
    
    # print(list(vocabulary))
    # print("vocabulary: ", vocabulary)

    v1 = word2vec.wv['artificial']
    v_all = word2vec.wv[vocabulary]




    # print(" 所有的 vector", v_all)

    # print("The vector of 'artificial': ", v1)

    # print(word2vec.wv)





    sim_words = word2vec.wv.most_similar('intelligence')

    # print("sim_words of ‘intelligence’ : ",sim_words )

   

    
    Num = cosine_distance(word2vec.wv, 'intelligence',  word_list, 5)
    print("word list", Num)





if __name__ == "__main__":
    main()

