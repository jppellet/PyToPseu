"""
Code                            │   Interpretation
——————————————————————————————————————————————————————————————————
"""                            #│
import typing  # │   we'll use the module t̲ypi̲n̲g

                               #│   
l: list[int] = []              #│   in l̲, intended for a list of integer numbers, store an empty list
l = [1, 2, 3]                  #│   in l̲, store a list with items 1, 2 and 3
ll: list[list[int]] = []       #│   in l̲l̲, intended for a list of lists of integer numbers,
                               #│   │     └╴ store an empty list
                               #│   
l: int = list()                #│   in l̲, intended for an integer number, store an empty list
                               #│   
l: typing.List[str] = 3        #│   in l̲, intended for a list of strings, store 3
d: dict[str, list[str]] = {}   #│   in d̲, intended for a dict linking strings to lists of strings,
                               #│   │     └╴ store an empty dictionary
                               #│   
l.append(42)                   #│   at the end of l̲, append 42
l.extend(l)                    #│   at the end of l̲, append all elements of l̲
l.extend([33, b])              #│   at the end of l̲, append elements 33 and b̲
l.insert() # bad               #│   in l̲, insert something badly defined
l.insert(b, 42)                #│   at position b̲ in l̲, insert 42
l.remove(42)                   #│   from l̲, remove 42
                               #│   
l.pop()                        #│   from l̲, remove the last item
                               #│   
l.pop(3)                       #│   from l̲, remove the item at position 3
                               #│   
l.clear()                      #│   remove all elements of l̲
                               #│   
l.index() # bad                #│   the position in l̲ of an undefined item
l.index(42)                    #│   the position in l̲ of 42
l.index(42, a)                 #│   the position in l̲ of 42 (starting at position a̲)
l.index(42, a, a+3)            #│   the position in l̲ of 42 (between position a̲ and position the sum of a̲ and 3)
                               #│   
l.count(30)                    #│   the number of occurrences in l̲ of 30
                               #│   
l.sort()                       #│   sort l̲
                               #│   
l.reverse()                    #│   reverse the order of the items of l̲
                               #│   
l2 = l.copy()                  #│   in l̲2̲, store a copy of l̲
                               #│   
nums: set[int] = {} # wrong    #│   in n̲u̲m̲s̲, intended for a set of integer numbers, store an empty dictionary
                               #│   
nums = {1,2,*l[:3],4}          #│   in n̲u̲m̲s̲, store a set with items 1, 2, ⟨the 3 first elements of l̲⟩ and 4
                               #│   
nums = set()                   #│   in n̲u̲m̲s̲, store an empty set
                               #│   
nums.add(42)                   #│   in n̲u̲m̲s̲, add 42