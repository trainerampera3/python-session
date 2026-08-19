# lets play Rocl Paper Scissor 
# Here we consider two colleagues ram and Shyam

ram = input("Ram says (Rock/Paper/Scissor): ")
shyam = input("Shyam says (Rock/Paper/Scissor): ")

ram = ram.lower()
shyam = shyam.lower()

if ram == shyam:
    print("It's a tie!")

elif (ram == "rock" and shyam == "scissor") or (ram == "paper" and shyam == "rock") or (ram == "scissor" and shyam == "paper"):
    print("Ram wins!")

elif (shyam == "rock" and ram == "scissor") or (shyam == "paper" and ram == "rock") or (shyam == "scissor" and ram == "paper"):
    print("Shyam wins!")

else:
    print("Invalid input! Please enter Rock, Paper, or Scissor.")