"""                                             #│

Source                                          #│   Interprétation

------------------------------------------------#│--------------------------------------------------

"""                                             #│

n = 10                                          #│   dans n̲, stocke 10

for i in range(9):                              #│   répète 9 fois (en comptant avec i̲ depuis 0):

    print(i)                                    #│   │   affiche i̲

                                                #│   

for i in range(n):                              #│   répète n̲ fois (en comptant avec i̲ depuis 0):

    print(i)                                    #│   │   affiche i̲

                                                #│   

for i in range(n + n*2):                        #│   répète ⟨la somme de n̲ et le produit n̲ × 2⟩ fois (en comptant avec i̲ depuis 0):

    print(i)                                    #│   │   affiche i̲

                                                #│   

for i in n:                                     #│   pour chaque élément de n̲ (qu'on va appeler i̲):

    print(i)                                    #│   │   affiche i̲

                                                #│   

for i in range(len(n)):                         #│   répète autant de fois qu'il y a d'éléments dans n̲

                                                #│   │     └╴ (en comptant avec i̲ depuis 0):

    print(i)                                    #│   │   affiche i̲

                                                #│   

for i in range(len("word")):                    #│   répète autant de fois qu'il y a d'éléments dans "word"

                                                #│   │     └╴ (en comptant avec i̲ depuis 0):

    print(i)                                    #│   │   affiche i̲

                                                #│   

                                                #│   

                                                #│   

# (a)                                           #│   

word = "Hello"                                  #│   dans w̲o̲r̲d̲, stocke "Hello"

for i in range(len(word)):                      #│   répète autant de fois qu'il y a d'éléments dans w̲o̲r̲d̲

                                                #│   │     └╴ (en comptant avec i̲ depuis 0):

    print(i, word[i])                           #│   │   affiche i̲ et le i̲ᵉ élément de w̲o̲r̲d̲

                                                #│   

# (b)                                           #│   

word = "Hello"                                  #│   dans w̲o̲r̲d̲, stocke "Hello"

i = 0                                           #│   dans i̲, stocke 0

for char in word:                               #│   pour chaque élément de w̲o̲r̲d̲ (qu'on va appeler c̲h̲a̲r̲):

    print(i, char)                              #│   │   affiche i̲ et c̲h̲a̲r̲

                                                #│   

# (c)                                           #│   

word = "Hello"                                  #│   dans w̲o̲r̲d̲, stocke "Hello"

for i, char in enumerate(word):                 #│   pour chaque élément de w̲o̲r̲d̲

                                                #│   │     └╴ (qu'on va appeler c̲h̲a̲r̲ et numéroter i̲ depuis 0):

    print(i, char)                              #│   │   affiche i̲ et c̲h̲a̲r̲

                                                #│   

# (d)                                           #│   

word = "Hello"                                  #│   dans w̲o̲r̲d̲, stocke "Hello"

i = 0                                           #│   dans i̲, stocke 0

while i < len(word):                            #│   tant que i̲ est plus petit que la longueur de w̲o̲r̲d̲:

    print(i, word[i])                           #│   │   affiche i̲ et le i̲ᵉ élément de w̲o̲r̲d̲

    i += 1                                      #│   │   ajoute 1 à i̲

                                                #│   

# (e)                                           #│   

                                                #│   

# %%                                            #│   

s = "Hello"                                     #│   dans s̲, stocke "Hello"

for i, character in enumerate(range(len(s))):   #│   pour chaque élément de la plage de 0 à ⟨la longueur de s̲⟩

                                                #│   │     └╴ (qu'on va appeler c̲h̲a̲r̲a̲c̲t̲e̲r̲ et numéroter i̲ depuis 0):

    print(i, character)                         #│   │   affiche i̲ et c̲h̲a̲r̲a̲c̲t̲e̲r̲
