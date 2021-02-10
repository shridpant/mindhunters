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

from flask import Blueprint, request, render_template
from src.auth import login_required
from cs50 import SQL
import os

search = Blueprint("search", __name__, static_folder="static", template_folder="templates")

db = SQL("sqlite:///src/main.db")

@search.route("/search", methods=["GET", "POST"])
@login_required
def landing():
    if request.method == "GET":
        return render_template("search.html")
    else:
        target_uname = request.form.get("username")
        match=db.execute("SELECT * FROM users WHERE username=:target_uname", target_uname=target_uname)
        if not match:
            return render_template("search.html", method="POST")
        dp = "static/dp/" + match[0]['username'] + "." + match[0]['dp']
        if not os.path.exists(dp):
            dp = "../static/dp/"+"default.png"
        else:
            dp = "../static/dp/" + match[0]['username'] + "." + match[0]['dp']
        return render_template("search.html", method="POST", dp=dp, results=match)
