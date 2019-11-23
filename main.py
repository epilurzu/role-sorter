import json
from people import People

with open('data/raw_ico_json_2019-09-19/ICOBench_ended_2019-09-19.json', 'r') as file:
    icos = json.load(file)

with open('data/raw_ico_json_2019-09-19/ICOBench_ongoing_2019-09-19.json', 'r') as file:
    icos = icos + json.load(file)

with open('data/raw_ico_json_2019-09-19/ICOBench_upcoming_2019-09-19.json', 'r') as file:
    icos = icos + json.load(file)

People.get_people_from_icos(icos)

print(People.count_people)
print(People.count_roles)
