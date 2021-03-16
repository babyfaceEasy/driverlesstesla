from flask import Flask, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/profile")
def profile():
	return render_template("profile.html")

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/signup")
def signup():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    
    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login')) 
	#return render_template("signup.html")

@app.route("/logout")
def logout():
	return 'work in progress'


if __name__ == "__main__":
	app.run(host='0.0.0.0')
