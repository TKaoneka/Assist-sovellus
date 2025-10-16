from flask import Flask
from flask import render_template, session, request, redirect, flash, abort, make_response, g
from werkzeug.security import generate_password_hash, check_password_hash
import config
import forum
import sqlite3
import secrets

app = Flask(__name__)
app.secret_key = config.secret_key

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index():
    products = forum.get_posts()
    return render_template("index.html", products=products)

@app.route("/search")
def search():
    search = request.args.get("searchbar")
    products = forum.get_search(search)
    return render_template("search.html", result=search, products=products)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("create_account.html")
    
    elif request.method == "POST":

        username = request.form["new_username"]
        password_1 = request.form["new_password"]
        password_2 = request.form["new_password2"]
        if password_1 != password_2:
            flash("Salasanat eivät ole samat. Ole hyvä ja kokeile uudestaan")
            return render_template("create_account.html")
        
        hash = generate_password_hash(password_1)
        try:
            user_id = forum.create_account(username, hash)
        except sqlite3.IntegrityError:
            flash("Tunnus on jo käytössä. Ole hyvä ja kokeile uudestaan")
            return render_template("create_account.html")
        session["id"] = user_id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":
        username = request.form["login_username"]
        password = request.form["login_password"]

        try:
            account = forum.get_account(username)
        except IndexError:
            flash("Väärä tunnus tai salasana. Kokeile uudestaan :)")
            return render_template("login.html")
        
        if check_password_hash(account[1], password):
            session["id"] = account[0]
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("Väärä tunnus tai salasana. Kokeile uudestaan :)")
            return render_template("login.html")

@app.route("/logout")
def logout():
    del session["id"]
    del session["username"]
    del session["csrf_token"]

    return redirect("/")

@app.route("/new_product", methods=["GET", "POST"])
def create_product():

    if request.method == "GET":
        return render_template("product_create.html")
    
    if request.method == "POST":
        check_csrf()

        if "cancel" in request.form:
            return redirect("/")
        
        if "confirm" in request.form:

            title = request.form["title"]
            subtitle = request.form["subtitle"]
            product_type = request.form["type"]
            product_tags = request.form["tags"]
            tags = product_type + product_tags
            thumbnail = request.files["thumbnail"]
            product_desc = request.form["product_description"]

            thumbnail_photo = thumbnail.read()
            if len(thumbnail_photo) > 1000 * 1024:
                message = "Kuva on liian suuri!"
                return render_template("product_create.html", caution=message)
            
            product_id = forum.create_product(title, session["id"], subtitle, tags, thumbnail_photo, product_desc)
            return redirect(f"/product/{product_id}")

@app.route("/modify_product/<int:product_id>", methods=["GET", "POST"])
def modify_product(product_id):

    if request.method == "GET":
        title, creator_id, sub_title, descript, time_posted = forum.get_product(product_id)
        return render_template("product_modify.html", title=title, sub_title=sub_title, 
                           descript=descript, product_id=product_id)
    
    if request.method == "POST":
        check_csrf()

        if "cancel" in request.form:
            return redirect(f"/product/{product_id}")
        
        if "confirm" in request.form:
            title = request.form["title"]
            subtitle = request.form["subtitle"]
            product_desc = request.form["product_description"]

            forum.modify_product(title, subtitle, product_desc, product_id)
            return redirect(f"/product/{product_id}")

@app.route("/product/<int:product_id>")
def show_product(product_id):
    title, creator_id, sub_title, descript, time_posted = forum.get_product(product_id)
    reviews = forum.get_reviews(product_id)

    return render_template("product.html", title=title, creator_id=creator_id, sub_title=sub_title, 
                           descript=descript, time_posted=time_posted, product_id=product_id, reviews=reviews)

@app.route("/delete_product/<int:product_id>", methods=["GET", "POST"])
def delete_product(product_id):

    if request.method == "GET":
        return render_template("product_delete.html", product_id=product_id)
    
    if request.method == "POST":
        check_csrf()

        if "delete_product" in request.form:
            return render_template("product_delete.html", product_id=product_id)
        
        if "cancel" in request.form:
            return redirect(f"/product/{product_id}")
        
        if "confirm" in request.form:
            forum.delete_product(product_id)
            return redirect("/")
        
@app.route("/new_thread/<int:product_id>", methods=["POST"])
def make_thread(product_id):
    check_csrf()
    first_message = request.form["first_message"]
    thread_id = forum.make_thread(first_message, product_id, session["id"])
    return redirect(f"/thread/{thread_id}")

@app.route("/thread/<int:thread_id>")
def show_thread(thread_id):
    messages, product_id, title, seller_id, seller_username = forum.get_thread(thread_id)
    return render_template("thread.html", product_id=product_id, title=title, seller_id=seller_id, seller_username=seller_username, messages=messages, thread_id=thread_id)

@app.route("/new_message/<int:thread_id>", methods=["POST"])
def send_message(thread_id):
    check_csrf()

    message = request.form["message"]
    forum.send_message(message, thread_id, session["id"])
    return redirect(f"/thread/{thread_id}")

@app.route("/new_review/<int:product_id>", methods=["POST"])
def make_review(product_id):
    check_csrf()
    
    title = request.form["review_title"]
    text = request.form["review_text"] or ""
    rating = request.form["rating"]
    review_id = forum.make_review(title, session["id"], text, rating, product_id)
    return redirect(f"/product/{product_id}#{review_id}")

@app.route("/delete_review/<int:review_id>", methods=["POST"])
def delete_review(review_id):
    check_csrf()
    
    forum.delete_review(review_id)
    return redirect(f"/")

@app.route("/profile/<int:user_id>")
def show_profile(user_id):

    if session["id"] == user_id:
        user, products, reviews, totals, likes, total_likes, threads = forum.get_profile(user_id, True)

        return render_template("profile.html", user=user, user_id=user_id, total_posts=totals[0], products=products, 
                               total_reviews=totals[1], avg_rating=totals[2], reviews=reviews, 
                               total_likes=total_likes, likes=likes, threads=threads)
    else:
        user, products, reviews, totals = forum.get_profile(user_id, False)

        return render_template("profile.html", user=user, user_id=user_id, total_posts=totals[0], products=products, 
                               total_reviews=totals[1], avg_rating=totals[2], reviews=reviews)

@app.route("/thumbnail/<int:product_id>")
def show_thumbnail(product_id):
    pass

@app.route("/add_pfp")
def add_pfp():
    pass

@app.route("/pfp/<int:user_id>")
def show_pfp(user_id):

    pass