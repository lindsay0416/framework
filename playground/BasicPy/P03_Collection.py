nameDict = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
print(nameDict)
thisName = 'Michael'
print(thisName, nameDict[thisName])
nameDict['Leo'] = 99  # add an element
print(nameDict)

list1 = ["123", 4, 2, "abc"]
print(list1[1:3])
list1.append("def")
print(list1)
print(len(list1))


# Set
print('=============')
s1 = set([1, 2, 3])
s1.add(4)
print(s1)
s1.remove(4)
print(s1)
for ss in s1:
    print(ss)
s2 = set([1, 2, 5, 6, 7])

print(s1 & s2)
print(s1 | s2)

