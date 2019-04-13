from flask import Flask,render_template,request,redirect, url_for, session
from flask_mail import Mail, Message
from models.model import user_exists, create_user, login_user, product_exists, add_product,add_to_cart, cart_info, remove_from_cart, cart_info, find_products, clear_cart #seller_products, buyer_products
import os

app = Flask(__name__) #Just to know where to look for templates and static files
mail=Mail(app)

app.config['SECRET_KEY'] = 'hello'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') 
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


mail=Mail(app)

@app.route('/buy', methods = ['POST','GET'])
def buy():
   msg = Message('Hello', sender = os.environ.get('MAIL_USERNAME'), recipients = ['mohan.bnkr@gmail.com'])
   msg.body = f"Hello {session['username']}, Flask message sent from Flask-Mail"
   mail.send(msg)
   clear_cart(session['username'])
   return redirect(url_for('home')) # sent	

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

# @app.route('/welcome')
# def welcome():
#  	return render_template('welcome.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
	#user = {'username':'Mohan','password':'12345'}
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		user = login_user(username)
		
		if user is None:
			return "This user doesn't exists. Go back and enter a valid user"

		if user['username'] == username:
			if user['password'] == password:
				session['username'] = username
				session['c_type'] = user["c_type"]
				return redirect(url_for('home'))
			return "wrong password.go back and try again"
		return "user doesn't exist.go back and enter valid username"

	else:
		return redirect(url_for('home'))

@app.route('/signup',methods = ['POST','GET'])
def signup():
	
	if request.method == 'POST':
		user_info = {}

		user_info['username'] = request.form['username']
		user_info['email'] = request.form['email']
		user_info['password'] = request.form['password']
		user_info['c_type'] = request.form['c_type']
		rpassword = request.form['rpassword']


		if user_exists(user_info['username']) is False:
			if user_info['password'] == rpassword:
				if user_info['c_type'] == 'buyer':
					user_info['cart'] = {}
				create_user(user_info)
				return render_template(url_for('home')) #'welcome.html', user = user_info['username'])
			return "Passwords don't match. Re-enter password correctly"
		return "user exists already. Enter new username"
	else:
		return redirect(url_for('home'))

@app.route('/seller', methods = ['POST','GET'])
def seller():

	if request.method == 'POST':
		product_info = {}

		product_info['name'] = request.form['name']
		product_info['price'] = int(request.form['price'])
		product_info['seller'] = session['username']
		product_info['description'] = request.form['description']

		if product_exists(product_info['name']) is False:
			add_product(product_info)
			return redirect(url_for('products'))
		return "Product already exists.Go back and enter another product"
		        

@app.route('/products')
def products():

	return render_template('products.html',products = find_products(session))
# def products():
# 	if session['c_type'] == "buyer":
# 		return render_template('products.html',products = buyer_products())
# 	return render_template('products.html',products = seller_products(session['username']))


@app.route('/addcart', methods = ['POST'])
def add_cart():
	product_id = str(request.form['id'])
	add_to_cart(product_id, session['username'])
	return redirect(url_for('home'))

@app.route('/removecart',methods = ['POST'])
def remove_cart():

	product_id = str(request.form['id'])
	remove_from_cart(product_id,session['username'])
	return redirect(url_for('cart'))

@app.route('/cart')
def cart():

	temp = cart_info(session['username'])
	product_info = temp[0]
	quantity = temp[1]
	total = 0
	for product, quant in zip(product_info, quantity):
		total = total + (product['price'] * quant)
	return render_template("cart.html", cart = zip(product_info,quantity),total = total)

@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('home'))



if __name__ == '__main__':
	app.run(debug = True)
