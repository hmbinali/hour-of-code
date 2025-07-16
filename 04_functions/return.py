def make_chai():
    return "here is your masala chai"


return_value = make_chai()


def idle_chaiwala():
    pass


print(idle_chaiwala())


def sold_cups():
    return 120


total = sold_cups()
print(total)


def chai_status(cups_left):
    if cups_left == 0:
        return "Sorry, chai over"
    return "Chai is ready"


print(chai_status(0))
print(chai_status(5))


def chai_report():
    return 100, 20, 3


sold, remain, not_paid = chai_report()
print(sold)
print(remain)
print(not_paid)
sold, remain, _ = chai_report()
