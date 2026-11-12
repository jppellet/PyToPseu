"""
Code                                                       │   Interpretation
————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
"""                                                       #│
### Cours 1                                               #│   
                                                          #│   
side = 4                                                  #│   in s̲i̲d̲e̲, store 4
area = side * side                                        #│   in a̲r̲e̲a̲, store the product s̲i̲d̲e̲ × s̲i̲d̲e̲
                                                          #│   
print(area)                                               #│   display a̲r̲e̲a̲
                                                          #│   
side: int = 4                                             #│   in s̲i̲d̲e̲, intended for an integer number, store 4
area: int = side * side                                   #│   in a̲r̲e̲a̲, intended for an integer number, store the product s̲i̲d̲e̲ × s̲i̲d̲e̲
                                                          #│   
print(area)                                               #│   display a̲r̲e̲a̲
                                                          #│   
                                                          #│   
side: int = 4                                             #│   in s̲i̲d̲e̲, intended for an integer number, store 4
                                                          #│   
length: float = 3.5                                       #│   in l̲e̲n̲gt̲h̲, intended for a decimal number, store 3.5
my_name: str = "Jean-Philippe"                            #│   in m̲y ̲n̲a̲m̲e̲, intended for a string, store "Jean-Philippe"
my_last_name: str = 'Pellet'                              #│   in m̲y ̲l̲a̲s̲t̲ ̲n̲a̲m̲e̲, intended for a string, store "Pellet"
                                                          #│   
                                                          #│   
                                                          #│   
some_int: int      = 34                                   #│   in s̲o̲m̲e̲ ̲i̲n̲t̲, intended for an integer number, store 34
some_int_as_float  = float(some_int)                      #│   in s̲o̲m̲e̲ ̲i̲n̲t̲ ̲a̲s̲ ̲f̲l̲o̲a̲t̲, store the conversion to a decimal number of s̲o̲m̲e̲ ̲i̲n̲t̲
some_int_as_string = str(some_int)                        #│   in s̲o̲m̲e̲ ̲i̲n̲t̲ ̲a̲s̲ ̲s̲t̲r̲i̲n̲g, store the conversion to a character string of s̲o̲m̲e̲ ̲i̲n̲t̲
                                                          #│   
                                                          #│   
# Conversion depuis un float                              #│   
import math                                               #│   we'll use the module m̲a̲t̲h̲
                                                          #│   
some_float: float       = 0.182                           #│   in s̲o̲m̲e̲ ̲f̲l̲o̲a̲t̲, intended for a decimal number,
                                                          #│   │     └╴ store 0.182
some_float_rounded_up   = math.ceil(some_float)  # 1      #│   in s̲o̲m̲e̲ ̲f̲l̲o̲a̲t̲ ̲r̲o̲u̲n̲d̲e̲d̲ ̲u̲p, store s̲o̲m̲e̲ ̲f̲l̲o̲a̲t̲ rounded up
some_float_rounded_down = math.floor(some_float) # 0      #│   in s̲o̲m̲e̲ ̲f̲l̲o̲a̲t̲ ̲r̲o̲u̲n̲d̲e̲d̲ ̲d̲o̲w̲n̲, store s̲o̲m̲e̲ ̲f̲l̲o̲a̲t̲ rounded down
some_float_as_int       = int(some_float)        # 0      #│   in s̲o̲m̲e̲ ̲f̲l̲o̲a̲t̲ ̲a̲s̲ ̲i̲n̲t̲, store the conversion to an integer number of s̲o̲m̲e̲ ̲f̲l̲o̲a̲t̲
                                                          #│   
                                                          #│   
math.ceil(some_float)                                     #│   s̲o̲m̲e̲ ̲f̲l̲o̲a̲t̲ rounded up
print(some_variable)                                      #│   display s̲o̲m̲e̲ ̲v̲a̲r̲i̲a̲b̲l̲e̲
                                                          #│   
                                                          #│   
my_string = "programmation"                               #│   in m̲y ̲s̲t̲r̲i̲n̲g, store "programmation"
# Vous choisissez le nom de la variable;                  #│   
# la valeur est toujours entre "" ou ''                   #│   
                                                          #│   
# la fonction len() retourne la longueur d'un string      #│   
length = len(my_string)                                   #│   in l̲e̲n̲gt̲h̲, store the length of m̲y ̲s̲t̲r̲i̲n̲g
                                                          #│   
# la méthode upper() s'écrit après un point et            #│   
# crée une version tout en majuscules de la valeur        #│   
# indiquée avant le point                                 #│   
my_string_upper = my_string.upper()                       #│   in m̲y ̲s̲t̲r̲i̲n̲g ̲u̲ppe̲r̲, store an uppercase copy of m̲y ̲s̲t̲r̲i̲n̲g
                                                          #│   
# le slicing (indexage d'une variable entre [])           #│   
# permet d'extraire une partie du string                  #│   
my_substring = my_string[1:4]                             #│   in m̲y ̲s̲u̲b̲s̲t̲r̲i̲n̲g, store the elements of m̲y ̲s̲t̲r̲i̲n̲g from position 1 to 4
                                                          #│   
my_substring = my_string[1:4].upper()                     #│   in m̲y ̲s̲u̲b̲s̲t̲r̲i̲n̲g, store an uppercase copy of the elements of m̲y ̲s̲t̲r̲i̲n̲g from position 1 to 4
                                                          #│   
### Cours 2                                               #│   
                                                          #│   
second_part = my_name[5:len(my_name)]                     #│   in s̲e̲c̲o̲n̲d̲ ̲pa̲r̲t̲, store the elements of m̲y ̲n̲a̲m̲e̲ starting at position 5
second_part = my_name[5:] # équivalent                    #│   in s̲e̲c̲o̲n̲d̲ ̲pa̲r̲t̲, store the elements of m̲y ̲n̲a̲m̲e̲ starting at position 5
                                                          #│   
first_char = my_name[0]                                   #│   in f̲i̲r̲s̲t̲ ̲c̲h̲a̲r̲, store element 0 of m̲y ̲n̲a̲m̲e̲
                                                          #│   
print(f"Durée du trajet: {duration} h")                   #│   display the expansion of 'Durée du trajet: {duration} h'
                                                          #│   
print(f"On a l’ensemble A = {{ x | x > {min_value} }}")   #│   display the expansion of 'On a l’ensemble A = {{ x | x > {min_value} }}'
                                                          #│   
duration_hours, rest = divmod(distance, speed)            #│   in (̲d̲u̲r̲a̲t̲i̲o̲n̲ ̲h̲o̲u̲r̲s̲,̲ ̲r̲e̲s̲t̲)̲, store the result of the function divmod with d̲i̲s̲t̲a̲n̲c̲e̲, s̲pe̲e̲d̲
                                                          #│   
age = input("Quel âge avez-vous? ")                       #│   in a̲ge̲, store the user response to the question "Quel âge avez-vous? "
print("Age actuel:", age)                                 #│   display "Age actuel:" and a̲ge̲
                                                          #│   
print("Dans deux ans:", age + 2)                          #│   display "Dans deux ans:" and the sum of a̲ge̲ and 2
                                                          #│   
print("Dans deux ans:", (int(age) + 2))                   #│   display "Dans deux ans:" and the sum of ⟨the conversion to an integer number of a̲ge̲⟩ and 2
                                                          #│   
                                                          #│   
age2 = int(age) + 2                                       #│   in a̲ge̲2̲, store the sum of ⟨the conversion to an integer number of a̲ge̲⟩ and 2
print("Dans deux ans:", age2)                             #│   display "Dans deux ans:" and a̲ge̲2̲
                                                          #│   
age = int(input("Quel âge avez-vous? "))                  #│   in a̲ge̲, store the conversion to an integer number of the user response to the question "Quel âge avez-vous? "
print("Age actuel:", age)                                 #│   display "Age actuel:" and a̲ge̲
print("Dans deux ans:", age + 2)                          #│   display "Dans deux ans:" and the sum of a̲ge̲ and 2
                                                          #│   
                                                          #│   
my_string = input()                                       #│   in m̲y ̲s̲t̲r̲i̲n̲g, store what the user will type
limit = 10                                                #│   in l̲i̲m̲i̲t̲, store 10
                                                          #│   
if len(my_string) > limit:                                #│   if the length of m̲y ̲s̲t̲r̲i̲n̲g is greater than l̲i̲m̲i̲t̲:
    short_string = my_string[:limit - 1] + "…"            #│   │   in s̲h̲o̲r̲t̲ ̲s̲t̲r̲i̲n̲g, store the sum of the ⟨the difference between l̲i̲m̲i̲t̲ and 1⟩ first elements of m̲y ̲s̲t̲r̲i̲n̲g and "…"
else:                                                     #│   else:
    short_string = my_string                              #│   │   in s̲h̲o̲r̲t̲ ̲s̲t̲r̲i̲n̲g, store m̲y ̲s̲t̲r̲i̲n̲g
                                                          #│   
print(short_string)                                       #│   display s̲h̲o̲r̲t̲ ̲s̲t̲r̲i̲n̲g
                                                          #│   
course = "Programmation"                                  #│   in c̲o̲u̲r̲s̲e̲, store "Programmation"
if course == "Programmation":                             #│   if c̲o̲u̲r̲s̲e̲ is equal to "Programmation":
    pass                                                  #│   │   don’t do anything
if course.lower() == "programmation":                     #│   if a lowercase copy of c̲o̲u̲r̲s̲e̲ is equal to "programmation":
    pass                                                  #│   │   don’t do anything
if course.startswith("Prog"):                             #│   if c̲o̲u̲r̲s̲e̲ starts with "Prog":
    pass                                                  #│   │   don’t do anything
if course.endswith("ation"):                              #│   if c̲o̲u̲r̲s̲e̲ ends with "ation":
    pass                                                  #│   │   don’t do anything
if "mmati" in course:                                     #│   if "mmati" is in c̲o̲u̲r̲s̲e̲:
    pass                                                  #│   │   don’t do anything
                                                          #│   
x: int = ...                                              #│   in x̲, intended for an integer number, store something to be defined
                                                          #│   
if x > 1 and x < 100:                                     #│   if x̲ is greater than 1 and if x̲ is smaller than 100:
    pass                                                  #│   │   don’t do anything
if x > 1 or x < 100:                                      #│   if x̲ is greater than 1 or if x̲ is smaller than 100:
    pass                                                  #│   │   don’t do anything
if not (x > 1):                                           #│   if ⟨x̲ is greater than 1⟩ is false:
    pass                                                  #│   │   don’t do anything
if (not x > 1) or (x > 1 and x < 100):                    #│   if ⟨x̲ is greater than 1⟩ is false or if x̲ is greater than 1 and x̲ is smaller than 100:
    pass                                                  #│   │   don’t do anything
                                                          #│   
                                                          #│   
                                                          #│   
name: str = input("Tapez votre nom: ")                    #│   in n̲a̲m̲e̲, intended for a string, store the user response to the question "Tapez votre nom: "
is_compound_name: bool = "-" in name or " " in name       #│   in i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲, intended for a true/false value,
                                                          #│   │     └╴ store true/false according to if "-" is in n̲a̲m̲e̲ or " " is in n̲a̲m̲e̲
is_long_name: bool = len(name) > 10                       #│   in i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲, intended for a true/false value,
                                                          #│   │     └╴ store true/false according to if the length of n̲a̲m̲e̲ is greater than 10
                                                          #│   
                                                          #│   
if is_compound_name and is_long_name:                     #│   if i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲ is true and if i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲ is true:
    print("Votre nom est long et composé")                #│   │   display "Votre nom est long et composé"
elif is_compound_name and not is_long_name:               #│   else, if i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲ is true and if i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲ is false:
    print("Votre nom est composé mais pas long")          #│   │   display "Votre nom est composé mais pas long"
elif not is_compound_name and is_long_name:               #│   else, if i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲ is false and if i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲ is true:
    print("Votre nom est long mais pas composé")          #│   │   display "Votre nom est long mais pas composé"
elif not is_compound_name and not is_long_name:           #│   else, if i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲ is false and if i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲ is false:
    print("Votre nom est court et simple")                #│   │   display "Votre nom est court et simple"
                                                          #│   
                                                          #│   
name: str = input("Tapez votre nom: ")                    #│   in n̲a̲m̲e̲, intended for a string, store the user response to the question "Tapez votre nom: "
is_compound_name: bool = "-" in name or " " in name       #│   in i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲, intended for a true/false value,
                                                          #│   │     └╴ store true/false according to if "-" is in n̲a̲m̲e̲ or " " is in n̲a̲m̲e̲
is_long_name: bool = len(name) > 10                       #│   in i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲, intended for a true/false value,
                                                          #│   │     └╴ store true/false according to if the length of n̲a̲m̲e̲ is greater than 10
                                                          #│   
                                                          #│   
if is_compound_name and is_long_name:                     #│   if i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲ is true and if i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲ is true:
    print("Votre nom est long et composé")                #│   │   display "Votre nom est long et composé"
elif is_compound_name and not is_long_name:               #│   else, if i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲ is true and if i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲ is false:
    print("Votre nom est composé mais pas long")          #│   │   display "Votre nom est composé mais pas long"
elif not is_compound_name and is_long_name:               #│   else, if i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲ is false and if i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲ is true:
    print("Votre nom est long mais pas composé")          #│   │   display "Votre nom est long mais pas composé"
elif not is_compound_name and not is_long_name:           #│   else, if i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲ is false and if i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲ is false:
    print("Votre nom est court et simple")                #│   │   display "Votre nom est court et simple"
                                                          #│   
if is_compound_name:                                      #│   if i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲ is true:
    if is_long_name:                                      #│   │   if i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲ is true:
        print("Votre nom est long et composé")            #│   │   │   display "Votre nom est long et composé"
    else:                                                 #│   │   else:
        print("Votre nom est composé mais pas long")      #│   │   │   display "Votre nom est composé mais pas long"
else:                                                     #│   else:
    if is_long_name:                                      #│   │   if i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲ is true:
        print("Votre nom est long mais pas composé")      #│   │   │   display "Votre nom est long mais pas composé"
    else:                                                 #│   │   else:
        print("Votre nom est court et simple")            #│   │   │   display "Votre nom est court et simple"