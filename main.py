from server.server import app
from logic.dropbox import *
from logic.local_pf import *
from dotenv import load_dotenv

load_dotenv(".env", override=True)

# refresh_expense_data()
# refresh_income_data()
# if __name__ == '__main__':
#     app.run(debug=True)