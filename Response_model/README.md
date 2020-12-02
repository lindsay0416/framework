1.  Pretrained Google T5 text generation model can be downloaded from google drive by accessing the following link: 
    https://drive.google.com/file/d/13LBZTx6be4WrED88YtBBnoC6lO01t0NW/view?usp=sharing

2.  cosine_similarity.py 
    - Retrieve all the articles related to the domain of our cconversational agent. 
    - Word2Vec: word embedding
    - Cosin Similarity: Calculate the cosine distance between each word. (The output wi)
    - triple_Similarity: Calculate the similarity between the input triple and the existing triple (Triples in db), and output the top 3 triples with the highest similarity. (Assign weights to subject(30%), relation (40%) and object (30%).)
    - Choose the triple that has the largest time value and the highest frequency attributes.  [Weight to be considered.]
