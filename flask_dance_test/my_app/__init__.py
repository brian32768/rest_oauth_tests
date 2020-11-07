import os 
from flask import Flask

app = Flask(__name__)

# Avoid that error "A secret key is required to use CSRF"
app.config['SECRET_KEY'] = os.urandom(32)

# Github brian32768 oauth_test
app.config["OAUTH_CLIENT_ID"] = "c59946f9e73b253b8aed"
app.config["OAUTH_CLIENT_SECRET"] = "7aa37a244f0eca6c89e6fc2f24cc067810534a10"
app.config["OAUTHLIB_RELAX_TOKEN_SCOPE"] = True

from my_app.auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)

