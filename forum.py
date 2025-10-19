import db

def get_products():
    sql = """SELECT p.id, p.title, p.creator_id, p.time_posted, 
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
    db.execute(sql, [username, hash, None])
    return db.last_insert_id()

def get_account(username):
    sql = """SELECT id, password_hash FROM users WHERE username = ?"""
    return db.query(sql, [username])[0]

def create_product(title, user_id, subtitle, product_type, thumbnail_photo, product_desc):
    sql = """INSERT INTO posts (title, creator_id, sub_title, descript, tags, time_posted, image) 
    VALUES (?, ?, ?, ?, ?, datetime('now'), ?)"""
    db.execute(sql, [title, user_id, subtitle, product_desc, product_type, thumbnail_photo])
    return db.last_insert_id()

def modify_product(title, subtitle, product_desc, thumbnail_photo, product_id):
    if len(thumbnail_photo) == 0:
        sql = """UPDATE posts SET title = ?, sub_title = ?, descript = ? WHERE id = ?"""
        db.execute(sql, [title, subtitle, product_desc, product_id])
    else:
        sql = """UPDATE posts SET title = ?, sub_title = ?, descript = ?, image = ? WHERE id = ?"""
        db.execute(sql, [title, subtitle, product_desc, thumbnail_photo, product_id])

def delete_product(product_id):
    sql_1 = """UPDATE threads SET product_id = NULL WHERE product_id = ?"""
    sql_2 = """DELETE FROM posts WHERE id = ?"""
    db.execute(sql_1, [product_id])
    db.execute(sql_2, [product_id])

def get_product(product_id):
    sql = """SELECT p.title, p.creator_id, u.username, p.sub_title, p.descript, p.time_posted 
    FROM posts p, users u WHERE u.id = p.creator_id AND p.id = ?"""
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

        sql_7 = """SELECT t.id, 
                  CASE 
                      WHEN t.seller_id = ? THEN u2.username 
                      ELSE u1.username 
                  END AS username, 
                  t.product_title 
           FROM threads t 
           JOIN users u1 ON u1.id = t.seller_id 
           JOIN users u2 ON u2.id = t.buyer_id 
           WHERE t.seller_id = ? OR t.buyer_id = ?"""

        likes = db.query(sql_5, [user_id]) or [0]
        total_likes = db.query(sql_6, [user_id])[0][0] if db.query(sql_6, [user_id]) else {'total_likes': 0}
        threads = db.query(sql_7, [user_id, user_id, user_id]) or []

        return user, products, reviews, totals, likes, total_likes, threads
    
    return user, products, reviews, totals

def make_thread(new_message, product_id, product_title, sender_id):
    sql_1 = """SELECT creator_id FROM posts WHERE id = ?"""
    seller_id = db.query(sql_1, [product_id])[0][0]

    sql_2 = """INSERT INTO threads (product_id, product_title, seller_id, buyer_id) VALUES (?, ?, ?, ?)"""
    db.execute(sql_2, [product_id, product_title, seller_id, sender_id])
    thread_id =  db.last_insert_id()

    sql_3 = """INSERT INTO messages (string, thread_id, sender_id, time_sent) VALUES (?, ?, ?, datetime('now'))"""
    db.execute(sql_3, [new_message, thread_id, sender_id])
    return thread_id

def get_thread(thread_id):
    sql_1 = """SELECT m.id, m.string, m.time_sent, m.sender_id, u.username 
    FROM messages m, users u 
    WHERE m.sender_id = u.id AND m.thread_id = ? ORDER BY m.id DESC"""

    sql_2 = """SELECT t.product_id, t.product_title, t.seller_id, t.buyer_id, u.username 
    FROM threads t, users u 
    WHERE t.seller_id = u.id AND t.id = ?"""

    messages = db.query(sql_1, [thread_id])
    product_id, title, seller_id, buyer_id, seller_username = db.query(sql_2, [thread_id])[0]

    
    return messages, product_id, title, seller_id, buyer_id, seller_username
    
def send_message(message, thread_id, sender_id):
    sql = """INSERT INTO messages (string, thread_id, sender_id, time_sent) VALUES (?, ?, ?, datetime('now'))"""
    db.execute(sql, [message, thread_id, sender_id])

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

def get_photo(indicator, id):
    if indicator == "pfp":
        sql = """SELECT image FROM Users WHERE id = ?"""

    elif indicator == "thumbnail":
        sql = """SELECT image FROM posts WHERE id = ?"""

    return db.query(sql, [id])[0][0]

def add_photo(photo, user_id):
    sql = """UPDATE users SET image = ? WHERE id = ?"""
    db.execute(sql, [photo, user_id])