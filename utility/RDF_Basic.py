from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, DCTERMS, XSD, RDF, SDO 
import configparser
import os


# # In[1]:
# # Initialize a graph 
# g = Graph()

# # Parse in an RDF file graph dbpedia
# g.parse('http://dbpedia.org/resource/Michael_Jackson')


# # loop through each triple in the graph (subj, pred, obj)
# for index, (subj, pred, obj) in enumerate(g):
#     print("Subject: ", subj, "\n", "Relation: ", pred)
#     if index == 10:
#         break


# # Print the size of the Graph
# print(f'graph has {len(g)} facts')


# # Print the entire Graph in the RDF xml (ttl etc.) format
# print(g.serialize(format = 'xml').decode('u8'))



# # In[2]:

# # Create a graph

# graph = Graph()

# # Create an RDF URI node to use as the subject for mutiple triples
# mason = URIRef("http://example.org/mason")

# # Add triples with add method.
# graph.add((mason, RDF.type, FOAF.Person))
# graph.add((mason, FOAF.nick, Literal("mason", lang = 'en')))
# graph.add((mason, FOAF.name, Literal("Mason Carter")))
# graph.add((mason, FOAF.mbox, URIRef("mailto:mason@example.org")))


# # Add another person

# shyla = URIRef("http://example.org/shyla")

# # Add triples with add method.
# graph.add((shyla, RDF.type, FOAF.Person))
# graph.add((shyla, FOAF.nick, Literal("shyla", datatype = XSD.string)))
# graph.add((shyla, FOAF.name, Literal("Shyla Sharples")))
# graph.add((shyla, FOAF.mbox, URIRef("mailto:shyla@example.org")))

# # Iterate over triples in store and print them out.

# for s, p, o in graph:
#     print(s, p, o)


# # For each foaf: Person in the graph, print out their nickname's value.
# print("*" * 50, "Nick: " ,"*" * 50)
# for person in graph.subjects(RDF.type, FOAF.Person):
#     for nick in graph.objects(person, FOAF.nick):
#         print(nick)


# # Bind the FOAF namespace to a prefix for more readable output

# graph.bind("foaf:", FOAF)


# # Print all the data in the n3 format
# print("*" * 50, "Print all the data in the n3 format: ", "*" * 50)
# print(graph.serialize(format = "n3").decode("utf-8"))

 

# In[2]:

# Define URI
mona_lisa = URIRef("http://www.wikidata.org/entity/Q12418")
davinci = URIRef("http://dbpedia.org/resource/leonardo_da_Vinci")
lajoconde = URIRef("http://data.europeana.eu/item/04802")

# Or give them a namespace
EX = Namespace("http://example.org")
bob = EX['Bob']
alice = EX['Alice']

birth_date = Literal('1990-07-04', datatype = XSD['date'])
title = Literal('mona_lisa', lang = 'en')

g = Graph()

# Bind prefix to namespace
g.bind('ex', EX)
g.bind('foaf', FOAF)
g.bind('schema', SDO)
g.bind('dcterms', DCTERMS)

g.add((bob, RDF.type, FOAF.Person))
g.add((bob, FOAF.knows, alice))
g.add((bob, FOAF['topic_interest'], mona_lisa))
g.add((bob, SDO['birthDate'], birth_date))
g.add((mona_lisa, DCTERMS['creator'], davinci))
g.add((mona_lisa, DCTERMS['title'], title))
g.add((lajoconde, DCTERMS['subject'], mona_lisa))

print("*" * 50, "Bind prefix to namespace: ", "*" * 50)
print(g.serialize(format = 'ttl').decode('u8'))

print("*" * 50, "prefix, ns: ", "*" * 50)
for prefix, ns in g.namespaces():
    print(prefix, ns)

# Replace Literal value
g.set((bob, SDO['birth_date'], Literal('1990-01-01', datatype = XSD.date)))
g.set((mona_lisa, DCTERMS['title'], Literal('La Joconde', lang = 'fr')))
print("*" * 50, "Replace Literal value: ", "*" * 50)
print(g.serialize(format = 'ttl').decode('u8'))

# Remove triples from graph
g.remove((lajoconde, None, None))
print("*" * 50, "Remove triples from graph: ", "*" * 50)
print(g.serialize(format = 'ttl').decode('utf-8'))