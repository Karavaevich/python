# math
print(5 + 8)  # =13 sum
print(31 - 2)  # =29 diff
print(12 * 9)  # =108 multiplication
print(6 / 4)  # =1.5 divide
print(6 % 4)  # =2 remainder of the division
print(9 ** 2)  # =81 exponentiation
print(6 // 4)  # =1 integer division

# comparsion
print(5 == 5)  # =true equals
print(12 != 12)  # =false reverse result
print(53 > 23)  # =true left is more
print(5 < 51)  # =true left is less
print(5 >= 5)  # =true left is more or equal
print(32 <= 232)  # =true left is less or equal

# assignment
var = 5  # set the right value into left
var += 4  # increase left value by right
var -= 2  # reduces left value by right
var *= 10  # multiply left value by right
var /= 4  # divide left value by right
var %= 10  # remainder of the division left value by right
var **= 8  # exponentiate left value by right
var //= 30  # integer divide right value into left

# binary
var = 0 & 0  # var == 0
var = 1 & 0  # var == 0
var = 0 & 1  # var == 0
var = 1 & 1  # var == 1
var = 101 & 110  # var == 100

var = 0 | 0  # var == 0
var = 1 | 0  # var == 1
var = 0 | 1  # var == 1
var = 1 | 1  # var == 1
var = 101 | 110  # var == 111

var = 0 ^ 0  # var == 0
var = 1 ^ 0  # var == 1
var = 0 ^ 1  # var == 1
var = 1 ^ 1  # var == 0
var = 101 ^ 110  # var == 011

var = ~1  # var == -2
var = ~0  # var == -1
var = ~101  # var == -110

var = 100 >> 2  # var == 001
var = 100 << 2  # var == 10000

# logic
var = True and True  # var == True
var = True and False  # var == False
var = False and True  # var == False
var = False and False  # var == False

# including
var = 'he' in 'hello'  # var == True
var = 5 in [1, 2, 3, 4, 5]  # var == True
var = 12 not in [1, 2, 4, 56]  # var == True

# identity (the same memory objects)
a = 12
b = 12
c = a is b  # c == True
c = a is not b  # c == False

# priorities high --> low
#   -->   **
#   -->   ~
#   -->   *,/,//,%
#   -->   +,-
#   -->   |,^,&,<<,>>
#   -->   <, <=, >, >=, !=, ==
#   -->   is, not is
#   -->   or, and, not