class Student:
    def __init__(self, marks):
        self.__marks = marks

    def set_marks(self, marks):
        if 0 <= marks <= 100:
            self.__marks = marks
        else:
            raise ValueError('Marks must be between 0 and 100')

    def get_marks(self):
        return self.__marks


stu1 = Student(90)
print(stu1.get_marks())


class Person:
    def __init__(self, id , name):
        self.id = id
        self.name = name

    def printDetails(self):
        print(self.id)
        print(self.name)

class Employee(Person):
    def __init__(self, id , name, salary):
        super().__init__(id, name)
        self.salary = salary
    

    def printDetails(self):
        super().printDetails()
        print(self.salary)

class SalesEmployee(Employee):
    def __init__(self, id, name, sal, si):
        super().__init__(id, name, sal)
        self.salesInc = si
    def printDetails(self):
        super().printDetails()
        print(self.salesInc)

se = SalesEmployee(101, 'Rahul',40000, 2000)
e = Employee(102, 'Sandub',500000)

se.printDetails()
e.printDetails()


class Student:
    def __init__(self, sid, dept):
        self.sid = sid
        self.dept = dept

class Faculty:
    def __init__(self, eid, dept):
        self.eid = eid
        self.dept = dept

class PhDStudent(Student, Faculty):
    def __init__(self, id, dept):
        super().__init__(id, dept)


ps = PhDStudent(101, 'CSE')

print(ps.eid)
print(ps.dept)
