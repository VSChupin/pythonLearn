import user
class Admin(user.User):
    
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