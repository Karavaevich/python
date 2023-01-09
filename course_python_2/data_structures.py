"""
# easy fill list
li = [x + 2 for x in range(10) if x % 2 != 0]
print(li)

li = [x ** 2 if x % 2 == 0 else x ** 3 for x in range(10)]
print(li)

li = [[x, y] for x in range(1, 5) for y in range(5, 1, -1) if x != y]
print(li[1][1])

        li.append(e)  # complexity O(1)
        li.insert(2, e)    # complexity O(n)
"""

from collections import namedtuple
Tup = ('')
print(t.__sizeof__())
