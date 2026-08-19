print('Welcome to the tip calculator!')
bill = float(input("What was the total bill $: "))
tip = float(input("How much tip would you like to give? 10, 12, or 15 "))
num = int(input("How many people to split the bill? "))

total = bill + (bill * (tip/100) )
print(f'Each peerson should pay: ${round(total / num, 2)}')