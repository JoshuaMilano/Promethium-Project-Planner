-- Drop tables if they exist, so the database can be easily reset.
DROP TABLE IF EXISTS users; -- For the users
DROP TABLE IF EXISTS boards; -- For the boards
DROP TABLE IF EXISTS lists; -- For the columns in the boards
DROP TABLE IF EXISTS cards; -- For the cards in the columns

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE boards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    background TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE lists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    board_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    position INTEGER NOT NULL,
    background TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(board_id) REFERENCES boards(id) ON DELETE CASCADE
);

CREATE TABLE cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lists_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    background TEXT NOT NULL,
    content TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(lists_id) REFERENCES lists(id) ON DELETE CASCADE
);

CREATE INDEX idx_boards_user ON boards(user_id);
CREATE INDEX idx_lists_board ON lists(board_id);
CREATE INDEX idx_cards_lists ON cards(lists_id);