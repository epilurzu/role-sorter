import json
from people import People
from utils import print_dict

"""with open('data/raw_ico_json_2019-09-19/ICOBench_ended_2019-09-19.json', 'r') as file:
    icos = json.load(file)

with open('data/raw_ico_json_2019-09-19/ICOBench_ongoing_2019-09-19.json', 'r') as file:
    icos = icos + json.load(file)"""

with open('data/raw_ico_json_2019-09-19/ICOBench_upcoming_2019-09-19.json', 'r') as file:
    #icos = icos + json.load(file)
    icos = json.load(file)

People.get_people_from_icos(icos)

print("ICOs count:\t{}".format(str(len(icos))))
print("People count:\t{}".format(People.count_people))
print("Roles count:\t{}".format(People.count_roles))

print("Roles count by role:")
print_dict(People.count_roles_by_role)

