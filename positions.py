from ico import Ico
from role import Role

class Positions:

    def __init__(self):
        self.positions = []
        

    def add(self, ico_name, ico_token, ico_url, role_name):
        duplicate = self.__find_duplicate(ico_url)
        
        if duplicate is not None:
            self.__add_role_to_ico(duplicate, Role(role_name))
        else:
            roles = []
            roles.append(Role(role_name))
            ico = Ico(ico_name, ico_token, ico_url)

            self.positions.append((ico, roles))


    def __find_duplicate(self, ico_url):
        for position in self.positions:
            if ico_url == position[0].url:
                return self.positions.index(position)

        return None


    def __add_role_to_ico(self, index, role):
        self.positions[index][1].append(role)
        self.__check_roles_validity(index)


    def __check_roles_validity(self, index):
        roles = set([])

        for role in self.positions[index][1][:]: # note the [:] creates a slice
            if role.name in roles:
                self.positions[index][1].remove(role)
            else:
                roles.add(role.name)

        if len(roles) > 2 and "UNCERTAIN" in roles and "UKNOWN" in roles:
            for role in self.positions[index][1][:]: # note the [:] creates a slice
                if role.name == "UNCERTAIN":
                    self.positions[index][1].remove(role)
                elif role.name == "UKNOWN":
                    self.positions[index][1].remove(role)
        elif len(roles) > 1 and ("UNCERTAIN" in roles or "UKNOWN" in roles):
            for role in self.positions[index][1][:]: # note the [:] creates a slice
                if role.name == "UNCERTAIN":
                    self.positions[index][1].remove(role)
                elif role.name == "UKNOWN":
                    self.positions[index][1].remove(role)


    def roles_check(self):
        roles = set([])

        for position in self.positions:
            for role in position[1]:
                if role.name not in roles:
                    roles.add(role.name)
        
        fixable = len(roles) == 3 and "UNCERTAIN" in roles and "UKNOWN" in roles
        fixable = fixable or (len(roles) == 2 and ("UNCERTAIN" in roles or "UKNOWN" in roles))

        if fixable:
            if "UNCERTAIN" in roles:
                roles.remove("UNCERTAIN")
            if "UKNOWN" in roles:
                roles.remove("UKNOWN")

            role_name = roles.pop()

            self.__conform_roles(role_name)


    def __conform_roles(self, role_name):
        for position in self.positions:
            roles = []
            roles.append(Role(role_name))

            position = (position[0], roles)


    def is_empty(self):
        return len(self.positions) == 0


    def get_count_roles(self):
        count = 0
        for position in self.positions:
            for role in position[1]:
                count += 1

        return count


    def get_count_people_by_role_name(self):
        count_people_by_role_name = dict()

        for position in self.positions:
            for role in position[1]:
                role_name = role.name

                if role_name not in count_people_by_role_name:
                    count_people_by_role_name[role_name] = 0
                
                count_people_by_role_name[role_name] += 1
        
        return count_people_by_role_name


    def get_data(self):
        data_list = []

        for position in self.positions:
            data = dict()

            ico = position[0]
            roles = position[1]

            role_names = []
            for role in roles:
                role_names.append(role.name)

            data["ico"] = ico.name
            data["token"] = ico.token
            data["url"] = ico.url
            data["roles"] = role_names

            data_list.append(data)

        return data_list

            

