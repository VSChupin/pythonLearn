class User():
    """Модель пользователя"""

    def __init__(self, first_name, last_name, age, location):
        self.fname = first_name
        self.lname = last_name
        self.age = age
        self.loc = location
        
    def describe_user(self):
        print("User info:" +
            f"\n{self.fname.title()}" +
            f"\n{self.lname.title()}" +
            f"\n{self.age}" +
            f"\n{self.loc.title()}")
        
    def greet_user(self):
        print(f"Hi, {self.fname.title()} {self.lname.title()}, {self.age} years old, from {self.loc.title()}!")
        
class Admin(User):
    
    def __init__(self, first_name, last_name, age, location):
        super().__init__(first_name, last_name, age, location)
        self.privileges = Privileges()
    
    def show_moves(self):
        for move in self.privileges:
            print(move)

class Privileges():
    
    def __init__(self):
        self.privileges = ['Разрешено добавлять сообщения',
                        'Разрешено удалять пользователей',
                        'Разрешено закреплять сообщения',
                        ]

    def show_moves(self):
        for move in self.privileges:
            print(move)