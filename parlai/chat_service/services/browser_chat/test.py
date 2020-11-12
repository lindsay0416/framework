import sys
sys.path.append("./utility")
from openie_utility import OpenieUtility
from utility import Utility


def main():
    # neo4j = neoUtility()
    # neo4j.find_entity("aa", "David")
    # neo4j.close()
    Utility.write_input_to_file({"text": "hello world"})


if __name__ == "__main__":
    main()