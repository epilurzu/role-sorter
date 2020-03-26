from constant import *
from utils import normalize, string_to_list, get_threshold

import math
from Levenshtein import distance

class Role:
    
    def __init__(self, name):
        self.name = name


    @staticmethod
    def detect_roles(unclear_role):
        unclear_role = normalize(unclear_role)

        for role in ALL_ROLES:
            examples = role['examples']
            for example in examples:
                if unclear_role == example:
                    return set([role["name"]])
        
        terms = string_to_list(unclear_role)
        roles = set([])

        for term in terms:
            if term in TERMS_ROLES:
                roles = roles | set([TERMS_ROLES[term]])
        
        if roles:
            return roles

        for term in terms:
            threshold = get_threshold(len(term))
            best_fit_term = ""

            for example, role in TERMS_ROLES.items():
                dis = distance(example, term)

                if dis < threshold or dis == threshold:
                        threshold = dis
                        best_fit_term = example
            
            if best_fit_term:
                roles = roles | set([TERMS_ROLES[best_fit_term]])

        if roles:
            return roles
        
        return set(["UNCERTAIN"])
