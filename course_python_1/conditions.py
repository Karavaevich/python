# find the smallest between three numbers
num1 = input("Write first number and press Enter\n")
print("first number is: "+num1)

num2 = input("Write second number and press Enter\n")
print("second number is: "+num2)

num3 = input("Write third number and press Enter\n")
print("third number is: "+num3)

if int(num1) < int(num2):
    if int(num1) < int(num3):
        print(num1)
    else:
        print(num3)
else:
    print(num2)


# find how many equals between three numbers

num1 = input("Write first number and press Enter\n")
print("first number is: "+num1)

num2 = input("Write second number and press Enter\n")
print("second number is: "+num2)

num3 = input("Write third number and press Enter\n")
print("third number is: "+num3)

if int(num1) == int(num2) == int(num3):
    print("3")
elif int(num1) == int(num2):
    print("2")
elif int(num2) == int(num3):
    print("2")
elif int(num1) == int(num3):
    print("2")
else:
    print("0")
