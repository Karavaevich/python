# print how many uniq elements in list
l = [1, 2, 3, 2, 1]
s = set(l)
print(len(s))

# print how many common numbers in two lists
l_1 = [1, 10, 223, 413, 2]
l_2 = [2, 40, 12, 100, 10]

s_1 = set(l_1)
s_2 = set(l_2)
s_intersect = s_1.intersection(s_2)

print(len(s_intersect))

# fist set is subset of second but not equal
s_1 = {1, 2, 3, 4, 5, 6, 7}
s_2 = {10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0}

print(s_1.issubset(s_2) & (s_1 != s_2))