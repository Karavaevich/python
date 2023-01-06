# calculate expressions, for example, 1+9 , 100%, 4**, 9**3, which are given as string
# ATTENTION! results for your expressions may be unexpected

def is_number(ch):
    allowed_numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    return allowed_numbers.__contains__(ch)


def is_math(ch):
    allowed_maths = ["+", "-", "/", "*", "%", "**"]
    return allowed_maths.__contains__(ch)


def is_valid_math_expression(exp):
    s = str(exp)
    last_i = len(s) - 1
    the_last_ok = s.endswith("**") | s.endswith("%") | is_number(s[last_i])
    the_first_ok = is_number(s[0])
    result = True

    if s.__contains__("%"):
        if s.index("%") == (len(s) - 1):
            print("INFO: percent is not in the middle of expression")
        else:
            print("ERROR: percent in the middle of expression")
            result = False

    if the_first_ok & the_last_ok:
        i = 2
        while i < len(s):
            curr = s[i]
            prev = s[i - 1]
            prev_prev = s[i - 2]
            if is_math(curr) & is_math(prev):
                if (not (curr == "*") & (prev == "*")) | ((curr == "*") & (prev == "*") & (prev_prev == "*")):
                    print("ERROR: not allowed serial math symbols")
                    result = False
                    break
            i += 1
    else:
        print("ERROR: first or last character are invalid")
        result = False
    return result


def all_characters_allowed(string):
    i = 0
    result = True
    while i < len(input_string):
        if not is_number(input_string[i]) | is_math(input_string[i]):
            print("ERROR: wrong character: " + input_string[i])
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

    return numbers_from_input, maths_from_input


def define_atomic_math_and_calculate(num1, math, num2):
    if math == "+":
        return num1 + num2
    if math == "-":
        return num1 - num2
    if math == "/":
        return num1 / num2
    if math == "*":
        return num1 * num2
    if math == "%":
        return float(num1) % num2
    if math == "**":
        return num1 ** num2


def define_atomic_math_and_calculate_without_right_number(num1, math):
    if math == "%":
        return float(num1) / 100
    if math == "**":
        return num1 ** 2


def calculate_input_string(input):
    lists = ()
    if not this_is_valid_expression(input):
        return "calculation is not successful"

    lists = separate_nums_and_maths_into_lists(input)

    numbers = list(map(int, lists[0]))
    maths = lists[1]


    i = 0
    while i != len(maths):
        if i < len(numbers) - 1:
            numbers[i + 1] = define_atomic_math_and_calculate(numbers[i], maths[i], numbers[i + 1])
        else:
            numbers[i] = define_atomic_math_and_calculate_without_right_number(numbers[i], maths[i])
        i += 1
    return str(numbers[len(numbers) - 1])


input_string = "9-1+3-5"
print("input string expression: "+input_string)
print("result: "+calculate_input_string(input_string))
