from flask import Blueprint, jsonify, request
from server.pf_stats import pf_stats_blueprint
import logic.local_pf as local_pf
from model.record import Expense, Income
import json

pf_blueprint = Blueprint("personal_finance", __name__)

# External blueprints
pf_blueprint.register_blueprint(pf_stats_blueprint, url_prefix="/stats")


# --- Expenses ---
@pf_blueprint.route("/expenses", methods=["GET"])
def get_expenses():
    return jsonify(local_pf.get_expense_data())


@pf_blueprint.route("/expense/<int:id>", methods=["GET"])
def get_expense(id: int):
    return jsonify(local_pf.get_expense(id))



@pf_blueprint.route("/expense/", methods=["POST"])
def create_expense():
    data = json.loads(request.data)
    expense = Expense(id=0, **data)
    success = local_pf.create_expense(expense)
    return jsonify({"res": success})


@pf_blueprint.route("/expense/<int:id>", methods=["PUT"])
def modify_expense(id: int):
    data = json.loads(request.data)
    expense = Expense(id=id, **data)
    success = local_pf.modify_expense(id, expense)
    return jsonify({"res": success})


@pf_blueprint.route("/expense/<int:id>", methods=["DELETE"])
def delete_expense(id: int):
    success = local_pf.remove_expense(id)
    return jsonify({"res": success})


# --- Incomes ---
@pf_blueprint.route("/incomes", methods=["GET"])
def get_incomes():
    return jsonify(local_pf.get_income_data())


@pf_blueprint.route("/income/<int:id>", methods=["GET"])
def get_income(id: int):
    return jsonify(local_pf.get_income(id))


@pf_blueprint.route("/income/", methods=["POST"])
def create_income():
    data = json.loads(request.data)
    income = Income(id=0, **data)
    success = local_pf.create_income(income)
    return jsonify({"res": success})


@pf_blueprint.route("/income/<int:id>", methods=["PUT"])
def modify_income(id: int):
    data = json.loads(request.data)
    income = Income(id=id, **data)
    success = local_pf.modify_income(id, income)
    return jsonify({"res": success})


@pf_blueprint.route("/income/<int:id>", methods=["DELETE"])
def delete_income(id: int):
    success = local_pf.remove_income(id)
    return jsonify({"res": success})
