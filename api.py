from flask import Flask,render_template,request,redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
	#username = "mohan"
	return render_template('home.html', title = 'home', home = 'home')

@app.route('/about')
def about():
	return render_template('about.html', title = 'about')

@app.route('/contact')
def contact():
	return render_template('contact.html', title = 'contact')

@app.route('/welcome')
def welcome():
 	return render_template('welcome.html')

@app.route('/login',methods = ['POST'])
def login():
	user = {'username':'Mohan','password':'12345'}

	username = request.form['username']
	password = request.form['password']

	if user['username'] == username:
		if user['password'] == password:
			return redirect(url_for('welcome'))
		return "wrong password.go back and try again"
	return "user doesn't exist.go back and enter valid username"

if __name__ == '__main__':
	app.run(debug = True)
