class Chai:
    temperature = "hot"
    strength = "strong"


cutting = Chai()
print(cutting.temperature)

cutting.temperature = "mild"
print("After changing ", cutting.temperature)
print("Direct look into the class ", Chai.temperature)

del cutting.temperature
# if object attribute doesn't exist it falls back on the class
print(cutting.temperature)
 