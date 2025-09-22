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
    sql = """INSERT INTO posts (title, creator_id, sub_title, descript, product_or_service, time_posted, image) 
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