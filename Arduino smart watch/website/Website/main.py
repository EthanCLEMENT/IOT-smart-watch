from flask import Flask, request, render_template, url_for, redirect, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import requests

# initiates Flask
app = Flask(__name__)
app.secret_key = "Next Step"
app.permanent_session_lifetime = timedelta(minutes=5) # the user must relog every 5 mins
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Users.sqlite3" # enables the communication between Flask and the database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # signals the application every time a change is about to be made in the database

# initiates SQLalchemy
database = SQLAlchemy(app)

# define users class
class users(database.Model):
	_id = database.Column("id", database.Integer, primary_key=True) # id
	name = database.Column(database.String(100)) # name
	username = database.Column(database.String(100)) # username
	password = database.Column(database.String(100)) # password
	email = database.Column(database.String(100)) # email

	def __init__(self, name, username, password, email):
		self.name = name
		self.password = password
		self.email = email
		self.username = username

# home page
@app.route("/")
def home():
	return render_template("home.html")

# signup page
@app.route("/signup", methods=["POST", "GET"])
def signup():
	if request.method=="POST": # checks if the user asks sends info 
		session.permanent = True # makes sure the user is connected
		usernm = request.form['usernm'] # saves username
		passwrd = request.form['passwrd'] # saves password
		nm = request.form['nm'] # saves name

		found_user = users.query.filter_by(username=usernm).first() # seeks for username within the database
		if found_user:
			flash("This username already exists! Please chose another one.") #displays message on screen
			return render_template('signup.html')

		usr = users(nm, usernm, passwrd, None)
		database.session.add(usr) # adds the user in the database if user does not exist
		database.session.commit()

		session["user"] = usernm, passwrd, nm
		session['email'] = None
		flash(f"Signed up successfully, {nm} !", "info") 
		return redirect(url_for("user"))

	if "user" in session:
		flash("You are already logged in") # displays if user is already connected 
		return redirect(url_for("user"))

	return render_template("signup.html")

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		session.permanent = True
		usernm = request.form["usrnm"] # asks for username
		password = request.form["passwrd"] # asks for password

		found_user = users.query.filter_by(username=usernm, password = password).first() # if user exists redirects to user.html
		if found_user:
			session["user"] = usernm, password, found_user.name
			session['email'] = found_user.email
			flash(f"Logged successfully, {found_user.name} !", "info")
			return redirect(url_for("user"))
		else:
			flash("The username or password you entered are not connected to an account !") # displays if password is incorrect 
			return render_template("login.html")
	else:
		if "user" in session:
			flash("You are already logged in") # displays if already logged in
			return redirect(url_for("user"))
		return render_template("login.html")

@app.route("/user", methods=["POST","GET"])
def user():
	email = None
	if "user" in session:
		usernm, passwd, nm = session["user"]
		if request.method =='POST':
			if "email" in request.form:
				email = request.form['email']
				session['email'] = email
				found_user = users.query.filter_by(name=nm, username = usernm, password=passwd).first() # search for existing users
				found_user.email = email # search for existing emails
				database.session.commit() # adds email to the database
				flash("Email was saved !") # displays when email is saved
			if "logout" in request.form: # disconnects the user if clicked
				return logout()
		else:
			if "email" in session:
				email = session["email"]
		return render_template("user.html", name=nm, username = usernm, password=passwd, email=email)
	else:
		flash("You are not logged in!") # displays if not logged in
		return redirect(url_for("login"))

@app.route("/logout")
def logout():
	if "user" in session:
		user=session["user"]
		flash(f"You have been logged out, {user[0]}", "info") # displays when logged out
	else:
		flash("You are not logged in !") # displays if not logged in
	session.pop("user", None) # pops the user so they get logged out 
	session.pop("email", None) # pops the email so the user gets logged out
	return redirect(url_for("login"))

@app.route("/view") # redirects to the database
def view():
	return render_template("view.html", values=users.query.all())

database.create_all()
app.run(debug=True)





