import os
import json
import csv
# install with: pip install python-Levenshtein
from Levenshtein import distance


def delete_unicode(string):
    string = string.replace(u'\u200c', '')
    string = string.replace(u'\u200e', '')
    string = string.replace(u'\u2013', '')  # todo: this?

    return string


def cyrillic_to_english(string):
    cyrillic_alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    english_alphabet = "ABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"

    for i in range(0, len(cyrillic_alphabet)):
        if cyrillic_alphabet[i] in string:
            string = string.replace(cyrillic_alphabet[i], english_alphabet[i])

    return string


def split_strings_in_list(list, split_char):
    new_list = []

    for string in list:
        new_list = new_list + string.split(split_char)

    return new_list


# string_to_list splits different roles from string to list
# ""Advisor & ceo"" ---> ["ADVISOR", "CEO"]
def string_to_list(string):
    roles = []

    string = string.replace('"', '')  # remove double quotes
    string = string.replace('“', '')  # remove left quotes
    string = delete_unicode(string)  # remove weird unicodes
    string = string.upper()  # all uppercase
    string = cyrillic_to_english(string)  # convert cyrillic

    roles.append(string)  # from now on, various splits
    roles = split_strings_in_list(roles, ",")
    roles = split_strings_in_list(roles, " AND ")
    roles = split_strings_in_list(roles, "&")
    roles = split_strings_in_list(roles, "/")
    roles = split_strings_in_list(roles, "\\")

    roles = [role.strip() for role in roles]  # remove useless spaces
    roles = list(filter(None, roles))  # remove ""

    return roles


def get_list_of_roles(icos):
    list_of_roles = []

    for ico in icos:
        team = ico['team']

        for person in team:
            string = json.dumps(person['role'], ensure_ascii=False)  # convert unicodes
            list_of_roles = list_of_roles + string_to_list(string)

    return sorted(list_of_roles)


def get_set_of_roles(list_of_roles):
    set_of_roles = set([])

    for role in list_of_roles:
        set_of_roles.add(role)

    return sorted(set_of_roles)


def get_dict_of_roles(list_of_roles, set_of_roles):
    dict_of_roles = {}

    for role in set_of_roles:
        dict_of_roles[role] = 0

    for role in list_of_roles:
        dict_of_roles[role] += 1

    return dict_of_roles


def get_list_from_file(path_to_file):
    list = []
    with open(path_to_file, 'r') as file:
        for line in file:
            list.append(line.rstrip("\n"))

    return list


def get_set_from_file(path_to_file):
    return sorted(set(get_list_from_file(path_to_file)))


def get_dict_from_file(path_to_file):
    dict_of_roles = {}
    with open(path_to_file, 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            dict_of_roles.update({line[1]: line[0]})

    return dict_of_roles


def dict_to_rank(dict):
    rank = []

    list = sorted(dict.items(), reverse=True, key=lambda x: x[1])

    for tuple in list:
        rank.append(str(tuple[1]) + " " + tuple[0])

    return rank


def write_list_to_file(path_to_file, list_of_lines):
    with open(path_to_file, 'w') as file:
        for i in range(0, len(list_of_lines) - 1):
            line = list_of_lines[i] + "\n"
            file.write(line)
        file.write(list_of_lines[len(list_of_lines) - 1])


def write_dict_to_file(path_to_file, dict):
    with open("temp.csv", 'w') as temp_file:
        for key in dict:
            temp_file.write("%s,%s\n" % (dict[key], key))

    with open("temp.csv", 'r') as temp_file:
        data = temp_file.read()
        with open(path_to_file, 'w') as file:
            file.write(data[:-1])

    os.remove("temp.csv")


def populate_files():
    with open('2019-09-19/ICOBench_ended_2019-09-19.json', 'r') as file:
        icos = json.load(file)

    with open('2019-09-19/ICOBench_ongoing_2019-09-19.json', 'r') as file:
        icos = icos + json.load(file)

    with open('2019-09-19/ICOBench_upcoming_2019-09-19.json', 'r') as file:
        icos = icos + json.load(file)

    list_of_roles = get_list_of_roles(icos)
    set_of_roles = get_set_of_roles(list_of_roles)
    dict_of_roles = get_dict_of_roles(list_of_roles, set_of_roles)
    rank_of_roles = dict_to_rank(dict_of_roles)

    write_list_to_file("parsed_data/list_of_roles.csv", list_of_roles)
    write_list_to_file("parsed_data/set_of_roles.csv", set_of_roles)
    write_dict_to_file("parsed_data/dict_of_roles.csv", dict_of_roles)
    write_list_to_file("parsed_data/rank_of_roles.csv", rank_of_roles)


# populate_files() #when files need be created

list_of_roles = get_list_from_file("parsed_data/list_of_roles.csv")
set_of_roles = get_set_from_file("parsed_data/set_of_roles.csv")
dict_of_roles = get_dict_from_file("parsed_data/dict_of_roles.csv")
rank_of_roles = get_list_from_file("parsed_data/rank_of_roles.csv")


for s in rank_of_roles:
    print(s)


