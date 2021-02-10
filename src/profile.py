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

from flask import Blueprint, request, render_template, redirect, jsonify, session
from werkzeug.utils import secure_filename
from cs50 import SQL
import os
from src.auth import login_required
from src.helpers import error, UserInfo

profile = Blueprint("profile", __name__, static_folder="static", template_folder="templates")
db = SQL("sqlite:///src/main.db")

@profile.route("/me", methods=["GET", "POST"])
@login_required
def landing():
    try:
        userInfo, dp = UserInfo(db)
        if request.method == "GET":
            get_posts = db.execute("SELECT * FROM :tablename", tablename=userInfo['username'])
            if get_posts:
                return render_template("profile.html", userInfo=userInfo, dp=dp, posts=get_posts, reputation=((userInfo['score']/userInfo['total'])*10))
            else:
                return render_template("profile.html", userInfo=userInfo, dp=dp, reputation=((userInfo['score']/userInfo['total'])*10))
        else:
            new_bio = request.form.get("bio")
            like_value = None
            if request.form.get("dp_submit"):
                dp_file = request.files['dp_upload']
            else :
                dp_file=""
            if dp_file:
                filename = secure_filename(dp_file.filename)
                file_extension = filename.rsplit('.', 1)[1].lower()
                db.execute("UPDATE users SET dp=:new_dp WHERE id=:user_id", new_dp=file_extension, user_id=session["user_id"])
                dp_file.save('static/dp/' + userInfo['username'] + "." + file_extension)
                return redirect("/me")
            elif new_bio:
                db.execute("UPDATE users SET bio=:new_bio WHERE id=:user_id", new_bio=new_bio, user_id=session["user_id"])
                return redirect("/me")
            elif like_value:
                if like_value:
                    db.execute("UPDATE :tablename SET likes=likes+1 WHERE id=:like_id", like_id=like_value)
                    return jsonify(status="success")
            else:
                return redirect("/me")
    except Exception as msg:
        return error(str(msg))

@profile.route("/<string:target>", methods=["GET", "POST"])
@login_required
def LookupProfiles(target):
    try:
        userInfo, dp = UserInfo(db)
        if target == userInfo["username"]:
            return redirect("/me")
        match = db.execute("SELECT * FROM users WHERE username=:target", target=target)
        if not match:
            return error("Page not found!")
        # DP Search
        dp = "static/dp/" + match[0]['username'] + "." + match[0]['dp']
        if not os.path.exists(dp):
            dp = "../static/dp/"+"default.png"
        else:
            dp = "../static/dp/" + match[0]['username'] + "." + match[0]['dp']
        # Following?
        following = request.form.get("follow_button")
        if following == "follow":
            db.execute("INSERT INTO :tablename ('following') VALUES (:target)", tablename=userInfo["username"]+'Social', target=target)
        elif following == "unfollow":
            db.execute("DELETE FROM :tablename WHERE following=(:target)", tablename=userInfo["username"]+'Social', target=target)
        # Profile Feed
        get_posts = db.execute("SELECT * FROM :tablename", tablename=match[0]['username'])
        # SELECT EXISTS
        follow_info = db.execute("SELECT * FROM :tablename WHERE following=:target", tablename=userInfo["username"]+'Social', target=target)
        if get_posts:
            return render_template("found_profile.html", dp=dp, user=match[0], posts=get_posts, follow_info=follow_info, reputation=((match[0]['score']/match[0]['total'])*10))
        else:
            return render_template("found_profile.html", dp=dp, user=match[0], follow_info=follow_info, reputation=((match[0]['score']/match[0]['total'])*10))

    except Exception as msg:
        return error(str(msg))

