# Created By :  Rutu Shah
# created Date : 
# This is the app.py containing all routes for my website of inventoryManagement System

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
from flask import flash, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Change this to your secret key (it can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
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

@app.route('/pythonlogin/vendors')
def vendors():
    return render_template('vendors.html')

#add inventory route

@app.route('/pythonlogin/addInventory', methods=['GET', 'POST'])
def addInventory():
    msg = ''  # Initialize the message variable
    products = []  # Initialize products to prevent issues if fetching fails

    try:
        # Fetch products from the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        cursor.close()
    except Exception as e:
        msg = f"Error fetching products: {str(e)}"

        categories = []  # Initialize categories to prevent issues if fetching fails

    try:
        # Fetch categories from the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM category')
        categories = cursor.fetchall()
        cursor.close()
    except Exception as e:
        msg = f"Error fetching categories: {str(e)}"

    if request.method == 'POST':
        # Collect product details from the form
        inventory_name = request.form.get('inventory_name', '').strip()
        quantity = request.form.get('quantity', '').strip()
        price = request.form.get('price', '').strip()
        sku_description = request.form.get('product', '')  # Match form name
        category = request.form.get('category')

        # Check if a valid product is selected
        if not sku_description or sku_description == 'noProduct':
            msg = "Please select a valid product."
            return render_template('addInventory.html', msg=msg, products=products,categories=categories)

        try:
            # Insert product into the database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            localtimestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                'INSERT INTO inventory (inventory_item_description, quantity, price, product_id, created_at, updated_at,cat_id) VALUES (%s, %s, %s, %s, %s, %s,%s)',
                (inventory_name, quantity, price, sku_description, localtimestamp, localtimestamp,category)
            )
            mysql.connection.commit()
            msg = 'Product added successfully!'
        except Exception as e:
            msg = f"Database error: {str(e)}"
        finally:
            cursor.close()

    # Render the page with a message and categories for the dropdown
    return render_template('addInventory.html', msg=msg, products=products,categories=categories)

# this route is for my viewInventory
@app.route('/pythonlogin/viewInventory')
def viewInventory():
    try:
        # Connect to the database and fetch category data
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select i.inventory_id,i.inventory_item_description, i.quantity,i.price,p.sku_description , c.category_name from inventory i left join products p on p.product_id = i.product_id left join category c on c.cat_id = i.cat_id')
        inventories = cursor.fetchall()  # Fetch all available inventories from db
        cursor.close()
        
        # Pass the data to the template
        return render_template('viewInventory.html', inventories=inventories)
    except Exception as e:
        return f"An error occurred: {str(e)}"

#This route is for adding category into the database
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


# this route is for my viewProducts page
@app.route('/pythonlogin/viewProducts')
def viewProducts():
    try:
        # Connect to the database and fetch category data
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select p.product_id, p.sku, p.sku_description, p.make, p.model, p.memory, p.color, c.category_name  from products p left join category c on c.cat_id = p.cat_id')
        products = cursor.fetchall()  # Fetch all products
        cursor.close()
        
        # Pass the data to the template
        return render_template('viewProducts.html', products=products)
    except Exception as e:
        return f"An error occurred: {str(e)}"

# this route is for my viewCategory
@app.route('/pythonlogin/viewCategory')
def viewCategory():
    msg = ''
    try:
        # Connect to the database and fetch category data
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM category')
        categories = cursor.fetchall()  # Fetch all categories
        cursor.close()
        
        # Pass the data to the template
        return render_template('viewCategory.html', categories=categories,msg=msg)
    except Exception as e:
        return f"An error occurred: {str(e)}"


#This route is for adding products in to the database
@app.route('/pythonlogin/AddProduct', methods=['GET', 'POST'])
def addProduct():
    msg = ''  # Initialize the message variable
    categories = []  # Initialize categories to prevent issues if fetching fails

    try:
        # Fetch categories from the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM category')
        categories = cursor.fetchall()
        cursor.close()
    except Exception as e:
        msg = f"Error fetching categories: {str(e)}"

    if request.method == 'POST':
        # Collect product details from the form
        sku = request.form.get('sku', '').strip()
        sku_description = request.form.get('sku_description', '').strip()
        make = request.form.get('make', '').strip()
        model = request.form.get('model', '').strip()
        memory = request.form.get('memory', '').strip()
        color = request.form.get('color', '').strip()
        category = request.form.get('category')  # Get selected category ID

        # Check if a valid category is selected
        if not category or category == 'noCategory':
            msg = "Please select a valid category."
            return render_template('addProduct.html', msg=msg, categories=categories)

        try:
            # Check if the product already exists
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM products WHERE sku = %s', (sku,))
            product = cursor.fetchone()

            if product:
                msg = 'Product already exists!'
            else:
                # Insert product into the database
                cursor.execute(
                    'INSERT INTO products (sku, sku_description, make, model, memory, color, cat_id) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (sku, sku_description, make, model, memory, color, category)
                )
                mysql.connection.commit()
                msg = 'Product added successfully!'
        except Exception as e:
            msg = f"Database error: {str(e)}"
        finally:
            cursor.close()

    # Render the page with a message and categories for the dropdown
    return render_template('addProduct.html', msg=msg, categories=categories)


# This route is for deleting a category from the database by cat_id
@app.route('/pythonlogin/deleteCategory/<int:cat_id>', methods=['GET'])
def deleteCategory(cat_id):
    try:
        # Connect to the database and execute the DELETE query
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM category WHERE cat_id = %s', (cat_id,))
        mysql.connection.commit()  # Commit the transaction

        # Check if any row was affected (i.e., category was deleted)
        if cursor.rowcount > 0:
            flash(f"Category with ID {cat_id} deleted successfully!", "success")
        else:
            flash("Category not found!", "error")

        cursor.close()
    except Exception as e:
        flash(f"Error occurred: {str(e)}", "error")
    
    # Redirect to the viewCategory page
    return redirect(url_for('viewCategory'))

# This route is for deleting a product from the database by product_id
@app.route('/pythonlogin/deleteProduct/<int:product_id>', methods=['GET'])
def deleteProduct(product_id):
    try:
        # Connect to the database and execute the DELETE query
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('delete from products where product_id =  %s', (product_id,))
        mysql.connection.commit()  # Commit the transaction

        # Check if any row was affected (i.e., category was deleted)
        if cursor.rowcount > 0:
            flash(f"Product with ID {product_id} deleted successfully!", "success")
        else:
            flash("Product not found!", "error")

        cursor.close()
    except Exception as e:
        flash(f"Error occurred: {str(e)}", "error")
    
    # Redirect to the viewProducts page
    return redirect(url_for('viewProducts'))


# This route is for deleting an inventory from the database by inventory_id
@app.route('/pythonlogin/deleteInventory/<int:inventory_id>', methods=['GET'])
def deleteInventory(inventory_id):
    try:
        # Connect to the database and execute the DELETE query
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('delete from inventory where inventory_id =  %s', (inventory_id,))
        mysql.connection.commit()  # Commit the transaction

        # Check if any row was affected (i.e., category was deleted)
        if cursor.rowcount > 0:
            flash(f"Inventory with ID {inventory_id} deleted successfully!", "success")
        else:
            flash("Inventory not found!", "error")

        cursor.close()
    except Exception as e:
        flash(f"Error occurred: {str(e)}", "error")
    
    # Redirect to the viewProducts page
    return redirect(url_for('viewInventory'))

#this route for edit category
@app.route('/pythonlogin/editCategory/<int:cat_id>', methods=['GET', 'POST'])
def editCategory(cat_id):
    try:
        # Connect to the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Fetch category data
        cursor.execute('SELECT * FROM category WHERE cat_id = %s', (cat_id,))
        category = cursor.fetchone()

        if request.method == 'POST':
            # Get the category name from the form
            category_name = request.form.get('categoryName')
            
            if not category_name:
                flash("Category name cannot be empty!", "error")
            else:
                # Update the category
                cursor.execute(
                    'UPDATE category SET category_name = %s WHERE cat_id = %s',
                    (category_name, cat_id)
                )
                mysql.connection.commit()
                flash(f"Category with ID {cat_id} updated successfully!", "success")
                # return redirect(url_for('editCategory', cat_id=cat_id))
                return redirect(url_for('viewCategory', cat_id=cat_id))
                  
            
        # Render the template
        return render_template('editCategory.html', category=category)
    
    except Exception as e:
        # Log the error for debugging
        app.logger.error(f"Error in editCategory: {e}")
        flash("An unexpected error occurred. Please try again later.", "error")
        return redirect(url_for('some_error_route'))  # Replace with a valid error route

    finally:
        # Ensure the cursor is closed
        if 'cursor' in locals():
            cursor.close()

#this route for edit category
@app.route('/pythonlogin/editProduct/<int:product_id>', methods=['GET', 'POST'])
def editProduct(product_id):
    try:
        # Connect to the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Fetch product data
        cursor.execute('SELECT * FROM products WHERE product_id = %s', (product_id,))
        product = cursor.fetchone()

        # If the product doesn't exist, redirect with an error
        if not product:
            flash("Product not found!", "error")
            return redirect(url_for('viewProducts'))

        if request.method == 'POST':
            # Get the form data
            sku = request.form.get('sku')
            sku_description = request.form.get('sku_description')
            make = request.form.get('make')
            model = request.form.get('model')
            memory = request.form.get('memory')
            color = request.form.get('color')
            
            # Validate the form inputs
            if not sku:
                flash("SKU cannot be empty!", "error")
            elif not sku_description: 
                flash("SKU Description cannot be empty!", "error")
            elif not make: 
                flash("Make cannot be empty!", "error")
            elif not model: 
                flash("Model cannot be empty!", "error")
            elif not memory: 
                flash("Memory cannot be empty!", "error")
            elif not color: 
                flash("Color cannot be empty!", "error")
            else:
                # Update the product in the database
                cursor.execute(
                    'UPDATE products SET sku = %s, sku_description = %s, make = %s, model = %s, memory = %s, color = %s WHERE product_id = %s',
                    (sku, sku_description, make, model, memory, color, product_id)
                )
                mysql.connection.commit()

                flash(f"Product with ID {product_id} updated successfully!", "success")
                return redirect(url_for('viewProducts'))

        # Render the template
        return render_template('editProduct.html', product=product)
    
    except Exception as e:
        # Log the error for debugging
        app.logger.error(f"Error in editProduct: {e}", exc_info=True)
        flash("An unexpected error occurred. Please try again later.", "error")
        return redirect(url_for('viewProducts'))  # Redirect to a valid route in case of an error

    finally:
        # Ensure the cursor is closed
        if 'cursor' in locals():
            cursor.close()


#this route for edit inventory
@app.route('/pythonlogin/editInventory/<int:inventory_id>', methods=['GET', 'POST'])
def editInventory(inventory_id):
    try:
        # Connect to the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Fetch inventory data
        cursor.execute('SELECT * FROM inventory WHERE inventory_id = %s', (inventory_id,))
        inventory = cursor.fetchone()

        # If the product doesn't exist, redirect with an error
        if not inventory:
            flash("Inventory not found!", "error")
            return redirect(url_for('viewInventory'))

        if request.method == 'POST':
            # Get the form data
            product = request.form.get('product')
            sku_description = request.form.get('sku_description')
            make = request.form.get('make')
            model = request.form.get('model')
            memory = request.form.get('memory')
            color = request.form.get('color')
            
            # Validate the form inputs
            if not sku:
                flash("SKU cannot be empty!", "error")
            elif not sku_description: 
                flash("SKU Description cannot be empty!", "error")
            elif not make: 
                flash("Make cannot be empty!", "error")
            elif not model: 
                flash("Model cannot be empty!", "error")
            elif not memory: 
                flash("Memory cannot be empty!", "error")
            elif not color: 
                flash("Color cannot be empty!", "error")
            else:
                # Update the product in the database
                cursor.execute(
                    'UPDATE products SET sku = %s, sku_description = %s, make = %s, model = %s, memory = %s, color = %s WHERE product_id = %s',
                    (sku, sku_description, make, model, memory, color, product_id)
                )
                mysql.connection.commit()

                flash(f"Product with ID {product_id} updated successfully!", "success")
                return redirect(url_for('viewProducts'))

        # Render the template
        return render_template('editProduct.html', product=product)
    
    except Exception as e:
        # Log the error for debugging
        app.logger.error(f"Error in editProduct: {e}", exc_info=True)
        flash("An unexpected error occurred. Please try again later.", "error")
        return redirect(url_for('viewProducts'))  # Redirect to a valid route in case of an error

    finally:
        # Ensure the cursor is closed
        if 'cursor' in locals():
            cursor.close()