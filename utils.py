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


def split_strings_by_separators(string_list, separators):
    new_list = []

    for string in string_list:
        new_list = new_list + string.split(separators[0])

    if len(separators) > 1:
        new_list = new_list + split_strings_by_separators(new_list, separators[1:])

    return new_list


# string_to_list splits different string to list like this:
# ""1# Advisor & 2# ceo"" ---> ["ADVISOR", "CEO"]
def string_to_list(string):

    string = normalize(string)

    string_list = [string]
    separators = [",", " AND ", "&", "/", "\\"]

    string_list = split_strings_by_separators(string_list, separators)# various splits
    string_list = [re.sub("[^ A-Z]+", "", string_list) for string_list in string_list]  # remove all special chars and numbers
    string_list = [re.sub(r"\b[A-Z]\b", "", string_list) for string_list in string_list] # remove single char
    string_list = [string_list.strip() for string_list in string_list]  # remove useless spaces
    string_list = [re.sub("\s+", " ", string_list) for string_list in string_list]  # multiple spaces as one

    return string_list