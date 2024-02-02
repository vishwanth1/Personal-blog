# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import smtplib


app = Flask(__name__)


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'us-cdbr-east-05.cleardb.net'
app.config['MYSQL_USER'] = 'b4119cc9dcdd6a'
app.config['MYSQL_PASSWORD'] = '4a5a8c74'
app.config['MYSQL_DB'] = 'heroku_d013d50a3e7acfe'

mysql = MySQL(app)

@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return redirect(url_for('home'))
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/about')
def about():
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("SELECT * FROM skills")
	skills = cursor.fetchall()
	return render_template('about.html', data=skills)

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', data=skills)

@app.route('/skills')
def skills():
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("SELECT * FROM skills")
	skills = cursor.fetchall()
	return render_template('skills.html', data=skills)

@app.route('/education')
def education():
	return render_template('education.html')


@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form and 'cnfrmpassword' in request.form:
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		repassword = request.form['cnfrmpassword']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s)', (username, password, email, repassword,))
			mysql.connection.commit()
			msg = 'Hi, Welcome to my personal blog You have successfully registered !'
			s = smtplib.SMTP('smtp.gmail.com', 587)
			s.starttls()
			s.login("blogp3059@gmail.com","Personal@1999")
			s.sendmail("blogp3059@gmail.com", str(email), msg)
			return render_template('login.html', msg = msg)
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

@app.route('/projectDetails')
def projectDetails():
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("SELECT * FROM projects")
	data = cursor.fetchall()
	print(data)
	return render_template('portfolio.html', data=data)

@app.route('/addSkill', methods =['POST'])
def addSkill():
	msg = ''
	if request.method == 'POST' and 'skill' in request.form and 'percentage' in request.form and 'description' in request.form and 'description' in request.form:
		skillName = request.form['skill']
		percentage = request.form['percentage']
		description = request.form['description']
		experience = request.form['experience']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM skills WHERE skillName = % s', (skillName, ))
		skill = cursor.fetchone()
		if skill:
			msg = 'Account already exists !'
		elif not skillName or not percentage or not description or not experience:
			msg = 'Please fill out the form !'
			print(msg)
		else:
			cursor.execute('INSERT INTO skills VALUES (%s, % s, % s, % s)', (skillName, percentage, description, experience, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
			return redirect(url_for('skills'))
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('skills.html', msg = msg)

@app.route('/addProjects', methods =['POST'])
def addProjects():
	msg = ''
	if request.method == 'POST' and 'projectTitle' in request.form and 'duration' in request.form and 'description' in request.form and 'technologies' in request.form and 'portfolio' in request.form:
		projectTitle = request.form['projectTitle']
		duration = request.form['duration']
		description = request.form['description']
		technologies = request.form['technologies']
		portfolio = request.form['portfolio']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		if not projectTitle or not duration or not description or not technologies or not portfolio:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO projects VALUES (%s,  % s, % s, % s, %s)', (projectTitle, duration, description, technologies, portfolio, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
			return redirect(url_for('projectDetails'))
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('portfolio.html', msg = msg)

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/submitFeedback', methods =['POST'])
def submitFeedback():
	if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'phonenumber' in request.form and 'feedback' in request.form:
		name = request.form['name']
		email = request.form['email']
		phonenumber = request.form['phonenumber']
		feedback = request.form['feedback']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('INSERT INTO feedback VALUES (%s,  % s, % s, % s)', (name, email, phonenumber, feedback, ))
		mysql.connection.commit()
		msg = str(feedback)
		s = smtplib.SMTP('smtp.gmail.com', 587)
		s.starttls()
		s.login("blogp3059@gmail.com","Personal@1999")
		s.sendmail("blogp3059@gmail.com", 'vishwanthgeddam94@gmail.com', msg)
		return render_template('contact.html')
