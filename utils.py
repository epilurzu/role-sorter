from constant import THRESHOLD

import re
import glob
import sys
import json

#Merge dictionaries and sum values of common keys in list
def merge_dict(dict1, dict2):
   dict3 = {**dict1, **dict2}
   for key, value in dict3.items():
       if key in dict1 and key in dict2:
               dict3[key] = value + dict1[key]
 
   return dict3


def print_dict(d):
    for key, value in sorted(d.items()):
        print("\t{}\t{}".format(value, key))


def delete_unicode(string):
    string = string.replace(u'\u200c', '')
    string = string.replace(u'\u200e', '')
    string = string.replace(u'\u2013', '')
    string = string.replace(u'\u2014', '')

    return string


def cyrillic_to_english(string):
    cyrillic_alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    english_alphabet = "ABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"

    for i in range(0, len(cyrillic_alphabet)):
        if cyrillic_alphabet[i] in string:
            string = string.replace(cyrillic_alphabet[i], english_alphabet[i])

    return string


def normalize(string):

    string = delete_unicode(string)  # remove weird unicodes
    string = string.upper()  # all uppercase
    string = cyrillic_to_english(string)  # convert cyrillic
    #string = re.sub("[^ A-Z]+", "", string)  # remove all special chars and numbers
    #string = [re.sub(r"\b[A-Z]\b", "", string) # remove single char
    string = string.strip()  # remove useless spaces
    string = re.sub("\s+", " ", string)  # multiple spaces as one

    return string


def split_strings_by_separators(string_list, separators):
    new_string_list = []

    for string in string_list:
        new_string_list = new_string_list + string.split(separators[0])

    if len(separators) > 1:
        return split_strings_by_separators(new_string_list, separators[1:])

    return new_string_list


def string_to_list(normalized_string):

    string_list = [normalized_string]
    separators = [" ", ",", " AND ", "&", "/", "\\", "-"]

    string_list = split_strings_by_separators(string_list, separators) # various splits
    string_list = " ".join(string_list).split()   #remove empty strings from list
    strins_list = "".join(string_list).split()    #remove empty strings from list

    return string_list


def get_threshold(n):
    keys = list(THRESHOLD.keys())

    for i in range(0, len(keys) - 1):
        if n == keys[i] or n > keys[i]:
            if n < keys[i + 1]:
                return THRESHOLD[keys[i]]
    
    
    return THRESHOLD[keys[-1]]


def progress(count, total):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + ' ' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s\r' % (bar, percents, '%'))
    sys.stdout.flush()


def create_uncertain_csv():
    dir = "data/parsed/"
    files = []

    for file in glob.glob(dir + "*UNCERTAIN_*.json"):
        files.append(file)

    people = []

    for file in files:
        with open(file, 'r') as f:
                people += json.load(f)["people"]

    roles = dict()

    for person in people:
        for position in person["positions"]:
            for role in position["roles"]:
                if not role in roles:
                    roles[role] = 0
                roles[role] += 1

    with open(dir + "UNCERTAIN.csv", 'w') as f:
        for role, count in sorted(roles.items(), key=lambda item: item[1], reverse=True):
            f.write("%s,%s\n"%(count, role))
