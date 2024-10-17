# OK
s = "bonjour"
for loop_var in s:
    if loop_var in "aeiou":
        print(loop_var)

# not OK
s = "bonjour"
for loop_var in range(s):
    if loop_var in "aeiou":
        print(loop_var)

# not OK
s = "bonjour"
for loop_var in range(len(s)):
    if loop_var in "aeiou":
        print(loop_var)

# not OK
s = "bonjour"
for loop_var in len(s):
    if loop_var in "aeiou":
        print(loop_var)