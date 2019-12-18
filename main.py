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

print("Count ICOs:\t{}".format(str(len(icos))))
print("Count People:\t{}".format(People.count_people))
print("Count Roles:\t{}".format(People.count_roles))

print("Count people by merging names of roles:")
print("\tPEOPLE\tROLE")
print_dict(People.count_people_by_role_name)

print("Count people by merging the count of roles by person:")
print("\tPEOPLE\tROLES")
print_dict(People.count_people_by_role_count)

