from position import Position
from role import Role

class Person:

    def __init__(self, person_name, person_socials, ico_name, ico_token, ico_url, unclear_role):
        roles = Role.detect_roles(unclear_role)

        self.name = person_name
        self.socials = person_socials
        self.positions = []

        for role in roles:
            self.positions.append(Position(ico_name, ico_token, ico_url, role))

    def print_info(self):
        print("--------------------------------------------")
        print(self.name)
        

        print("\nSOCIALS")
        for social in self.socials:
            print(social)

        print("\nPOSITIONS")
        for position in self.positions:
            position.print_all()