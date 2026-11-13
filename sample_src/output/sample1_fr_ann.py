"""
Code                          │   Interprétation
——————————————————————————————————————————————————————————————
"""                          #│
import math                  #│   on va utiliser le module m̲a̲t̲h̲
from sys import exit as ex   #│   on va utiliser l’élément e̲x̲i̲t̲ (en l’appelant e̲x̲) du module s̲ys̲
                             #│   
a: int = 4                   #│   dans a̲, prévu pour un nombre entier, stocke 4
b: float = 4 * 6             #│   dans b̲, prévu pour un nombre à virgule, stocke le produit 4 × 6
a = a + 1                    #│   ajoute 1 à a̲
a = 1 + a                    #│   ajoute 1 à a̲
a = a - 1                    #│   soustrais 1 de a̲
a = a * 2                    #│   multiplie a̲ par 2
a = 2 * a                    #│   multiplie a̲ par 2
a = a / 2                    #│   divise a̲ par 2
a = a // 2                   #│   divise a̲ par 2 en nombres entiers
                             #│   
b = math.sqrt(a)             #│   dans b̲, stocke la racine carrée de a̲
                             #│   
for i in range(0, 10, 1):    #│   répète 10 fois (en comptant avec i̲ à partir de 0):
    print(i)                 #│   │   affiche i̲
    print(i)                 #│   │   affiche i̲
                             #│   
for c in "abc":              #│   répète pour chaque caractère dans "abc" (qu'on va appeler c̲):
    for _ in range(5):       #│   │   répète 5 fois
        print(c)             #│   │   │   affiche c̲
