def pure_chai(cups):
    return cups * 10


total_chai = 0


# Not recommended
def impure_chai(cups):
    global total_chai
    total_chai += cups


# recursive function
def pour_chai(n):
    if n == 0:
        return "All cups poured"
    return pour_chai(n - 1)


print(pour_chai(3))


chai_types = ["light", "kadak", "ginger", "kadak"]

# lambda or anonymous function
strong_chai = list(filter(lambda chai: chai == "kadak", chai_types))
print(strong_chai)
