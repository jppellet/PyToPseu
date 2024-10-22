### Cours 1

side = 4
area = side * side

print(area)

side: int = 4
area: int = side * side

print(area)


side: int = 4

length: float = 3.5
my_name: str = "Jean-Philippe"
my_last_name: str = 'Pellet'



some_int: int      = 34
some_int_as_float  = float(some_int) 
some_int_as_string = str(some_int) 


# Conversion depuis un float
import math

some_float: float       = 0.182
some_float_rounded_up   = math.ceil(some_float)  # 1
some_float_rounded_down = math.floor(some_float) # 0
some_float_as_int       = int(some_float)        # 0


math.ceil(some_float)
print(some_variable)


my_string = "programmation"
# Vous choisissez le nom de la variable;
# la valeur est toujours entre "" ou ''

# la fonction len() retourne la longueur d'un string
length = len(my_string)

# la méthode upper() s'écrit après un point et
# crée une version tout en majuscules de la valeur
# indiquée avant le point
my_string_upper = my_string.upper()

# le slicing (indexage d'une variable entre [])
# permet d'extraire une partie du string
my_substring = my_string[1:4]

my_substring = my_string[1:4].upper()

### Cours 2

second_part = my_name[5:len(my_name)]
second_part = my_name[5:] # équivalent

first_char = my_name[0]

print(f"Durée du trajet: {duration} h")

print(f"On a l’ensemble A = {{ x | x > {min_value} }}")

duration_hours, rest = divmod(distance, speed)

age = input("Quel âge avez-vous? ")
print("Age actuel:", age)

print("Dans deux ans:", age + 2)

print("Dans deux ans:", (int(age) + 2))


age2 = int(age) + 2
print("Dans deux ans:", age2)

age = int(input("Quel âge avez-vous? "))
print("Age actuel:", age)
print("Dans deux ans:", age + 2)


my_string = input()
limit = 10

if len(my_string) > limit:
    short_string = my_string[:limit - 1] + "…"
else:
    short_string = my_string

print(short_string)

course = "Programmation"       
if course == "Programmation":  
    pass
if course.lower() == "programmation": 
    pass
if course.startswith("Prog"):   
    pass
if course.endswith("ation"):   
    pass
if "mmati" in course:        
    pass

x: int = ...

if x > 1 and x < 100:
    pass
if x > 1 or x < 100:
    pass
if not (x > 1):  
    pass
if (not x > 1) or (x > 1 and x < 100):
    pass



name: str = input("Tapez votre nom: ")
is_compound_name: bool = "-" in name or " " in name
is_long_name: bool = len(name) > 10


if is_compound_name and is_long_name:
    print("Votre nom est long et composé")
elif is_compound_name and not is_long_name:
    print("Votre nom est composé mais pas long")
elif not is_compound_name and is_long_name:
    print("Votre nom est long mais pas composé")
elif not is_compound_name and not is_long_name:
    print("Votre nom est court et simple")


name: str = input("Tapez votre nom: ")
is_compound_name: bool = "-" in name or " " in name
is_long_name: bool = len(name) > 10


if is_compound_name and is_long_name:
    print("Votre nom est long et composé")
elif is_compound_name and not is_long_name:
    print("Votre nom est composé mais pas long")
elif not is_compound_name and is_long_name:
    print("Votre nom est long mais pas composé")
elif not is_compound_name and not is_long_name:
    print("Votre nom est court et simple")

if is_compound_name:
    if is_long_name:
        print("Votre nom est long et composé")
    else:
        print("Votre nom est composé mais pas long")
else:
    if is_long_name:
        print("Votre nom est long mais pas composé")
    else:
        print("Votre nom est court et simple")