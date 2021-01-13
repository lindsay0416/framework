import rdflib
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace
import time
import json
import configparser


# All the triples are stored in rdflib plugin database: BSDDB3
class rdfUtility:
    users = ["Jason","Lindsay"]
    @staticmethod
    def add(triple):
        config = configparser.ConfigParser()
        config.read("Config/config.ini")
        namespace = config.get("config","rdfNamespace")
        graph = rdflib.Graph('Sleepycat', identifier=namespace)
        graph.open('db', create=True)
        # s = rdflib.URIRef(triple[0])
        # p = rdflib.URIRef(triple[1])
        # o = rdflib.URIRef(triple[2])
        s = Literal(triple[0])
        p = Literal(triple[1])
        o = Literal(triple[2])
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
        graph.close()
        return (ss,ps,os)

    @staticmethod
    def getAlltriplesByuser(namespace):
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
        graph.close()
        return (ss,ps,os)

    @staticmethod
    def getProperty(s,p):
        config = configparser.ConfigParser()
        config.read("Config/config.ini")
        namespace = config.get("config","rdfNamespace")
        graph = rdflib.Graph('Sleepycat', identifier=namespace)
        graph.open('db', create=True)
        s = Literal(s)
        p = rdflib.URIRef(p)
        value = graph.value(s,p)
        graph.close()
        return value

    @staticmethod
    def getP(namespace,s,p):
        graph = rdflib.Graph('Sleepycat', identifier=namespace)
        graph.open('db', create=True)
        s = Literal(s)
        p = rdflib.URIRef(p)
        value = graph.value(s,p)
        graph.close()
        return value

    @staticmethod
    def getAlldata():
        data = {}
        nodes = []
        ns = []
        es = []
        for i,user in enumerate(rdfUtility.users):
            graph = rdflib.Graph('Sleepycat', identifier=user)
            graph.open('db', create=True)
            for subject, predicate, object in graph:
                s = str(subject)
                if (s not in nodes):
                    nodes.append(s)  
                    n = {"label": s, "group": i}
                    ns.append(n)
            graph.close()


        for i,node in enumerate(nodes):
            cts = []
            for user in rdfUtility.users:
                graph = rdflib.Graph('Sleepycat', identifier=user)
                graph.open('db', create=True)

                if rdfUtility.getP(user,node,"Created")!=None:
                    cts.append(rdfUtility.getP(user,node,"Created"))
                graph.close()
            index = cts.index(min(cts))
            ns[index]["group"] = index
            

        count = 0
        for i,user in enumerate(rdfUtility.users):
            graph = rdflib.Graph('Sleepycat', identifier=user)
            graph.open('db', create=True)
            for subject, predicate, object in graph:
                s = str(subject)
                p = str(predicate)
                o = str(object)
                if str(predicate) != "Mentions" and str(predicate) != "Created":
                    e = {"id": count, "from": nodes.index(s), "to": nodes.index(o), "label": p, "group": i}
                    es.append(e)
                    count += 1     
            graph.close()
        data["nodes"] = ns
        for i,n in enumerate(ns):
            n["id"] = i
        data["edges"] = es 
        return data           

def main():
    rdfUtility.getAlldata()
    # ct = int(rdfUtility.getProperty("fish","Created"))
    # now = int(time.time())
    # print(now-ct)
    # graph = rdflib.Graph('Sleepycat', identifier="Lindsay")
    # graph.open('db', create=True)
    # print(graph.serialize(format="turtle").decode("utf-8"))
    # print(rdfUtility.getProperty("dog","Created"))
    # graph.close()


if __name__ == "__main__":
    main()



 

