from collections import UserDict
from .Record import Record
from datetime import datetime, timedelta
from helpers.constants import format
from helpers.json_converter import to_json

class AddressBook(UserDict):
    def add_record(self, rec:Record):
        self.data[rec.name.value] = rec

    def find(self, name:str) -> Record:
        return self.data.get(name)

    def get_upcoming_birthdays(self) -> list[dict]:
        today = datetime.today().date()
        # for test
        # today = datetime.strptime("22.01.2024", format).date()
        next_week = today + timedelta(days=6)
        greatings = []
        for rec in self.data.values():
            birth_date = rec.birthday.value
            birthday_this_year = datetime(year=today.year, month=birth_date.month, day=birth_date.day).date()
            if (birthday_this_year < today or birthday_this_year > next_week):
                continue
            birthday_this_year_weekday = birthday_this_year.weekday()
            if (birthday_this_year_weekday == 5):
                #if its saturday, move greatings to monday
                greatings_day = (birthday_this_year + timedelta(days=2)).strftime(format)
            elif (birthday_this_year_weekday == 6):
                #if its sunday, move greatings to monday
                greatings_day = (birthday_this_year + timedelta(days=1)).strftime(format)
            else:
                greatings_day = birthday_this_year.strftime(format)
            greatings.append({"name": rec.name.value, "congratulation_date": greatings_day})
        return greatings

    def __getstate__(self):
        attributes = self.__dict__
        return attributes

    def __setstate__(self, state):
        self.__dict__ = state

    def to_json(self):
        return to_json(self.data)

    @classmethod
    def from_json(cls, json_dict: dict):
        book = cls()
        for rec_info in json_dict.values():
            record = Record.from_json(rec_info)
            if record:
                book.add_record(record)
        return book