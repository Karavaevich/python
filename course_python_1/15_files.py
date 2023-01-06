# var = open(<name>, <key>)
# keys:
# r - open for reading (default)
# w - open for re-writing, if not exists - open new
# x - open for writing, only when file is not exist
# a - open for writing in the end
# b - open in binary
# t - open in text (default)
# + - open for reading and writing

# example
# f_w = open("course_python_1/python_test_file.txt", "w")
# f_w.write("Hello_World\n")
# f_w.close()
#
# f_r = open("course_python_1/python_test_file.txt")
# print(f_r.read())
# f_r.close()

# fill e-mails in task_file

def is_telephone_number(input_string):
    s = str(input_string)
    try:
        if len(s) == 7:
            for ch in s:
                if not (int(ch) >= 0) & (int(ch) <= 9):
                    return False
        else:
            return False
    except ValueError as ex:
        print("WARN: skip, caught Exception while checking telephone number: ", end="")
        print(ex)
        return False
    else:
        return True


def email_gen(list_of_names):
    emails = []
    for i in list_of_names:
        letter = 1
        while i[1] + '.' + i[0][0:letter] + '@company.io' in emails:
            letter += 1
        generated_email = i[1] + '.' + i[0][0:letter] + '@company.io'
        emails.append(generated_email)
        i.append(generated_email)
    return list_of_names


def fill_list_of_lines_from_file(file_name):
    '''
    fill list_of_lines from file with removing extra chars
    '''
    file = open(file_name, "r")
    list_of_lines_from_file = []
    for line in file:
        line = line.replace(" ", "")
        line = line.replace("\n", "")
        list_of_lines_from_file.append(line.split(","))
    file.close()
    return list_of_lines_from_file


def enrich_list_of_lines(list_of_lines, list_of_names_and_surnames_with_emails):
    for line in list_of_lines:
        for subline in list_of_names_and_surnames_with_emails:
            if (line[1] == subline[0]) & (line[2] == subline[1]) & (subline[2] != "used"):
                line[0] = subline[2]
                subline[2] = "used"
                break
    return list_of_lines


def create_filled_list_with_emails(filename):
    list_of_lines = fill_list_of_lines_from_file(filename)
    list_of_names_and_surnames = []
    header = True
    for line in list_of_lines:
        name_and_surname = []
        if (header | len(line[1]) == 0) | (len(line[2]) == 0) | (not is_telephone_number(line[3])):
            continue
        name_and_surname.append(line[1])
        name_and_surname.append(line[2])
        list_of_names_and_surnames.append(name_and_surname)
        header = False

    list_of_names_and_surnames_with_emails = email_gen(list_of_names_and_surnames)
    return enrich_list_of_lines(list_of_lines, list_of_names_and_surnames_with_emails)


def create_new_file_with_emails(original_file, filled_file):
    result_list_with_emails = create_filled_list_with_emails(original_file)
    result_file_object = open(filled_file, "w")

    for line in result_list_with_emails:
        i = 0
        for element in line:
            if i != len(line) - 1:
                result_file_object.write(element + ", ")
            else:
                result_file_object.write(element + "\n")
            i += 1

    result_file_object.close()


task_file = "course_python_1/15_files_task_file.txt"
result_file = "course_python_1/15_files_task_file_result.csv"
create_new_file_with_emails(task_file, result_file)
