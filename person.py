from constant import *
from positions import Positions
from social import Social
from role import Role
from utils import mergeDict

from Levenshtein import distance

class Person:

    def __init__(self, person_name, person_socials, ico_name, ico_token, ico_url, unclear_role):
        self.name = person_name
        self.socials = Social(person_socials)
        self.positions = Positions()

        roles = Role.detect_roles(unclear_role)
        for role in roles:
            self.positions.add(ico_name, ico_token, ico_url, role)


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


    def get_count_roles(self):
        return self.positions.count()


    def get_count_roles_by_role(self):
        return self.positions.get_count_roles_by_role()