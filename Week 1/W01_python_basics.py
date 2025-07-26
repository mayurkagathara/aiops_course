# name = "john"
# num = 2.56982
# greeting = f"hi {name} and number is {num:>10.3f}"
# print(greeting)

# log_entries = [
#     "INFO: App started",
#     "ERROR: DB conn failed"
# ]

# cpu_metrics = (98.3, 85.6)
# set2 = {1, 2, 3}

# set2.add(2)

# num = 10
# if num != 25:
#     print("1")
# else:
#     print("else")

# fruits = ["apple", "banana", "cherry"]
# my_dict = {"a": 1, "b": 2, "c": 3}

# fruits_2 = {fruit:fruit.capitalize() for fruit in fruits}
# print(fruits_2)

# for key, value in my_dict.items():
#     if value == 2:
#         break
#     else:
#         print(key, " ", value)
# else:
#     print("loop excuted successfully")

# print("out")

# incorrect_input = True
# while incorrect_input:
#     choice = input("You want to continue (y/n): ")
#     if choice == 'y' or choice == 'n':
#         print("correct input")
#         incorrect_input = False
#     else:
#         incorrect_input = True
    
# # print(6/0)
# try:
#     #code which can throw error
#     print(6/0)
#     print(int("hi"))
# except ZeroDivisionError as ze:
#     print("ze occurred", ze)
# except Exception as e:
#     print("eror occured: ", str(e))
# finally:
#     print("this is always executed. con.close() file.close() del files")

# print("next operation started")


def function_name(a1, a2, b1 = 0, b2=1):
    print(a1, a2, b1, b2, (a1 + a2 - b1)**b2)
    pass

function_name(3, 4)

def add_all(*number:int)->int: 
    print(number)
    return sum(number)

ans = add_all(2,3)
print(ans)

def display_numbers(a, b=0, *args, **people_directory):
    print(a, b, args, people_directory)

display_numbers(2, 3, 4, "78", mario=92717291, shaktiman=988382872, batman="987654321")

class Animal():
    def __init__(self, name):
        self.name = name
        
    # A method of the class
    def greet(self):
        print(f"Hi I am {self.name}")

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
    def greet(self):
        print(f"woof woof, I'm {self.name} and my breed is {self.breed}")

my_dog = Animal("bruno")
your_dog = Dog("fluffy", "labrador")
print(my_dog.greet())
print(your_dog.greet())
