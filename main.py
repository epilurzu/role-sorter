import json
from person import Person

with open('data/raw_ico_json_2019-09-19/ICOBench_ended_2019-09-19.json', 'r') as file:
    icos = json.load(file)

with open('data/raw_ico_json_2019-09-19/ICOBench_ongoing_2019-09-19.json', 'r') as file:
    icos = icos + json.load(file)

with open('data/raw_ico_json_2019-09-19/ICOBench_upcoming_2019-09-19.json', 'r') as file:
    icos = icos + json.load(file)

people = []

for ico in icos:
    ico_name = ico["name"]
    ico_token = ico["token"]
    ico_url = ico["url"]

    team = ico["team"]
    for employee in team:
        person_name = employee["name"]
        person_socials = employee["socials"]
        person_role = employee["role"]

        people.append(Person(person_name, person_socials, ico_name, ico_token, ico_url, person_role))

for person in people:
    person.print_info()