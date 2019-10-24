from .load import *
import math
import re
import json
from Levenshtein import distance

############################ utils ############################


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


def split_strings_by_char(list, split_char):
    new_list = []

    for string in list:
        new_list = new_list + string.split(split_char)

    return new_list


def normalize(string):

    string = delete_unicode(string)  # remove weird unicodes
    string = string.upper()  # all uppercase
    string = cyrillic_to_english(string)  # convert cyrillic

    return string

# string_to_list splits different roles from string to list
# ""1# Advisor & 2# ceo"" ---> ["ADVISOR", "CEO"]
def string_to_list(string):
    roles = []

    string = normalize(string)

    roles.append(string)  # from now on, various splits
    roles = split_strings_by_char(roles, ",")
    roles = split_strings_by_char(roles, " AND ")
    roles = split_strings_by_char(roles, "&")
    roles = split_strings_by_char(roles, "/")
    roles = split_strings_by_char(roles, "\\")

    roles = [re.sub("[^ A-Z]+", "", role) for role in roles]  # remove all special chars and numbers
    roles = [re.sub(r"\b[A-Z]\b", "", role) for role in roles] # remove single char
    roles = [role.strip() for role in roles]  # remove useless spaces
    roles = [re.sub("\s+", " ", role) for role in roles]  # multiple spaces as one

    return roles


############################ end utils ############################


############################ roles ############################


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


def role_to_json(json_of_roles, unallocated_workers, unallocated_role, is_recursive):
    min_distance = 3
    best_fit_role = ""

    for role in json_of_roles:
        examples = role['examples']

        if role['name'] == "UNCERTAIN":
            set_of_examples = set([])
            for example in examples:    #make a sorted set of UNCERTAIN before return
                set_of_examples.add(example)

            role['examples'] = sorted(set_of_examples)
            break


        for example in examples:
            dis = distance(example, unallocated_role)

            if dis < min_distance:
                min_distance = dis
                best_fit_role = role['name']

    if min_distance > 2: # unallocated_role not found in examples...
        if (' ' in unallocated_role and is_recursive): # ... maybe its substrings can be found...
            middle_space = (len(unallocated_role.split(" ")) - 1) / 2

            head = " ".join(unallocated_role.split(" ")[:math.ceil(middle_space)])
            json_of_roles = role_to_json(json_of_roles, unallocated_workers, head, is_recursive)

            tail = " ".join(unallocated_role.split(" ")[math.ceil(middle_space):])
            json_of_roles = role_to_json(json_of_roles, unallocated_workers, tail, is_recursive)


        else: # unallocated_role is UNCERTAIN
            role['workers'] = int(role['workers']) + unallocated_workers
            role['examples'].append(unallocated_role)

    else: # unallocated_role FOUND in examples!!!
        for role in json_of_roles:
            if role['name'] == best_fit_role:
                role['workers'] = int(role['workers']) + unallocated_workers

    return json_of_roles


def get_json_of_roles(path_to_dict_of_roles, path_to_template_file, is_recursive):
    dict_of_roles = get_dict_from_file(path_to_dict_of_roles)

    with open(path_to_template_file, 'r') as file:
        json_of_roles = json.load(file)

    for unallocated_role, unallocated_workers in dict_of_roles.items():

        json_of_roles = role_to_json(json_of_roles, unallocated_workers, unallocated_role, is_recursive)

    return json_of_roles


############################ end roles ############################


############################ people ############################


def socials_to_dict(socials):
    dict_of_socials = {"linkedin" : "",
                       "twitter" : "",
                       "facebook": "",
                       "instagram": "",
                       "github" : "",
                       "wikipedia" : ""
                            #,"other" : [] #Todo: check
                       }

    for social in socials:
        for key in dict_of_socials:
            if key in social and "company" not in social:
                if key == "linkedin":
                    if re.match("(in\/|pub\/|id=)(.*)", social):
                        username = re.search("(in\/|pub\/|id=)(.*)", social).group(2).split("/")[0]
                        social = "https://www.linkedin.com/in/" + username + "/"
                    else:
                        break

                dict_of_socials[key] = social

                break

    return dict_of_socials


def update_if_person_fits(person_name, person_socials, dict_of_people):
    for person, value in dict_of_people.items():
        if value[0] == person_name:
            for social, url in value[1].items():
                if url == person_socials[social]:

                    dict_of_people[person][1] = {**dict_of_people[person][1], **person_socials} # same person, merge dict_of_socials
                    new_key = hash((person_name, json.dumps(person_socials)))
                    dict_of_people[new_key] = dict_of_people[person]
                    del dict_of_people[person]

                    return dict_of_people

    return dict_of_people


def get_dict_of_people(icos):
    dict_of_people = {}

    for ico in icos:
        ico_name = ico['name']
        ico_url = ico['url']
        ico_token = ico['token']

        ico_team = ico['team']

        for person in ico_team:
            person_name = json.dumps(person['name'], ensure_ascii=False)  # convert unicodes
            person_name = normalize(person_name)
            person_name = re.sub("[^ A-Z]+", "", person_name)  # remove all special chars and numbers

            person_socials = socials_to_dict(person['socials'])

            key = hash((person_name, json.dumps(person_socials)))

            person_role = json.dumps(person['role'], ensure_ascii=False)  # convert unicodes

            dict_of_people = update_if_person_fits(person_name, person_socials, dict_of_people) # check if person exist in dict_of_people and if that's the case update it

            ico = {'name': ico_name,
                   'url': ico_url,
                   'token': ico_token,
                   'role': person_role} #Todo: specify as parsed

            if key not in dict_of_people:
                dict_of_people[key] = [person_name, person_socials, [ico]]
            elif ico not in dict_of_people[key][2]:
                dict_of_people[key][2].append(ico)

    return dict_of_people

def get_json_of_people(icos):
    dict_of_people = get_dict_of_people(icos)

    json_of_people = []

    for hash_of_person, value in dict_of_people.items():
        dict_of_person = {}

        dict_of_person['name'] = value[0]
        dict_of_person['socials'] = {k: v for k, v in value[1].items() if v is not ""}
        dict_of_person['icos'] = value[2]

        json_of_people.append(dict_of_person)

    return json_of_people


############################ end people ############################