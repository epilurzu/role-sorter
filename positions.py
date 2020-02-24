from ico import Ico
from role import Role

class Positions:

    def __init__(self):
        self.positions = []
        
    def add(self, ico_name, ico_token, ico_url, role_name):
        ico = Ico(ico_name, ico_token, ico_url)
        role = Role(role_name)

        self.positions.append((ico, role))

    def is_empty(self):
        return len(self.positions) == 0

    def count(self):
        return len(self.positions)

    def get_count_people_by_role_name(self):
        count_people_by_role_name = dict()

        for position in self.positions:
            role = position[1].name

            if role not in count_people_by_role_name:
                count_people_by_role_name[role] = 0
            
            count_people_by_role_name[role] += 1
        
        return count_people_by_role_name

    def get_data(self):
        data_list = []

        for position in self.positions:
            data = dict()

            ico = position[0]
            role = position[1]

            data["ico"] = ico.name
            data["token"] = ico.token
            data["url"] = ico.url
            data["role"] = role.name

            data_list.append(data)

        return data_list

            

