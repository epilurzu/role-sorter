from .load import *
import math
import re
import json
from Levenshtein import distance


def delete_unicode(string):
    string = string.replace(u'\u200c', '')
    string = string.replace(u'\u200e', '')
    string = string.replace(u'\u2013', '')

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
# ""1# Advisor & 2# ceo"" ---> ["ADVISOR", "CEO"]
def string_to_list(string):
    roles = []

    string = delete_unicode(string)  # remove weird unicodes
    string = string.upper()  # all uppercase
    string = cyrillic_to_english(string)  # convert cyrillic

    roles.append(string)  # from now on, various splits
    roles = split_strings_in_list(roles, ",")
    roles = split_strings_in_list(roles, " AND ")
    roles = split_strings_in_list(roles, "&")
    roles = split_strings_in_list(roles, "/")
    roles = split_strings_in_list(roles, "\\")

    roles = [re.sub("[^ A-Z]+", "", role) for role in roles]  # remove all special chars and numbers
    roles = [re.sub(r"\b[A-Z]\b", "", role) for role in roles] # remove single char
    roles = [role.strip() for role in roles]  # remove useless spaces
    roles = [re.sub("\s+", " ", role) for role in roles]  # multiple spaces as one
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


def dict_to_rank(dict):
    rank = []

    list = sorted(dict.items(), reverse=True, key=lambda x: x[1])

    for tuple in list:
        rank.append(str(tuple[1]) + " " + tuple[0])

    return rank


def role_to_json(json_of_roles, unallocated_workers, unallocated_role):
    min_distance = 3
    best_fit_role = ""

    for role in json_of_roles:
        if role['name'] == "UNCERTAIN":
            break

        examples = role['examples']


        for example in examples:
            dis = distance(example, unallocated_role)

            if dis < min_distance:
                min_distance = dis
                best_fit_role = role['name']

    if min_distance > 2: # unallocated_role not found in examples...
        if (' ' in unallocated_role): # ... maybe its substrings can be found...
            middle_space = (len(unallocated_role.split(" ")) - 1) / 2

            head = " ".join(unallocated_role.split(" ")[:math.ceil(middle_space)])
            json_of_roles = role_to_json(json_of_roles, unallocated_workers, head)

            tail = " ".join(unallocated_role.split(" ")[math.ceil(middle_space):])
            json_of_roles = role_to_json(json_of_roles, unallocated_workers, tail)


        else: # unallocated_role is UNCERTAIN
            role['workers'] = int(role['workers']) + unallocated_workers
            role['examples'].append(unallocated_role)

    else: # unallocated_role FOUND in examples!!!
        for role in json_of_roles:
            if role['name'] == best_fit_role:
                role['workers'] = int(role['workers']) + unallocated_workers

    return json_of_roles


def get_json_of_roles():
    rank_of_roles = get_list_from_file("parsed_data/rank_of_roles.csv")

    with open('templates/roles_template.json', 'r') as file:
        json_of_roles = json.load(file)

    for undefined_role in rank_of_roles:
        unallocated_workers = int(undefined_role.split(" ", 1)[0])
        unallocated_role = undefined_role.split(" ", 1)[1]

        json_of_roles = role_to_json(json_of_roles, unallocated_workers, unallocated_role)

    return json_of_roles