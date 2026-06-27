# Imports
import os
import sqlite3
from dotenv import load_dotenv
from flask import Flask, render_template, session, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import login_required, fetch_db
from api import api


# Load the .env file
load_dotenv()


# Creating app
app = Flask(__name__)


# Grab secret_key from the .env file
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Pull the API routes
app.register_blueprint(api, url_prefix='/api')

# Routes
# index page
@app.route('/')
@login_required
def index():
    db = fetch_db()
    boards = db.execute('SELECT id, title FROM boards WHERE user_id = ?', (session.get('user_id'),)).fetchall()
    db.close()
    return render_template('index.html', users_boards=boards)


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
            flash('Username is taken', 'error')
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
            flash('Incorrect username or password', 'error')
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

# View Board
@app.route('/board/<int:board_id>')
@login_required
def view_board(board_id):
    # Open database connection
    db = fetch_db()

    # Check user owns board
    active_board = db.execute('SELECT * FROM boards WHERE id = ? AND user_id = ?', (board_id, session.get('user_id'))).fetchone()
    if active_board is None:
        db.close()
        return redirect('/')
    
    # Grab lists for board
    # lists = db.execute('SELECT * FROM lists WHERE board_id = ? ORDER BY position', (board_id,)).fetchall() # ORDERED
    lists = db.execute('SELECT * FROM lists WHERE board_id = ?', (board_id,)).fetchall() # UNORDERED

    # Grab all the cards for board
    cards = db.execute('SELECT cards.* FROM cards JOIN lists ON cards.lists_id = lists.id WHERE lists.board_id = ? ORDER BY cards.position', (board_id,)).fetchall()

    # Grab users other boards
    users_boards = db.execute('SELECT id, title FROM boards WHERE user_id = ?', (session.get('user_id'),)).fetchall()

    # Close database connection
    db.close()
    return render_template('board.html', users_boards=users_boards, active_board=active_board, board_lists=lists, board_cards=cards)

# Account page
@app.route('/account')
@login_required
def account():
    return render_template('account.html')

@app.route('/mobile')
def mobile():
    return render_template('mobile.html')

if __name__ == '__main__':
    app.run(debug=True)