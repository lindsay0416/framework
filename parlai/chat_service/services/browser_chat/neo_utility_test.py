from neo_utility import neoUtility

def main():
    neo4j = neoUtility()
    neo4j.find_entity("aa", "David")
    neo4j.close()


if __name__ == "__main__":
    main()