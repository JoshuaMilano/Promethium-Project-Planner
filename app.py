# Imports
import os
from dotenv import load_dotenv
from flask import Flask, render_template, session, request, redirect, url_for
from functools import wraps

# Load the .env file
load_dotenv()

# Creating app
app = Flask(__name__)

# Grab secret_key from the .env file
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Creating the login_required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function



@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')