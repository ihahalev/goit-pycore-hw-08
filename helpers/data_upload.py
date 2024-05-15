import pickle, json
from classes import AddressBook
from .book_operations import get_all_contacts
from .wrappers import file_read_error

def save_data(book: AddressBook, filename="addressbook.pkl"):
    try:
        with open(filename, "wb") as f:
            pickle.dump(book, f)
            # for testing json
            # raise
    except Exception as error:
        print(f"Error occured on create file, {type(error)}, {error}")
        print(get_all_contacts(book))
        fallback = input("Fallback to JSON (Y/N): ")
        if fallback.upper() == "Y":
            json_file = filename.split(".")[0]+'.json'
            try:
                json_data = book.to_json()
                with open(json_file, "w") as f:
                    json.dump(json_data, f)
            except Exception as error:
                print(f"Error occured on create file, {type(error)}, {error}")

def load_data(filename="addressbook.pkl"):
    book = load_binary_data(filename)
    if not book:
        print("Trying fallback json")
        json_file = filename.split(".")[0]+'.json'
        json_book = load_json_data(json_file)
        if not json_book:
            book = AddressBook()
        else:
            book = AddressBook.from_json(json_book)
    return book

@file_read_error
def load_binary_data(filename="addressbook.pkl"):
    with open(filename, "rb") as f:
        return pickle.load(f)

@file_read_error
def load_json_data(filename="addressbook.json"):
    with open(filename, "r") as f:
        return json.load(f)