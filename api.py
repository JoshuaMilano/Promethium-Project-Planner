from flask import Blueprint, request, redirect, jsonify, session, flash
from helpers import fetch_db, login_required
from werkzeug.security import check_password_hash, generate_password_hash

api = Blueprint('api', __name__)

# Dictionary to define what can be changed
allowed_updates = {
    'boards': ['title', 'background'],
    'lists': ['title', 'position'],
    'cards': ['content', 'position']
}

@api.route('/create_board', methods=['POST'])
@login_required
def api_create_board():
    # Get user id, and set default board values
    user_id = session.get('user_id')
    default_title = 'Untitled Board'
    default_background = '#FFFFFF'

    # Open database and create the board
    db = fetch_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO boards (user_id, title, background) VALUES (?, ?, ?)', (user_id, default_title, default_background))
    db.commit()

    # Store board id a variable, and close the connection
    new_board_id = cursor.lastrowid
    db.close()
    return jsonify({'success': True, 'new_board_id': new_board_id})

@api.route('/add_list', methods=['POST'])
@login_required
def api_create_list():

    # Grab JSON data
    data = request.get_json()
    board_id = data.get('board_id') # ID of the board being updated.

    # Grab user id
    user_id = session.get('user_id')

    # Grab database
    db = fetch_db()

    # Check user owns board
    user_owns_board = db.execute('SELECT id FROM boards WHERE id = ? AND user_id = ?', (board_id, user_id)).fetchone()

    if not user_owns_board:
        db.close()
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    # Adding the list
    cursor = db.cursor()
    cursor.execute('INSERT INTO lists (board_id, title, position, background) VALUES (?, ?, ?, ?)', (board_id, 'New List', 99, '#FFFFFF'))

    # Grabbing list id
    new_list_id = cursor.lastrowid

    # Closing the Database
    db.commit()
    db.close()
    return jsonify({'success': True, 'new_id': new_list_id})

@api.route('/add_card', methods=['POST'])
@login_required
def api_create_card():
    
    # Grab JSON data
    data = request.get_json()
    board_id = data.get('board_id')
    column_id = data.get('column_id')

    # Grab user id
    user_id = session.get('user_id')

    # Grab database
    db = fetch_db()

    # Check user owns board
    user_owns_board = db.execute('SELECT id FROM boards WHERE id = ? AND user_id = ?', (board_id, user_id)).fetchone()

    if not user_owns_board:
        db.close()
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    # Check user owns list
    user_owns_list = db.execute('SELECT id FROM lists WHERE board_id = ? and id = ?', (board_id, column_id)).fetchone()

    if not user_owns_list:
        db.close()
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    # Adding the card
    cursor = db.cursor()
    cursor.execute('INSERT INTO cards (lists_id, position, background, content) VALUES (?, ?, ?, ?)', (column_id, 99, '#FFFFFF', 'New Card!'))

    # Grabbing the card id
    new_card_id = cursor.lastrowid

    # Closing the Database
    db.commit()
    db.close()
    return jsonify({'success': True, 'new_id': new_card_id})

@api.route('/delete_item', methods=['POST'])
@login_required
def api_delete_item():
    data = request.get_json()
    item_id = data.get('item_id')
    table_name = data.get('table_name')
    
    user_id = session.get('user_id')

    if table_name not in allowed_updates:
        return jsonify({'success': False, 'error': 'Invalid table'}), 400
    
    db = fetch_db()

    # Check Ownership
    if table_name == 'boards':
        user_owns = db.execute('SELECT id FROM boards WHERE id = ? AND user_id = ?', (item_id, user_id)).fetchone()
    
    elif table_name == 'lists':
        user_owns = db.execute('''
        SELECT lists.id FROM lists
        JOIN boards ON lists.board_id = boards.id
        WHERE lists.id = ? AND boards.user_id = ?
        ''', (item_id, user_id)).fetchone()

    elif table_name == 'cards':
        user_owns = db.execute('''
        SELECT cards.id FROM cards
        JOIN lists ON cards.lists_id = lists.id
        JOIN boards ON lists.board_id = boards.id
        WHERE cards.id = ? AND boards.user_id = ?
        ''', (item_id, user_id)).fetchone()

    if not user_owns:
        db.close()
        return jsonify({'success': False, 'error': 'Access denied'}), 403

    db.execute(f'DELETE FROM {table_name} WHERE id = ?', (item_id,))
    
    db.commit()
    db.close()

    return jsonify({'success': True})


@api.route('/update_board', methods=['POST'])
@login_required
def api_update_board():
    data = request.get_json()

    table_name = data.get('element') # name of element
    item_id = data.get('item_id') # ID of item being changed
    field_to_update = data.get('field') # Field to update
    new_value = data.get('value') # New value from the browser
    board_id = data.get('board_id') # ID of the board being updated.

    user_id = session.get('user_id')

    # Does the element exist in the list
    if table_name not in allowed_updates:
        return jsonify({'success': False, 'error': 'Invalid element'}), 400
    
    if field_to_update not in allowed_updates[table_name]:
        return jsonify({'success': False, 'error': 'Invalid field for this element'}), 400
    
    db = fetch_db()

    # Check Ownership
    if table_name == 'boards':
        user_owns = db.execute('SELECT id FROM boards WHERE id = ? AND user_id = ?', (item_id, user_id)).fetchone()
    
    elif table_name == 'lists':
        user_owns = db.execute('''
        SELECT lists.id FROM lists
        JOIN boards ON lists.board_id = boards.id
        WHERE lists.id = ? AND boards.user_id = ?
        ''', (item_id, user_id)).fetchone()

    elif table_name == 'cards':
        user_owns = db.execute('''
        SELECT cards.id FROM cards
        JOIN lists ON cards.lists_id = lists.id
        JOIN boards ON lists.board_id = boards.id
        WHERE cards.id = ? AND boards.user_id = ?
        ''', (item_id, user_id)).fetchone()

    if not user_owns:
        db.close()
        return jsonify({'success': False, 'error': 'Access denied'}), 403

    # Building the query
    query = f'UPDATE {table_name} SET {field_to_update} = ? WHERE id = ?'

    db.execute(query, (new_value, item_id))

    db.commit()
    db.close()

    return jsonify({'success': True})

# Account changes
# Change username
@api.route('/change_username', methods=['POST'])
@login_required
def change_username():
    # Grab the form info
    old_username = request.form.get('old_username')
    new_username = request.form.get('new_username')
    password = request.form.get('password')

    # Check form info was entered
    if not old_username or not new_username or not password:
        return redirect('/account')
    
    # Grab user id
    user_id = session.get('user_id')
    
    # Grab DB
    db = fetch_db()

    # Grab user info
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

    # compare usernames
    if user['username'] != old_username:
        flash('Old username is incorrect', 'error')
        return redirect('/account')

    # Compare user passwords
    if not check_password_hash(user['hash'], password):
        flash('Wrong password', 'error')
        return redirect('/account')
    
    # Update username
    db.execute('UPDATE users SET username = ? WHERE id = ?', (new_username, user_id))
    db.commit()
    db.close()

    flash('Username updated', 'success')
    return redirect('/account')

# Change Password
@api.route('/change_password', methods=['POST'])
@login_required
def change_password():
    # Grab the form info
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')

    if not old_password or not new_password:
        return redirect('/account')

    # Grab user id
    user_id = session.get('user_id')

    # Grab DB
    db = fetch_db()

    # Grab user info
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

    # Check user password
    if not check_password_hash(user['hash'], old_password):
        flash('Wrong password', 'error')
        return redirect('/account')
    
    # Update user password
    db.execute('UPDATE users SET hash = ? WHERE id = ?', (generate_password_hash(new_password), user_id))
    db.commit()
    db.close()

    flash('Password updated', 'success')
    return redirect('/account')



# Delete Account
@api.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    # Get form info
    username = request.form.get('username')
    password = request.form.get('password')

    # Check form
    if not username or not password:
        return redirect('/account')

    # Get user id
    user_id = session.get('user_id')

    # Fetch DB
    db = fetch_db()

    # Get user info
    user = db.execute('SELECT * FROM users WHERE id = ? AND username = ?', (user_id, username)).fetchone()

    if not user:
        flash('User doesn\'t exist', 'error')
        return redirect('/account')

    # Check Password
    if not check_password_hash(user['hash'], password):
        flash('Wrong Password', 'error')
        return redirect('/account')
    
    # Delete from users
    db.execute('DELETE FROM users WHERE id = ?', (user_id,))
    db.commit()
    db.close()
    flash('User deleted', 'success')
    session.clear()
    return redirect('/')