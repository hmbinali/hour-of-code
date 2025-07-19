class Engine:
    def __init__(self, horsepower: int):
        self.horsepower = horsepower

    def get_engine_info(self):
        return f"{self.horsepower} HP Engine"


class Vehicle:
    total_vehicles = 0  # class variable

    def __init__(self, brand: str, model: str, engine: Engine):
        self.brand = brand
        self.model = model
        self.engine = engine
        self._rental_price = 0  # for property demo
        Vehicle.total_vehicles += 1

    @staticmethod
    def get_vehicle_type():
        return "Generic Vehicle"

    @classmethod
    def get_total_vehicles(cls):
        return cls.total_vehicles

    @property
    def rental_price(self):
        return self._rental_price

    @rental_price.setter
    def rental_price(self, price: int):
        if price >= 0:
            self._rental_price = price

    def get_details(self):
        return f"{self.brand} {self.model} - {self.engine.get_engine_info()}"


class Car(Vehicle):
    def __init__(self, brand: str, model: str, engine: Engine, seats: int):
        super().__init__(brand, model, engine)
        self.seats = seats

    def get_details(self):
        return f"{super().get_details()} - Seats: {self.seats}"
