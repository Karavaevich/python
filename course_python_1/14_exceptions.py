# try:
#     try_suite
# except exception_group1 as variable1:
#     except_suite1
# ...
# except exception_groupN as variableN:
#     except_suiteN
# else:
#     else_suite
# finally:
#     finally_suite

# check string is telephone number or not
def is_telephone_number(st):
    s = str(st)
    try:
        if len(s) == 7:
            for ch in s:
                if not (int(ch) >= 0) & (int(ch) <= 9):
                    return False
        else:
            return False
    except ValueError as ex:
        print("ERROR: caught Exception: ", end="")
        print(ex)
        return False
    else:
        return True


input_string = "12322r4"

if is_telephone_number(input_string):
    print(input_string + " is telephone number")
else:
    print(input_string + " is not a telephone number")
