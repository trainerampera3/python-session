class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    def __add__(self, other):
        return self.price + other.price

b1 = Product('Keyboard', 600)
b2 = Product('Mouse', 400)

print(b1 + b2)