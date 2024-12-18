import json
import csv
from typing import Dict, Union, List


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
            record["to"] = record["to"].lower().replace(" ", "_")
            writer.writerow(record.values())
