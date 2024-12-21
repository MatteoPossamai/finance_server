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
        with open(".env.test", "w") as f:
            f.write(f"DROPBOX_EXPENSES_FILE_NAME={self.exp_test}\n")
            f.write(f"DROPBOX_INCOMES_FILE_NAME={self.inc_test}\n")

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

    def test_get_income(self):
        income = json.loads(self.client.get("/personal_finance/income/0").data)
        assert int(income["id"]) == 0
        assert int(income["amount"]) == 2
        assert income["category"] == "salary"
        assert income["currency"] == "GBP"
        assert income["issuer"] == "Casello"

    def test_remove_income(self):
        assert json.loads(self.client.delete("/personal_finance/income/0").data)["res"]
        incomes = json.loads(self.client.get("/personal_finance/incomes").data)

        assert len(incomes) == 4
        ids = [int(income["id"]) for income in incomes]
        assert ids == list(range(1, 5))

    def test_create_income(self):
        new_income = {
            "category": "salary",
            "amount": "12",
            "currency": "GBP",
            "issuer": "Comune",
            "date": "2027-01-01",
        }

        assert json.loads(
            self.client.post(
                "/personal_finance/income/",
                data=json.dumps(new_income),
                content_type="application/json",
            ).data
        )["res"]
        incomes = json.loads(self.client.get("/personal_finance/incomes").data)
        assert len(incomes) == 6

        new_income_got: dict = incomes[-1]
        del new_income_got["id"]

        assert sorted(new_income.values()) == sorted(new_income_got.values())
        assert sorted(new_income.keys()) == sorted(new_income_got.keys())

    def test_update_income(self):
        upd_income = {
            "category": "Tax Refund",
            "amount": "12",
            "currency": "GBP",
            "issuer": "Comune",
            "date": "2027-01-01",
        }

        assert json.loads(
            self.client.put(
                "/personal_finance/income/0",
                data=json.dumps(upd_income),
                content_type="application/json",
            ).data
        )["res"]
        incomes = json.loads(self.client.get("/personal_finance/incomes").data)
        assert len(incomes) == 5
        upd_income_got: dict = incomes[0]
        del upd_income_got["id"]
        assert sorted(upd_income.values()) == sorted(upd_income_got.values())
        assert sorted(upd_income.keys()) == sorted(upd_income_got.keys())

    def test_get_expenses(self):
        expenses = json.loads(self.client.get("/personal_finance/expenses").data)
        assert len(expenses) == 5
        for i, income in enumerate(expenses):
            assert int(income["id"]) == i
            assert int(income["amount"]) == i + 2
            assert income["category"] == "grocery"
            assert income["currency"] == "GBP"
            assert income["to"] == "Aldi"

    def test_get_expense(self):
        expense = json.loads(self.client.get("/personal_finance/expense/0").data)
        assert int(expense["id"]) == 0
        assert int(expense["amount"]) == 2
        assert expense["category"] == "grocery"
        assert expense["currency"] == "GBP"
        assert expense["to"] == "Aldi"


    def test_remove_expense(self):
        assert json.loads(self.client.delete("/personal_finance/expense/0").data)["res"]
        expenses = json.loads(self.client.get("/personal_finance/expenses").data)

        assert len(expenses) == 4
        ids = [int(income["id"]) for income in expenses]
        assert ids == list(range(1, 5))

    def test_create_expense(self):
        new_expense = {
            "category": "grocery",
            "amount": "12",
            "currency": "GBP",
            "to": "Aldi",
            "date": "2027-01-01",
        }

        assert json.loads(
            self.client.post(
                "/personal_finance/expense/",
                data=json.dumps(new_expense),
                content_type="application/json",
            ).data
        )["res"]
        expenses = json.loads(self.client.get("/personal_finance/expenses").data)
        assert len(expenses) == 6

        new_expense_got: dict = expenses[-1]
        del new_expense_got["id"]

        assert sorted(new_expense.values()) == sorted(new_expense_got.values())
        assert sorted(new_expense.keys()) == sorted(new_expense_got.keys())

    def test_update_expense(self):
        upd_expense = {
            "category": "grocery",
            "amount": "12",
            "currency": "GBP",
            "to": "Tesco",
            "date": "2027-01-01",
        }

        assert json.loads(
            self.client.put(
                "/personal_finance/expense/0",
                data=json.dumps(upd_expense),
                content_type="application/json",
            ).data
        )["res"]
        expenses = json.loads(self.client.get("/personal_finance/expenses").data)
        assert len(expenses) == 5
        upd_expense_got: dict = expenses[0]
        del upd_expense_got["id"]
        assert sorted(upd_expense.values()) == sorted(upd_expense_got.values())
        assert sorted(upd_expense.keys()) == sorted(upd_expense_got.keys())

    def teardown_method(
        self,
    ):
        os.remove("./data/" + self.exp_test)
        os.remove("./data/" + self.inc_test)
