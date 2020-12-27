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

from flask import redirect, render_template, request, session
from functools import wraps
import os, random
from cs50 import SQL
from src import meme

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
    meme.meme(message)
    # The random variable prevents browser caching by adding a
    # randomly generated query string to each request for the dynamic image.
    return render_template("error.html", random=random.randint(1,32500))