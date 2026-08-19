'''
f=open("file.txt")
with_read=f.read()
f.seek(0)
with_readline=f.readlines()
f.seek(0)
with_readlines=f.readline()
print(with_readlines)
print(with_readline)

f.seek(0)
with open('file.txt','w') as file:
    file.write("\n This is just added at the end!")


no_of_lines=0
no_of_words=0
with open('file.txt','r') as file:
    lines=file.readlines()
    for line in lines:
        no_of_words+=len(line)
    no_of_lines=len(lines)
print(no_of_lines)
print(no_of_words)

tracker=dict()

with open('file.txt','r') as file:
    text=file.read()

after_spliting=text.split(" ")
for word in after_spliting:
    if(word in tracker):
        tracker[word]+=1
    else:
        tracker[word]=1
after_sorting=list(sorted(tracker.items(),key=lambda x:x[1],reverse=True))
print(after_sorting[:10])


class myownerror(Exception):
    pass 


a=10
try:
    if(a==10):
        raise myownerror("Value can not be equal to 10!!")
except:
    print("Error!!")
    

def decorator(func):
    def wrapper():
        res=func()
        return res.upper()
    return wrapper
def decorator_1(func):
    def wrapper():
        res=func()
        return res.split(" ")
    return wrapper
@decorator_1
@decorator
def normal_func():
    return "this is a normal function!"
res=normal_func()
print(res)


class PersonAccount:
    def __init__(self,firstname,lastname,incomes,expenses):
        self.firstname=firstname
        self.lastname=lastname
        self.incomes=incomes
        self.expenses=expenses
    def total_income(self):
        return sum(self.incomes)
    def total_expense(self):
        return sum(self.expenses)
    def acc_info(self):
        return f"account holder name {self.firstname} and income is {sum(self.incomes)} and {sum(self.expenses)} are the expenses!" 
    def add_income(self,income):
        self.incomes.append(income)
        return "DOne!"
    def add_expenses(self,expense):
        self.expenses.append(expense)
        return "Done!"
    
person_1=PersonAccount("shahir","shaik",[1,2,3,4],[5,3,2,2])
print(f"total income is {person_1.total_income()}")
print(f"total expenses is {person_1.total_expense()}")
'''
#level-1
class Book:
    total_books=0
    def __init__(self,title,author,isbn,price,avilable):
        self.title=title
        self.author=author
        self.isbn=isbn
        self.price=price
        self.avilable=avilable
        Book.total_books+=1
    @classmethod
    def dis_current_total(cls):
        return cls.total_books
    def dis_info(self):
        return f"Book info {self.title},author name :{self.author}, isbn {self.isbn} ,price {self.price} and avilable {self.avilable}"
    def brrow(self):
        self.avilable="Not Avilable!"
    def return_book(self):
        self.avilable="Avilable!"

class Member:
    def __init__(self,name,member_id,email,fine):
        self.name=name
        self.member_id=member_id
        self.email=email
        self.__fine=fine
    @property
    def display(self):
        return self.__fine
    @display.setter
    def display(self,value):
        if(value>0):
            self.__fine+=value

class Person:
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def display(self):
        return f"My name is {self.name} and age is {self.age}"
class Member(Person):
    def __init__(self,mem_id,name,age):
        self.mem_id=mem_id
        super().__init__(name,age)
class Librarian(Person):
    def __init__(self,employee_id,salary,name,age):
        self.employee_id=employee_id
        self.salary=salary
        super().__init__(name,age)



from abc import ABC,abstractmethod
class LibraryItem(ABC):
    @abstractmethod
    def make_sound():
        pass
class Child(LibraryItem):
    def hello():
        pass
    def make_sound():
        pass
child=Child()
