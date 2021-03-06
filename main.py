import json
from people import People
from utils import print_dict, create_uncertain_csv
import time

def analize(file_name):
    with open('data/raw/' + file_name, 'r') as file:
        icos = json.load(file)

    People.get_people_from_raw_data(icos, file_name)
    People.to_parsed_json(file_name)
    People.uncertain_roles_to_parsed_json(file_name)

    print()

    print("Count ICOs:\t{}".format(str(len(icos))))
    print("Count People:\t{}".format(People.count_people))
    print("Count Roles:\t{}".format(People.count_roles))
    print()
    print("Count people by merging names of roles:")
    print("\tPEOPLE\tROLE")
    print_dict(People.count_people_by_role_name)
    print()
    print("Count people by merging the count of roles by person:")
    print("\tPEOPLE\tROLES")
    print_dict(People.count_people_by_role_count)
    print()


def ended():
    t0 = time.time()
    analize("ICOBench_ended_2019-09-19.json")
    t1 = time.time()
    print("\nAnalysis time for ended file: %s seconds\n\n" % (t1-t0))


def ongoing():
    t0 = time.time()
    analize("ICOBench_ongoing_2019-09-19.json")
    t1 = time.time()
    print("\nAnalysis time for ongoing file: %s seconds\n\n" % (t1-t0))


def upcoming():
    t0 = time.time()
    analize("ICOBench_upcoming_2019-09-19.json")
    t1 = time.time()
    print("\nAnalysis time for upcoming file: %s seconds\n\n" % (t1-t0))


def all():
    ended()
    ongoing()
    upcoming()


choice = input("""
[1] Ended
[2] Ongoing
[3] Upcoming

[9] All the above

(data updated to 2019-09-19)
Choose the ICOBench json to analize: """)

print()

{
    "1": ended,
    "2": ongoing,
    "3": upcoming,
    "9": all
    
}[choice]()

create_uncertain_csv()

print("All UNCERTAIN roles saved in data/parsed/UNCERTAIN.csv")