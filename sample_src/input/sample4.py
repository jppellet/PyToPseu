# OK
s = "Examen BS11INF1"
for loop_var in range(len(s)):
    if loop_var == 1:
        print(s[loop_var:])
        
# Not OK
s = "Examen BS11INF1"
for loop_var in len(s):
    if loop_var == 1:
        print(s[loop_var:])

# Not OK
s = "Examen BS11INF1"
for loop_var in range(s):
    if loop_var == 1:
        print(s[loop_var:])

# Not OK
s = "Examen BS11INF1"
for loop_var in s:
    if loop_var == 1:
        print(s[loop_var:])
