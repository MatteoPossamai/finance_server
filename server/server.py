from flask import Flask, jsonify
import os
from server.personal_finance import pf_blueprint


app = Flask(__name__)

app.register_blueprint(pf_blueprint, url_prefix="/personal_finance")


# Health endpoint
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"healthy": True})
