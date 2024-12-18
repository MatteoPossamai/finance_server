import requests
import dotenv
import csv
import os
from typing import List
from model.record import RecordType, Record

dotenv.load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
DROPBOX_DOWNLOAD_URL = os.getenv("DROPBOX_DOWNLOAD_URL")
BASE_DOWNLOAD_DIR = os.getenv("BASE_DOWNLOAD_DIR")


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


def read_from_file(
    file_path: str, record_type: RecordType = RecordType.Expense
) -> List[Record]:
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
        
        header = data[0].header 
        writer.writerow(header)
        
        for record in data:
            writer.writerow(record.to_list())


def modify_file(file, data):
    pass


def get_expense_data() -> dict:
    pass


def get_income_data() -> dict:
    pass


def update_expense_data() -> bool:
    pass


def update_income_data() -> bool:
    pass
