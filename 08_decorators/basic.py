from functools import wraps


def my_decorator(func):
    @wraps(func)  # preserve function metadata
    def wrapper():
        print("Before function runs")
        func()
        print("After function runs")

    return wrapper


@my_decorator
def greet():
    print("Hello from decorators class from chaicode")


greet()
print(greet.__name__)
