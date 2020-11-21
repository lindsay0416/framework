class Employee:
    # 'Common base class for all employees'
    empCount = 0  # This is the static variable

    def __init__(self, name, salary):
        self.name = name  # instance variable
        self.salary = salary
        self.id = Employee.empCount
        Employee.empCount += 1

    def displayCount(self):
        print("Total Employee %d" % Employee.empCount)

    def displayEmployee(self):
        print("ID: " + str(self.id) + "Name : ", self.name, ", Salary: ", self.salary)
        return "ID: " + str(self.id) + " Name : " + self.name + ", Salary: " + str(self.salary)

    def displayAll(self):
        self.displayEmployee()
        self.displayCount()

    def __str__(self):
        return self.displayEmployee()


def main():
    emp1 = Employee("Leo", 3000)
    emp2 = Employee("Adam", 4000)
    emp1.age = 32
    emp2.age = 33
    print(hasattr(emp1, 'age'))
    print(getattr(emp2, 'age'))
    setattr(emp1, 'age', 8)
    print(getattr(emp1, 'age'))
    print(emp1)
    emp2.displayAll()


if __name__ == "__main__":
    main()
