"""
Code                         │   Interprétation
————————————————————————————————————————————————————————————
"""                         #│
x = 0                       #│   dans x̲, stocke 0
for i in range(10):         #│   répète 10 fois (en comptant avec i̲ depuis 0):
    if i % 2 == 0:          #│   │   si i̲ est un nombre pair:
        x += 2              #│   │   │   ajoute 2 à x̲
    if i % 3 == 0:          #│   │   si i̲ est un multiple de 3:
        x -= 3              #│   │   │   diminue x̲ de 3
print(x)                    #│   affiche x̲