import json
import time


def delete_unicode(string):
    string = string.replace(u'\u200c', '')
    string = string.replace(u'\u200e', '')
    string = string.replace(u'\u2013', '')  # todo: this?

    return string


def cyrillic_to_english(string):
    cyrillic_alphabet = "АВЕЅZІКМНОРСТХШѴУ"
    english_alphabet = "ABESZIKMHOPCTXWVY"

    for i in range(0, len(cyrillic_alphabet)):
        if cyrillic_alphabet[i] in string:
            string = string.replace(cyrillic_alphabet[i], english_alphabet[i])

    return string


def split_strings_in_list(list, split_char):
    new_list = []

    for string in list:
        new_list = new_list + string.split(split_char)

    return new_list


# this function splits different roles from string to list
# ""Advisor & ceo"" ---> ["ADVISOR", "CEO"]
def string_to_list(string):
    roles = []

    string = string[1:-1]  # remove double quotes
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
    n_people = 0

    for ico in icos:
        team = ico['team']

        for person in team:
            string = json.dumps(person['role'], ensure_ascii=False)  # convert unicodes
            list_of_roles = list_of_roles + string_to_list(string)
            n_people = n_people + 1

    return sorted(list_of_roles)


def get_set_of_roles(icos, list_of_roles):
    set_of_roles = set([])

    for role in list_of_roles:
        set_of_roles.add(role)

    return sorted(set_of_roles)


def get_dict_of_roles(icos, list_of_roles, set_of_roles):
    dict_of_roles = {}

    for role in set_of_roles:
        dict_of_roles[role] = 0

    for role in list_of_roles:
        dict_of_roles[role] += 1

    return dict_of_roles


with open('2019-09-19/ICOBench_ended_2019-09-19.json', 'r') as file:
    icos = json.load(file)

with open('2019-09-19/ICOBench_ongoing_2019-09-19.json', 'r') as file:
    icos = icos + json.load(file)

with open('2019-09-19/ICOBench_upcoming_2019-09-19.json', 'r') as file:
    icos = icos + json.load(file)

t0= time.clock()
list_of_roles = get_list_of_roles(icos)
print("End get_list_of_roles in ", time.clock() - t0, " s\n")

t0= time.clock()
set_of_roles = get_set_of_roles(icos, list_of_roles)
print("End get_set_of_roles in ", time.clock() - t0, " s\n")

t0= time.clock()
dict_of_roles = get_dict_of_roles(icos, list_of_roles, set_of_roles)
print("End get_dict_of_roles in ", time.clock() - t0, " s\n")

rank_of_roles = sorted(dict_of_roles.items(), reverse=True, key=lambda x: x[1])
with open('rank_of_roles_v01.txt', 'w') as file:
    for tuple in rank_of_roles:
        line = str(tuple[1]) + " " + tuple[0] + "\n"
        file.write(line)
