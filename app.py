# Imports
import os
import sqlite3
from dotenv import load_dotenv
from flask import Flask, render_template, session, request, redirect, url_for
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import login_required, fetch_db


# Load the .env file
load_dotenv()


# Creating app
app = Flask(__name__)


# Grab secret_key from the .env file
app.secret_key = os.getenv("FLASK_SECRET_KEY")


# Routes
# index page
@app.route('/')
@login_required
def index():
    return render_template('index.html')


# register page
@app.route('/register', methods=['GET', 'POST'])
def register():

    # This is awkard. If a logged in user is accessing register,
    # they might be attempting to make another account?

    # Either way, safest option is to just send them back to the home page.
    if session.get('user_id'):
        return redirect('/')

    if request.method == 'POST':
        # Retrieve form info
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirmation = request.form.get('password-confirmation')

        # Check form info is valid
        if not username or not password or password != password_confirmation:
            # Eventually, I'll use flash here to let the user know what went wrong
            return render_template('register.html')
        
        # Create the password hash
        hashed_password = generate_password_hash(password)

        db = fetch_db()

        # Try to add the user to the database
        try:
            # Create db cursor
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hashed_password))
            db.commit()
            # Store user in session
            session['user_id'] = cursor.lastrowid
        except sqlite3.IntegrityError:
            # If username already exists
            db.close()
            # Flash an error to the user
            return render_template('register.html')
        
        db.close()

        return redirect('/')
    return render_template('register.html')


# login page
@app.route('/login', methods=['GET', 'POST'])
def login():

    # If the user is already logged in, just send them straight to home.
    if session.get('user_id'):
        return redirect('/')

    if request.method == 'POST':
        # Retrieve form info
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate
        if not username or not password:
            # Flash an apology
            render_template('login.html')

        # Grab database
        db = fetch_db()

        # Make cursor
        cursor = db.cursor()

        # Point to user info
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))

        # Store user info in variable
        user_info = cursor.fetchone()

        # Close database connection
        db.close()

        # Check user info is correct
        if user_info is None or not check_password_hash(user_info['hash'], password):
            # Add Flash message (Might use an elif to check if the username was incorrect, or if the password was wrong.)
            return render_template('login.html')
        
        # Log user in
        session['user_id'] = user_info['id']

        # Send the user to home
        return redirect('/')
    return render_template('login.html')


# Log out
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)