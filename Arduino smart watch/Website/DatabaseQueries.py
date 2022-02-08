from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

database = SQLAlchemy(app)

def printUserInfo():
    for i in users.query.all():
        print(f"Name: {i.name}, Username:{i.username}, Password:{i.password}, Email: {i.email}")

def deleteUser(usernm):
	u = users.query.filter_by(username=usernm)
	database.session.delete(u)
	database.session.commit()
	
class users(database.Model):
	_id = database.Column("id", database.Integer, primary_key=True)
	name = database.Column(database.String(100))
	username = database.Column(database.String(100))
	password = database.Column(database.String(100))
	email = database.Column(database.String(100))

	def __init__(self, name, username, password, email):
		self.name = name
		self.password = password
		self.email = email
		self.username = username
