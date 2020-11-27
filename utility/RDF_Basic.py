from rdflib import Graph
# from rdflib.namespace import FOAF, XSD
import configparser
import os


# In[1]:
# Initialize a graph 
g = Graph()

# Parse in an RDF file graph dbpedia
g.parse('http://dbpedia.org/resource/Michael_Jackson')


# loop through each triple in the graph (subj, pred, obj)
for index, (subj, pred, obj) in enumerate(g):
    print("Subject: ", subj, "\n", "Relation: ", pred)
    if index == 10:
        break


# Print the size of the Graph
print(f'graph has {len(g)} facts')


# Print the entire Graph in the RDF xml (ttl etc.) format
print(g.serialize(format = 'xml').decode('u8'))



# In[2]:

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
 
