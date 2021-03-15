from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
	returnrender_template("index.html")

@app.route("/profile")
def profile():
	render_template("profile.thml")

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/signup")
def signup():
	return render_template("signup.html")


if __name__ == "__main__":
	app.run(host='0.0.0.0')
