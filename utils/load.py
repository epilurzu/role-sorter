import pandas as pd
import numpy as np


def get_list_from_file(path_to_file):
    df = pd.read_csv(path_to_file)
    list = df.values.tolist()

    return list


def get_set_from_file(path_to_file):
    return sorted(set(get_list_from_file(path_to_file)))


def get_dict_from_file(path_to_file):
    df = pd.read_csv(path_to_file, index_col=0, squeeze=True)
    dict = df.to_dict()

    dict[" "] = dict[np.nan]
    del dict[np.nan]

    return dict
