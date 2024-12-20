from flask import Blueprint, jsonify
from logic.dropbox import *
from server.pf_stats import pf_stats_blueprint

pf_blueprint = Blueprint("personal_finance", __name__)

# External blueprints
pf_blueprint.register_blueprint(pf_stats_blueprint, url_prefix="/stats")


# --- Expenses ---
@pf_blueprint.route("/expenses", methods=["GET"])
def get_expenses():
    return jsonify(get_expense_data())


@pf_blueprint.route("/expense/<id>", methods=["GET"])
def get_expense(id: int):
    # TODO
    return jsonify({"res": "GET"})


@pf_blueprint.route("/expense/", methods=["POST"])
def create_expense():
    # TODO
    return jsonify({"res": "POST"})


@pf_blueprint.route("/expense/", methods=["PUT"])
def modify_expense():
    # TODO
    return jsonify({"res": "PUT"})


@pf_blueprint.route("/expense/", methods=["DELETE"])
def delete_expense():
    # TODO
    return jsonify({"res": "DELETE"})


# --- Incomes ---
@pf_blueprint.route("/incomes", methods=["GET"])
def get_incomes():
    return jsonify(get_income_data())


@pf_blueprint.route("/income/<id>", methods=["GET"])
def get_income(id: int):
    # TODO
    return jsonify({"res": "GET"})


@pf_blueprint.route("/income/", methods=["POST"])
def create_income():
    # TODO
    return jsonify({"res": "POST"})


@pf_blueprint.route("/income/", methods=["PUT"])
def modify_income():
    # TODO
    return jsonify({"res": "PUT"})


@pf_blueprint.route("/income/", methods=["DELETE"])
def delete_income():
    # TODO
    return jsonify({"res": "DELETE"})
