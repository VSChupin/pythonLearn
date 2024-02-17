import json

def input_number():
    
    number = input("Enter your favorite number: ")

    filename = 'pythonLearn/normal/10_character/number.json'
    with open(filename, 'w') as file_obj:
        json.dump(number, file_obj)
    return number

def get_number():
    filename = "pythonLearn/normal/10_character/number.json"
    try:
        with open(filename) as file_obj:
            number = json.load(file_obj)
    except FileNotFoundError:
        return None
    else:
        return number
        
1
def show_number():
    number = get_number()
    
    if number:
        print(f"Your favorite number is {number}")
    else:
        number = input_number()
        print(f"We remember your favorite number {number}.")
    

show_number()