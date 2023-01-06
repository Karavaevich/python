# create and print
d = dict(short='dict', long='dictionary')
print(d)

d = dict([(1, 1), (2, 4)])
print(d)

d = {}
print(d)

d = {'dict': 1, 'dictionary': 2}
print(d)

d = dict.fromkeys(['a', 'b'])
print(d)  # output: {'a': None, 'b': None}

d = dict.fromkeys(['a', 'b'], 100)
print(d)  # output: {'a': 100, 'b': 100}

d = {a: a ** 2 for a in range(7)}
print(d)  # output: {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36}

# print value by key
d = {'Hello': 'Hi', 'Bye': 'Goodbye', 'List': 'Array'}
k = input("enter key: ")
print("value: " + d.get(k))

# print key by value
d = {'Hello': 'Hi', 'Bye': 'Goodbye', 'List': 'Array'}
k = input("enter value: ")

for i in d:
    if d[i] == k:
        print(i)
        break

# how many repeats
l = ['abc', 'bcd', 'abc', 'abd', 'abd', 'dcd', 'abc']
d = {}

for s in l:
    if d.get(s) is None:
        d.update({s: 0})

for k in d:
    for s in l:
        if k == s:
            d.update({k: d[k] + 1})

for k in d:
    print(d[k], end=" ")
