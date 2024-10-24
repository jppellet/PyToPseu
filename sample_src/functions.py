a = lambda: 42
a = lambda x: x + 1
a = lambda x, y: x + 1
a = lambda x, y, z: x + 1


def b() -> int:
    return 42

def b(x) -> int:
    return x + 1

def b(x, y) -> int:
    return x + 1

def b(x, y, z) -> int:
    return x + 1

def b() -> None:
    return 42

def b(x) -> None:
    return x + 1

def b(x, y) -> None:
    return x + 1

def b(x, y, z) -> None:
    return x + 1

def b():
    return 42

def b(x):
    return x + 1

def b(x, y):
    return x + 1

def b(x, y, z):
    return x + 1

def c(a: int, b: bool):
    return None