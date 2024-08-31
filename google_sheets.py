# google sheets module
import datetime
import os

from dotenv import load_dotenv
import gspread

import user_utils


class GoogleSheets:
    def __init__(self) -> None:
        self.time_reload = 10
        self.now = datetime.datetime.now() - datetime.timedelta(minutes=self.time_reload)
        self.result: str

        self.read = load_dotenv('.env')

        self.credentials_file = os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE')
        self.token = os.getenv('GOOGLE_SHEETS_TOKEN')

        self.client = gspread.service_account(filename=self.credentials_file)
        self.book = self.client.open_by_key(self.token)


    # write question to sheet
    def write_question(self, question: str) -> None:
        sheet = self.book.get_worksheet_by_id(0)
        current_data = sheet.get_all_values()
        data = [*current_data, [question]]
        sheet.update(data)


    # write feedback to sheet
    def write_feedback(self, feedback: str) -> None:
        sheet = self.book.get_worksheet_by_id(1384298617)
        current_data = sheet.get_all_values()
        data = [*current_data, [feedback]]
        sheet.update(data)


    # get schedule from sheet
    def get_schedule(self) -> list:
        difference = datetime.datetime.now() - self.now
        if difference >= datetime.timedelta(minutes=self.time_reload):
            sheet = self.book.get_worksheet_by_id(72452919)
            schedule = sheet.get_all_values()
            schedule.pop(0)
            self.now = datetime.datetime.now()
            self.result = user_utils.make_schedule_text(schedule)
        return self.result


    # write to talk with clergyman
    def write_to_talk(self, clergyman: int, user_data: list) -> None:
        sheet = self.book.get_worksheet_by_id(406103439)
        current_data = sheet.get_all_values()
        data = [*current_data, user_data]
        sheet.update(data)
