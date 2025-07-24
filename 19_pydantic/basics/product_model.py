from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool = True


product_one = Product(id=1, name="laptop", price="999.99", in_stock=True)
product_two = Product(id=2, name="Mouse", price="29.00")

product_three = Product(name="Keyboard")
