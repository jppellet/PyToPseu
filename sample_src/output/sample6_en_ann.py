"""
Code                                 │   Interpretation
————————————————————————————————————————————————————————————————————————————
"""                                 #│
for i in range(10):                 #│   repeat 10 times (counting with i̲ from 0):
    if i % 2 == 0 and i % 3 == 0:   #│   │   if i̲ is an even number and if i̲ is a multiple of 3:
        print("fizzbuzz")           #│   │   │   display "fizzbuzz"
    elif i % 2 == 0:                #│   │   else, if i̲ is an even number:
        print("fizz")               #│   │   │   display "fizz"
    elif i % 3 == 0:                #│   │   else, if i̲ is a multiple of 3:
        print("buzz")               #│   │   │   display "buzz"
