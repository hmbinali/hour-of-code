from typing import List, Optional
from pydantic import BaseModel


class Address(BaseModel):
    street: str
    city: str
    postal_code: str


class User(BaseModel):
    id: int
    name: str
    address: Address


address = Address(street="123 something", city="Jaipuer", postal_code="100101")
user = User(id=123, name="hitesh", address=address)

user_data = {
    "id": 1,
    "name": "hitesh",
    "address": {
        "street": "321 something",
        "city": "Medina",
        "postal_code": "012834",
    },
}
new_user = User(**user_data)
print(user)
print(new_user)
