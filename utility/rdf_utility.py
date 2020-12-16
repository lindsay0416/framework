import rdflib
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace
import time
import configparser


# All the triples are stored in rdflib plugin database: BSDDB3
class rdfUtility:

    @staticmethod
    def add(triple):
        config = configparser.ConfigParser()
        config.read("Config/config.ini")
        namespace = config.get("config","rdfNamespace")
        graph = rdflib.Graph('Sleepycat', identifier=namespace)
        graph.open('db', create=True)
        s = rdflib.URIRef(triple[0])
        p = rdflib.URIRef(triple[1])
        o = rdflib.URIRef(triple[2])
        #两个节点属性： 创建Unix timestamp，节点提到次数
        m = rdflib.URIRef("Mentions")
        c = rdflib.URIRef("Created")
        #判断三元组中是subject和object是否存在KG中
        #subject
        #如果存在：update提到次数
        if (s, None, None) in graph or (None, None, s) in graph:
                attr = (s,m,Literal(graph.value(s,m)+1))
                graph.set(attr)
        #如果不存在：新建节点并添加上述两个节点属性
        else: 
            graph.add((s,m,Literal(1)))
            t = time.time()
            graph.add((s,c,Literal(int(t))))

        #object：
        if (o, None, None) in graph or (None, None, o) in graph:
                attr = (o,m,Literal(graph.value(s,m)+1))
                graph.set(attr)
        else: 
            graph.add((o,m,Literal(1)))
            t = time.time()
            graph.add((o,c,Literal(int(t))))

        #添加三元组(s,p,o)到KG中    
        graph.add((s,p,o))
        graph.close()


    @staticmethod
    def remove(triple):
        config = configparser.ConfigParser()
        config.read("Config/config.ini")
        namespace = config.get("config","rdfNamespace")
        graph = rdflib.Graph('Sleepycat', identifier=namespace)
        graph.open('db', create=True)
        s = rdflib.URIRef(triple[0])
        p = rdflib.URIRef(triple[1])
        o = rdflib.URIRef(triple[2])
        graph.remove((s,p,o))
        graph.close()


    @staticmethod
    def getAlltriples():
        config = configparser.ConfigParser()
        config.read("Config/config.ini")
        namespace = config.get("config","rdfNamespace")
        ss=[]
        ps=[]
        os=[]
        graph = rdflib.Graph('Sleepycat', identifier=namespace)
        graph.open('db', create=True)
        #遍历整个graph除去predicate为Mentions和Created的triple
        for subject, predicate, object in graph:
            if str(predicate) != "Mentions" and str(predicate) != "Created":
                ss.append(str(subject))
                ps.append(str(predicate))
                os.append(str(object))
        return (ss,ps,os)


    def getProperty(s,p):
        config = configparser.ConfigParser()
        config.read("Config/config.ini")
        namespace = config.get("config","rdfNamespace")
        graph = rdflib.Graph('Sleepycat', identifier=namespace)
        graph.open('db', create=True)
        s = rdflib.URIRef(s)
        p = rdflib.URIRef(p)
        return graph.value(s,p)


def main():
    # # nb is a namespace(unique Identifier)
    # print("Triple under a specific namespace: ", rdfUtility.getAlltriples("nb"))  
    # print("TimeStamp: ", rdfUtility.getProperty("nb","aa","Created")) # Timestamp
    
    ## Domain  == AI
    # rdfUtility.add(("ai","stop","fear")) # Add triples with add method.
    # rdfUtility.add(("battlefield","decide","benefit")) # Add triples with add method.
    # rdfUtility.add(("siri","choose","photographs"))

    ## Domain  == Food
    

    g_t = rdflib.Graph('Sleepycat', identifier='default') # # Initialize a graph，指定数据库
    g_t.open('db') # 打开数据库并进行操作

    rdfUtility.add(("hello world","is","conding languange"))

    # Print the entire Graph in the RDF ttl format
    print(g_t.serialize(format="turtle").decode("utf-8"))
    
    g_t.close()
    #print(rdfUtility.getAlltriples())

if __name__ == "__main__":
    main()



 

