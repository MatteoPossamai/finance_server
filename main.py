from server.server import app
import os
from dotenv import load_dotenv
from logic.local_pf import refresh_expense_data, refresh_income_data

load_dotenv()

ENV = os.getenv("ENV", "prod")
DROPBOX_LOCAL_DATA_FOLDER=os.getenv("DROPBOX_LOCAL_DATA_FOLDER")

if ENV == "prod":
    os.makedirs(DROPBOX_LOCAL_DATA_FOLDER, exist_ok=True)
    refresh_expense_data()
    refresh_income_data()

if __name__ == "__main__":
    app.run(debug=True)
