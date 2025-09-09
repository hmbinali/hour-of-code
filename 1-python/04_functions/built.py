def chai_flavor(flavor="masala"):
    """Return the flavor of chai."""
    return flavor


# dunder - dunder doc
print(chai_flavor.__doc__)
print(chai_flavor.__name__)
# help(len)


def generate_bill(chai=0, samosa=0):
    """calculate the total bill for chai and samosa

    Args:
        chai (int, optional): nuber of chai cups. Defaults to 0.
        samosa (int, optional): number of samosa. Defaults to 0.
        return: (total amount, thank you message)
    """
    total = chai * 10 + samosa * 15
    return total, "Thank you visiting chaicode.com"


generate_bill()
