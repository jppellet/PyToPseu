"""
Code                                                        │   Interprétation
——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
"""                                                        #│
# OK                                                       #│   
s = "Un message arbitrairement long"                       #│   dans s̲, stocke "Un message arbitrairement long"
if len(s) % 2 == 0:                                        #│   si la longueur de s̲ est un nombre pair:
    print("s contient un nombre pair de caractères")       #│   │   affiche "s contient un nombre pair de caractères"
else:                                                      #│   sinon:
    print("s contient un nombre impair de caractères")     #│   │   affiche "s contient un nombre impair de caractères"
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
s = "Un message arbitrairement long"                       #│   dans s̲, stocke "Un message arbitrairement long"
if s % 2 == 0:                                             #│   si s̲ est un nombre pair:
    print("s contient un nombre pair de caractères")       #│   │   affiche "s contient un nombre pair de caractères"
else:                                                      #│   sinon:
    print("s contient un nombre impair de caractères")     #│   │   affiche "s contient un nombre impair de caractères"
                                                           #│   
text = ...                                                 #│   dans t̲e̲x̲t̲, stocke quelque chose à définir
                                                           #│   
if len(text) % 2 == 0:                                     #│   si la longueur de t̲e̲x̲t̲ est un nombre pair:
    print("text has an even number of characters")         #│   │   affiche "text has an even number of characters"
else:                                                      #│   sinon:
    print("text has an odd number of characters")          #│   │   affiche "text has an odd number of characters"
