from flask import Blueprint, jsonify

pf_stats_blueprint = Blueprint("pf_stats", __name__)

# --- Stats functions for personal finance --- 
@pf_stats_blueprint.route("/net", methods=["GET"])
def net():
    # TODO
    return "TODO"

# TODO: decide what stats want and create functions with logic
# - net value
# - total expenses
# - total incomes
# - mean, median incomes and expenses
# - all of the prev, filtering by start and end date, category, issuer or receiver
# - Possibility to choose the currency