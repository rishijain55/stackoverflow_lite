from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'secret_key'
login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'

print("app/__init__.py: app = Flask(__name__)")
from app import routes