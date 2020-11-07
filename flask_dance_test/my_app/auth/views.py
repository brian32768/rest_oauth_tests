from flask import request, render_template, flash, redirect, url_for, Blueprint 
from my_app import app 
from flask_dance.contrib.github import make_github_blueprint, github
 
auth_blueprint = Blueprint('auth', __name__) 
 
@auth_blueprint.route('/') 
@auth_blueprint.route('/home') 
def home():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok
#    return render_template('home.html') 
    return "You are @{login} on GitHub".format(login=resp.json()["login"])
   
@auth_blueprint.route('/logout') 
def logout(): 
    if 'username' in session: 
        session.pop('username') 
        flash('You have successfully logged out.', 'success') 
 
    return redirect(url_for('auth.home')) 
