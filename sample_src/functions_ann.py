"""
Code                         │   Interprétation
————————————————————————————————————————————————————————————
"""                         #│
a = lambda: 42              #│   dans a̲, stocke une fonction anonyme sans argument
                            #│   │     └╴ qui renvoie 42
a = lambda x: x + 1         #│   dans a̲, stocke une fonction anonyme qui prend un argument, x̲, et
                            #│   │     └╴ qui renvoie la somme de x̲ et 1
a = lambda x, y: x + 1      #│   dans a̲, stocke une fonction anonyme qui prend 2 arguments, x̲ et y̲, et
                            #│   │     └╴ qui renvoie la somme de x̲ et 1
a = lambda x, y, z: x + 1   #│   dans a̲, stocke une fonction anonyme qui prend 3 arguments, x̲, y̲ et z̲, et
                            #│   │     └╴ qui renvoie la somme de x̲ et 1
                            #│   
                            #│   
def b() -> int:             #│   définis la fonction b̲, sans argument, 
                            #│   │     └╴ qui renvoie un nombre entier, ainsi:
    return 42               #│   │   sors de la fonction en renvoyant 42
                            #│   
def b(x) -> int:            #│   définis la fonction b̲, qui prend un argument, x̲, et 
                            #│   │     └╴ qui renvoie un nombre entier, ainsi:
    return x + 1            #│   │   sors de la fonction en renvoyant la somme de x̲ et 1
                            #│   
def b(x, y) -> int:         #│   définis la fonction b̲, qui prend 2 arguments, x̲ et y̲, et 
                            #│   │     └╴ qui renvoie un nombre entier, ainsi:
    return x + 1            #│   │   sors de la fonction en renvoyant la somme de x̲ et 1
                            #│   
def b(x, y, z) -> int:      #│   définis la fonction b̲, qui prend 3 arguments, x̲, y̲ et z̲, et 
                            #│   │     └╴ qui renvoie un nombre entier, ainsi:
    return x + 1            #│   │   sors de la fonction en renvoyant la somme de x̲ et 1
                            #│   
def b() -> None:            #│   définis la fonction b̲, sans argument, qui ne renvoie rien, ainsi:
    return 42               #│   │   sors de la fonction en renvoyant 42
                            #│   
def b(x) -> None:           #│   définis la fonction b̲, qui prend un argument, x̲, et 
                            #│   │     └╴ qui ne renvoie rien, ainsi:
    return x + 1            #│   │   sors de la fonction en renvoyant la somme de x̲ et 1
                            #│   
def b(x, y) -> None:        #│   définis la fonction b̲, qui prend 2 arguments, x̲ et y̲, et 
                            #│   │     └╴ qui ne renvoie rien, ainsi:
    return x + 1            #│   │   sors de la fonction en renvoyant la somme de x̲ et 1
                            #│   
def b(x, y, z) -> None:     #│   définis la fonction b̲, qui prend 3 arguments, x̲, y̲ et z̲, et 
                            #│   │     └╴ qui ne renvoie rien, ainsi:
    return x + 1            #│   │   sors de la fonction en renvoyant la somme de x̲ et 1
                            #│   
def b():                    #│   définis la fonction b̲, sans argument, ainsi:
    return 42               #│   │   sors de la fonction en renvoyant 42
                            #│   
def b(x):                   #│   définis la fonction b̲, qui prend un argument, x̲, ainsi:
    return x + 1            #│   │   sors de la fonction en renvoyant la somme de x̲ et 1
                            #│   
def b(x, y):                #│   définis la fonction b̲, qui prend 2 arguments, x̲ et y̲, ainsi:
    return x + 1            #│   │   sors de la fonction en renvoyant la somme de x̲ et 1
                            #│   
def b(x, y, z):             #│   définis la fonction b̲, qui prend 3 arguments, x̲, y̲ et z̲, ainsi:
    return x + 1            #│   │   sors de la fonction en renvoyant la somme de x̲ et 1
                            #│   
def c(a: int, b: bool):     #│   définis la fonction c̲, qui prend 2 arguments, a̲ (un nombre entier) et 
                            #│   │     └╴ b̲ (une valeur vrai/faux), ainsi:
    return None             #│   │   sors de la fonction en renvoyant une valeur vide