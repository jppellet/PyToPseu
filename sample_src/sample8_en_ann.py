"""
Code                                             │   Interpretation
————————————————————————————————————————————————————————————————————————————————————————————————————
"""                                             #│
n = 10                                          #│   in n̲, store 10
for i in range(9):                              #│   repeat 9 times (counting with i̲ from 0):
    print(i)                                    #│   │   display i̲
                                                #│   
for i in range(n):                              #│   repeat n̲ times (counting with i̲ from 0):
    print(i)                                    #│   │   display i̲
                                                #│   
for i in range(n + n*2):                        #│   repeat ⟨the sum of n̲ and ⟨the product n̲ × 2⟩⟩ times (counting with i̲ from 0):
    print(i)                                    #│   │   display i̲
                                                #│   
for i in n:                                     #│   repeat for each item of n̲ (which we’ll call i̲):
    print(i)                                    #│   │   display i̲
                                                #│   
for i in range(len(n)):                         #│   repeat as many times as there are elements in n̲
                                                #│   │     └╴ (counting with i̲ from 0):
    print(i)                                    #│   │   display i̲
                                                #│   
for i in range(len("word")):                    #│   repeat as many times as there are elements in "word"
                                                #│   │     └╴ (counting with i̲ from 0):
    print(i)                                    #│   │   display i̲
                                                #│   
                                                #│   
                                                #│   
# (a)                                           #│   
word = "Hello"                                  #│   in w̲o̲r̲d̲, store "Hello"
for i in range(len(word)):                      #│   repeat as many times as there are elements in w̲o̲r̲d̲
                                                #│   │     └╴ (counting with i̲ from 0):
    print(i, word[i])                           #│   │   display i̲ and the i̲th element of w̲o̲r̲d̲
                                                #│   
# (b)                                           #│   
word = "Hello"                                  #│   in w̲o̲r̲d̲, store "Hello"
i = 0                                           #│   in i̲, store 0
for char in word:                               #│   repeat for each item of w̲o̲r̲d̲ (which we’ll call c̲h̲a̲r̲):
    print(i, char)                              #│   │   display i̲ and c̲h̲a̲r̲
                                                #│   
# (c)                                           #│   
word = "Hello"                                  #│   in w̲o̲r̲d̲, store "Hello"
for i, char in enumerate(word):                 #│   repeat for each item of w̲o̲r̲d̲
                                                #│   │     └╴ (which we’ll call c̲h̲a̲r̲ and number i̲ from 0):
    print(i, char)                              #│   │   display i̲ and c̲h̲a̲r̲
                                                #│   
# (d)                                           #│   
word = "Hello"                                  #│   in w̲o̲r̲d̲, store "Hello"
i = 0                                           #│   in i̲, store 0
while i < len(word):                            #│   while i̲ is smaller than the length of w̲o̲r̲d̲:
    print(i, word[i])                           #│   │   display i̲ and the i̲th element of w̲o̲r̲d̲
    i += 1                                      #│   │   add 1 to i̲
                                                #│   
# (e)                                           #│   
                                                #│   
# %%                                            #│   
s = "Hello"                                     #│   in s̲, store "Hello"
for i, character in enumerate(range(len(s))):   #│   repeat for each item of the range from 0 to ⟨the length of s̲⟩
                                                #│   │     └╴ (which we’ll call c̲h̲a̲r̲a̲c̲t̲e̲r̲ and number i̲ from 0):
    print(i, character)                         #│   │   display i̲ and c̲h̲a̲r̲a̲c̲t̲e̲r̲
