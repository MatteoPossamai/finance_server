from flask import Flask
from server.personal_finance import pf_blueprint

app = Flask(__name__)

app.register_blueprint(pf_blueprint, url_prefix='/personal_finance')
    
if __name__ == '__main__':
    app.run(debug=True)