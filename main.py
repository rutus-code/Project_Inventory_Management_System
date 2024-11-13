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
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'inventory_management_system'

# Intialize MySQL
mysql = MySQL(app)

# http://localhost:5000/pythonlogin/ - the following will be our login page, which will use both GET and POST requests
@app.route('/pythonlogin', methods=['GET', 'POST'])
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    msg = ''
    return render_template('index.html', msg=msg)
