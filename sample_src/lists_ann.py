"""
Code                            │   Interprétation
——————————————————————————————————————————————————————————————————
"""                            #│
import typing                  #│   on va utiliser le module t̲ypi̲n̲g
                               #│   
l: list[int] = []              #│   dans l̲, prévu pour une liste de nombres entiers, stocke une liste vide
                               #│   
l = [1,2, 3]                   #│   dans l̲, stocke une liste avec les éléments 1, 2 et 3
                               #│   
l: typing.List[str] = 3        #│   dans l̲, prévu pour une liste de chaînes de caractères,
                               #│   │     └╴ stocke 3
                               #│   
l: list[list[int]] = []        #│   dans l̲, prévu pour une liste de listes de nombres entiers,
                               #│   │     └╴ stocke une liste vide
                               #│   
l: int = list()                #│   dans l̲, prévu pour un nombre entier, stocke une liste vide
                               #│   
d: dict[str, list[str]] = {}   #│   dans d̲, prévu pour un dictionnaire reliant des chaînes de caractères à des listes de chaînes de caractères,
                               #│   │     └╴ stocke un dictionnaire vide
                               #│   
l.append(42)                   #│   à la fin de l̲, ajoute 42
l.extend(l)                    #│   à la fin de l̲, ajoute tous les éléments de l̲
l.extend([33, b])              #│   à la fin de l̲, ajoute les éléments 33 et b̲
l.insert() # bad               #│   dans l̲, insère quelque chose de mal défini
l.insert(b, 42)                #│   à la position b̲ de l̲, insère 42
l.remove(42)                   #│   de l̲, retire 42
                               #│   
l.pop()                        #│   de l̲, retire le dernier élément
                               #│   
l.pop(3)                       #│   de l̲, retire l'élément à la position 3
                               #│   
l.clear()                      #│   supprime tous les éléments de l̲
                               #│   
l.index() # bad                #│   la position dans l̲ d’un élément mal défini
l.index(42)                    #│   la position dans l̲ de 42
l.index(42, a)                 #│   la position dans l̲ de 42 (à partir de la position a̲)
l.index(42, a, a+3)            #│   la position dans l̲ de 42 (entre la position a̲ et la position la somme de a̲ et 3)
                               #│   
l.count(30)                    #│   le nombre d’occurrences dans l̲ de 30
                               #│   
l.sort()                       #│   trie l̲
                               #│   
l.reverse()                    #│   inverse l’ordre des éléments de l̲
                               #│   
l2 = l.copy()                  #│   dans l̲2̲, stocke une copie de l̲
                               #│   
nums: set[int] = {} # wrong    #│   dans n̲u̲m̲s̲, prévu pour un ensemble de nombres entiers,
                               #│   │     └╴ stocke un dictionnaire vide
                               #│   
nums = {1,2,*l[:3],4}          #│   dans n̲u̲m̲s̲, stocke un ensemble avec les éléments 1, 2, ⟨les 3 premiers éléments de l̲⟩ et 4
                               #│   
nums = set()                   #│   dans n̲u̲m̲s̲, stocke un ensemble vide
                               #│   
nums.add(42)                   #│   dans n̲u̲m̲s̲, inclus 42