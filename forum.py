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

    sql_4 = """SELECT (SELECT COUNT(p.id) FROM posts p WHERE p.creator_id = ?) total_posts, 
    (SELECT COUNT(r.id) FROM reviews r WHERE r.reviewer = ?) total_reviews, 
    (SELECT IFNULL(AVG(r.rating), 0) FROM reviews r WHERE r.reviewer = ?) avg_rating"""

    user = db.query(sql_1, [user_id])[0]
    products = db.query(sql_2, [user_id]) or []
    reviews = db.query(sql_3, [user_id]) or []

    totals_result = db.query(sql_4, [user_id, user_id, user_id])
    totals = totals_result[0] if totals_result else {'total_posts': 0, 'total_reviews': 0, 'avg_rating': 0}

    if account_is_owned:
        sql_5 = """SELECT product_id FROM likes WHERE liker = ?"""

        sql_6 = """SELECT COUNT(id) total_likes FROM likes WHERE liker = ?"""

        sql_7 = """SELECT m.product_id, p.title, 
       CASE 
           WHEN m.messanger = ? THEN u2.username 
           ELSE u.username 
       END other_username,
       CASE 
           WHEN m.messanger = ? THEN m.messaged 
           ELSE m.messanger 
       END other_user_id
       FROM messages m
       JOIN posts p ON m.product_id = p.id
       JOIN users u ON m.messanger = u.id
       JOIN users u2 ON m.messaged = u2.id
       WHERE m.messanger = ? OR m.messaged = ? 
       GROUP BY m.product_id, p.title"""

        likes = db.query(sql_5, [user_id]) or [0]
        total_likes = db.query(sql_6, [user_id])[0][0] if db.query(sql_6, [user_id]) else {'total_likes': 0}
        threads = db.query(sql_7, [user_id, user_id, user_id, user_id]) or []

        return user, products, reviews, totals, likes, total_likes, threads
    
    return user, products, reviews, totals

def send_message(message, product_id, messanger, messaged):
    sql = """INSERT INTO messages (string, product_id, messanger, messaged, time_sent) VALUES (?, ?, ?, ?, datetime('now'))"""
    db.execute(sql, [message, product_id, messanger, messaged])

def get_messaged(product_id):
    sql = """SELECT creator_id FROM posts WHERE id = ?"""
    return db.query(sql, [product_id])[0][0]

def get_thread(product_id, user_id):

    sql_1 = """SELECT m.id, m.string, m.time_sent, m.product_id, m.messanger sender_id, m.messaged recipient_id,
    sender.username sender_username, recipient.username recipient_username
    FROM messages m JOIN users sender ON sender.id = m.messanger
    JOIN users recipient ON recipient.id = m.messaged
    WHERE m.product_id = ?
    AND (m.messanger = ? OR m.messaged = ?)
    ORDER BY m.time_sent DESC;"""

    sql_2 = """SELECT u.id, u.username, p.title 
    FROM users u, posts p 
    WHERE p.creator_id = u.id AND p.id = ?"""

    seller_id, seller_username, title = db.query(sql_2, [product_id])[0]
    return seller_id, seller_username, title, db.query(sql_1, [product_id, user_id, user_id])

def make_review(title, reviewer, text, rating, product_id):
    sql = """INSERT INTO reviews (title, reviewer, review, rating, time_posted, product_id) 
    VALUES (?, ?, ?, ?, datetime('now'), ?)"""
    db.execute(sql, [title, reviewer, text, rating, product_id])
    return db.last_insert_id

def get_reviews(product_id):
    sql = """SELECT r.id, r.title, r.reviewer, u.username, r.review, r.rating, r.time_posted 
    FROM reviews r, users u WHERE u.id = r.reviewer AND r.product_id = ?"""
    reviews = db.query(sql, [product_id]) or []
    return reviews

def delete_review(review_id):
    sql = """DELETE FROM reviews WHERE id = ?"""
    db.execute(sql, [review_id])