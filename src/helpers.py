from flask import redirect, render_template, request, session
from functools import wraps
import os
from cs50 import SQL

def UserInfo(db):
    user_id_info = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])[0]
    dp = "static/dp/" + user_id_info['username'] + "." + user_id_info['dp']
    if not os.path.exists(dp):
        dp = "../static/dp/"+"default.png"
    else:
        dp = "../static/dp/" + user_id_info['username'] + "." + user_id_info['dp']
    return user_id_info, dp

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def error(message, code=400):
    return render_template("error.html", top=code, bottom=message), code