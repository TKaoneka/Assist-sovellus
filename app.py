from flask import Flask
from flask import render_template, session, request, redirect, abort, make_response, g
from werkzeug.security import generate_password_hash, check_password_hash
import config
import forum

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
    pass

@app.route("/login", methods=["GET", "POST"])
def login():
    pass

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/profile/<int:user_id>")
def show_profile(user_id):
    pass

@app.route("/new_product")
def create():
    pass

@app.route("/edit_product/<int:product_id>")
def edit_product(product_id):
    pass

@app.route("/delete_product/<int:product_id>")
def delete_product(product_id):
    pass