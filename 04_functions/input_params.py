chai = "Ginger chai"


def prepare_chai(order):
    print("Preparing ", order)


prepare_chai(chai)

chai = [1, 2, 3]


def edit_chai(cup):
    cup[1] = 42


edit_chai(chai)
print(chai)


def make_chai(tea, milk, sugar):
    print(tea, milk, sugar)


make_chai("Darjeeling", "Yes", "Low")  # Positional
make_chai(tea="Darjeeling", sugar="Medium", milk="Yes")  # Keywords


# *args and **kwargs
def special_chai(*ingredients, **extras):
    print("Ingredients", ingredients)
    print("Extras", extras)


special_chai("Cinnamon", "Cardmom", sweetener="Honey", foam="yes")


# avoid default traps
def chai_order(order=[]):
    order.append("masala")
    print(order)


chai_order()
chai_order()


def chai_order_two(order=None):
    if order is None:
        order = []
    print(order)


chai_order_two()
