class Chai:
    origin = "India"


print(Chai.origin)

Chai.is_hot = True
print(Chai.is_hot)

# Creating objects from class chai
masala = Chai()
print("masala", masala.origin)
print("masala", masala.is_hot)
masala.is_hot = False

print("class", Chai.is_hot)
print("masala", masala.is_hot)

masala.flavor = "masala"
print(masala.flavor)
