from datetime import date
import calendar
import json
import random


class Person:
    def __init__(self, name, year, month, day, pronoun):
        self.name = name
        self.year = year
        self.month = month
        self.day = day
        self.pronoun = pronoun


today = date.today()
with open("cream_birthdays.json", "r") as f:
    people = json.loads(f.read(), object_hook=lambda d: Person(**d))


def next_birthday():
    for person in people:
        if today.month <= int(person.month) and today.day < int(person.day):
            next_birthday_age = str(today.year - int(person.year))
            next_birthday_month = str(calendar.month_name[int(person.month)])

            ordinal = "th"
            if (
                str(person.day) == "11"
                or str(person.day) == "12"
                or str(person.day) == "13"
            ):
                ordinal = "th"
            elif str(person.day)[-1] == "1":
                ordinal = "st"
            elif str(person.day)[-1] == "2":
                ordinal = "nd"
            elif str(person.day)[-1] == "3":
                ordinal = "rd"

            message = (
                "The next birthday is "
                + person.name
                + "'s, which will be on "
                + next_birthday_month
                + " "
                + person.day
                + ordinal
                + ". "
                + person.pronoun
                + " will be turning "
                + next_birthday_age
                + "."
            )
            return message
    else:
        return "No more birthdays this year! Check again next year."


def wish_birthday():
    print("This is signifying a check for a birthday today.")
    for person in people:
        if today.month == person.month and today.day == person.day:
            birthday_boy = person.name
            message = (
                "Wow @everyone! Today is our very own's "
                + birthday_boy
                + " birthday. Please wish them a happy birthday!"
            )
            return message
    return False


def list_birthdays():
    birthdays = ""
    for person in people:
        message = (
            person.name + "'s birthday is on " + person.month + "/" + person.day + ".\n"
        )
        birthdays += message
    return birthdays


def send_joke():
    lines = open("jokes.txt", encoding="utf8").read().splitlines()
    myline = random.choice(lines)
    myline = myline.replace("|", "\n",1)
    return myline


def handle_response(message: str) -> str:
    p_message = message.lower()
    if p_message == "!nextbirthday":
        return next_birthday()

    if p_message == "!help":
        return "`Beep boop I am a robo :)`"

    if "!cum" in p_message:
        return "😩💦"

    if p_message == "!checkbirthday":
        return wish_birthday()

    if p_message == "!listbirthdays":
        return list_birthdays()

    if p_message == "!joke":
        return send_joke()

    return False
