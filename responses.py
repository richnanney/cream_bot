from datetime import date
import calendar
import json
import random
import os
from person import *

today = date.today()

if os.path.exists("cream_birthdays.json"):
    with open("cream_birthdays.json", "r") as f:
        people = json.loads(f.read(), object_hook=lambda d: Person(**d))
else:
    people = {}


def next_birthday(server):
    file_name = f"{server}_birthdays.json"

    today = date.today()

    if not os.path.exists(file_name):
        with open(file_name, "w") as file:
            json.dump([], file)
    with open(file_name, "r") as file:
        data = json.load(file)

    for person in data:
        if today.month < person["month"] or (
            today.month == person["month"] and today.day < person["day"]
        ):
            next_birthday_age = str(today.year - int(person["year"]))
            next_birthday_month = str(calendar.month_name[int(person["month"])])

            ordinal = "th"
            if (
                str(person["day"]) == "11"
                or str(person["day"]) == "12"
                or str(person["day"]) == "13"
            ):
                ordinal = "th"
            elif str(person["day"])[-1] == "1":
                ordinal = "st"
            elif str(person["day"])[-1] == "2":
                ordinal = "nd"
            elif str(person["day"])[-1] == "3":
                ordinal = "rd"

            message = f"The next birthday is {person['name']}'s, which will be on {next_birthday_month} {person['day']}{ordinal}. {person['pronoun'].capitalize()} will be turning {next_birthday_age}."
            return message
    else:
        return "No more birthdays this year! Check again next year."


def wish_birthday(server):
    file_name = f"{server}_birthdays.json"

    if not os.path.exists(file_name):
        with open(file_name, "w") as file:
            json.dump([], file)
    with open(file_name, "r") as file:
        data = json.load(file)
    print(f"This is signifying a check for a birthday today in the {server} server.")
    for person in data:
        if today.month == person["month"] and today.day == person["day"]:
            message = f"Wow @everyone! Please wish our very own {person['name']} a very happy birthday! They turn {today.year - person['year']} today!"
            return message
    return False


def list_birthdays(server):
    file_name = f"{server}_birthdays.json"

    if not os.path.exists(file_name):
        with open(file_name, "w") as file:
            json.dump([], file)

    with open(file_name, "r") as file:
        data = json.load(file)

        if not data:
            return "No birthdays found in the system."

        birthday_list = []
        for birthday in data:
            name = birthday["name"].capitalize()
            date = f"{birthday['month']}/{birthday['day']}"
            birthday_list.append(f"{name}'s birthday is on {date}.")

        return "\n".join(birthday_list)


def send_joke():
    lines = open("jokes.txt", encoding="utf8").read().splitlines()
    joke = random.choice(lines)
    joke = joke.replace("|", "\n", 1)
    return joke


def add_birthday(message, server):
    birthday_list = message.split(",")

    try:
        new_person = Person(
            birthday_list[1].strip(),  # Name
            int(birthday_list[2]),  # Year
            int(birthday_list[3]),  # Month
            int(birthday_list[4]),  # Day
            birthday_list[5].strip(),  # Pronoun
        )
    except Exception as e:
        return (
            "Looks like you formatted the command wrong. Try !help to see an example."
        )

    file_name = f"{server}_birthdays.json"

    if not os.path.exists(file_name):
        with open(file_name, "w") as file:
            json.dump([], file)

    with open(file_name, "r+") as file:
        data = json.load(file)

        if is_duplicate_birthday(data, new_person.__dict__):
            return "This birthday already exists in the system."

        data.append(new_person.__dict__)
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

    sort_birthdays_by_date(server)

    return f"Okay, new birthday added. {new_person.name.strip().capitalize()}'s birthday is on {new_person.month}/{new_person.day}/{new_person.year}, and {new_person.pronoun} would turn {today.year - new_person.year} this year."


def is_duplicate_birthday(existing_birthdays, new_birthday):
    for birthday in existing_birthdays:
        if (
            birthday["name"] == new_birthday["name"]
            and birthday["year"] == new_birthday["year"]
            and birthday["month"] == new_birthday["month"]
            and birthday["day"] == new_birthday["day"]
        ):
            return True
    return False


def sort_birthdays_by_date(server):
    file_name = f"{server}_birthdays.json"

    with open(file_name, "r+") as file:
        data = json.load(file)

        sorted_data = sorted(data, key=lambda bday: (bday["month"], bday["day"]))

        file.seek(0)
        json.dump(sorted_data, file, indent=4)
        file.truncate()


def handle_response(message):
    p_message = message.content.lower()
    if p_message == "!nextbirthday":
        return next_birthday(message.guild.name)

    if p_message == "!help":
        help_message = """Welcome to CremeBot! The currently available commands are:
            **!help** : You probably know this one, since you just called it.
            **!checkbirthday** : This is a debugging tool to see if anyone's birthday is today. You're welcome to call it, I guess.
            **!nextbirthday** : Should display the next birthday this year. If there are none, currently just says so instead of checking the next year. It's on the feature list, believe me.
            **!listbirthdays** : Lists the currently saved birthdays for a server. Should be server specific.
            **!addbirthday** : Adds a birthday to the saved list of birthdays. An example of the formatting would be '!addbirthday,Richard,1998,8,6,He'
            **!joke** : Tells a joke. I stole these from the /r/3amjokes and /r/dadjokes subreddits, so they're mostly quick and clean. If you want me to add one, I'd be more than happy to."""
        return help_message

    if p_message == "!checkbirthday":
        return wish_birthday(message.guild.name)

    if p_message == "!listbirthdays":
        return list_birthdays(message.guild.name)

    if p_message == "!joke":
        return send_joke()

    if "!addbirthday" in p_message:
        return add_birthday(p_message, message.guild.name)

    return f"{p_message[1:]} is not a known command. Try using !help for a list of commands, or otherwise don't begin messages with an exclamation point if you don't want to get yelled at by the robot."
