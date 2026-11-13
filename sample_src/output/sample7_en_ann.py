"""
Code                         │   Interpretation
————————————————————————————————————————————————————————————
"""                         #│
s = "bonjour"               #│   in s̲, store "bonjour"
output = ""                 #│   in o̲u̲t̲pu̲t̲, store an empty string
i = 0                       #│   in i̲, store 0
while i < len(s):           #│   while i̲ is smaller than the length of s̲:
    output += s[i]          #│   │   add the i̲th element of s̲ to o̲u̲t̲pu̲t̲
    if s[i] == "o":         #│   │   if the i̲th element of s̲ is equal to "o":
        i += 2              #│   │   │   add 2 to i̲
    else:                   #│   │   else:
        i += 1              #│   │   │   add 1 to i̲
print(output)               #│   display o̲u̲t̲pu̲t̲