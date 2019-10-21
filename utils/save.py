from .parse import *
import os

def write_list_to_file(path_to_file, list_of_lines): #TODO: csv not readable, check csv write to file. also see printline/printlines
    with open(path_to_file, 'w') as file:
        for i in range(0, len(list_of_lines) - 1):
            line = list_of_lines[i] + "\n"
            file.write(line)
        file.write(list_of_lines[len(list_of_lines) - 1])


def write_dict_to_file(path_to_file, dict): #TODO: csv not readable, check csv write to file. also see printline/printlines
    with open("temp.csv", 'w') as temp_file:
        for key in dict:
            temp_file.write("%s,%s\n" % (dict[key], key))

    with open("temp.csv", 'r') as temp_file:
        data = temp_file.read()
        with open(path_to_file, 'w') as file:
            file.write(data[:-1])

    os.remove("temp.csv")

def populate_csv_files(icos, path_to_files):
    list_of_roles = get_list_of_roles(icos)
    set_of_roles = get_set_of_roles(list_of_roles)
    dict_of_roles = get_dict_of_roles(list_of_roles, set_of_roles)
    rank_of_roles = dict_to_rank(dict_of_roles)

    write_list_to_file(path_to_files + "list_of_roles.csv", list_of_roles)
    write_list_to_file(path_to_files + "set_of_roles.csv", set_of_roles)
    write_dict_to_file(path_to_files + "dict_of_roles.csv", dict_of_roles)
    write_list_to_file(path_to_files + "rank_of_roles.csv", rank_of_roles)