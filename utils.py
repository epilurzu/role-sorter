import re
import sys

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

    return string


def split_strings_by_separators(string_list, separators):
    new_string_list = []

    for string in string_list:
        new_string_list = new_string_list + string.split(separators[0])

    if len(separators) > 1:
        return split_strings_by_separators(new_string_list, separators[1:])

    return new_string_list


# string_to_list splits different string to list like this:
# ""1# Advisor & 2# ceo"" ---> ["ADVISOR", "CEO"]
def string_to_list(string):

    string = normalize(string)

    string_list = [string]
    separators = [",", " AND ", "&", "/", "\\", "-"]

    string_list = split_strings_by_separators(string_list, separators)# various splits
    string_list = [re.sub("[^ A-Z]+", "", string_list) for string_list in string_list]  # remove all special chars and numbers
    string_list = [re.sub(r"\b[A-Z]\b", "", string_list) for string_list in string_list] # remove single char
    string_list = [string_list.strip() for string_list in string_list]  # remove useless spaces
    string_list = [re.sub("\s+", " ", string_list) for string_list in string_list]  # multiple spaces as one

    return string_list

def progress(count, total):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + ' ' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s\r' % (bar, percents, '%'))
    sys.stdout.flush()