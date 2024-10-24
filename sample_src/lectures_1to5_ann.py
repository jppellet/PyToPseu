"""
Code                                                       │   Interprétation
————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
"""                                                       #│
### Cours 1                                               #│   
                                                          #│   
side = 4                                                  #│   dans s̲i̲d̲e̲, stocke 4
area = side * side                                        #│   dans a̲r̲e̲a̲, stocke le produit s̲i̲d̲e̲ × s̲i̲d̲e̲
                                                          #│   
print(area)                                               #│   affiche a̲r̲e̲a̲
                                                          #│   
side: int = 4                                             #│   dans s̲i̲d̲e̲, prévu pour un nombre entier, stocke 4
area: int = side * side                                   #│   dans a̲r̲e̲a̲, prévu pour un nombre entier, stocke le produit s̲i̲d̲e̲ × s̲i̲d̲e̲
                                                          #│   
print(area)                                               #│   affiche a̲r̲e̲a̲
                                                          #│   
                                                          #│   
side: int = 4                                             #│   dans s̲i̲d̲e̲, prévu pour un nombre entier, stocke 4
                                                          #│   
length: float = 3.5                                       #│   dans l̲e̲n̲gt̲h̲, prévu pour un nombre à virgule, stocke 3.5
my_name: str = "Jean-Philippe"                            #│   dans m̲y ̲n̲a̲m̲e̲, prévu pour une chaîne de caractères,
                                                          #│   │     └╴ stocke "Jean-Philippe"
my_last_name: str = 'Pellet'                              #│   dans m̲y ̲l̲a̲s̲t̲ ̲n̲a̲m̲e̲, prévu pour une chaîne de caractères,
                                                          #│   │     └╴ stocke "Pellet"
                                                          #│   
                                                          #│   
                                                          #│   
some_int: int      = 34                                   #│   dans s̲o̲m̲e̲ ̲i̲n̲t̲, prévu pour un nombre entier, stocke 34
some_int_as_float  = float(some_int)                      #│   dans s̲o̲m̲e̲ ̲i̲n̲t̲ ̲a̲s̲ ̲f̲l̲o̲a̲t̲, stocke la conversion en nombre à virgule de s̲o̲m̲e̲ ̲i̲n̲t̲
some_int_as_string = str(some_int)                        #│   dans s̲o̲m̲e̲ ̲i̲n̲t̲ ̲a̲s̲ ̲s̲t̲r̲i̲n̲g, stocke la conversion en chaîne de caractères de s̲o̲m̲e̲ ̲i̲n̲t̲
                                                          #│   
                                                          #│   
# Conversion depuis un float                              #│   
import math                                               #│   on va utiliser le module m̲a̲t̲h̲
                                                          #│   
some_float: float       = 0.182                           #│   dans s̲o̲m̲e̲ ̲f̲l̲o̲a̲t̲, prévu pour un nombre à virgule,
                                                          #│   │     └╴ stocke 0.182
some_float_rounded_up   = math.ceil(some_float)  # 1      #│   dans s̲o̲m̲e̲ ̲f̲l̲o̲a̲t̲ ̲r̲o̲u̲n̲d̲e̲d̲ ̲u̲p, stocke l’arrondi supérieur de s̲o̲m̲e̲ ̲f̲l̲o̲a̲t̲
some_float_rounded_down = math.floor(some_float) # 0      #│   dans s̲o̲m̲e̲ ̲f̲l̲o̲a̲t̲ ̲r̲o̲u̲n̲d̲e̲d̲ ̲d̲o̲w̲n̲, stocke l’arrondi inférieur de s̲o̲m̲e̲ ̲f̲l̲o̲a̲t̲
some_float_as_int       = int(some_float)        # 0      #│   dans s̲o̲m̲e̲ ̲f̲l̲o̲a̲t̲ ̲a̲s̲ ̲i̲n̲t̲, stocke la conversion en nombre entier de s̲o̲m̲e̲ ̲f̲l̲o̲a̲t̲
                                                          #│   
                                                          #│   
math.ceil(some_float)                                     #│   l’arrondi supérieur de s̲o̲m̲e̲ ̲f̲l̲o̲a̲t̲
print(some_variable)                                      #│   affiche s̲o̲m̲e̲ ̲v̲a̲r̲i̲a̲b̲l̲e̲
                                                          #│   
                                                          #│   
my_string = "programmation"                               #│   dans m̲y ̲s̲t̲r̲i̲n̲g, stocke "programmation"
# Vous choisissez le nom de la variable;                  #│   
# la valeur est toujours entre "" ou ''                   #│   
                                                          #│   
# la fonction len() retourne la longueur d'un string      #│   
length = len(my_string)                                   #│   dans l̲e̲n̲gt̲h̲, stocke la longueur de m̲y ̲s̲t̲r̲i̲n̲g
                                                          #│   
# la méthode upper() s'écrit après un point et            #│   
# crée une version tout en majuscules de la valeur        #│   
# indiquée avant le point                                 #│   
my_string_upper = my_string.upper()                       #│   dans m̲y ̲s̲t̲r̲i̲n̲g ̲u̲ppe̲r̲, stocke une copie tout en majuscules de m̲y ̲s̲t̲r̲i̲n̲g
                                                          #│   
# le slicing (indexage d'une variable entre [])           #│   
# permet d'extraire une partie du string                  #│   
my_substring = my_string[1:4]                             #│   dans m̲y ̲s̲u̲b̲s̲t̲r̲i̲n̲g, stocke les éléments de m̲y ̲s̲t̲r̲i̲n̲g de la position 1 à 4
                                                          #│   
my_substring = my_string[1:4].upper()                     #│   dans m̲y ̲s̲u̲b̲s̲t̲r̲i̲n̲g, stocke une copie tout en majuscules des éléments de m̲y ̲s̲t̲r̲i̲n̲g de la position 1 à 4
                                                          #│   
### Cours 2                                               #│   
                                                          #│   
second_part = my_name[5:len(my_name)]                     #│   dans s̲e̲c̲o̲n̲d̲ ̲pa̲r̲t̲, stocke les éléments de m̲y ̲n̲a̲m̲e̲ à partir de la position 5
second_part = my_name[5:] # équivalent                    #│   dans s̲e̲c̲o̲n̲d̲ ̲pa̲r̲t̲, stocke les éléments de m̲y ̲n̲a̲m̲e̲ à partir de la position 5
                                                          #│   
first_char = my_name[0]                                   #│   dans f̲i̲r̲s̲t̲ ̲c̲h̲a̲r̲, stocke l'élément 0 de m̲y ̲n̲a̲m̲e̲
                                                          #│   
print(f"Durée du trajet: {duration} h")                   #│   affiche l'expansion de 'Durée du trajet: {duration} h'
                                                          #│   
print(f"On a l’ensemble A = {{ x | x > {min_value} }}")   #│   affiche l'expansion de 'On a l’ensemble A = {{ x | x > {min_value} }}'
                                                          #│   
duration_hours, rest = divmod(distance, speed)            #│   dans (̲d̲u̲r̲a̲t̲i̲o̲n̲ ̲h̲o̲u̲r̲s̲,̲ ̲r̲e̲s̲t̲)̲, stocke le résultat de la fonction divmod avec d̲i̲s̲t̲a̲n̲c̲e̲, s̲pe̲e̲d̲
                                                          #│   
age = input("Quel âge avez-vous? ")                       #│   dans a̲ge̲, stocke la réponse de l'utilisateur à la question "Quel âge avez-vous? "
print("Age actuel:", age)                                 #│   affiche "Age actuel:" et a̲ge̲
                                                          #│   
print("Dans deux ans:", age + 2)                          #│   affiche "Dans deux ans:" et la somme de a̲ge̲ et 2
                                                          #│   
print("Dans deux ans:", (int(age) + 2))                   #│   affiche "Dans deux ans:" et la somme de la conversion en nombre entier de a̲ge̲ et 2
                                                          #│   
                                                          #│   
age2 = int(age) + 2                                       #│   dans a̲ge̲2̲, stocke la somme de la conversion en nombre entier de a̲ge̲ et 2
print("Dans deux ans:", age2)                             #│   affiche "Dans deux ans:" et a̲ge̲2̲
                                                          #│   
age = int(input("Quel âge avez-vous? "))                  #│   dans a̲ge̲, stocke la conversion en nombre entier de la réponse de l'utilisateur à la question "Quel âge avez-vous? "
print("Age actuel:", age)                                 #│   affiche "Age actuel:" et a̲ge̲
print("Dans deux ans:", age + 2)                          #│   affiche "Dans deux ans:" et la somme de a̲ge̲ et 2
                                                          #│   
                                                          #│   
my_string = input()                                       #│   dans m̲y ̲s̲t̲r̲i̲n̲g, stocke ce que l'utilisateur va taper
limit = 10                                                #│   dans l̲i̲m̲i̲t̲, stocke 10
                                                          #│   
if len(my_string) > limit:                                #│   si la longueur de m̲y ̲s̲t̲r̲i̲n̲g est plus grand que l̲i̲m̲i̲t̲:
    short_string = my_string[:limit - 1] + "…"            #│   │   dans s̲h̲o̲r̲t̲ ̲s̲t̲r̲i̲n̲g, stocke la somme des ⟨la différence entre l̲i̲m̲i̲t̲ et 1⟩ premiers éléments de m̲y ̲s̲t̲r̲i̲n̲g et "…"
else:                                                     #│   sinon:
    short_string = my_string                              #│   │   dans s̲h̲o̲r̲t̲ ̲s̲t̲r̲i̲n̲g, stocke m̲y ̲s̲t̲r̲i̲n̲g
                                                          #│   
print(short_string)                                       #│   affiche s̲h̲o̲r̲t̲ ̲s̲t̲r̲i̲n̲g
                                                          #│   
course = "Programmation"                                  #│   dans c̲o̲u̲r̲s̲e̲, stocke "Programmation"
if course == "Programmation":                             #│   si c̲o̲u̲r̲s̲e̲ est égal à "Programmation":
    pass                                                  #│   │   ne fais rien de spécial
if course.lower() == "programmation":                     #│   si une copie tout en minuscules de c̲o̲u̲r̲s̲e̲ est égal à "programmation":
    pass                                                  #│   │   ne fais rien de spécial
if course.startswith("Prog"):                             #│   si c̲o̲u̲r̲s̲e̲ commence par "Prog":
    pass                                                  #│   │   ne fais rien de spécial
if course.endswith("ation"):                              #│   si c̲o̲u̲r̲s̲e̲ finit par "ation":
    pass                                                  #│   │   ne fais rien de spécial
if "mmati" in course:                                     #│   si "mmati" fait partie de c̲o̲u̲r̲s̲e̲:
    pass                                                  #│   │   ne fais rien de spécial
                                                          #│   
x: int = ...                                              #│   dans x̲, prévu pour un nombre entier, stocke quelque chose à définir
                                                          #│   
if x > 1 and x < 100:                                     #│   si x̲ est plus grand que 1 et que x̲ est plus petit que 100:
    pass                                                  #│   │   ne fais rien de spécial
if x > 1 or x < 100:                                      #│   si x̲ est plus grand que 1 ou que x̲ est plus petit que 100:
    pass                                                  #│   │   ne fais rien de spécial
if not (x > 1):                                           #│   si ⟨x̲ est plus grand que 1⟩ est faux:
    pass                                                  #│   │   ne fais rien de spécial
if (not x > 1) or (x > 1 and x < 100):                    #│   si ⟨x̲ est plus grand que 1⟩ est faux ou que x̲ est plus grand que 1 et x̲ est plus petit que 100:
    pass                                                  #│   │   ne fais rien de spécial
                                                          #│   
                                                          #│   
                                                          #│   
name: str = input("Tapez votre nom: ")                    #│   dans n̲a̲m̲e̲, prévu pour une chaîne de caractères, stocke la réponse de l'utilisateur à la question "Tapez votre nom: "
is_compound_name: bool = "-" in name or " " in name       #│   dans i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲, prévu pour une valeur booléenne,
                                                          #│   │     └╴ stocke vrai/faux selon si "-" fait partie de n̲a̲m̲e̲ ou " " fait partie de n̲a̲m̲e̲
is_long_name: bool = len(name) > 10                       #│   dans i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲, prévu pour une valeur booléenne,
                                                          #│   │     └╴ stocke vrai/faux selon si la longueur de n̲a̲m̲e̲ est plus grand que 10
                                                          #│   
                                                          #│   
if is_compound_name and is_long_name:                     #│   si i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲ est vrai et que i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲ est vrai:
    print("Votre nom est long et composé")                #│   │   affiche "Votre nom est long et composé"
elif is_compound_name and not is_long_name:               #│   sinon, si i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲ est vrai et que i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲ est faux:
    print("Votre nom est composé mais pas long")          #│   │   affiche "Votre nom est composé mais pas long"
elif not is_compound_name and is_long_name:               #│   sinon, si i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲ est faux et que i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲ est vrai:
    print("Votre nom est long mais pas composé")          #│   │   affiche "Votre nom est long mais pas composé"
elif not is_compound_name and not is_long_name:           #│   sinon, si i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲ est faux et que i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲ est faux:
    print("Votre nom est court et simple")                #│   │   affiche "Votre nom est court et simple"
                                                          #│   
                                                          #│   
name: str = input("Tapez votre nom: ")                    #│   dans n̲a̲m̲e̲, prévu pour une chaîne de caractères, stocke la réponse de l'utilisateur à la question "Tapez votre nom: "
is_compound_name: bool = "-" in name or " " in name       #│   dans i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲, prévu pour une valeur booléenne,
                                                          #│   │     └╴ stocke vrai/faux selon si "-" fait partie de n̲a̲m̲e̲ ou " " fait partie de n̲a̲m̲e̲
is_long_name: bool = len(name) > 10                       #│   dans i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲, prévu pour une valeur booléenne,
                                                          #│   │     └╴ stocke vrai/faux selon si la longueur de n̲a̲m̲e̲ est plus grand que 10
                                                          #│   
                                                          #│   
if is_compound_name and is_long_name:                     #│   si i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲ est vrai et que i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲ est vrai:
    print("Votre nom est long et composé")                #│   │   affiche "Votre nom est long et composé"
elif is_compound_name and not is_long_name:               #│   sinon, si i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲ est vrai et que i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲ est faux:
    print("Votre nom est composé mais pas long")          #│   │   affiche "Votre nom est composé mais pas long"
elif not is_compound_name and is_long_name:               #│   sinon, si i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲ est faux et que i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲ est vrai:
    print("Votre nom est long mais pas composé")          #│   │   affiche "Votre nom est long mais pas composé"
elif not is_compound_name and not is_long_name:           #│   sinon, si i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲ est faux et que i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲ est faux:
    print("Votre nom est court et simple")                #│   │   affiche "Votre nom est court et simple"
                                                          #│   
if is_compound_name:                                      #│   si i̲s̲ ̲c̲o̲m̲po̲u̲n̲d̲ ̲n̲a̲m̲e̲ est vrai:
    if is_long_name:                                      #│   │   si i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲ est vrai:
        print("Votre nom est long et composé")            #│   │   │   affiche "Votre nom est long et composé"
    else:                                                 #│   │   sinon:
        print("Votre nom est composé mais pas long")      #│   │   │   affiche "Votre nom est composé mais pas long"
else:                                                     #│   sinon:
    if is_long_name:                                      #│   │   si i̲s̲ ̲l̲o̲n̲g ̲n̲a̲m̲e̲ est vrai:
        print("Votre nom est long mais pas composé")      #│   │   │   affiche "Votre nom est long mais pas composé"
    else:                                                 #│   │   sinon:
        print("Votre nom est court et simple")            #│   │   │   affiche "Votre nom est court et simple"