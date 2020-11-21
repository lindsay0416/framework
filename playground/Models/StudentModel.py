# from a file import a class name
from playground.Models.PersonModel import PersonModel as Person


class StudentModel(Person):
    def __init__(self, id, name, age):
        super().__init__(name)
        self.id = id
        self.age = age

    # override
    def say_hello(self):
        print("Student is saying hello" + str(self.id) + self.name + str(self.age))


if __name__ == '__main__':
    s1 = StudentModel(1, "Leo", 12)
    s2 = StudentModel(2, "Lee", 13)
    s1.say_hello()
    s2.say_hello()
