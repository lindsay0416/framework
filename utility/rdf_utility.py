from rdflib import Graph
import configparser
import os

class rdfUtility:

    @staticmethod
    def loadGraph():
        #读取配置文件
        pro_dir = os.path.split(os.path.realpath(__file__))[0]
        config_path = os.path.join(pro_dir, "config.ini")
        #if not os.path.exists(config_path):print("无配置文件")
        config = configparser.ConfigParser()
        config.read(config_path)
        path = config.get("config","RDFstorePath")
        graph = Graph(store='Sleepycat')
        graph.open(path, create = True)
        return graph
        

    # Create
    @staticmethod
    def insert2Graph():
        graph = rdfUtility.loadGraph()
        bob = URIRef("http://example.org/people/Bob")
        linda = BNode()  # a GUID is generated

        name = Literal('Bob')  # passing a string
        age = Literal(24)  # passing a python int
        height = Literal(76.5)  # passing a python float
        graph.bind("foaf", FOAF)

        graph.add(bob, RDF.type, FOAF.Person)
        graph.add(bob, FOAF.name, name)
        graph.add(bob, FOAF.knows, linda)
        graph.add(linda, RDF.type, FOAF.Person)
        graph.add(linda, FOAF.name, Literal("Linda")
         


def main():
    rdfUtility.loadGraph()


if __name__ == "__main__":
    main()