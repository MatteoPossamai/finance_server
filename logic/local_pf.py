import csv
import os
from typing import List
from model.record import RecordType, Record, Expense, Income
from logic.dropbox import DropBoxManager

BASE_DOWNLOAD_DIR = os.getenv("BASE_DOWNLOAD_DIR")
DROPBOX_DIR = os.getenv("DROPBOX_DIR")
ENV=os.getenv("ENV", "dev")

def upload_updates(file_name: str):
    def decorator(function):
        def wrapper(*args, **kwargs):
            result = function()
            if ENV != "test":
                dm = DropBoxManager()
                success = dm.upload_file(file_name)
                if not success:
                    return success
            return result

        return wrapper

    return decorator


def get_remote(file_name: str):
    def decorator(function):
        def wrapper(*args, **kwargs):
            if ENV != "test":
                dm = DropBoxManager()
                success = dm.download_file(file_name)
                if not success:
                    return success
            return function()

        return wrapper

    return decorator


#  --- Local File management ---
def read_from_file(file_path: str, record_type: RecordType = RecordType.Expense) -> List[Record]:
    res = []
    with open(file_path, "r", newline="", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        _ = next(reader)  # Skip the header
        for row in reader:
            record: Record = record_type.value(*row)
            res.append(record)
    return res


def write_to_file(file_path: str, data: List[Record]):
    with open(file_path, "w+", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        header = [f.name for f in data[0].header]
        writer.writerow(header)

        for record in data:
            writer.writerow(record.to_list())


def _get_file(file_name: str, type):
    try:
        return read_from_file(f"{BASE_DOWNLOAD_DIR}/{file_name}", type)

    except FileExistsError:
        return read_from_file(f"{BASE_DOWNLOAD_DIR}/{file_name}")


def get_expense_data() -> list:
    DROPBOX_EXPENSES_FILE_NAME = os.getenv("DROPBOX_EXPENSES_FILE_NAME")
    return _get_file(DROPBOX_EXPENSES_FILE_NAME, RecordType.Expense)


def get_income_data() -> list:
    DROPBOX_INCOMES_FILE_NAME = os.getenv("INCOMES_FILE_NAME")
    return _get_file(DROPBOX_INCOMES_FILE_NAME, RecordType.Income)


@get_remote(os.getenv("DROPBOX_EXPENSES_FILE_NAME"))
def refresh_expense_data() -> bool:
    print("EXPENSES REFRESH COMPLETED")


@upload_updates(os.getenv("DROPBOX_EXPENSES_FILE_NAME"))
def remove_expense(id: int) -> bool:
    DROPBOX_EXPENSES_FILE_NAME = os.getenv("DROPBOX_EXPENSES_FILE_NAME")
    expenses = read_from_file(
        f"{BASE_DOWNLOAD_DIR}/{DROPBOX_EXPENSES_FILE_NAME}", RecordType.Expense
    )
    updated_expenses = [expense for expense in expenses if int(expense.id) != id]

    if len(expenses) == len(updated_expenses):
        return False

    write_to_file(f"{BASE_DOWNLOAD_DIR}/{DROPBOX_EXPENSES_FILE_NAME}", updated_expenses)
    return True


@upload_updates(os.getenv("DROPBOX_EXPENSES_FILE_NAME"))
def modify_expense(id: int, expense: Expense) -> bool:
    DROPBOX_EXPENSES_FILE_NAME = os.getenv("DROPBOX_EXPENSES_FILE_NAME")
    expenses = read_from_file(
        f"{BASE_DOWNLOAD_DIR}/{DROPBOX_EXPENSES_FILE_NAME}", RecordType.Expense
    )
    updated = False

    for i, existing_expense in enumerate(expenses):
        if int(existing_expense.id) == id:
            expenses[i] = expense
            updated = True
            break

    if not updated:
        return False

    write_to_file(f"{BASE_DOWNLOAD_DIR}/{DROPBOX_EXPENSES_FILE_NAME}", expenses)
    return updated


@upload_updates(os.getenv("DROPBOX_EXPENSES_FILE_NAME"))
def create_expense(expense: Expense) -> bool:
    DROPBOX_EXPENSES_FILE_NAME = os.getenv("DROPBOX_EXPENSES_FILE_NAME")
    expenses = read_from_file(
        f"{BASE_DOWNLOAD_DIR}/{DROPBOX_EXPENSES_FILE_NAME}", RecordType.Expense
    )
    num_exp = len(expenses)
    expense.id = num_exp
    expenses.append(expense)

    write_to_file(f"{BASE_DOWNLOAD_DIR}/{DROPBOX_EXPENSES_FILE_NAME}", expenses)
    return True


@get_remote(os.getenv("DROPBOX_INCOMES_FILE_NAME"))
def refresh_income_data() -> bool:
    print("INCOMESS REFRESH COMPLETED")


@upload_updates(os.getenv("DROPBOX_INCOMES_FILE_NAME"))
def remove_income(id: int) -> bool:
    DROPBOX_INCOMES_FILE_NAME = os.getenv("DROPBOX_INCOMES_FILE_NAME")
    incomes = read_from_file(f"{BASE_DOWNLOAD_DIR}/{DROPBOX_INCOMES_FILE_NAME}", RecordType.Income)
    updated_incomes = [income for income in incomes if int(income.id) != id]

    if len(incomes) == len(updated_incomes):
        return False

    write_to_file(f"{BASE_DOWNLOAD_DIR}/{DROPBOX_INCOMES_FILE_NAME}", updated_incomes)
    return True


@upload_updates(os.getenv("DROPBOX_INCOMES_FILE_NAME"))
def modify_income(id: int, income: Income) -> bool:
    DROPBOX_INCOMES_FILE_NAME = os.getenv("DROPBOX_INCOMES_FILE_NAME")
    incomes = read_from_file(f"{BASE_DOWNLOAD_DIR}/{DROPBOX_INCOMES_FILE_NAME}", RecordType.Income)
    updated = False

    for i, existing_incomes in enumerate(incomes):
        if int(existing_incomes.id) == id:
            incomes[i] = income
            updated = True
            break

    if not updated:
        return False

    write_to_file(f"{BASE_DOWNLOAD_DIR}/{DROPBOX_INCOMES_FILE_NAME}", incomes)
    return updated


@upload_updates(os.getenv("DROPBOX_INCOMES_FILE_NAME"))
def create_income(income: Income) -> bool:
    DROPBOX_INCOMES_FILE_NAME = os.getenv("DROPBOX_INCOMES_FILE_NAME")
    incomes = read_from_file(f"{BASE_DOWNLOAD_DIR}/{DROPBOX_INCOMES_FILE_NAME}", RecordType.Income)
    num_exp = len(incomes)
    income.id = num_exp
    incomes.append(income)

    write_to_file(f"{BASE_DOWNLOAD_DIR}/{DROPBOX_INCOMES_FILE_NAME}", incomes)
    return True


def get_expense(id: int) -> Expense:
    return get_expense_data()[id]


def get_income(id: int) -> Income:
    return get_income_data()[id]
