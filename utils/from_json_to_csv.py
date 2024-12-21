import json
import csv
from typing import Dict, Union, List

FORMATTED_FIELDS = ["to", "issuer"]
def format_function(data: str):
    return data.replace(" ", "_").upper()

def from_json_to_csv(json_file_path: str, csv_file_path: str):
    with open(json_file_path, "r") as json_file:
        data: Dict[str, List[Dict[str, Union[int, str]]]] = json.load(json_file)
    records = data.get("records", [])

    with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        if records:
            header = records[0].keys()
            writer.writerow(header)

        for record in records:
            data_to_write = []
            for field in header:
                if field in FORMATTED_FIELDS:
                    data_to_write.append(format_function(record[field]))
                else:
                    data_to_write.append(record[field])
            
            writer.writerow(data_to_write)


if __name__ == "__main__":
    from_json_to_csv("../data/expenses.json", "../data/expenses.csv")
    from_json_to_csv("../data/incomes.json", "../data/incomes.csv")