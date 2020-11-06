import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Avoid that error "A secret key is required to use CSRF"
app.config['SECRET_KEY'] = os.urandom(32)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///auth_test.db"
db = SQLAlchemy(app)


from my_app.auth.views import auth
app.register_blueprint(auth)

db.create_all()
