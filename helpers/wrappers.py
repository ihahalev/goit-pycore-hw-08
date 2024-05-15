import re
from classes.customErrors import ShortName, PhoneValidationError, DateFormatError

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            # get error message
            msg: str = ve.args[0]
            # if we have 'got', pattern of error will be like (expected 2, got N)
            pattern = r"got (\d)"
            got = re.search(pattern, msg)
            if got:
                is_birthday = func.__name__ == "add_birthday"
                count = got.group(1)
                # depending on N return corresponding message
                if count == '0':
                    if is_birthday:
                        return "Give me name and bithday please."
                    return "Give me name and phone please."
                elif count == '1':
                    if is_birthday:
                        return "Give me bithday please."
                    return "Give me phone please."
                elif count == '2':
                    return "Give me new phone please."
            # if we have only expected, too many entered args
            elif msg.find("expected") != -1:
                return "Too many arguments"
            # any other unexpected ValueError
            return f"{func.__name__} error, {type(ve)}, {ve}"
        except KeyError:
            return "Contact does not exist"
        except IndexError:
            return "Enter user name"
        except ShortName as name:
            return f"{name}"
        except PhoneValidationError as phone:
            return f"{phone}"
        except DateFormatError as format:
            return f"{format}"
        except Exception as error:
            return f"{func.__name__} error, {type(error)}, {error}"
    return inner

def file_read_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as error:
            print(f"File {error.filename} not found")
        except Exception as error:
            print(f"File could not be read, {type(error)}, {error}")
    return inner

