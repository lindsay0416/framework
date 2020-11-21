import re
regex = re.compile('[^a-zA-Z\'#]')
#First parameter is the replacement, second parameter is your input string
print(regex.sub('', "#ab3d*EI've a good idea12!'@"))
#Out: 'abdE'

sentence = 'Python is fun.'

result = sentence.index('is fun')
print(sentence[:7-1])
print("Substring 'is fun':", result)


sample = "sHEd ! @@like got"

if "'" in sample:
    sample = sample[:sample.index("'")]
sample = regex.sub('', sample)
print('==========')
print(sample)
