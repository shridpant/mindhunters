from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from functools import wraps
import os
from cs50 import SQL
from tempfile import mkdtemp
from werkzeug.utils import secure_filename
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Configure to use SQLite database
db = SQL("sqlite:///main.db")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def error(message, code=400):
    return render_template("error.html", top=code, bottom=message), code

def UserInfo():
    user_id_info = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])
    return user_id_info

@app.route("/register", methods=["GET", "POST"])
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
            return redirect("/")
        except Exception as msg:
            if "unique constraint failed" in str(msg).lower():
                return error("Username already taken")
            else:
                return error(str(msg))

@app.route("/login", methods=["GET", "POST"])
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

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    userInfo = UserInfo()[0]
    if request.method == "GET":
        get_posts = db.execute("SELECT * FROM :tablename", tablename=userInfo['username'])
        if get_posts:
            return render_template("index.html", posts=get_posts)
        else:
            return render_template("index.html")
    else:
        post_text = request.form.get("post")
        if not post_text:
            return redirect("/")
        #TODO Integrate the ML Model
        try:
            db.execute("INSERT INTO :tablename ('text') VALUES (:post_text)", tablename=userInfo['username'], post_text=post_text)
            return redirect("/")
        except:
            return error("Request could not be performed")

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    userInfo = UserInfo()[0]
    get_posts = db.execute("SELECT * FROM :tablename", tablename=userInfo['username'])
    dp = "static/dp/" + userInfo['username'] + "." + userInfo['dp']
    if not os.path.exists(dp):
        dp = "../static/dp/"+"default.png"
    else:
        dp = "../static/dp/" + userInfo['username'] + "." + userInfo['dp']
    if request.method == "GET":
        return render_template("profile.html", userInfo=userInfo, dp=dp, posts=get_posts)
    else:
        new_bio = request.form.get("bio")
        new_post = request.form.get("post")
        if request.form.get("dp_submit"):
            dp_file = request.files['dp_upload']
        else :
            dp_file=""
        if dp_file:
            filename = secure_filename(dp_file.filename)
            file_extension = filename.rsplit('.', 1)[1].lower()
            db.execute("UPDATE users SET dp=:new_dp WHERE id=:user_id", new_dp=file_extension, user_id=session["user_id"])
            dp_file.save('static/dp/' + userInfo['username'] + "." + file_extension)
            return redirect("/profile")
        elif new_bio:
            db.execute("UPDATE users SET bio=:new_bio WHERE id=:user_id", new_bio=new_bio, user_id=session["user_id"])
            return redirect("/profile")
        elif new_post:
            try:
                db.execute("INSERT INTO :tablename ('text') VALUES (:post_text)", tablename=userInfo['username'], post_text=new_post)
                return redirect("/profile")
            except:
                return error("Request could not be performed")
        else:
            return redirect("/profile")

# Error handler
def errorhandler(e):
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return error(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run(debug=True)

