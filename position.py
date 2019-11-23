from ico import Ico
from role import Role

class Position:

    def __init__(self, ico_name, ico_token, ico_url, role_name):
        self.ico = Ico(ico_name, ico_token, ico_url)
        self.role = Role(role_name)