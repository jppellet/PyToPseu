# OK
s = "Un message arbitrairement long"
if len(s) % 2 == 0:
    print("s contient un nombre pair de caractères")
else:
    print("s contient un nombre impair de caractères")

# Not OK
# s = "Un message arbitrairement long"
# if len(s) % 2 = 0:
#     print("s contient un nombre pair de caractères")
# else:
#     print("s contient un nombre impair de caractères")

# Not OK
# s = "Un message arbitrairement long"
# if s % 2 = 0:
#     print("s contient un nombre pair de caractères")
# else:
#     print("s contient un nombre impair de caractères")

# Not OK
s = "Un message arbitrairement long"
if s % 2 == 0:
    print("s contient un nombre pair de caractères")
else:
    print("s contient un nombre impair de caractères")

text = ...

if len(text) % 2 == 0:
    print("text has an even number of characters")
else:
    print("text has an odd number of characters")
