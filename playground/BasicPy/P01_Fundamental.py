# AUTO format ALT+CTRL+L

print('hello world')
print("hello, world")
# name = input();
# print(name, 'abcd')

# If then else statement
a = 80
if a > 90:
    print(a)
else:
    print(a + 100)

print('\u4e2d\u6587', 'xxxx')
print('Hello, %s' % 'world')
print('Hi, %s, you have $%d.' % ('Michael', 1000000))
print('中文'.encode('gb2312'))

# List
classmates = ['Michael', 'Bob', 'Tracy']
print(classmates)
print(len(classmates))
print(classmates[0])
print(classmates[-1])  # the last item, - means倒数

classmates.append('Leo')
classmates.append('Adam')
print(classmates)

classmates.insert(1, 123)  # add an item to a particular position
print(classmates[0] + '2')

last = classmates.pop()  # remove the last element
print(last)
print(classmates)

# Tuple 元组
# tuple一旦初始化就不能修改
students = ('michael', 'bob', 'tracy')
print(students)
# tuple 里面的指向不变,tuple里面list的元素可以变
t = ('a', 'b', ['A', 'B'])
t[2][0] = 'X'
t[2][1] = 'Y'
print(t)

# If then else
age = 3
if age >= 18:
    print('adult')
elif age >= 6:
    print('teenager')
else:
    print('kid')

# loop approach 1
names = ['Michael', 'Bob', 'Tracy']
for name in names:
    print(name)

# loop approach 2
for i in range(len(names)):
    print(names[i])

# loop approach 3
while i < len(names):
    print(names[i])
    i += 1


sumNumber = 0
for x in range(10, 101):
    sumNumber = sumNumber + x
print(sumNumber)

# noticed that the Indentation is very important
# This error: IndentationError: unexpected indent
n = 99
sumNumber = 0
while n > 0:
    sumNumber = sumNumber + n
    if sumNumber % 100 == 0:
        print('==Fully divided by 100===', sumNumber)
        print('This statement is still included in the If statement')
    print('===what?====')  # this is not part of If statement
    n = n - 2
print(sumNumber)

# Dict (called map in other language) and set
'''
Dict和list比较，dict有以下几个特点：

查找和插入的速度极快，不会随着key的增加而变慢；
需要占用大量的内存，内存浪费多。
而list相反：

查找和插入的时间随着元素的增加而增加；
占用空间小，浪费内存很少。
所以，dict是用空间来换取时间的一种方法。
'''
nameDict = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
thisName = 'Michael'
print(thisName, nameDict[thisName])
nameDict['Leo'] = 99  # add an element
print(nameDict)

if 'Leo' in nameDict:  # check the existence of an element before using it
    print("Yes, he is here!", nameDict['Leo'])

print('bob', nameDict.get('bob'))  # return none if not exist, case sensitive

removeBob = nameDict.pop('Bob')
print('Remove bob', removeBob)
print(nameDict)

# Set
s1 = set([1, 2, 3])
s1.add(4)
s1.remove(4)
print(s1)
for ss in s1:
    print(ss)
s2 = set([1, 2, 5, 6, 7])

print(s1 & s2)
print(s1 | s2)

# 再议不可变对象
# List 可变，String 不可变

a = ['c', 'b', 'a']
a.sort()  # a is changed
print(a)

a = 'abc'
b = a.replace('a', 'A')  # a is not changed, String 不可变
print(a, b)
