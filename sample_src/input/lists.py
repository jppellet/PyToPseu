import typing

l: list[int] = []
l = [1, 2, 3]
ll: list[list[int]] = []

l: int = list()

l: typing.List[str] = 3
d: dict[str, list[str]] = {}

l.append(42)
l.extend(l)
l.extend([33, b])
l.insert() # bad
l.insert(b, 42)
l.remove(42)

l.pop()

l.pop(3)

l.clear()

l.index() # bad
l.index(42)
l.index(42, a)
l.index(42, a, a+3)

l.count(30)

l.sort()

l.reverse()

l2 = l.copy()

nums: set[int] = {} # wrong

nums = {1,2,*l[:3],4}

nums = set()

nums.add(42)