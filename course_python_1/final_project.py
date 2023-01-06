# read original file with wrong values and without emails
# write incorrect lines to another file
# create new file with only correct values

from course_python_1.files import create_new_file_with_emails as imported_create_new_file_with_emails
from course_python_1.imports import create_password as imported_create_password
import re


def fill_list_of_lines_from_all_file(file_name):
    '''
    fill list_of_lines from file
    '''
    file = open(file_name, "r")
    list_of_lines_from_file = []
    for line in file:
        line = line.replace("\n", "")
        list_of_lines_from_file.append(line.split(","))
    file.close()
    return list_of_lines_from_file


def is_line_valid(list_of_lines):
    for value in list_of_lines:
        if re.findall(r"^$", value):
            return False
        if re.findall(r"^[a-z]", value):
            return False
        if re.findall(r"[A-Z]$", value):
            return False
    return True


def create_new_files_with_sorted_values(name_all, name_good, name_bad):
    list_of_lines = fill_list_of_lines_from_all_file(name_all)
    list_of_bad_lines = [list_of_lines[0]]
    list_of_good_lines = [list_of_lines[0]]

    i = 1
    while i < len(list_of_lines) - 1:  # creates two new lists
        if is_line_valid(list_of_lines[i]):
            list_of_good_lines.append(list_of_lines[i])
        else:
            list_of_bad_lines.append(list_of_lines[i])
        i += 1

    header = True
    for line in list_of_good_lines:  # append passwords
        if header:
            line.append("PASSWORD")
            header = False
        else:
            line.append(imported_create_password())

    result_file_object_bad = open(name_bad, "w")
    for line in list_of_bad_lines: # fill bad file
        i = 0
        for element in line:
            if i != len(line) - 1:
                result_file_object_bad.write(element + ", ")
            else:
                result_file_object_bad.write(element + "\n")
            i += 1
    result_file_object_bad.close()

    result_file_object_good = open(name_good, "w")
    for line in list_of_good_lines:  # fill bad file
        i = 0
        for element in line:
            if i != len(line) - 1:
                result_file_object_good.write(element + ", ")
            else:
                result_file_object_good.write(element + "\n")
            i += 1
    result_file_object_good.close()


task_file = "course_python_1/files_task_file.txt"
result_file_all = "course_python_1/final_project_result_all.csv"
result_file_good = "course_python_1/final_project_result_good.csv"
result_file_bad = "course_python_1/final_project_result_bad.csv"

imported_create_new_file_with_emails(task_file, result_file_all)
create_new_files_with_sorted_values(result_file_all, result_file_good, result_file_bad)
