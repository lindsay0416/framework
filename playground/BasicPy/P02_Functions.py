def my_abs(x):
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x

print(my_abs(-12))


age = 19
if age >= 18:
    pass  # pass语句什么都不做

# print(my_abs('a'))
