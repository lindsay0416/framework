import rdflib
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace
import time


class rdf_test:

    @staticmethod
    def add(namespace, triple):
        graph = rdflib.Graph('Sleepycat', identifier = namespace)
        graph.open('db', create=True)
        s = rdflib.URIRef(triple[0])
        p = rdflib.URIRef(triple[1])
        o = rdflib.URIRef(triple[2])
        #两个节点属性： 创建Unix timestamp，节点提到次数(Frequency)
        m = rdflib.URIRef("Mentions")
        c = rdflib.URIRef("Created")
        #判断三元组中subject和object是否存在KG中
        #subject
        #如果存在：update提到次数
        if (s, None, None) in graph or (None, None, s) in graph:
                attr = (s,m,Literal(graph.value(s,m)+1))
                graph.set(attr) # set(plugin function: Replace Literal value)
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
    def remove(namespace, triple):
        graph = rdflib.Graph('Sleepycat', identifier=namespace)
        graph.open('db', create=True)
        s = rdflib.URIRef(triple[0])
        p = rdflib.URIRef(triple[1])
        o = rdflib.URIRef(triple[2])
        graph.remove((s,p,o))
        graph.close()



def main():
    rdf_test.add("nb",("aa","bb","dd"))
    g_t = rdflib.Graph('Sleepycat', identifier='nb') # 新建图，指定数据库
    g_t.open('db') # 打开数据库并进行操作
    print(g_t.serialize(format="turtle").decode("utf-8"))
    g_t.close()

if __name__ == "__main__":
    main()



 

