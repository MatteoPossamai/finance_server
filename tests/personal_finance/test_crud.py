import pytest
import os
from server.server import app
import csv
from dotenv import load_dotenv
import json


class TestPFCrud:

    @classmethod
    def setup_class(cls):
        load_dotenv()

    def setup_method(
        self,
    ):
        self.app = app
        self.client = app.test_client()

        self.exp_test = "test_e.csv"
        self.inc_test = "test_i.csv"
        os.environ["EXPENSES_FILE_NAME"] = self.exp_test
        os.environ["INCOMES_FILE_NAME"] = self.inc_test
        with open(".env.test", "w") as f:
            f.write(f"EXPENSES_FILE_NAME={self.exp_test}\n")
            f.write(f"INCOMES_FILE_NAME={self.inc_test}\n")

        load_dotenv(".env.test", override=True)

        with open("./data/" + self.exp_test, "w+") as file:
            writer = csv.writer(file)
            headers = ["id", "date", "category", "amount", "currency", "to"]
            writer.writerow(headers)
            for i in range(5):
                writer.writerow([i, "2025-01-01", "grocery", i + 2, "GBP", "Aldi"])

        with open("./data/" + self.inc_test, "w+") as file:
            writer = csv.writer(file)
            headers = ["id", "date", "category", "amount" "currency", "issuer"]
            writer.writerow(headers)
            for i in range(5):
                writer.writerow([i, "2025-01-01", "salary", i + 2, "GBP", "Casello"])

    def test_get_incomes(self):
        incomes = json.loads(self.client.get("/personal_finance/incomes").data)
        assert len(incomes) == 5
        for i, income in enumerate(incomes):
            assert int(income["id"]) == i
            assert int(income["amount"]) == i + 2
            assert income["category"] == "salary"
            assert income["currency"] == "GBP"
            assert income["issuer"] == "Casello"

    def test_get_expenses(self):
        expenses = json.loads(self.client.get("/personal_finance/expenses").data)
        assert len(expenses) == 5
        for i, income in enumerate(expenses):
            assert int(income["id"]) == i
            assert int(income["amount"]) == i + 2
            assert income["category"] == "grocery"
            assert income["currency"] == "GBP"
            assert income["to"] == "Aldi"

    def teardown_method(
        self,
    ):
        os.remove("./data/" + self.exp_test)
        os.remove("./data/" + self.inc_test)
