# print elements from list with even indexes
var = [90, 45, 3, 43]
res = []
i = 0

while i < len(var):
    if i % 2 == 0:
        res.append(var[i])
    i += 1

print(res)

# print elements which larger than previous
var = [1, 2, 3, 4, 5]
res = []
i = 0

while i < len(var):
    if i == 0:
        i += 1
        continue
    if var[i] > var[i - 1]:
        res.append(var[i])
    i += 1

print(res)

# switch the largest and smallest element in list
var = [-5, 5, 10]
i = 0
min_i = 0
max_i = 0

while i < len(var):
    if var[i] < var[min_i]:
        min_i = i
    if var[i] > var[max_i]:
        max_i = i
    i += 1

min = var[min_i]
max = var[max_i]
var[min_i] = max
var[max_i] = min

print(var)
