"""                              #│
Source                           #│    Pseudocode
---------------------------------#│------------------------------------
"""                              #│
# OK                             #│    
s = "Examen BS11INF1"            #│    dans s̲, stocke "Examen BS11INF1"
for loop_var in range(len(s)):   #│    répète autant de fois qu'il y a d'éléments dans s̲
                                 #│    │     └╴ (en comptant avec l̲o̲o̲p ̲v̲a̲r̲ depuis 0):
    if loop_var == 1:            #│    │   si l̲o̲o̲p ̲v̲a̲r̲ est égal à 1:
        print(s[loop_var:])      #│    │   │   affiche les éléments de s̲ à partir de la position l̲o̲o̲p ̲v̲a̲r̲
                                 #│    
# Not OK                         #│    
s = "Examen BS11INF1"            #│    dans s̲, stocke "Examen BS11INF1"
for loop_var in len(s):          #│    pour chaque élément de la longueur de s̲ (qu'on va appeler l̲o̲o̲p ̲v̲a̲r̲):
    if loop_var == 1:            #│    │   si l̲o̲o̲p ̲v̲a̲r̲ est égal à 1:
        print(s[loop_var:])      #│    │   │   affiche les éléments de s̲ à partir de la position l̲o̲o̲p ̲v̲a̲r̲
                                 #│    
# Not OK                         #│    
s = "Examen BS11INF1"            #│    dans s̲, stocke "Examen BS11INF1"
for loop_var in range(s):        #│    répète s̲ fois (en comptant avec l̲o̲o̲p ̲v̲a̲r̲ depuis 0):
    if loop_var == 1:            #│    │   si l̲o̲o̲p ̲v̲a̲r̲ est égal à 1:
        print(s[loop_var:])      #│    │   │   affiche les éléments de s̲ à partir de la position l̲o̲o̲p ̲v̲a̲r̲
                                 #│    
# Not OK                         #│    
s = "Examen BS11INF1"            #│    dans s̲, stocke "Examen BS11INF1"
for loop_var in s:               #│    pour chaque élément de s̲ (qu'on va appeler l̲o̲o̲p ̲v̲a̲r̲):
    if loop_var == 1:            #│    │   si l̲o̲o̲p ̲v̲a̲r̲ est égal à 1:
        print(s[loop_var:])      #│    │   │   affiche les éléments de s̲ à partir de la position l̲o̲o̲p ̲v̲a̲r̲
