CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    descript TEXT,
    image BLOB
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    title TEXT,
    creator_id INTEGER REFERENCES users(id),
    sub_title TEXT,
    time_posted TEXT,
    descript TEXT,
    product_info TEXT,
    image BLOB
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    title TEXT,
    reviewer INTEGER REFERENCES users(id),
    review TEXT,
    rating INTEGER,
    time_posted TEXT,
    product_id INTEGER REFERENCES posts(id)
);

CREATE TABLE likes (
    id INTEGER PRIMARY KEY,
    liker INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES posts(id)
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    string TEXT,
    product_id INTEGER REFERENCES posts(id),
    messanger INTEGER REFERENCES users(id),
    messanged INTEGER REFERENCES users(id),
    time_posted TEXT
);