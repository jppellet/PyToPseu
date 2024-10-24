"""                              #│

Source                           #│   Interprétation

---------------------------------#│-----------------------------------

"""                              #│

# OK                             #│   

s = "bonjour"                    #│   dans s̲, stocke "bonjour"

for loop_var in s:               #│   pour chaque élément de s̲ (qu'on va appeler l̲o̲o̲p ̲v̲a̲r̲):

    if loop_var in "aeiou":      #│   │   si l̲o̲o̲p ̲v̲a̲r̲ fait partie de "aeiou":

        print(loop_var)          #│   │   │   affiche l̲o̲o̲p ̲v̲a̲r̲

                                 #│   

# not OK                         #│   

s = "bonjour"                    #│   dans s̲, stocke "bonjour"

for loop_var in range(s):        #│   répète s̲ fois (en comptant avec l̲o̲o̲p ̲v̲a̲r̲ depuis 0):

    if loop_var in "aeiou":      #│   │   si l̲o̲o̲p ̲v̲a̲r̲ fait partie de "aeiou":

        print(loop_var)          #│   │   │   affiche l̲o̲o̲p ̲v̲a̲r̲

                                 #│   

# not OK                         #│   

s = "bonjour"                    #│   dans s̲, stocke "bonjour"

for loop_var in range(len(s)):   #│   répète autant de fois qu'il y a d'éléments dans s̲

                                 #│   │     └╴ (en comptant avec l̲o̲o̲p ̲v̲a̲r̲ depuis 0):

    if loop_var in "aeiou":      #│   │   si l̲o̲o̲p ̲v̲a̲r̲ fait partie de "aeiou":

        print(loop_var)          #│   │   │   affiche l̲o̲o̲p ̲v̲a̲r̲

                                 #│   

# not OK                         #│   

s = "bonjour"                    #│   dans s̲, stocke "bonjour"

for loop_var in len(s):          #│   pour chaque élément de la longueur de s̲ (qu'on va appeler l̲o̲o̲p ̲v̲a̲r̲):

    if loop_var in "aeiou":      #│   │   si l̲o̲o̲p ̲v̲a̲r̲ fait partie de "aeiou":

        print(loop_var)          #│   │   │   affiche l̲o̲o̲p ̲v̲a̲r̲
