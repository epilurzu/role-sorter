from ico import Ico
from role import Role

class Positions:

    def __init__(self):
        self.positions = []
        
    def add(self, ico_name, ico_token, ico_url, role_name):
        ico = Ico(ico_name, ico_token, ico_url)
        role = Role(role_name)

        self.positions.append((ico, role))

    def count(self):
        return len(self.positions)

    def get_count_roles_by_role(self):
        count_roles_by_role = dict()

        for position in self.positions:
            role = position[1].name

            if role not in count_roles_by_role:
                count_roles_by_role[role] = 0
            
            count_roles_by_role[role] += 1
        
        return count_roles_by_role
