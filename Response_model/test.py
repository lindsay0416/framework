from Load_T5_model import TextGenerationUtility
from cosine_similarity import cosine_Similarity_Utility



def main():
    ## Test load_model Text generation.
    # tokenizer, model_saved = TextGenerationUtility.load_Model()
    # print(TextGenerationUtility.generate('Amy | pet |  cat ', model_saved, tokenizer)) # pass


    ## Test cosine Similarity

    article_text = cosine_Similarity_Utility.getData()
    all_words = cosine_Similarity_Utility.textPreprocessing(article_text)
    word2vec = cosine_Similarity_Utility.train_Model(all_words)
    vector_all, word_list, vocabulary = cosine_Similarity_Utility.get_wordVec(word2vec) 
    sim_words = cosine_Similarity_Utility.similarity_Cal(word2vec, word_list)


    cdistance = cosine_Similarity_Utility.cosine_distance(word2vec.wv, 'intelligence', word_list, 5)

    ## The vector of the specific word
    vector_1 = word2vec.wv['artificial']  
    print("The vector of 'artificial': \n ", vector_1)   # pass 

    ## Most similar words 
    sim_words = word2vec.wv.most_similar('intelligence') # pass 
    print("sim_words of ‘intelligence’ : ",sim_words )   # pass 

    ## The 5 words with the most similar meanings
    # most_5 = cosine_Similarity_Utility.similarity_Cal(word2vec, word_list)


    print("word list", cdistance)



if __name__ == "__main__":
    main()