from utils.save import *

with open('2019-09-19/ICOBench_ended_2019-09-19.json', 'r') as file:
    icos = json.load(file)

with open('2019-09-19/ICOBench_ongoing_2019-09-19.json', 'r') as file:
    icos = icos + json.load(file)

with open('2019-09-19/ICOBench_upcoming_2019-09-19.json', 'r') as file:
    icos = icos + json.load(file)

#populate_csv_files(icos) #when files need be created

json_of_roles = get_json_of_roles()

with open('parsed_data/roles.json', 'w') as file:
    json.dump(json_of_roles, file, ensure_ascii=False, indent=4)