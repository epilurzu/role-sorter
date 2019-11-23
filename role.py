from constant import *
from utils import string_to_list

import math
from Levenshtein import distance

class Role:
    
    def __init__(self, name):
        self.name = name


    @staticmethod
    def detect_roles(unclear_role):

        def get_roles(unclear_role):

            best_fit_role = ""
            best_distance = MIN_DISTANCE

            for role in ROLES:
                examples = role['examples']

                for example in examples:

                    dis = distance(example, unclear_role)

                    if dis < best_distance:
                        best_distance = dis
                        best_fit_role = role['name']

            if best_distance < MIN_DISTANCE:
                return set([best_fit_role])

            elif ' ' in unclear_role:
                middle_space = (len(unclear_role.split(" ")) - 1) / 2

                head = " ".join(unclear_role.split(" ")[:math.ceil(middle_space)])
                tail = " ".join(unclear_role.split(" ")[math.ceil(middle_space):])

                return get_roles(head) | get_roles(head) 

            else:
                return set(["UNCERTAIN"])

        roles = set([])

        for role in string_to_list(unclear_role):
            roles = roles | get_roles(role)

        if len(roles) > 1 and "UNCERTAIN" in roles:
            roles.discard("UNCERTAIN")

        return roles

        

