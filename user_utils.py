# user utils
import os

from dotenv import load_dotenv
import yaml


with open("replies.yaml", encoding="utf-8") as f:
    replies = yaml.safe_load(f)

read = load_dotenv('.env')

# select username from text for ban/unban 
def select_username_from_text(text: str) -> str:
    username = []

    if len(text) > 0:
        for i in text:
            if i != " ":
                username.append(i)
            else:
                break

        return "".join(username)
    else:
        return "none"


# make schedule text
def make_schedule_text(schedule: list) -> str:
    result = [
        replies['button']['schedule']['text']['body'].format(
            time=event[0],
            event=event[1]
        ) for event in schedule
    ]
    return replies['button']['schedule']['text']['head'] + "".join(result)


# get id for counselor sheet
def get_sheet_id(counselor: int) -> None:
    if counselor == 1:
        return os.getenv('SHEET_OF_COUNSELOR_1')
    elif counselor == 2:
        return os.getenv('SHEET_OF_COUNSELOR_2')
    elif counselor == 3:
        return os.getenv('SHEET_OF_COUNSELOR_3')
    elif counselor == 4:
        return os.getenv('SHEET_OF_COUNSELOR_4')
