from flask import Flask, jsonify
import os
from server.personal_finance import pf_blueprint
from dotenv import load_dotenv
from logic.local_pf import refresh_expense_data, refresh_income_data

load_dotenv(".env", override=True)

ENV = os.getenv("ENV", "dev")
if ENV == "prod":
    refresh_expense_data()
    refresh_income_data()

app = Flask(__name__)

app.register_blueprint(pf_blueprint, url_prefix="/personal_finance")


# Health endpoint
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"healthy": True})
