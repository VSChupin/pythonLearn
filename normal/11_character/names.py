from name_function import get_formatted_name

print("Enter the 'q' if you want finish.")

while True:
    
    first = input("\nPlease give me a first name: ")
    if first == 'q':
        break
    last = input("Please give me a lsat name: ")
    if last == 'q':
        break
    
    formatted_name = get_formatted_name(first, last)
    print("\tNeatly formatted name: " + formatted_name + ".")