#Variables
"""
number=10
n2=20.5
print(number+n2)
first="Shahir"
last="shaik"
print(first+last)
"""

#Control flow statements
number=20
if number>20:
    print("Greater than 20!!")
else:
    print("less than or equal to 20!!")


#List Operations
lis=[1,2]
#lis.append([3,2,5])
lis.extend([2,1,4])
lis.insert(0,123)
print("after using the inser method:",lis)
lis.remove(1)
lis.pop(0)
print("After remvoing:",lis)
#lis.clear()
#del lis
#lis.sort()
"""
new_list=sorted(lis)
num_lis=[[1,2,3],[5,3,2],[6,4,3,4]]
num_lis.sort(key=lambda x:sum(x),reverse=True)
print(num_lis)

"""

#tuples
#Packing 
tup=10,4,5,63
print(tup)
#unpacking
a,b,c,d=tup
print(tup.count(10))

#Sets
sets={1,4,3,6}
sets.add(10)
a={1,3,4}
b={6,7,8,1}
#Union
print(a.union(b))
#Intersection
print(f"Intersection of two sets is {a.intersection(b)}")
#differene A-B
print(f"A-B {a.difference(b)}")
print(f"B-A {b.difference(a)}")

#list comphersion
lis=[x for x in range(1,10)]
lis=[x for x in range(1,10) if x%2==0]
lis=[x for x  in range(1,10) if x%2!=0]
lis=[x if x%2==0  else x+1 for x in range(1,10)]


#Dictionary
lis=[(1,10),(4,5)]
tracker=dict(lis)
tracker[3]=11
print(f"list of key {tracker.keys()}")
print(f"list of values {tracker.values()}")
print(f"list of items {tracker.items()}")
#SORTING A DICT
sorted_one=dict(sorted(tracker.items(),key=lambda x:x[1]))
print(sorted_one)

#String methods 
name="Shahir"
print(name[2])
print(name[:4])
print(len(name))
print(name.lower())
print(f"Upper format is {name.upper()}")
name2="   python   "
print(f"strip {name2.strip()}")
print(f"left strip {name2.lstrip()}")
print(f"right strip {name2.rstrip()}")
new_strig=name.replace("S","K")
print(f"after replacing {new_strig}")
name="Hello,world"
res=name.split(",")
res="".join(res)
print(res.count("l"))
print(f"Does it contain only alphabets:{res.isalpha()}")
print(f"Does it contain only number:{res.isdigit()}")
print(f"Does it contain both numbers and alphabetes:{res.isalnum()}")


#Loops
lis=[1,2,3,4]
for i in lis:
    if(i%2==0):
        break
    print(i)
for i in lis:
    if(i%10==0):
        break
    print(i)

else:
    print("good")

i=0
while(i<=10):
    print(i)
    i=i+1
    