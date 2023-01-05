# third symbol
s = "Abraсadabra"
print(s[2])

# pre last symbol
s = "Abraсadabra"
l = len(s)
print(s[l-2])

# first five symbols
s = "Abraсadabra"
print(s[:5])

# first five symbols
s = "Abraсadabra"
l = len(s)
print(s[:l-2])

# evem index symbols
s = "Abraсadabra"
ind = 0
for ch in s:
    if ind % 2 == 0:
        print(ch, end="")
    ind += 1

# odd index symbols
s = "Abraсadabra"
ind = 0
for ch in s:
    if not ind % 2 == 0:
        print(ch, end="")
    ind += 1

# print chars in reverse order
s = "Abraсadabra"
ind = len(s)-1
while ind >= 0:
    print(s[ind], end="")
    ind -= 1

# print chars in reverse order through one
s = "Abraсadabra"
ind = len(s)-1
pr = True
while ind >= 0:
    if pr:
        print(s[ind], end="")
    ind -= 1
    pr = not pr

# capitalize every word
s = "a1 2b  3   abc d3e r2D2"
a = s.split(" ")
for w in a:
    print(w.capitalize(), end=" ")


# capitalize every word
s = "a1 2b  3   abc d3e r2D2"
a = s.split(" ")
for w in a:
    print(w.capitalize(), end=" ")

# check password
pas = "@PowerRangers123@"
allwd_num = "1234567890"
allwd_let_low = "abcdefghijklmnopqrstuvwxyz"
allwd_let_upp = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
allwd_spec = "!@#$%^&*()-+"
cnt_glb = 0
cnt_num = 0
cnt_let_low = 0
cnt_let_upp = 0
cnt_spec = 0

for ch in pas:

    for n in allwd_num:
        if ch == n:
            cnt_num += 1
            cnt_glb += 1

    for ll in allwd_let_low:
        if ch == ll:
            cnt_let_low += 1
            cnt_glb += 1

    for lu in allwd_let_upp:
        if ch == lu:
            cnt_let_upp += 1
            cnt_glb += 1

    for sp in allwd_spec:
        if ch == sp:
            cnt_spec += 1
            cnt_glb += 1

length_ok = len(pas) >= 12
numbers_ok = cnt_num > 0
low_letters_ok = cnt_let_low > 0
upper_letters_ok = cnt_let_upp > 0
spec_symbols_ok = cnt_spec > 0
all_symbols_allowed = cnt_glb == len(pas)

if not length_ok:
    print("BAD: password length less than 12")

if not numbers_ok:
    print("BAD: numbers required")

if not low_letters_ok:
    print("BAD: letters in lower case required")

if not upper_letters_ok:
    print("BAD: letters in upper case required")

if not spec_symbols_ok:
    print("BAD: spec symbols required")

if not all_symbols_allowed:
    print("BAD: password has unallowed symbols")

if length_ok and numbers_ok and low_letters_ok and upper_letters_ok and spec_symbols_ok and all_symbols_allowed:
    print("GOOD")
