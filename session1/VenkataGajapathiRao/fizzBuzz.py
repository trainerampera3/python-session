"""A fizz buzz is a game that says when you say a number 
if it is multiple with 3 then its fizz or 
if number is  multiple with 5 then its buzz or 
if it is multiple by both 3 and 5 then its Fizz buzz """

# lets check frim 1 to 101 numbers
for tomSays in range(1, 101):
    if tomSays % 3 == 0 and tomSays%5 ==0:
        print("Fizz Buzz")
    elif(tomSays%3==0) :
        print("Fizz")
    elif(tomSays % 5 == 0):
        print("Buzz")
    else:
        print(tomSays, end=" , ")
