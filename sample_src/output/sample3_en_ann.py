"""
Code                              │   Interpretation
——————————————————————————————————————————————————————————————————————
"""                              #│
# OK                             #│   
s = "bonjour"                    #│   in s̲, store "bonjour"
for loop_var in s:               #│   repeat for each item of s̲ (which we’ll call l̲o̲o̲p ̲v̲a̲r̲):
    if loop_var in "aeiou":      #│   │   if l̲o̲o̲p ̲v̲a̲r̲ is in "aeiou":
        print(loop_var)          #│   │   │   display l̲o̲o̲p ̲v̲a̲r̲
                                 #│   
# not OK                         #│   
s = "bonjour"                    #│   in s̲, store "bonjour"
for loop_var in range(s):        #│   repeat s̲ times (counting with l̲o̲o̲p ̲v̲a̲r̲ from 0):
    if loop_var in "aeiou":      #│   │   if l̲o̲o̲p ̲v̲a̲r̲ is in "aeiou":
        print(loop_var)          #│   │   │   display l̲o̲o̲p ̲v̲a̲r̲
                                 #│   
# not OK                         #│   
s = "bonjour"                    #│   in s̲, store "bonjour"
for loop_var in range(len(s)):   #│   repeat as many times as there are elements in s̲
                                 #│   │     └╴ (counting with l̲o̲o̲p ̲v̲a̲r̲ from 0):
    if loop_var in "aeiou":      #│   │   if l̲o̲o̲p ̲v̲a̲r̲ is in "aeiou":
        print(loop_var)          #│   │   │   display l̲o̲o̲p ̲v̲a̲r̲
                                 #│   
# not OK                         #│   
s = "bonjour"                    #│   in s̲, store "bonjour"
for loop_var in len(s):          #│   repeat for each item of the length of s̲ (which we’ll call l̲o̲o̲p ̲v̲a̲r̲):
    if loop_var in "aeiou":      #│   │   if l̲o̲o̲p ̲v̲a̲r̲ is in "aeiou":
        print(loop_var)          #│   │   │   display l̲o̲o̲p ̲v̲a̲r̲