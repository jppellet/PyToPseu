"""
Code                          │   Interpretation
——————————————————————————————————————————————————————————————
"""                          #│
a = lambda: 42               #│   in a̲, store an anonymous function without any arguments
                             #│   │     └╴ which returns 42
a = lambda x: x ** 4         #│   in a̲, store an anonymous function which accepts one argument, x̲, and
                             #│   │     └╴ which returns x̲ to the power of 4
a = lambda x, y: x + 1       #│   in a̲, store an anonymous function which accepts 2 arguments, x̲ and y̲, and
                             #│   │     └╴ which returns the sum of x̲ and 1
a = lambda x, y, z: x + 1    #│   in a̲, store an anonymous function which accepts 3 arguments, x̲, y̲ and z̲, and
                             #│   │     └╴ which returns the sum of x̲ and 1
                             #│   
                             #│   
def b() -> int:              #│   define the function b̲, without any arguments, 
                             #│   │     └╴ which returns an integer number, like so:
    return 42                #│   │   get out of the function returning 42
                             #│   
def b(x) -> int:             #│   define the function b̲, which accepts one argument, x̲, and 
                             #│   │     └╴ which returns an integer number, like so:
    return x + 1             #│   │   get out of the function returning the sum of x̲ and 1
                             #│   
def add_abs(x, y) -> int:    #│   define the function a̲d̲d̲ ̲a̲b̲s̲, which accepts 2 arguments, 
                             #│   │     └╴ x̲ and y̲, and which returns an integer number, like so:
    return abs(x) + abs(y)   #│   │   get out of the function returning the sum of ⟨the absolute value of x̲⟩ and 
                             #│   │   │     └╴ ⟨the absolute value of y̲⟩
                             #│   
def b(x, y, z) -> int:       #│   define the function b̲, which accepts 3 arguments, x̲, y̲ and 
                             #│   │     └╴ z̲, and which returns an integer number, like so:
    return x + 1             #│   │   get out of the function returning the sum of x̲ and 1
                             #│   
def b() -> None:             #│   define the function b̲, without any arguments, 
                             #│   │     └╴ which returns nothing, like so:
    return 42                #│   │   get out of the function returning 42
                             #│   
def b(x) -> None:            #│   define the function b̲, which accepts one argument, x̲, and 
                             #│   │     └╴ which returns nothing, like so:
    return x + 1             #│   │   get out of the function returning the sum of x̲ and 1
                             #│   
def b(x, y) -> None:         #│   define the function b̲, which accepts 2 arguments, x̲ and y̲, and 
                             #│   │     └╴ which returns nothing, like so:
    return x + 1             #│   │   get out of the function returning the sum of x̲ and 1
                             #│   
def b(x, y, z) -> None:      #│   define the function b̲, which accepts 3 arguments, x̲, y̲ and 
                             #│   │     └╴ z̲, and which returns nothing, like so:
    return x + 1             #│   │   get out of the function returning the sum of x̲ and 1
                             #│   
def b():                     #│   define the function b̲, without any arguments, like so:
    return 42                #│   │   get out of the function returning 42
                             #│   
def b(x):                    #│   define the function b̲, which accepts one argument, x̲, like so:
    return x + 1             #│   │   get out of the function returning the sum of x̲ and 1
                             #│   
def b(x, y):                 #│   define the function b̲, which accepts 2 arguments, x̲ and y̲, like so:
    return x + 1             #│   │   get out of the function returning the sum of x̲ and 1
                             #│   
def b(x, y, z):              #│   define the function b̲, which accepts 3 arguments, x̲, y̲ and 
                             #│   │     └╴ z̲, like so:
    return x + 1             #│   │   get out of the function returning the sum of x̲ and 1
                             #│   
def c(a: int, b: bool):      #│   define the function c̲, which accepts 2 arguments, a̲ (an integer number) and 
                             #│   │     └╴ b̲ (a true/false value), like so:
    return None              #│   │   get out of the function returning an empty value