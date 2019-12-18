from person import Person
from utils import merge_dict

import json

class People:

    people = []

    count_people = 0
    count_roles = 0
    count_people_by_role_name = dict()
    count_people_by_role_count = dict()

    @staticmethod
    def get_people_from_raw_data(icos):
        people = []

        print("Analyzing ICOs...")

        for ico in icos:
            ico_name = ico["name"]
            ico_token = ico["token"]
            ico_url = ico["url"]

            team = ico["team"]
            for employee in team:
                person_name = employee["name"]
                person_socials = employee["socials"]
                person_role = employee["role"]

                duplicate = Person.find_duplicate(people, person_name, person_socials)
                
                if duplicate is not None:
                    people[duplicate].update(person_socials, ico_name, ico_token, ico_url, person_role)
                else:
                    people.append(Person(person_name, person_socials, ico_name, ico_token, ico_url, person_role))

            if icos.index(ico) != 0 and (icos.index(ico) % 100) == 0:
                print("{} ICOs analyzed out of {}".format(str(icos.index(ico)), str(len(icos))))

        print("Done.\n")

        People.people = people

        People.count_people = len(People.people)
        People.count_roles = People.__get_count_roles()
        People.count_people_by_role_name = People.__get_count_people_by_role_name()
        People.count_people_by_role_count = People.__get_count_people_by_role_count()

    @staticmethod
    def __get_count_roles():
        count_roles = 0

        for person in People.people:
            count_roles += person.get_count_roles()

        return count_roles

    
    def __get_count_people_by_role_name():
        count_people_by_role_name = dict()

        for person in People.people:
            count_people_by_role_name = merge_dict(count_people_by_role_name, person.get_count_people_by_role_name())
        
        return count_people_by_role_name

    def __get_count_people_by_role_count():
        count_people_by_role_count = dict()

        for person in People.people:
            count_roles = person.get_count_roles()

            if count_roles not in count_people_by_role_count:
                count_people_by_role_count[count_roles] = 0
            
            count_people_by_role_count[count_roles] += 1
        
        return count_people_by_role_count

    def to_parsed_json(file_name):
        data = dict()
        data["people"] = []

        for person in People.people:
            data["people"].append(person.get_data())

        with open('data/parsed/' + file_name, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        print("Data saved in {}\n".format('data/parsed' + file_name))
