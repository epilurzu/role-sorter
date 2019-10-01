import json

def removeUnicodeChar(s):
    s = s.replace(u'\u200c', '')
    s = s.replace(u'\u200e', '')
    s = s.replace(u'\u2013', '') #todo: this?

    return s

def cyrillic2english(s):
    toBeReplaces = "АВЕЅZІКМНОРСТХШѴУ"
    toReplace = "ABESZIKMHOPCTXWVY"

    for i in range(0,len(toBeReplaces)):
        if toBeReplaces[i] in s:
            s = s.replace(toBeReplaces[i], toReplace[i])

    return s

def removeFirstSpace(s):
    for i in range(0,len(s)):
        if s[i]!=" ":
            return s[i:]

    return ""


roles = set([])
counter = 0

with open('2019-09-19/ICOBench_ongoing_2019-09-19.json', 'r') as file:
    ICOs = json.load(file)

for ICO in ICOs:
    team = ICO['team']
    for person in team:
        role = json.dumps(person['role'], ensure_ascii=False)
        role = role[1:-1]
        role = removeUnicodeChar(role)
        role = role.upper()
        role = cyrillic2english(role)
        role = removeFirstSpace(role)

        if role!= "":
            roles.add(role)
        counter = counter + 1

roles = sorted(roles)

for role in roles:
    print(role)

print( )
print("Roles:\t" + str(len(roles)))
print("People:\t" + str(counter))

