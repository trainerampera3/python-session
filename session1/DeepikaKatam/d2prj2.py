# Rock Paper Scissors
 import random

 user = int(input("Choose 0 for Rock, 1 for Paper, 2 for Scissors: "))

 if user < 0 or user > 2:
     print("You entered an invalid number.")
 else:
     computer = random.randint(0, 2)

     choices = ["Rock", "Paper", "Scissors"]

     print(f"You chose: {choices[user]}")
     print(f"Computer chose: {choices[computer]}")

     if user == computer:
         print("Draw!")
     elif (user == 0 and computer == 2) or \
          (user == 1 and computer == 0) or \
          (user == 2 and computer == 1):
         print("You win!")
     else:
         print("Computer wins!")

 n=int(input("enter the number:"))
 a=0
 b=1
 for i in range(n+1):
     print(a)
     c=a+b
     a=b
     b=c



#amstrong number
 num=int(input("enter the number: "))
 temp=num
 digits=len(str(num))
 total=0
 while temp>0:
     digit=temp%10
     total=total+digit**digits
     temp=temp//10
 if total==num:
     print("amstrong number")
 else:
     print("not an amstrong number")

#amstrong number
 num=int(input("enter the number: "))
 temp=num
 reverse=0
 while num>0:
     digit=num%10
     reverse=reverse*10+digit
     num=num//10
 if temp==reverse:
     print("it is palindrom number")
 else:
     print("not a plindrome number")



#second largest number
numbers = [10, 25, 7, 45, 18]

largest = numbers[0]
second_largest = numbers[0]

for num in numbers:
    if num > largest:
        second_largest = largest
        largest = num
    elif num > second_largest and num != largest:
        second_largest = num

print("Largest:", largest)
print("Second largest:", second_largest)




#lists
#Remove Duplicate Elements
l1= [1, 2, 2, 3, 4, 4, 5]
unique = []
for i in l1:
    if i not in unique:
        unique.append(i)

print(unique)


#find second largest number
l2=[10,20,30,40,50]
l2.sort()
print("second largest is:",l2[-2])



#Count Even and Odd Numbers
l3=[1,2,3,4,5,6,7,8,9,]
even=0
odd=0

for i in l3:
    if i%2==0:
        even+=1
    else:
        odd+=1
print("even:",even)
print("odd:",odd)


#loops and conditional statements
check whether the number is positive or negative or zero
num=int(input("enter the number:"))
if num>0:
    print("it is positive number:")
elif num<0:
    print("it is negative number:")
else:
    print("zero")


#find the largest among three numbers
a=int(input("enter the first number:"))
b=int(input("enter the second number:"))
c=int(input("enter the third number:"))
if a>b and a>c:
    print("the largest",a)
elif b>c:
    print("the largest is",b)
else:
    print("the largest",c)



# #sum of numbers

#for loop
n=int(input("enter the number:"))
sum=0
for i in range(0,n+1):
    print(i)
    sum=sum+i
print("sum=",sum)

#while loop
n=int(input("enter the number:"))
i=1
sum=0
while i<=n:
    sum=sum+i
    i=i+1
print("sum=",sum)


# #multiplication tabel
n=int(input("enter the number:"))
for i in range(1,11):
    print(n,"*",i,"=",n*i)

#while loop
n=5
i=1
while i<=10:
    print(n,"*",i,"=",n*i)
    i=i+1

#check prime number
n=int(input("enter the number:"))
count=0
for i in range(1,n+1):
    if n%i==0:
        count=count+1 
if count==2:
    print("it is prime number")
else:
    print("it is not a prime number")

#while loop
n=int(input("enter the number:"))
count=0
i=1
while i<=n:
    if n%i==0:
        count=count+1
    i=i+1
if count==2:
    print("it is prime number")
else:
    print("it is not a prime number")

#fibonnaci series
n=int(input("enter the number:"))
a=0
b=1
count=0
while count<n:
    print(a)
    c=a+b
    a=b
    b=c
    count=count+1

#while loop
n=int(input("enter the number:"))
a=0
b=1
for i in range(n):
    print(a)
    c=a+b
    a=b
    b=c

#count vowels
v=input("enter the string:")
count=0
for ch in v:
    if ch in "AEIOUaeiou":
        count=count+1
print("the count of vowels are",count)

#WHILE LOOP
v=input("enter the string:")
count=0
i=1
while i<len(v):
    if v[i] in "AEIOUaeiou":
        count=count+1
    i=i+1
print("the count of vowels are",count) 

#amstrong number
n=int(input("enter A number:"))
sum=0
for i in str(n):
    sum=sum+int(i)**3
if sum==n:
    print(n,"is an amstrong number")
else:
    print(n,"is not an amstrong number")

#while loop
n=int(input("enter A number:"))
temp=n
sum=0
while temp>0:
    digit=temp%10
    sum=sum+(digit**3)
    temp=temp//10
if sum==n:
    print(n,"is an amstrong number")
else:
    print(n,"is not an amstrong number")

#palindrome number
n=int(input("enter the number:"))
temp=n
reverse=0
while temp>0:
    digit=temp%10
    reverse=reverse*10+digit
    temp=temp//10
if n==reverse:
    print("it is a palindrome number")
else:
    print("it is not a palindrome number")

#for loop
n=int(input("enter the number:"))
temp=n
reverse=0
for i in range(len(str(n))):
    digit=temp%10
    reverse=reverse*10+digit
    temp=temp//10
if n==reverse:
    print("it is a  palindrome number")
else:
    print("it is not a palindrome number")

#largest word in a setence
s=input("enter the sentence:")
words=s.split()
largest=""
for word in words:
    if len(word)>len(largest):
        largest=word
print("the largest word is",largest)
print("the length of largest word is",len(largest))

#while loop
s=input("enter the sentence:")
word=s.split()
largest=""
i=0
while i<len(word):
    if len(word)>len(largest):
       largest=word[i]
    i=i+1
print("the largest word is",largest)
print("the length of largest word is",len(largest))

