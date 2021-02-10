# MIT License

# Copyright (c) 2020 Shrid Pant

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, session, request, render_template, redirect
from src.helpers import error
from functools import wraps
from cs50 import SQL

auth = Blueprint("auth", __name__, static_folder = "static", template_folder = "templates")
db = SQL("sqlite:///src/main.db")

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        # Ensure username was submitted
        if not username:
            return error("You must provide a username")
        # Ensure password was submitted
        elif not password:
            return error("You must provide a password")
        # Ensure the passwords match
        elif password != confirm:
            return error("Your passwords do not match")
        # Insert the username and hash onto the SQL database
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=generate_password_hash(password))
            db.execute("CREATE TABLE IF NOT EXISTS :tablename ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'text' TEXT NOT NULL, 'timestamp' DATETIME DEFAULT CURRENT_TIMESTAMP, 'nature' TEXT DEFAULT 'na')", tablename=username)
            db.execute("CREATE TABLE IF NOT EXISTS :tablename ('following' TEXT PRIMARY KEY NOT NULL, 'timestamp' DATETIME DEFAULT CURRENT_TIMESTAMP)", tablename=str(username)+'Social')
            return redirect("/")
        except Exception as msg:
            if "unique constraint failed" in str(msg).lower():
                return error("Username already taken")
            else:
                return error(str(msg))

@auth.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return error("You must provide username", 403)
        elif not request.form.get("password"):
            return error("You must provide password", 403)
        accountExists = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        if len(accountExists) != 1 or not check_password_hash(accountExists[0]["hash"], request.form.get("password")):
            return error("Invalid username and/or password", 403)
        session["user_id"] = accountExists[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")

@auth.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
