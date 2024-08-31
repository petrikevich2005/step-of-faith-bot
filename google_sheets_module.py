# google sheets module
import datetime
import os

from dotenv import load_dotenv
import gspread

import user_utils

time_reload = 10
now = datetime.datetime.now() - datetime.timedelta(minutes=time_reload)
result: str

read = load_dotenv('.env')

credentials_file = os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE')
token = os.getenv('GOOGLE_SHEETS_TOKEN')

client = gspread.service_account(filename=credentials_file)
book = client.open_by_key(token)


# write question to sheet
def write_question(question: str) -> None:
    sheet = book.get_worksheet_by_id(0)
    current_data = sheet.get_all_values()
    data = [*current_data, [question]]
    sheet.update(data)


# write feedback to sheet
def write_feedback(feedback: str) -> None:
    sheet = book.get_worksheet_by_id(1384298617)
    current_data = sheet.get_all_values()
    data = [*current_data, [feedback]]
    sheet.update(data)


# get schedule from sheet
def get_schedule() -> list:
    global result  # noqa: PLW0603
    global now  # noqa: PLW0603
    difference = datetime.datetime.now() - now
    if difference >= datetime.timedelta(minutes=time_reload):
        sheet = book.get_worksheet_by_id(72452919)
        schedule = sheet.get_all_values()
        schedule.pop(0)
        now = datetime.datetime.now()
        result = user_utils.make_schedule_text(schedule)
    return result


# write to talk with clergyman
def write_to_talk(clergyman: int, user_data: list) -> None:
    sheet = book.get_worksheet_by_id(406103439)
    current_data = sheet.get_all_values()
    data = [*current_data, user_data]
    sheet.update(data)
