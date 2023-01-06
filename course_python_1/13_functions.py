# calculate expressions, for example, 1+9 , 100%, 4**, 9**3, which are given as string
def is_number(ch):
    allowed_numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    return allowed_numbers.__contains__(ch)


def is_math(ch):
    allowed_maths = ["+", "-", "/", "*", "%"]
    return allowed_maths.__contains__(ch)


def is_valid_math_expression(exp):
    s = str(exp)
    last_i = len(s) - 1
    the_last_ok = s.endswith("**") | s.endswith("%") | is_number(s[last_i])
    the_first_ok = is_number(s[0])
    result = True
    if the_first_ok & the_last_ok:
        i = 2
        while i < len(s):
            curr = s[i]
            prev = s[i - 1]
            prev_prev = s[i - 2]
            if is_math(curr) & is_math(prev):
                if (not (curr == "*") & (prev == "*")) | ((curr == "*") & (prev == "*") & (prev_prev == "*")):
                    print("not allowed serial math symbols")
                    result = False
                    break
            i += 1
    else:
        print("first or last character are invalid")
        result = False
    return result


def all_characters_allowed(string):
    i = 0
    result = True
    while i < len(input_string):
        if not is_number(input_string[i]) | is_math(input_string[i]):
            print("wrong character: " + input_string[i])
            result = False
            break
        i += 1
    return result


def this_is_valid_expression(str):
    if all_characters_allowed(str) & is_valid_math_expression(str):
        return True
    else:
        return False


def separate_nums_and_maths_into_lists(input_string_orig):
    str_from_input = input_string_orig
    numbers_from_input = []
    maths_from_input = []

    while str_from_input != "":

        if len(str_from_input) != 0:
            if is_number(str_from_input[0]):

                num_list = []
                i = 0
                while (len(str_from_input) != 0) & (i < len(str_from_input)):
                    if not is_number(str_from_input[i]):
                        break
                    num_list.append(str_from_input[i])
                    i += 1
                num = ""
                num = num.join(num_list)
                numbers_from_input.append(num)
                str_from_input = str_from_input.removeprefix(num)
                print(numbers_from_input)
                print(str_from_input)

        if len(str_from_input) != 0:
            if is_math(str_from_input[0]):

                math_list = []
                i = 0
                while (len(str_from_input) != 0) & (i < len(str_from_input)):
                    if not is_math(str_from_input[i]):
                        break
                    math_list.append(str_from_input[i])
                    i += 1
                math = ""
                math = math.join(math_list)
                maths_from_input.append(math)
                str_from_input = str_from_input.removeprefix(math)
                print(maths_from_input)
                print(str_from_input)

    return numbers_from_input, maths_from_input


input_string = "123+9+10**2"

lists = ()
if this_is_valid_expression(input_string):
    lists = separate_nums_and_maths_into_lists(input_string)

print(lists)
