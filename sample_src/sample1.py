import math
from sys import exit as ex

a: int = 4
b: float = 4 * 6
a = a + 1
a = 1 + a
a = a - 1
a = a * 2
a = 2 * a
a = a / 2
a = a // 2

b = math.sqrt(a)

for i in range(0, 10, 1):
    print(i)
    print(i)

for c in "abc":
    for _ in range(5):
        print(c)
