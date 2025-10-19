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
    descript TEXT,
    tags TEXT,
    time_posted TEXT,
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

CREATE TABLE threads (
    id INTEGER PRIMARY KEY,
    product_id INTEGER REFERENCES posts(id),
    product_title TEXT,
    seller_id INTEGER REFERENCES users(id),
    buyer_id INTEGER REFERENCES users(id)
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    string TEXT,
    thread_id INTEGER REFERENCES threads(id),
    sender_id INTEGER REFERENCES users(id),
    time_sent TEXT
);