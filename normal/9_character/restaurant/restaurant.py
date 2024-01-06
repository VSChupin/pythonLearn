class Restaurant():
    """Модель ресторана."""

    def __init__(self, restaurant_name, cuisine_type):
        self.name = restaurant_name
        self.type = cuisine_type
        
    def describe_restaurant(self):
        print(f"This restaurant name is {self.name} and type is {self.type}.")

    def open_restaurant(self):
        print(f"The restaurant {self.name} is open.")