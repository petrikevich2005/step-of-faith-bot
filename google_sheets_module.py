# google sheets module
import datetime
import os

from dotenv import load_dotenv
import gspread


now = datetime.datetime.now() - datetime.timedelta(minutes=5)
schedule = []

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
    global schedule
    global now
    difference = datetime.datetime.now() - now
    if difference >= datetime.timedelta(minutes=5):
        sheet = book.get_worksheet_by_id(72452919)
        schedule = sheet.get_all_values()
        now = datetime.datetime.now()
    return schedule


# write to talk with clergyman
def write_to_talk(clergyman: int, user_data: list) -> None:
    sheet = book.get_worksheet_by_id(406103439)
    current_data = sheet.get_all_values()
    data = [*current_data, user_data]
    sheet.update(data)
