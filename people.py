from person import Person
from utils import mergeDict

class People:

    people = []

    count_people = 0
    count_roles = 0
    count_roles_by_role = dict()
    #count_positions_by_people = dict()

    @staticmethod
    def get_people_from_icos(icos):
        people = []

        print("Analyzing ICOs...")

        for ico in icos:
            ico_name = ico["name"]
            ico_token = ico["token"]
            ico_url = ico["url"]

            team = ico["team"]
            for employee in team:
                person_name = employee["name"]
                person_socials = employee["socials"]
                person_role = employee["role"]

                duplicate = Person.find_duplicate(people, person_name, person_socials)
                
                if duplicate is not None:
                    people[duplicate].update(person_socials, ico_name, ico_token, ico_url, person_role)
                else:
                    people.append(Person(person_name, person_socials, ico_name, ico_token, ico_url, person_role))

            if icos.index(ico) != 0 and (icos.index(ico) % 100) == 0:
                print("{} ICOs analyzed out of {}".format(str(icos.index(ico)), str(len(icos))))

        print("Done.\n")

        People.people = people

        People.count_people = len(People.people)
        People.count_roles = People.__get_count_roles()
        People.count_roles_by_role = People.__get_count_roles_by_role()
        #People.count_positions_by_people = People.__get_count_positions_by_people()

    @staticmethod
    def __get_count_roles():
        count_roles = 0

        for person in People.people:
            count_roles += person.get_count_roles()

        return count_roles

    
    def __get_count_roles_by_role():
        count_roles_by_role = dict()

        for person in People.people:
            count_roles_by_role = mergeDict(count_roles_by_role, person.get_count_roles_by_role())
        
        return count_roles_by_role

    #def __get_count_positions_by_people():









    #self.rank_of_role = dict
    #self.count_positions_by_people = dict

    #@staticmethod
    #def print_all():
    #    for person in People.people:
    #        print("-------------------------")
    #        print(person.name)
    #
    #        for p in person.position:
    #            print(p.) 