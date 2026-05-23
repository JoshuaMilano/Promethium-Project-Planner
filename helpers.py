# Imports
import sqlite3
from flask import session, request, redirect, url_for
from functools import wraps

# Creating the login_required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Fetch Database function
def fetch_db():
    # Fetch Database
    db = sqlite3.connect('promethium.db')

    # return data as dictionaries
    db.row_factory = sqlite3.Row
    return db