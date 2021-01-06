from flask import Flask, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github
import os

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET']
blueprint = make_github_blueprint(
    client_id = os.environ['GITHUB_APPID'],
    client_secret = os.environ['GITHUB_APPSECRET'],
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok
    return "You are @{login} on GitHub".format(login=resp.json()["login"])

if __name__ == "__main__":
    app.run()
