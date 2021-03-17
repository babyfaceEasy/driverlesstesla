from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, current_user, logout_user, login_user

# init SQLAlchemy so we can use it later in our models
app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'pHd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///presentation.sqlite'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
#login_manager.init_app(app)

# models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    created_on = db.Column(db.DateTime, server_default=db.func.Now())
    update_on = db.Column(db.DateTime, server_default=db.func.Now(), server_onupdate=db.func.Now())


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# routes
@app.route("/old-index")
def index():
	return render_template("new_index.html")

@app.route("/")
def new_index():
    return render_template("new_index.html")

@app.route("/new-index", methods=['POST'])
def new_index_post():
    email = request.form.get('email')
    password = request.form.get('password')

    new_participant = Participant(email=email, password=password)

    db.session.add(new_participant)
    db.session.commit()
    return redirect(url_for('new_welcome'))

@app.route("/new-welcome")
def new_welcome():
    return render_template("new_welcome.html")


@app.route("/profile")
@login_required
def profile():
    participants = Participant.query.all()
	return render_template("profile.html", name=current_user.name, participants=participants)

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/signup")
@login_required
def signup():
	return render_template("signup.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    # new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    new_user = User(email=email, name=name, password=password)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('profile'))

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    #if not user or not check_password_hash(user.password, password):
    if not user or user.password != password:
        flash('Please check your login details and try again.')
        return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('profile'))

# run application
if __name__ == "__main__":
	app.run(host='0.0.0.0')
