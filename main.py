from collections import UserDict
from datetime import datetime
import pickle
import re


class Field:
    def __init__(self, value):
        self.__value = value
        self.value = value
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value
    
    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if not bool(re.match(r"\d{10}", value)) or len(value) > 10:
            raise ValueError("Incorrect phone number formatу")
        self.__value = value

class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, '%d-%m-%Y')
        except ValueError:
            raise ValueError("Birthdate must be in 'dd-mm-yyyy' format")

    def __str__(self):
        return self.__value.strftime('%d-%m-%Y')


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for i in self.phones:
            if i.value == phone:
                self.phones.remove(i)
                return
        raise ValueError

    def edit_phone(self, old_phone, new_phone):
        found = False
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                found = True
                break
        if not found:
            raise ValueError 

    def find_phone(self, phone):
        for i in self.phones:
            if i.value == phone:
                return i
        return None
    
    def days_to_birthday(self):
        if self.birthday:
            bd = self.birthday.value
            today = datetime.today().date()
            current_year_birthday = datetime(today.year, bd.month, bd.day).date()
            if current_year_birthday < today:
                current_year_birthday = datetime(today.year + 1, bd.month, bd.day).date()
            delta = current_year_birthday - today
            return delta.days
        return "The contact does not have a birthday"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, page_number):
        records = list(self.data.values())
        total_pages = len(records) // page_number + 1

        for page in range(total_pages):
            start = page * page_number
            end = start + page_number
            yield records[start:end]

    def save_address_book(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)
        print('Address book saved successfully')

    def load_address_book(self, filename):
        with open(filename, 'rb') as file:
            self.data = pickle.load(file)
        print('Address book load successfully')
        
    def search(self, word):
        found_list = []
        for record in self:
            if word in record.name:
                found_list.append(record.name)
                continue
            if record.phones:
                for phone in record.phones:
                    if word in phone:
                        found_list.append(record.name)
                        continue
        print(found_list)
