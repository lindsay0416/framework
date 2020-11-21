# str = input("Please enter something")
# print(str)

# https://www.tutorialspoint.com/python/python_files_io.htm

fo = open("foo.txt", "wb")
print("Name of the file: ", fo.name)
print("Closed or not : ", fo.closed)
print("Opening mode : ", fo.mode)

fo.write("Python is a great language.\nYeah its great!!\n".encode())
fo.close()

with open('foo.txt', 'r') as f:
    # Read chunk of data
    chunk = 4
    while True:
        # line = f.read(chunk)
        line = f.readline()
        if not line:
            line = "i've read Nothing"
            print("EOF reached. What i read when i reach EOF:", line)
            break
        else:
            print('Read: {} at position: {}'.format(line.replace('\n', ''), f.tell()))

