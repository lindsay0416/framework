from nltk.tokenize import sent_tokenize
from nltk.tag import StanfordNERTagger
from nltk.internals import find_jars_within_path
from nltk import word_tokenize

# http://www.nltk.org/api/nltk.tag.html#module-nltk.tag.stanford

# Alternatively to setting the CLASSPATH add the jar and model via their path:
jar = 'D:/stanford-ner-2018-02-27/stanford-ner.jar'
model = 'D:/stanford-ner-2018-02-27/classifiers/english.muc.7class.distsim.crf.ser.gz'

st = StanfordNERTagger(model, jar)
print(st.tag('Rami Eid is studying at Stony Brook University in NY'.split()))
print(st.tag('RT @_CocoaDream: I relate to this on a level that most ppl are fortunate enough not to understand https://t.co/RNpVYaP6OH'.split()))
print(st.tag('I like, watching a movie'.split()))

# pos_tagger = StanfordPOSTagger(model, jar)
#
# # Add other jars from Stanford directory
# stanford_dir = pos_tagger._stanford_jar.rpartition('/')[0]
# stanford_jars = find_jars_within_path(stanford_dir)
# pos_tagger._stanford_jar = ':'.join(stanford_jars)
#
# text = pos_tagger.tag(word_tokenize("What's the airspeed of an unladen swallow ?"))
# print(text)



# st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
# st.tag('Rami Eid is studying at Stony Brook University in NY'.split())




# Sentence tokenization
# mytext = "Hello Adam, how are you? I hope everything is going well. Today is a good day, see you dude."
# print(sent_tokenize(mytext))





