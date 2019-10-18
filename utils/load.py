import csv


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