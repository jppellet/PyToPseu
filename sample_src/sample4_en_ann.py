"""
Code                              │   Interpretation
——————————————————————————————————————————————————————————————————————
"""                              #│
# OK                             #│   
s = "Examen BS11INF1"            #│   in s̲, store "Examen BS11INF1"
for loop_var in range(len(s)):   #│   repeat as many times as there are elements in s̲
                                 #│   │     └╴ (counting with l̲o̲o̲p ̲v̲a̲r̲ from 0):
    if loop_var == 1:            #│   │   if l̲o̲o̲p ̲v̲a̲r̲ is equal to 1:
        print(s[loop_var:])      #│   │   │   display the elements of s̲ starting at position l̲o̲o̲p ̲v̲a̲r̲
                                 #│   
# Not OK                         #│   
s = "Examen BS11INF1"            #│   in s̲, store "Examen BS11INF1"
for loop_var in len(s):          #│   repeat for each item of the length of s̲ (which we’ll call l̲o̲o̲p ̲v̲a̲r̲):
    if loop_var == 1:            #│   │   if l̲o̲o̲p ̲v̲a̲r̲ is equal to 1:
        print(s[loop_var:])      #│   │   │   display the elements of s̲ starting at position l̲o̲o̲p ̲v̲a̲r̲
                                 #│   
# Not OK                         #│   
s = "Examen BS11INF1"            #│   in s̲, store "Examen BS11INF1"
for loop_var in range(s):        #│   repeat s̲ times (counting with l̲o̲o̲p ̲v̲a̲r̲ from 0):
    if loop_var == 1:            #│   │   if l̲o̲o̲p ̲v̲a̲r̲ is equal to 1:
        print(s[loop_var:])      #│   │   │   display the elements of s̲ starting at position l̲o̲o̲p ̲v̲a̲r̲
                                 #│   
# Not OK                         #│   
s = "Examen BS11INF1"            #│   in s̲, store "Examen BS11INF1"
for loop_var in s:               #│   repeat for each item of s̲ (which we’ll call l̲o̲o̲p ̲v̲a̲r̲):
    if loop_var == 1:            #│   │   if l̲o̲o̲p ̲v̲a̲r̲ is equal to 1:
        print(s[loop_var:])      #│   │   │   display the elements of s̲ starting at position l̲o̲o̲p ̲v̲a̲r̲
