class PersonModel:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print("Hello" + self.name)

    def __del__(self):
        print("Object Person has been terminated")


if __name__ == '__main__':
    p = PersonModel("Leo")
    p.say_hello()