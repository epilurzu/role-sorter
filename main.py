import json
from people import People
from utils import print_dict

#file_name = "ICOBench_ended_2019-09-19.json"
#file_name = "ICOBench_ongoing_2019-09-19.json"
file_name = "ICOBench_upcoming_2019-09-19.json"

with open('data/raw/' + file_name, 'r') as file:
    icos = json.load(file)

People.get_people_from_raw_data(icos)
People.to_parsed_json(file_name)
People.uncertain_roles_to_parsed_json(file_name)

print("Count ICOs:\t{}".format(str(len(icos))))
print("Count People:\t{}".format(People.count_people))
print("Count Roles:\t{}".format(People.count_roles))

print("Count people by merging names of roles:")
print("\tPEOPLE\tROLE")
print_dict(People.count_people_by_role_name)

print("Count people by merging the count of roles by person:")
print("\tPEOPLE\tROLES")
print_dict(People.count_people_by_role_count)

