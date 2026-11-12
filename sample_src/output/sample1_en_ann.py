"""
Code                          │   Interpretation
——————————————————————————————————————————————————————————————
"""                          #│
import math                  #│   we'll use the module m̲a̲t̲h̲
from sys import exit as ex   #│   we'll use the element e̲x̲i̲t̲ (calling it e̲x̲) from module s̲ys̲
                             #│   
a: int = 4                   #│   in a̲, intended for an integer number, store 4
b: float = 4 * 6             #│   in b̲, intended for a decimal number, store the product 4 × 6
a = a + 1                    #│   add 1 to a̲
a = 1 + a                    #│   add 1 to a̲
a = a - 1                    #│   subtract 1 from a̲
a = a * 2                    #│   multiply a̲ by 2
a = 2 * a                    #│   multiply a̲ by 2
a = a / 2                    #│   divide a̲ by 2
a = a // 2                   #│   divide a̲ by 2 as integer numbers
                             #│   
b = math.sqrt(a)             #│   in b̲, store the square root of a̲
                             #│   
for i in range(0, 10, 1):    #│   repeat 10 times (counting with i̲ from 0):
    print(i)                 #│   │   display i̲
    print(i)                 #│   │   display i̲
                             #│   
for c in "abc":              #│   repeat for each character in "abc" (which we’ll call c̲):
    for _ in range(5):       #│   │   repeat 5 times
        print(c)             #│   │   │   display c̲
