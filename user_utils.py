# user utils
import yaml


with open("replies.yaml", encoding="utf-8") as f:
    replies = yaml.safe_load(f)


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
