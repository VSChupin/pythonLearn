class Employee():
    
    def __init__(self, first, last, salary):
        self.first = first
        self.last = last
        self.salary = salary
        
        
    def give_raise(self, up_salary=5000):
        self.salary = self.salary + up_salary
        print(f"New salary = {self.salary}.")
        return self.salary
    
    
# my_empl = Employee('Ivan', 'Kekov', 1000)
# my_empl.give_raise()
# my_empl.give_raise(1000)
