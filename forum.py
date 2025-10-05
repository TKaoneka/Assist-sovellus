import db

def get_posts():
    sql = """SELECT p.title, p.creator_id, p.time_posted, 
    u.id, u.username 
    FROM posts p, users u 
    WHERE u.id = p.creator_id ORDER BY p.id DESC"""
    return db.query(sql)

def get_search(searched):
    sql = """SELECT p.title, p.creator_id, p.time_posted, 
    u.id, u.username 
    FROM posts p, users u 
    WHERE u.id = p.creator_id AND p.title LIKE ? ORDER BY p.id DESC"""
    search = f"%{searched}%"
    return db.query(sql, [search])

def create_account(username, hash):
    sql = """INSERT INTO users (username, password_hash, descript) 
    VALUES (?, ?, ?)"""
    db.execute(sql, [username, hash, "NULL"])
    return db.last_insert_id()

def get_account(username):
    sql = """SELECT id, password_hash FROM users WHERE username = ?"""
    return db.query(sql, [username])[0]

def create_product(title, user_id, subtitle, product_type, thumbnail_photo, product_desc):
    sql = """INSERT INTO posts (title, creator_id, sub_title, descript, tags, time_posted, image) 
    VALUES (?, ?, ?, ?, ?, datetime('now'), ?)"""
    db.execute(sql, [title, user_id, subtitle, product_desc, product_type, thumbnail_photo])
    return db.last_insert_id()

def modify_product(title, subtitle, product_desc, product_id):
    sql = """UPDATE posts SET title = ?, sub_title = ?, descript = ? WHERE id = ?"""
    db.execute(sql, [title, subtitle, product_desc, product_id])

def delete_product(product_id):
    sql = """DELETE FROM posts WHERE id = ?"""
    db.execute(sql, [product_id])

def get_product(product_id):
    sql = """SELECT title, creator_id, sub_title, descript, time_posted FROM posts WHERE id = ?"""
    return db.query(sql, [product_id])[0]

def get_profile(user_id, account_is_owned):
    sql_1 = """SELECT username, image IS NOT NULL has_pfp FROM users WHERE id = ?"""
    sql_2 = """SELECT id, title, sub_title, time_posted FROM posts WHERE creator_id = ?"""
    sql_3 = """SELECT title, review, rating, time_posted, product_id FROM reviews WHERE reviewer = ?"""
    sql_4 = """SELECT COUNT(p.title) total_posts, COUNT(r.title) total_reviews, AVG(r.rating) avg_rating 
    FROM posts p LEFT JOIN reviews r ON p.creator_id = r.reviewer WHERE p.creator_id = ?"""

    user = db.query(sql_1, [user_id])[0]
    products = db.query(sql_2, [user_id]) or []
    reviews = db.query(sql_3, [user_id]) or []
    totals = db.query(sql_4, [user_id])[0] if db.query(sql_4, [user_id]) else {'total_posts': 0, 'total_reviews': 0, 'avg_rating': None}

    if account_is_owned:
        sql_5 = """SELECT product_id FROM likes WHERE liker = ?"""
        sql_6 = """SELECT COUNT(id) total_likes FROM likes WHERE liker = ?"""
        sql_7 = """SELECT id, messanged FROM messages WHERE messanger = ?"""

        likes = db.query(sql_5, [user_id]) or [0]
        total_likes = db.query(sql_6, [user_id])[0][0] if db.query(sql_6, [user_id]) else {'total_likes': 0}
        threads = db.query(sql_7, [user_id]) or []
        return user, products, reviews, totals, likes, total_likes, threads
    
    return user, products, reviews, totals

def send_message(message, product_id, messanger, messaged):
    sql = """INSERT INTO messages (string, product_id, messanger, messaged, time_sent) VALUES (?, ?, ?, ?, datetime('now'))"""
    db.execute(sql, [message, product_id, messanger, messaged])

def get_messaged(product_id):
    sql = """SELECT creator_id FROM posts WHERE id = ?"""
    return db.query(sql, [product_id])[0][0]

def get_thread(product_id, user_id):
    sql_1 = """SELECT m.string, m.time_sent, u.username FROM messages m, users u WHERE u.id = m.messanger OR u.id = m.messaged 
    AND product_id = ? AND messanger = ? OR messaged = ? ORDER BY time_messaged DESC"""
    sql_2 = """SELECT u.id, u.username, p.title FROM users u, posts p WHERE p.creator_id = u.id AND p.id = ?"""
    seller_id, seller_username, title = db.query(sql_2, [product_id])[0]
    return seller_id, seller_username, title, db.query(sql_1, [product_id, user_id, user_id])