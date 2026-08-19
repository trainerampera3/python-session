def fun(a, b):
    print(a)
    print(b)

def fun(a, b, c):
    print(a)
    print(b)
    print(c)

def fun(l):
    for c in l:
        print(c)



# fun(10,20)

fun([10,20])

def fun(data):
    print(data)

# fun(10,20)
fun([10,20])
fun('sandeep')

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


el = [Employee(101, 'Sandup',4000), SalesEmployee(102,'Rahul',5000, 50)]

for x in el:
    x.printDetails()


class Admin:
    def fun(self):
        print('fun() in EMployee')

class Customer:
    def fun(self):
        print('fun() in Cusotmer')

l = [Admin(), Customer()]

for x in l:
    x.fun()