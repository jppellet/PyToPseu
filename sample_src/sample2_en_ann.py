"""
Code                                                        │   Interpretation
——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
"""                                                        #│
# OK                                                       #│   
s = "Un message arbitrairement long"                       #│   in s̲, store "Un message arbitrairement long"
if len(s) % 2 == 0:                                        #│   if the length of s̲ is an even number:
    print("s contient un nombre pair de caractères")       #│   │   display "s contient un nombre pair de caractères"
else:                                                      #│   else:
    print("s contient un nombre impair de caractères")     #│   │   display "s contient un nombre impair de caractères"
                                                           #│   
# Not OK                                                   #│   
# s = "Un message arbitrairement long"                     #│   
# if len(s) % 2 = 0:                                       #│   
#     print("s contient un nombre pair de caractères")     #│   
# else:                                                    #│   
#     print("s contient un nombre impair de caractères")   #│   
                                                           #│   
# Not OK                                                   #│   
# s = "Un message arbitrairement long"                     #│   
# if s % 2 = 0:                                            #│   
#     print("s contient un nombre pair de caractères")     #│   
# else:                                                    #│   
#     print("s contient un nombre impair de caractères")   #│   
                                                           #│   
# Not OK                                                   #│   
s = "Un message arbitrairement long"                       #│   in s̲, store "Un message arbitrairement long"
if s % 2 == 0:                                             #│   if s̲ is an even number:
    print("s contient un nombre pair de caractères")       #│   │   display "s contient un nombre pair de caractères"
else:                                                      #│   else:
    print("s contient un nombre impair de caractères")     #│   │   display "s contient un nombre impair de caractères"
                                                           #│   
text = ...                                                 #│   in t̲e̲x̲t̲, store something to be defined
                                                           #│   
if len(text) % 2 == 0:                                     #│   if the length of t̲e̲x̲t̲ is an even number:
    print("text has an even number of characters")         #│   │   display "text has an even number of characters"
else:                                                      #│   else:
    print("text has an odd number of characters")          #│   │   display "text has an odd number of characters"
