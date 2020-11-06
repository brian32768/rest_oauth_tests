import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Avoid that error "A secret key is required to use CSRF"
app.config['SECRET_KEY'] = os.urandom(32)

app.config["OAUTH_CLIENT_ID"] = ""
app.config["OAUTH_CLIENT_SECRET"] = ""
app.config["OAUTHLIB_RELAX_TOKEN_SCOPE"] = True


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///C:/Users/bwilson/source/repos/arcgis_rest/flask_auth_test/auth_test.db"
db = SQLAlchemy(app)


from my_app.auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)

db.create_all()