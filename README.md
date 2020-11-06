# rest_oauth_tests
Learning how to REST and OAUTH with Github, ESRI ArcGIS, Accela Construct, and maybe even Ecobee.

## Set up
### Conda environment

 conda create -n flask-oauth
 conda activate flask-oauth
 conda install --file requirements.txt

## REST Authentication

I have been testing out auth following along with the book "Flask
Framework Cookbook - Second Edition", (available in Safari) more or
less.

flask_session_auth/
is a simple test based on sessions.

flask_dance_test/
uses the flask_dance oauth library.
At this point it's going to be
connecting with github.

When I needed to start using URIs I moved over to
Bellman so that I could easily have a secure public web site.

I will be tucking it behind my nginx proxy under https://rest.wildsong.biz/ for now.