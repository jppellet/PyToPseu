"""
Code                         │   Interpretation
————————————————————————————————————————————————————————————
"""                         #│
x = 0                       #│   in x̲, store 0
for i in range(10):         #│   repeat 10 times (counting with i̲ from 0):
    if i % 2 == 0:          #│   │   if i̲ is an even number:
        x += 2              #│   │   │   add 2 to x̲
    if i % 3 == 0:          #│   │   if i̲ is a multiple of 3:
        x -= 3              #│   │   │   diminish x̲ by 3
print(x)                    #│   display x̲