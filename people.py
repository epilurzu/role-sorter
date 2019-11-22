from person import Person

class People:

    def __init__(self, icos):
        self.people = self._get_people_from_icos(icos)
        
    def _get_people_from_icos(self, icos):
        people = []

        for ico in icos:
            ico_name = ico["name"]
            ico_token = ico["token"]
            ico_url = ico["url"]

            team = ico["team"]
            for employee in team:
                person_name = employee["name"]
                person_socials = employee["socials"]
                person_role = employee["role"]

                people.append(Person(person_name, person_socials, ico_name, ico_token, ico_url, person_role))

        return people

    def print(self):
        for person in self.people:
            person.print_info()