import datetime
import calendar
import json
import random

class Person:
    def __init__(self, name, date, pronouns):
        self.name = name
        self.date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        self.pronouns = pronouns
    
today = datetime.date.today()
with open("data/cream_birthdays.json", "r") as f:
    people = json.loads(f.read(), object_hook=lambda d: Person(**d))

def next_birthday_spitter(person, next_year = False):
    next_age = today.year - person.date.year + int(next_year)
    birthmonth = str(calendar.month_name[int(person.date.month)])
    ordinal = "th"
    if person.date.day not in {11, 12, 13}:
        if str(person.date.day)[-1] == "1":
            ordinal = "st"
        elif str(person.date.day)[-1] == "2":
            ordinal = "nd"
        elif str(person.date.day)[-1] == "3":
            ordinal = "rd"
    return f"The next birthday is {person.name}'s, which will be on {birthmonth} {person.date.day}{ordinal}. {person.pronouns[0].capitalize()} will be turning {next_age}."


def next_birthday():
    for person in people:
        this_date = datetime.date(today.year, person.date.month, person.date.day)
        if today < this_date:
            return next_birthday_spitter(person)
    else:
        return next_birthday_spitter(people[0], True)


def wish_birthday():
    print("This is signifying a check for a birthday today.")
    for person in people:
        if today.strftime("%m-%d") == person.date.strftime("%m-%d"):
            return f"Wow @everyone! Today is our very own {person.name}'s birthday. Please wish {person.pronouns[1]} a very happy birthday!"
    return False


def list_birthdays():
    birthdays = []
    for person in people:
        birthdays.append(f"{person.name}: {person.date.month}/{person.date.day}")
    return "\n".join(birthdays)


def send_joke():
    lines = open("data/jokes.txt", encoding="utf8").read().splitlines()
    myline = random.choice(lines)
    myline = myline.replace("|", "\n",1)
    return myline


def handle_response(message: str) -> str:
    p_message = message.lower()
    if p_message == "!nextbirthday":
        return next_birthday()

    if p_message == "!checkbirthday":
        return wish_birthday()

    if p_message == "!listbirthdays":
        return list_birthdays()

    if p_message == "!joke":
        return send_joke()

    return False
