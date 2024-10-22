n = 10
for i in range(9):
    print(i)

for i in range(n):
    print(i)

for i in range(n + n*2):
    print(i)

for i in n:
    print(i)

for i in range(len(n)):
    print(i)

for i in range(len("word")):
    print(i)



# (a)
word = "Hello"
for i in range(len(word)):
    print(i, word[i])

# (b)
word = "Hello"
i = 0
for char in word:
    print(i, char)

# (c)
word = "Hello"
for i, char in enumerate(word):
    print(i, char)

# (d)
word = "Hello"
i = 0
while i < len(word):
    print(i, word[i])
    i += 1

# (e)

# %%
s = "Hello"
for i, character in enumerate(range(len(s))):
    print(i, character)
