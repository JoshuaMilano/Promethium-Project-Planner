from flask import Blueprint, request, redirect, jsonify, session
from helpers import fetch_db, login_required

api_bp = Blueprint('api', __name__)

# Dictionary to define what can be changed
allowed_updates = {
    'boards': ['title', 'background'],
    'lists': ['title', 'position'],
    'cards': ['content', 'position']
}

# TODO: Add API route for creating a board

@api_bp.route('/add_list', methods=['POST'])
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

@api_bp.route('/add_card', methods=['POST'])
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

@api_bp.route('/delete_item', methods=['POST'])
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
    
    if not user_owns:
        db.close()
        return jsonify({'success': False, 'error': 'Access denied'}), 403

    if table_name == 'boards':
        db.execute(f'DELETE FROM {table_name} WHERE id = ?', (item_id,))
    
    db.commit()
    db.close()

    return jsonify({'success': True})


@api_bp.route('/update_board', methods=['POST'])
@login_required
def api_update_board():
    data = request.get_json()

    element_name = data.get('element') # name of element # NOTE: update this variable to table.
    item_id = data.get('item_id') # ID of item being changed
    field_to_update = data.get('field') # Field to update
    new_value = data.get('value') # New value from the browser
    board_id = data.get('board_id') # ID of the board being updated.

    user_id = session.get('user_id')

    # Does the element exist in the list
    if element_name not in allowed_updates:
        return jsonify({'success': False, 'error': 'Invalid element'}), 400
    
    if field_to_update not in allowed_updates[element_name]:
        return jsonify({'success': False, 'error': 'Invalid field for this element'}), 400
    
    db = fetch_db()

    # Does user have access?
    user_owns_board = db.execute('SELECT id FROM boards WHERE id = ? AND user_id = ?', (board_id, user_id)).fetchone()

    if not user_owns_board:
        db.close()
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    # TODO: If element_name = lists, verify user owns list
    # TODO: If element_name = cards, verify user owns cards

    # Building the query
    query = f'UPDATE {element_name} SET {field_to_update} = ? WHERE id = ?'

    db.execute(query, (new_value, item_id))

    db.commit()
    db.close()

    return jsonify({'success': True})