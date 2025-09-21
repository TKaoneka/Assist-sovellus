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
    return render_template("index.html")

@app.route("/search")
def search():
    pass

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
            return render_template("new_account.html", caution=viesti)
        session["id"] = user_id
        session["username"] = username
        return render_template("account_created.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":
        username = request.form["login_username"]
        password = request.form["login_password"]

        try:
            info = forum.get_account(username)
        except IndexError:
            viesti = "Väärä tunnus tai salasana. Kokeile uudestaan :)"
            return render_template("login.html", caution=viesti)
        
        if check_password_hash(info[1], password):
            session["id"] = info[0]
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

@app.route("/profile/<int:user_id>")
def show_profile(user_id):
    pass

@app.route("/new_product")
def create_product():
    pass

@app.route("/modify_product")
def modify_product():
    pass

@app.route("/product/<int:product_id>")
def show_product(product_id):
    pass

@app.route("/edit_product/<int:product_id>")
def edit_product(product_id):
    pass

@app.route("/delete_product/<int:product_id>")
def delete_product(product_id):
    pass