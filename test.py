from utils.save import *


with open('data/raw_ico_json_2019-09-19/ICOBench_ended_2019-09-19.json', 'r') as file:
    icos = json.load(file)

with open('data/raw_ico_json_2019-09-19/ICOBench_ongoing_2019-09-19.json', 'r') as file:
    icos = icos + json.load(file)

with open('data/raw_ico_json_2019-09-19/ICOBench_upcoming_2019-09-19.json', 'r') as file:
    icos = icos + json.load(file)

#populate_csv_files(icos, 'data/parsed/') #when files need be created


path_to_rank_of_roles = "data/parsed/rank_of_roles.csv"
path_to_template_file = "data/templates/roles_template.json"
is_recursive = True # if True checks also substrings in the examples

json_of_roles = get_json_of_roles(path_to_rank_of_roles, path_to_template_file, is_recursive)

if is_recursive:
    path_to_json = "data/parsed/roles.json"
else:
    path_to_json = "data/parsed/roles-easy_check.json"

with open(path_to_json, 'w') as file:
    json.dump(json_of_roles, file, ensure_ascii=False, indent=4)