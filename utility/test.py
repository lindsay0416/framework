# from openie_utility import OpenieUtility
# from utility import Utility
from preprocess_utility import PreprocessUtility

def main():
    # neo4j = neoUtility()
    # neo4j.find_entity("aa", "David")
    # neo4j.close()
    # triples = OpenieUtility.sentence_to_triple('Lindsay has a cat.')
    # print(triples)
    # Utility.write_to_file({"text": "hello world"})
    # print(PreprocessUtility.lemmatize_document(PreprocessUtility.preprocess("i ate a cake."))[0][0])
    print(PreprocessUtility.preprocess("i had a cake."))
    



if __name__ == "__main__":
    main()