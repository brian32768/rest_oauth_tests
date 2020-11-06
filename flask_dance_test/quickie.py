from flask import Flask, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github
import os

app = Flask(__name__)
app.secret_key = "mygituhubsecret"
blueprint = make_github_blueprint(
    client_id="my-key-here",
    client_secret="my-secret-here",
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok
    return "You are @{login} on GitHub".format(login=resp.json()["login"])