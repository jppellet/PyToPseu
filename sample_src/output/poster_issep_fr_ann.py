"""
Code                                   │   Interprétation
————————————————————————————————————————————————————————————————————————————————
"""                                   #│
                                      #│   
                                      #│   
side = 4                              #│   dans s̲i̲d̲e̲, stocke 4
side: int = 4                         #│   dans s̲i̲d̲e̲, prévu pour un nombre entier, stocke 4
                                      #│   
area: int                             #│   on prépare a̲r̲e̲a̲ pour y stocker un nombre entier
area = side * side                    #│   dans a̲r̲e̲a̲, stocke le produit s̲i̲d̲e̲ × s̲i̲d̲e̲
                                      #│   
side += 2                             #│   ajoute 2 à s̲i̲d̲e̲
side = side + 2                       #│   ajoute 2 à s̲i̲d̲e̲
                                      #│   
val = math.sqrt(area)                 #│   dans v̲a̲l̲, stocke la racine carrée de a̲r̲e̲a̲
length = len(text)                    #│   dans l̲e̲n̲gt̲h̲, stocke la longueur de t̲e̲x̲t̲
                                      #│   
a[i] = 2                              #│   dans à la position i̲ de a̲, stocke 2
                                      #│   
if age >= 18:                         #│   si a̲ge̲ est plus grand que ou égal à 18:
  print("you can drive")              #│   │   affiche "you can drive"
                                      #│   
if value is None:                     #│   si v̲a̲l̲u̲e̲ est vide:
  print("missing")                    #│   │   affiche "missing"
                                      #│   
if 0 <= index < 10:                   #│   si i̲n̲d̲e̲x̲ est entre 0 (inclusif) et 10 (exclusif):
  print("index is valid")             #│   │   affiche "index is valid"
                                      #│   
                                      #│   
text: str = "programming"             #│   dans t̲e̲x̲t̲, prévu pour une chaîne de caractères, stocke "programming"
                                      #│   
cond1 = "gr" in text                  #│   dans c̲o̲n̲d̲1̲, stocke vrai/faux selon si "gr" fait partie de t̲e̲x̲t̲
cond2 = text == text.upper()          #│   dans c̲o̲n̲d̲2̲, stocke vrai/faux selon si t̲e̲x̲t̲ est égal à une copie tout en majuscules de t̲e̲x̲t̲
                                      #│   
if cond1:                             #│   si c̲o̲n̲d̲1̲ est vrai:
  if not cond2:                       #│   │   si c̲o̲n̲d̲2̲ est faux:
    print("cond1 && !cond2")          #│   │   │   affiche "cond1 && !cond2"
                                      #│   
                                      #│   
                                      #│   
                                      #│   
                                      #│   
                                      #│   
                                      #│   
ng = 0                                #│   dans n̲g, stocke 0
for i in range(len(text)):            #│   répète autant de fois qu’il y a d’éléments dans t̲e̲x̲t̲
                                      #│   │     └╴ (en comptant avec i̲ à partir de 0):
  if text[i] == "g":                  #│   │   si le i̲ᵉ élément de t̲e̲x̲t̲ est égal à "g":
    ng += 1                           #│   │   │   ajoute 1 à n̲g
                                      #│   
                                      #│   
ng = 0                                #│   dans n̲g, stocke 0
for c in text:                        #│   répète pour chaque élément de t̲e̲x̲t̲ (qu'on va appeler c̲):
  if c == "g":                        #│   │   si c̲ est égal à "g":
    ng += 1                           #│   │   │   ajoute 1 à n̲g
                                      #│   
for c in len(text):                   #│   répète pour chaque élément de la longueur de t̲e̲x̲t̲ (qu'on va appeler c̲):
  print(c)                            #│   │   affiche c̲
                                      #│   
n = 0                                 #│   dans n̲, stocke 0
for i in range(5):                    #│   répète 5 fois (en comptant avec i̲ à partir de 0):
  n += i                              #│   │   ajoute i̲ à n̲
                                      #│   
for _ in range(5):                    #│   répète 5 fois
  print("hello")                      #│   │   affiche "hello"
                                      #│   
for i, c in enumerate(text):          #│   répète pour chaque élément de t̲e̲x̲t̲
                                      #│   │     └╴ (qu'on va appeler c̲ et numéroter i̲ depuis 0):
  print(f"at pos {i}, we have {c}")   #│   │   affiche l’expansion de 'at pos {i}, we have {c}'
                                      #│   
                                      #│   
