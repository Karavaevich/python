# # example 1
# import datetime
# print(datetime.datetime.today())
#
# # example 2
# import datetime as d
# print(d.datetime.today())
#
# # example 3
# from datetime import datetime as d
# print(d.today())
#
# # example 4
# from datetime import *
# print(datetime.today())
#
# example 5
# import random as r
# print(r.randrange(10))
# print(r.randrange(10, 20))
# print(r.randrange(10, 20, 3))
# print(r.randint(0, 200))
# hello_string = "Hello"
# hello_list = ["H", "e", "l", "l", "o"]
# print(r.choice(hello_string))
# print(r.choice(hello_list))
# r.shuffle(hello_list)
# print(hello_list)
# print(r.random())

# create random password
import random as r


def create_password():
    allwd_num = "1234567890"
    allwd_let_low = "abcdefghijklmnopqrstuvwxyz"
    allwd_let_upp = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    allwd_spec = "!@#$%^&*()-+"
    allwd_list = [allwd_num, allwd_let_low, allwd_let_upp, allwd_spec]
    created_list = []
    created_password = ""

    created_list.append(r.choice(allwd_num))
    created_list.append(r.choice(allwd_let_low))
    created_list.append(r.choice(allwd_let_upp))
    created_list.append(r.choice(allwd_spec))

    i = 0
    while i <= 8:
        created_list.append(r.choice(allwd_list[r.randint(0, len(allwd_list) - 1)]))
        i += 1

    r.shuffle(created_list)
    created_password = created_password.join(created_list)

    return created_password


print(create_password())
