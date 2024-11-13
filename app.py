from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib

app = Flask(__name__)

# Change this to your secret key (it can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'inventory_management_system'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/test_db')
def test_db():
    cursor = mysql.connection.cursor()
    cursor.execute("SHOW TABLES;")  # Fetch all tables from the database
    tables = cursor.fetchall()
    cursor.close()
    return f"Tables: {tables}"


# http://localhost:5000/pythonlogin/ - the following will be our login page, which will use both GET and POST requests
@app.route('/pythonlogin', methods=['GET', 'POST'])
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output a message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)


@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if POST request with required form data exists
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form and 'email' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']

            # Check if account exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            account = cursor.fetchone()

            # If account exists show error and validation checks
            if account:
                msg = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                # Hash the password
                # hash = password + app.secret_key
                # hashed_password = hashlib.sha1(hash.encode()).hexdigest()

                # Account doesn't exist, insert new account
                try:
                    cursor.execute(
                        'INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)',
                        (username, password, email,)
                    )
                    mysql.connection.commit()
                    msg = 'You have successfully registered!'
                except Exception as e:
                    msg = f"Database error: {str(e)}"
                finally:
                    cursor.close()
        else:
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'

    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)



# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for logged in users
@app.route('/pythonlogin/home')
def home():
    # Check if the user is logged in
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for logged in users
@app.route('/pythonlogin/profile')
def profile():
    # Check if the user is logged in
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not logged in redirect to login page
    return redirect(url_for('login'))

@app.route('/pythonlogin/configuration')
def configuration():
    return render_template('configuration.html')

@app.route('/pythonlogin/customers')
def customers():
    return render_template('customers.html')

@app.route('/pythonlogin/inventory')
def inventory():
    return render_template('inventory.html')

@app.route('/pythonlogin/AddCategory', methods=['GET', 'POST'])
def addCategory():
    msg = ''
    if request.method == 'POST' and 'categoryName' in request.form:
        # Create variables for easy access
        categoryName = request.form['categoryName']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM category WHERE category_name = %s', (categoryName,))
        category = cursor.fetchone()

        if category:
            msg = 'Category already exists!'
        else:
            # Account doesn't exist, insert new account
            try:
                cursor.execute(
                    'INSERT INTO category (category_name) VALUES (%s)',
                    (categoryName,)
                )
                mysql.connection.commit()
                msg = 'Category successfully added!'
            except Exception as e:
                msg = f"Database error: {str(e)}"
            finally:
                cursor.close()
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    return render_template('addCategory.html', msg=msg)


@app.route('/pythonlogin/viewCategory')
def viewCategory():
    try:
        # Connect to the database and fetch category data
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM category')
        categories = cursor.fetchall()  # Fetch all categories
        cursor.close()
        
        # Pass the data to the template
        return render_template('viewCategory.html', categories=categories)
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/pythonlogin/AddProduct', methods=['GET', 'POST'])
def addProduct():
    return render_template('addProduct.html')