import re

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


def normalize(string):

    string = delete_unicode(string)  # remove weird unicodes
    string = string.upper()  # all uppercase
    string = cyrillic_to_english(string)  # convert cyrillic

    return string


def split_strings_by_separators(list, separators):
    new_list = []

    for string in list:
        new_list = new_list + string.split(separators[1])

    if len(separators) > 1:
        split_strings_by_separators(new_list, separators[1:])
    return new_list


# string_to_list splits different string to list like this:
# ""1# Advisor & 2# ceo"" ---> ["ADVISOR", "CEO"]
def string_to_list(string):

    string = normalize(string)

    roles = []
    roles.append(string)
    separators = [",", " AND ", "&", "/", "\\"]

    roles = split_strings_by_separators(roles, separators)# various splits
    roles = [re.sub("[^ A-Z]+", "", role) for role in roles]  # remove all special chars and numbers
    roles = [re.sub(r"\b[A-Z]\b", "", role) for role in roles] # remove single char
    roles = [role.strip() for role in roles]  # remove useless spaces
    roles = [re.sub("\s+", " ", role) for role in roles]  # multiple spaces as one

    return roles