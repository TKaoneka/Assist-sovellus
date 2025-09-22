from flask import Flask
from flask import render_template, session, request, redirect, abort, make_response, g
from werkzeug.security import generate_password_hash, check_password_hash
import config
import forum
import sqlite3

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    products = forum.get_posts()
    return render_template("index.html", products=products)

@app.route("/search")
def search():
    search = request.args.get("searchbar")
    products = forum.get_search(search)
    return render_template("search.html", products=products)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("create_account.html")
    
    elif request.method == "POST":

        username = request.form["new_username"]
        password_1 = request.form["new_password"]
        password_2 = request.form["new_password2"]
        if password_1 != password_2:
            viesti = "Salasanat eivät ole samat. Ole hyvä ja kokeile uudestaan"
            return render_template("create_account.html", caution=viesti)
        
        hash = generate_password_hash(password_1)
        try:
            user_id = forum.create_account(username, hash)
        except sqlite3.IntegrityError:
            viesti = "Tunnus on jo käytössä. Ole hyvä ja kokeile uudestaan"
            return render_template("create_account.html", caution=viesti)
        session["id"] = user_id
        session["username"] = username
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
            viesti = "Väärä tunnus tai salasana. Kokeile uudestaan :)"
            return render_template("login.html", caution=viesti)
        
        if check_password_hash(account[1], password):
            session["id"] = account[0]
            session["username"] = username
            return redirect("/")
        else:
            viesti = "Väärä tunnus tai salasana. Kokeile uudestaan :)"
            return render_template("login.html", caution=viesti)

@app.route("/logout")
def logout():
    del session["id"]
    del session["username"]

    return redirect("/")

@app.route("/new_product", methods=["GET", "POST"])
def create_product():
    if request.method == "GET":
        return render_template("product_create.html")
    
    if request.method == "POST":

        if "cancel" in request.form:
            return redirect("/")
        
        if "confirm" in request.form:

            title = request.form["title"]
            subtitle = request.form["subtitle"]
            product_type = request.form["type"]
            thumbnail = request.files["thumbnail"]
            product_desc = request.form["product_description"]

            thumbnail_photo = thumbnail.read()
            if len(thumbnail_photo) > 1000 * 1024:
                message = "Kuva on liian suuri!"
                return render_template("product_create.html", caution=message)
            
            product_id = forum.create_product(title, session["id"], subtitle, product_type, thumbnail_photo, product_desc)
            return redirect(f"/product/{product_id}")

@app.route("/modify_product/<int:product_id>", methods=["GET", "POST"])
def modify_product(product_id):
    if request.method == "GET":
        title, creator_id, sub_title, descript, time_posted = forum.get_product(product_id)
        return render_template("product_modify.html", title=title, sub_title=sub_title, 
                           descript=descript, product_id=product_id)
    
    if request.method == "POST":

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

    return render_template("product.html", title=title, creator_id=creator_id, sub_title=sub_title, 
                           descript=descript, time_posted=time_posted, product_id=product_id)

@app.route("/delete_product/<int:product_id>", methods=["GET", "POST"])
def delete_product(product_id):
    if request.method == "GET":
        return render_template("product_delete.html", product_id=product_id)
    
    if request.method == "POST":
        if "cancel" in request.form:
            return redirect(f"/product/{product_id}")
        
        if "confirm" in request.form:
            forum.delete_product(product_id)
            return redirect("/")

@app.route("/profile/<int:user_id>")
def show_profile(user_id):
    pass

@app.route("/thumbnail/<int:product_id>")
def show_thumbnail(product_id):
    pass