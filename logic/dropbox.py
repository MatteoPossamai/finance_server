import requests
import csv
import os
from typing import List
from model.record import RecordType, Record, Expense, Income

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
DROPBOX_DOWNLOAD_URL = os.getenv("DROPBOX_DOWNLOAD_URL")
BASE_DOWNLOAD_DIR = os.getenv("BASE_DOWNLOAD_DIR")
DROPBOX_DIR = os.getenv("DROPBOX_DIR")

def dowload_dropbox_file(file: str):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Dropbox-API-Arg": f'{{"path": "{file}"}}',
    }
    try:
        response = requests.post(DROPBOX_DOWNLOAD_URL, headers=headers)
        response.raise_for_status()

        filename = file.split("/")[-1]
        with open(BASE_DOWNLOAD_DIR + filename, "wb") as file:
            file.write(response.content)

    except requests.exceptions.RequestException as e:
        print(f"Failed to download the file: {e}")


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
        dowload_dropbox_file(f"/{DROPBOX_DIR}/{file_name}")
        return read_from_file(f"{BASE_DOWNLOAD_DIR}/{file_name}")


def get_expense_data() -> list:
    EXPENSES_FILE_NAME = os.getenv("EXPENSES_FILE_NAME")
    return _get_file(EXPENSES_FILE_NAME, RecordType.Expense)


def get_income_data() -> list:
    INCOMES_FILE_NAME = os.getenv("INCOMES_FILE_NAME")
    return _get_file(INCOMES_FILE_NAME, RecordType.Income)


def refresh_expense_data() -> bool:
    EXPENSES_FILE_NAME = os.getenv("EXPENSES_FILE_NAME")
    try:
        dowload_dropbox_file(f"/{DROPBOX_DIR}/{EXPENSES_FILE_NAME}")
        return True
    except Exception as e:
        return False


def remove_expense(id: int) -> bool:
    EXPENSES_FILE_NAME = os.getenv("EXPENSES_FILE_NAME")
    expenses = read_from_file(f"{BASE_DOWNLOAD_DIR}/{EXPENSES_FILE_NAME}", RecordType.Expense)
    updated_expenses = [expense for expense in expenses if int(expense.id) != id]

    if len(expenses) == len(updated_expenses):
        return False

    write_to_file(f"{BASE_DOWNLOAD_DIR}/{EXPENSES_FILE_NAME}", updated_expenses)
    return True


def modify_expense(id: int, expense: Expense) -> bool:
    EXPENSES_FILE_NAME = os.getenv("EXPENSES_FILE_NAME")
    expenses = read_from_file(f"{BASE_DOWNLOAD_DIR}/{EXPENSES_FILE_NAME}", RecordType.Expense)
    updated = False

    for i, existing_expense in enumerate(expenses):
        if int(existing_expense.id) == id:
            expenses[i] = expense
            updated = True
            break

    if not updated:
        return False

    write_to_file(f"{BASE_DOWNLOAD_DIR}/{EXPENSES_FILE_NAME}", expenses)
    return updated


def create_expense(expense: Expense) -> bool:
    EXPENSES_FILE_NAME = os.getenv("EXPENSES_FILE_NAME")
    expenses = read_from_file(f"{BASE_DOWNLOAD_DIR}/{EXPENSES_FILE_NAME}", RecordType.Expense)
    num_exp = len(expenses)
    expense.id = num_exp
    expenses.append(expense)

    write_to_file(f"{BASE_DOWNLOAD_DIR}/{EXPENSES_FILE_NAME}", expenses)
    return True


def refresh_income_data() -> bool:
    INCOMES_FILE_NAME = os.getenv("INCOMES_FILE_NAME")
    try:
        dowload_dropbox_file(f"/{DROPBOX_DIR}/{INCOMES_FILE_NAME}")
        return True
    except Exception as e:
        return False


def remove_income(id: int) -> bool:
    INCOMES_FILE_NAME = os.getenv("INCOMES_FILE_NAME")
    incomes = read_from_file(f"{BASE_DOWNLOAD_DIR}/{INCOMES_FILE_NAME}", RecordType.Income)
    updated_incomes = [income for income in incomes if int(income.id) != id]

    if len(incomes) == len(updated_incomes):
        return False

    write_to_file(f"{BASE_DOWNLOAD_DIR}/{INCOMES_FILE_NAME}", updated_incomes)
    return True


def modify_income(id: int, income: Income) -> bool:
    INCOMES_FILE_NAME = os.getenv("INCOMES_FILE_NAME")
    incomes = read_from_file(f"{BASE_DOWNLOAD_DIR}/{INCOMES_FILE_NAME}", RecordType.Income)
    updated = False

    for i, existing_incomes in enumerate(incomes):
        if int(existing_incomes.id) == id:
            incomes[i] = income
            updated = True
            break

    if not updated:
        return False

    write_to_file(f"{BASE_DOWNLOAD_DIR}/{INCOMES_FILE_NAME}", incomes)
    return updated


def create_income(income: Income) -> bool:
    EXPENSES_FILE_NAME = os.getenv("EXPENSES_FILE_NAME")
    INCOMES_FILE_NAME = os.getenv("INCOMES_FILE_NAME")
    incomes = read_from_file(f"{BASE_DOWNLOAD_DIR}/{INCOMES_FILE_NAME}", RecordType.Income)
    num_exp = len(incomes)
    income.id = num_exp
    incomes.append(income)

    write_to_file(f"{BASE_DOWNLOAD_DIR}/{EXPENSES_FILE_NAME}", incomes)
    return True

def get_expense(id: int) -> Expense:
    return get_expense_data()[id]

def get_income(id: int) -> Income:
    return get_income_data()[id]