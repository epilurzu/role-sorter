import json
import re
from urllib.parse import unquote

class Social:

    def __init__(self, socials):
        self.socials = Social.normalize(socials)

    def get_socials(self):
        return self.socials

    def update(self, socials):
        self.socials = self.socials|Social.normalize(socials)

    @staticmethod
    def __base_normalize(social,template):
        if not social.endswith("/"):
            social = social+"/"

        base_regex = r".*?tps?.*?/@?(?P<username>[a-z0-9_\.]+)[/?]"
        id_regex = r".*?tps?.*(facebook|)/(?P<username>profile.php\?id=[0-9]*)/"

        match = re.search(id_regex,social)
        if match is not None:
            username = match.group("username")
            return template.format(username)

        match = re.search(base_regex,social)
        if match is not None:
            username = match.group("username")
            return template.format(username)

        return None

    @staticmethod
    def __normalize_linkedin(social):
        prefix = ""
        username = ""
        linkedin_regex = r".*?tps?.*linkedin.*?/(?P<prefix>in|company|pub|profile|showcase)/(?P<username>[^/]*)/?"
        linkedin_fault_regex = r"https?://(www\.)?linkedin.com/(?P<username>[a-z0-9]+?)/?"

        if re.match(linkedin_regex,social):
            match = re.search(linkedin_regex,social)
            prefix = match.group("prefix")
            username = match.group("username")

        elif re.match(linkedin_fault_regex,social):
            match = re.search(linkedin_fault_regex,social)
            username = match.group("username")
            prefix = "in"

        if prefix != "" and username != "":
            return "https://www.linkedin.com/{0}/{1}/".format(prefix,username)

        return None

    @staticmethod
    def __normalize_twitter(social):
        return Social.__base_normalize(social,"https://twitter.com/{0}")

    @staticmethod
    def __normalize_facebook(social):
        return Social.__base_normalize(social,"https://www.facebook.com/{0}")

    @staticmethod
    def __normalize_instagram(social):
        return Social.__base_normalize(social,"https://instagram.com/{0}")

    @staticmethod
    def __normalize_telegram(social):
        return Social.__base_normalize(social, "https://t.me/{0}")

    @staticmethod
    def __normalize_github(social):
        return Social.__base_normalize(social, "https://github.com/{0}")

    @staticmethod
    def __normalize_vk(social):
        return Social.__base_normalize(social, "https://vk.com/{0}")

    __blacklist = [
        "https://www.linkedin.com/",
        "https://www.linkedin.com/in/"
    ]

    @staticmethod
    def __normalize_url(url):
        url = url.strip()
        url = url.lower()
        url = url.replace(" ","")
        url = url.replace("%20","")
        return url

    @staticmethod
    def normalize(socials):

        normalized_socials = set()
        
        for social in socials:
            if social in Social.__blacklist:
                continue

            social = Social.__normalize_url(social)

            rec_regex = r".*?tps?.*(twitter|facebook|instagram|linkedin|t\.me|github|vk).*?/.*"
            match = re.search(rec_regex,social)

            if match is not None:
                website = match.group(1)
                if "twitter" in website:
                    normalized_socials.add(Social.__normalize_twitter(social))
                    continue

                if "facebook" in website:
                    normalized_socials.add(Social.__normalize_facebook(social))
                    continue
                
                if "instagram" in website:
                    normalized_socials.add(Social.__normalize_instagram(social))
                    continue
                
                if "linkedin" in website:
                    normalized_socials.add(Social.__normalize_linkedin(social))
                    continue
                
                if "t.me" in website:
                    normalized_socials.add(Social.__normalize_telegram(social))
                    continue
                
                if "github" in website:
                    normalized_socials.add(Social.__normalize_github(social))
                    continue
                
                if "vk" in website:
                    normalized_socials.add(Social.__normalize_vk(social))
                    continue
                
            else:
                normalized_socials.add(social)
                
        return normalized_socials

    #Social.match must receve normalized socials
    @staticmethod
    def match(socials1, socials2):
        if not socials1 and not socials2:
            return True 

        for s1 in socials1:
            for s2 in socials2:
                if s1 == s2:
                    return True
        
        return False
