"""                                 #│

Source                              #│   Interprétation

------------------------------------#│--------------------------------------

"""                                 #│

for i in range(10):                 #│   répète 10 fois (en comptant avec i̲ depuis 0):

    if i % 2 == 0 and i % 3 == 0:   #│   │   si i̲ est un nombre pair et que i̲ est un multiple de 3:

        print("fizzbuzz")           #│   │   │   affiche "fizzbuzz"

    elif i % 2 == 0:                #│   │   sinon, si i̲ est un nombre pair:

        print("fizz")               #│   │   │   affiche "fizz"

    elif i % 3 == 0:                #│   │   sinon, si i̲ est un multiple de 3:

        print("buzz")               #│   │   │   affiche "buzz"
