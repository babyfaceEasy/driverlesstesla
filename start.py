from flask import Flask, render_template
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
	return render_template("signup.html")

@app.route("/logout")
def logout():
	return 'work in progress';


if __name__ == "__main__":
	app.run(host='0.0.0.0')
