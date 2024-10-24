"""
Code                   │   Interprétation
————————————————————————————————————————————————
"""                   #│
s = "bonjour"         #│   dans s̲, stocke "bonjour"
output = ""           #│   dans o̲u̲t̲pu̲t̲, stocke une chaîne de caractères vide
i = 0                 #│   dans i̲, stocke 0
while i < len(s):     #│   tant que i̲ est plus petit que la longueur de s̲:
    output += s[i]    #│   │   ajoute le i̲ᵉ élément de s̲ à o̲u̲t̲pu̲t̲
    if s[i] == "o":   #│   │   si le i̲ᵉ élément de s̲ est égal à "o":
        i += 2        #│   │   │   ajoute 2 à i̲
    else:             #│   │   sinon:
        i += 1        #│   │   │   ajoute 1 à i̲
print(output)         #│   affiche o̲u̲t̲pu̲t̲