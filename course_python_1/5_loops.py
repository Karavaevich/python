# while
var = 1

while var <= 13:
    print(var)
    var += 1

# for
for char in 'Python':
    print(char, end=" ")

# continue
for char in "Python":
    if char == "h":
        continue
    print(char, end=" ")  # output:P y t h o n

# break
for char in "Python":
    if char == "h":
        break
    print(char, end=" ")  # output:P y t

# else
char_for_check = "a"
original_string = "Python"

for char in original_string:
    if char == char_for_check:
        break
else:
    print("character \"" + char_for_check + "\" not found")

# print sum of num array
arr_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
sum = 0

for num in arr_num:
    sum += num
print(sum)

# print number of zeros in num array
arr_num = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
cnt = 0

for num in arr_num:
    if num == 0:
        cnt += 1
if cnt == 0:
    print("zeros not found")
else:
    print("number of zeros: " + str(cnt))

# print subsequences up the given number
given_number = input("enter number\n")
i = 1

while i < int(given_number) + 1:
    j = 1
    while j < i + 1:
        print(str(j), end="")
        j += 1
    print("")
    i += 1

# print pyramid up the given number
given_number = input("enter number\n")
i = 1

while i < int(given_number) + 1:
    j = 0
    while j < int(given_number) - i:
        print(" ", end="")
        j += 1

    j = 1
    while j < i:
        print(str(j), end="")
        j += 1

    j = i
    while j > 0:
        print(str(j), end="")
        j -= 1

    j = 0
    while j < int(given_number) - i:
        print(" ", end="")
        j += 1

    print("")
    i += 1

# print rhombus up the given number
given_number = input("enter number\n")
i = 1

while i < int(given_number) + 1:  # upper part
    j = 0
    while j < int(given_number) - i:
        print(" ", end="")
        j += 1

    j = 1
    while j < i:
        print(str(j), end="")
        j += 1

    j = i
    while j > 0:
        print(str(j), end="")
        j -= 1

    j = 0
    while j < int(given_number) - i:
        print(" ", end="")
        j += 1

    print("")
    i += 1

i -= 2
while i > 0:  # bottom part
    j = int(given_number) - i
    while j > 0:
        print(" ", end="")
        j -= 1

    j = 1
    while j < i:
        print(str(j), end="")
        j += 1

    j = i
    while j > 0:
        print(str(j), end="")
        j -= 1

    j = int(given_number) - i
    while j > 0:
        print(" ", end="")
        j -= 1

    print("")
    i -= 1

# bonus - the left side of the previous rhombus
given_number = input("enter number\n")
i = 1

while i < int(given_number) + 1:  # upper part
    j = 0
    while j < int(given_number) - i:
        print(" ", end="")
        j += 1

    j = 1
    while j <= i:
        print(str(j), end="")
        j += 1

    print("")
    i += 1

i -= 2
while i >= 1:  # bottom part
    j = int(given_number) - i
    while j > 0:
        print(" ", end="")
        j -= 1

    j = 1
    while j <= i:
        print(str(j), end="")
        j += 1

    print("")
    i -= 1