# google sheets module
import os

from dotenv import load_dotenv
import gspread


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
    sheet = book.get_worksheet_by_id(1)
    current_data = sheet.get_all_values()
    data = [*current_data, [feedback]]
    sheet.update(data)


# write to talk with clergyman
def write_to_talk(clergyman: int, user_data: list) -> None:
    sheet = book.get_worksheet(clergyman + 1)
    current_data = sheet.get_all_values()
    data = [*current_data, user_data]
    sheet.update(data)
