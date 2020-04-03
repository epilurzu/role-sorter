# Role sorter

Analysis of Data scraped brom [ICOBench](icobench.com) using Python.

The main goal is to list and address to specific types various roles in right categories, to see their frequency, analyze the results and highlight possible relationships between ICO companies.

________________________________

## :paperclip: Table of Contents
- :hammer: [Install](#hammer-install)
- :video_game: [Usage](#video_game-usage)
- :page_facing_up: [License](#page_facing_up-license)
- :telephone_receiver: [Contacts](#telephone_receiver-contacts)
  - :boy: [Developers](#boy-developers)

## :hammer: Install

You must have the following packages installed on the system:
- git
- python 3.x
- Pip 3

And also the following python packages:
- [levenshtein](https://pypi.org/project/python-Levenshtein/)

Then clone the repo:

```bash
git clone https://github.com/epilurzu/role-sorter.git
cd role-sorter
```
## :video_game: Usage

Just 2 things:

1. To let the code run as it is, you need to put 3 json files in the "data/raw" folder. The files are called:

- `ICOBench_ended_2019-09-19.json`
- `ICOBench_ongoing_2019-09-19.json`
- `ICOBench_upcoming_2019-09-19.json`


Each file have to include at least this values:

```json
[
    {
        "name": "ico_name",
        "url": "https://icobench.com/ico/ico_name",
        "token": "XXXX,XXX,XXX,XXX",
        "team": [
            {
                "name": "member_name_0",
                "role": "Founder",
                "socials": [
                    "https://www.linkedin.com/in/member_name"
                ]
            },
            {
                "name": "member_name_1",
                "role": "Co-Founder",
                "socials": [
                    "https://www.linkedin.com/in/member_name_1"
                ]
            }
        ]
    }
    {
        //And again...
    }
]
```

2. Run from inside the repo dir:

```bash
python3 main.py
```

That's it!

## :page_facing_up: License
* See [LICENSE](https://github.com/epilurzu/role-sorter/blob/master/LICENSE) file.

## :telephone_receiver: Contacts
### :boy: Developers

#### epilurzu
* E-mail : e.ipodda@gmail.com
* Github : [@epilurzu](https://github.com/epilurzu)
