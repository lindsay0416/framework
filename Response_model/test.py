from rdflib import Namespace
from Load_T5_model import TextGenerationUtility
from cosine_similarity import cosine_Similarity_Utility
import sys
sys.path.append(r'./utility')
'''python import模块时， 是在sys.path里按顺序查找的。
sys.path是一个列表，里面以字符串的形式存储了许多路径。
使用A.py文件中的函数需要先将他的文件路径放到sys.path中'''
from rdf_test import rdf_test_Utility



def main():

    ''' Get word lists (Subjects, repations, objects) from rdf db '''
    ss,ps,os = rdf_test_Utility.getAlltriples("nb")

    print("subject list: ", ss, "\n",  "relation list: ", ps, "\n", "object list: ", os)


    ''' Test cosine Similarity'''

    article_text = cosine_Similarity_Utility.getData()
    all_words = cosine_Similarity_Utility.textPreprocessing(article_text)
    word2vec = cosine_Similarity_Utility.train_Model(all_words)
    vector_all, word_list, vocabulary = cosine_Similarity_Utility.get_wordVec(word2vec) 
    sim_words = cosine_Similarity_Utility.similarity_Cal(word2vec, word_list)

    cdistance = cosine_Similarity_Utility.cosine_distance_rank(word2vec.wv, 'intelligence', word_list, 5)
    max_triple = cosine_Similarity_Utility.triple_Similarity(word2vec, word_list)

    ''' The vector of the specific word'''
    vector_1 = word2vec.wv['artificial']  
    # print("The vector of 'artificial': \n ", vector_1)   # pass 

    ''' Most similar words '''
    inputWord = 'intelligence'
    sim_words = word2vec.wv.most_similar(inputWord) # pass 
    # print("sim_words of " + inputWord + " :" ,sim_words )   # pass 
    print("Top 5 most similar: ", cdistance) # pass

    ''' Test load_model Text generation. '''
    tokenizer, model_saved = TextGenerationUtility.load_Model()  
    # print(TextGenerationUtility.generate('Amy | pet | cat ', model_saved, tokenizer)) # pass

    ''' Use the ouput triple from cosine distance.'''
    
    print(TextGenerationUtility.generate(max_triple, model_saved, tokenizer))




if __name__ == "__main__":
    main()