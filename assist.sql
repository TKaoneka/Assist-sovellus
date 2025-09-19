CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    title TEXT,
    user_id INTEGER REFERENCES users(id)
    sub_title TEXT,
    time_posted TEXT
);