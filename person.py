from constant import *
from positions import Positions
from social import Social
from role import Role
from utils import merge_dict

from Levenshtein import distance

class Person:

    def __init__(self, person_name, person_socials, ico_name, ico_token, ico_url, unclear_role):
        self.name = person_name
        self.socials = Social(person_socials)
        self.positions = Positions()
        self.uncertain_positions = Positions()

        roles = Role.detect_roles(unclear_role)

        for role in roles:
            self.positions.add(ico_name, ico_token, ico_url, role)

        if len(roles) == 1 and "UNCERTAIN" in roles:
            self.uncertain_positions.add(ico_name, ico_token, ico_url, unclear_role)


    @staticmethod
    def find_duplicate(people, person_name, person_socials):
        for person in people:
            name_match = distance(person.name, person_name) < MIN_DISTANCE
            if name_match:
                social_match = Social.match(person.socials.get_socials(), Social.normalize(person_socials))
                if social_match:
                    return people.index(person)

        return None


    def update(self, person_socials, ico_name, ico_token, ico_url, unclear_role):
        self.socials.update(person_socials)
        
        roles = Role.detect_roles(unclear_role)

        for role in roles:
            self.positions.add(ico_name, ico_token, ico_url, role)

        if len(roles) == 1 and "UNCERTAIN" in roles:
            self.uncertain_positions.add(ico_name, ico_token, ico_url, unclear_role)

    def roles_check(self):
        self.positions.roles_check()


    def get_count_roles(self):
        return self.positions.get_count_roles()


    def get_count_people_by_role_name(self):
        return self.positions.get_count_people_by_role_name()


    def get_data(self):
        data = dict()

        data["name"] = self.name
        data["socials"] = list(self.socials.get_socials())
        data["positions"] = self.positions.get_data()

        return data

    def has_uncertain_roles(self):
        return not self.uncertain_positions.is_empty()

    
    def get_data_uncertain_roles(self):
        data = dict()

        data["name"] = self.name
        data["socials"] = list(self.socials.get_socials())
        data["positions"] = self.uncertain_positions.get_data()

        return data