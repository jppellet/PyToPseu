"""
Code                                   │   Interpretation
————————————————————————————————————————————————————————————————————————————————
"""                                   #│
                                      #│   
                                      #│   
side = 4                              #│   in s̲i̲d̲e̲, store 4
side: int = 4                         #│   in s̲i̲d̲e̲, intended for a an integer number, store 4
                                      #│   
area: int                             #│   prepare a̲r̲e̲a̲ to store an integer number
area = side * side                    #│   in a̲r̲e̲a̲, store the product s̲i̲d̲e̲ × s̲i̲d̲e̲
                                      #│   
side += 2                             #│   add 2 to s̲i̲d̲e̲
side = side + 2                       #│   add 2 to s̲i̲d̲e̲
                                      #│   
val = math.sqrt(area)                 #│   in v̲a̲l̲, store the square root of a̲r̲e̲a̲
length = len(text)                    #│   in l̲e̲n̲gt̲h̲, store the length of t̲e̲x̲t̲
                                      #│   
a[i] = 2                              #│   in position i̲ of a̲, store 2
                                      #│   
if age >= 18:                         #│   if a̲ge̲ is greater than or equal to 18:
  print("you can drive")              #│   │   display "you can drive"
                                      #│   
if value is None:                     #│   if v̲a̲l̲u̲e̲ is empty:
  print("missing")                    #│   │   display "missing"
                                      #│   
if 0 <= index < 10:                   #│   if i̲n̲d̲e̲x̲ is between 0 (inclusive) and 10 (exclusive):
  print("index is valid")             #│   │   display "index is valid"
                                      #│   
                                      #│   
text: str = "programming"             #│   in t̲e̲x̲t̲, intended for a a string, store "programming"
                                      #│   
cond1 = "gr" in text                  #│   in c̲o̲n̲d̲1̲, store true/false according to if "gr" is in t̲e̲x̲t̲
cond2 = text == text.upper()          #│   in c̲o̲n̲d̲2̲, store true/false according to if t̲e̲x̲t̲ is equal to an uppercase copy of t̲e̲x̲t̲
                                      #│   
if cond1:                             #│   if c̲o̲n̲d̲1̲ is true:
  if not cond2:                       #│   │   if c̲o̲n̲d̲2̲ is false:
    print("cond1 && !cond2")          #│   │   │   display "cond1 && !cond2"
                                      #│   
                                      #│   
                                      #│   
                                      #│   
                                      #│   
                                      #│   
                                      #│   
ng = 0                                #│   in n̲g, store 0
for i in range(len(text)):            #│   repeat as many times as there are elements in t̲e̲x̲t̲
                                      #│   │     └╴ (counting with i̲ from 0):
  if text[i] == "g":                  #│   │   if the i̲th element of t̲e̲x̲t̲ is equal to "g":
    ng += 1                           #│   │   │   add 1 to n̲g
                                      #│   
                                      #│   
ng = 0                        #│   in n̲g, store 0
for c in text:                #│   repeat for each item of t̲e̲x̲t̲ (which we’ll call c̲):
  if c == "g":                #│   │   if c̲ is equal to "g":
    ng += 1                   #│   │   │   add 1 to n̲g
                                      #│   
for c in len(text):                   #│   repeat for each item of the length of t̲e̲x̲t̲ (which we’ll call c̲):
  print(c)                            #│   │   display c̲
                                      #│   
n = 0                       #│   in n̲, store 0
for i in range(5):          #│   repeat 5 times (counting with i̲ from 0):
  n += i                    #│   │   add i̲ to n̲
                            #│   
for _ in range(5):          #│   repeat 5 times
  print("hello")            #│   │   display "hello"
                                      #│   
for i, c in enumerate(text):          #│   repeat for each item of t̲e̲x̲t̲
                                      #│   │     └╴ (which we’ll call c̲ and number i̲ from 0):
  print(f"at pos {i}, we have {c}")   #│   │   display the expansion of 'at pos {i}, we have {c}'
                                      #│   
                                      #│   
