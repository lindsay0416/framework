from openie_utility import OpenieUtility
from utility import Utility

def main():
    # neo4j = neoUtility()
    # neo4j.find_entity("aa", "David")
    # neo4j.close()
    # triples = OpenieUtility.sentence_to_triple('Lindsay has a cat.')
    # print(triples)
    Utility.write_to_file({"text": "hello world"})




if __name__ == "__main__":
    main()