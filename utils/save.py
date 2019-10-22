from .parse import *
import pandas as pd

def write_list_to_file(path_to_file, lines):
    df = pd.DataFrame(lines, columns=["Roles"])
    df.to_csv(path_to_file, index=False)


def write_dict_to_file(path_to_file, dict):
    df = pd.DataFrame(list(dict.items()), columns=['Roles','Occurrences'])
    df.to_csv(path_to_file, index=False)


def populate_csv_files(icos, path_to_files):
    list_of_roles = get_list_of_roles(icos)
    set_of_roles = get_set_of_roles(list_of_roles)
    dict_of_roles = get_dict_of_roles(list_of_roles, set_of_roles)
    rank_of_roles = dict_to_rank(dict_of_roles)

    write_list_to_file(path_to_files + "list_of_roles.csv", list_of_roles)
    write_list_to_file(path_to_files + "set_of_roles.csv", set_of_roles)
    write_dict_to_file(path_to_files + "dict_of_roles.csv", dict_of_roles)
    write_list_to_file(path_to_files + "rank_of_roles.csv", rank_of_roles)  #Todo: separate with commas. Is this file useful though?
