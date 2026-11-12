s = "bonjour"
output = ""
i = 0
while i < len(s):
    output += s[i]
    if s[i] == "o":
        i += 2
    else:
        i += 1
print(output)