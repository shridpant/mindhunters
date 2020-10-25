from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from functools import wraps
import os
from cs50 import SQL
from tempfile import mkdtemp
from werkzeug.utils import secure_filename
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

<<<<<<< HEAD
=======


>>>>>>> bff7908fc0d7db42d527cd06d59a53066f8a76aa
#######
import pickle
import pandas as pd
import numpy as np
import string
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk import pos_tag
from nltk.tokenize import word_tokenize
<<<<<<< HEAD
=======
from sklearn.feature_extraction.text import CountVectorizer
>>>>>>> bff7908fc0d7db42d527cd06d59a53066f8a76aa
from tensorflow.keras.models import load_model

from keras.models import Model
from keras.layers import Dense, Input, Dropout, LSTM, Activation
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.initializers import glorot_uniform

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
stop_words.update(list(string.punctuation))

def get_simple_pos(tag) :
    if tag.startswith('J') :
        return wordnet.ADJ
    elif tag.startswith('V') :
        return wordnet.VERB
    elif tag.startswith('N') :
        return wordnet.NOUN
    elif tag.startswith('R') :
        return wordnet.ADV
    else:
        return wordnet.NOUN

max_len = 30
def clean_text(review) :
    global max_len 
    words = word_tokenize(review)
    output_words = []
    for word in words :
        if word.lower() not in stop_words :
            pos = pos_tag([word])
            clean_word = lemmatizer.lemmatize(word,pos = get_simple_pos(pos[0][1]))
            output_words.append(clean_word.lower())
    max_len = max(max_len, len(output_words))
    return " ".join(output_words)

def read_glove_vecs(glove_file):
    with open(glove_file, 'r', encoding="utf8") as file:
        word_to_vec_map = {}
        word_to_index = {}
        index_to_word = {}
        index = 0
        for line in file:
            line = line.strip().split()
            curr_word = line[0]
            word_to_index[curr_word] = index
            index_to_word[index] = curr_word
            word_to_vec_map[curr_word] = np.array(line[1:], dtype=np.float64)
            index += 1
    return word_to_index, index_to_word, word_to_vec_map

def sentences_to_indices(X, word_to_index, max_len):
    m = len(X)
    X_indices = np.zeros((m, max_len))
    for i in range(m):
        sentence_words = [w.lower() for w in X[i].split()]
        j = 0
        for word in sentence_words:
            if word in word_to_index:
                X_indices[i, j] = word_to_index[word]
            j += 1
    return X_indices

#word_to_index, index_to_word, word_to_vec_map = read_glove_vecs('glove.6B.50d.txt')
filename = 'word_to_index.pkl'
word_to_index =  pickle.load(open(filename, 'rb')) 
print(len(word_to_index))

model = load_model('model.h5')
#print(model.summary())

#######


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
    user_id_info = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])[0]
    dp = "static/dp/" + user_id_info['username'] + "." + user_id_info['dp']
    if not os.path.exists(dp):
        dp = "../static/dp/"+"default.png"
    else:
        dp = "../static/dp/" + user_id_info['username'] + "." + user_id_info['dp']
    return user_id_info, dp

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
    userInfo, dp = UserInfo()
    if request.method == "GET":
        get_posts = db.execute("SELECT * FROM :tablename", tablename=userInfo['username'])
        if get_posts:
            return render_template("index.html", posts=get_posts, dp=dp, user=userInfo, reputation = ((userInfo['score']/userInfo['total'])*10))
        else:
            return render_template("index.html")
    else:
        post_text = request.form.get("post")
        if not post_text:
            return redirect("/")
        text = clean_text(post_text)
        text = [text]
        text = sentences_to_indices(text,word_to_index,max_len)
        ans = model.predict(text)[0][0]
<<<<<<< HEAD
        db.execute("INSERT INTO :tablename ('text', 'nature') VALUES (:post_text, :score)", tablename=userInfo['username'], post_text=post_text, score=str(ans))
        if (ans < 0.4):
            score = (0.4 - ans)
            total = "{:.2f}".format(userInfo['total'] + score)
            good_score = "{:.2f}".format(userInfo['score'] + score)
            db.execute("UPDATE users SET score=:score, total=:total WHERE id=:user_id", score = good_score, total = total, user_id = session["user_id"])
=======
        #print(ans)
        if(ans < 0.5) :
            print("Not Flagged !")
            return render_template('index.html',result=f"Posted !{ans}")
        else :
            print("Flagged !")
            return render_template('index.html',result=f"Post has been flagged ! {ans}")
        try:
            db.execute("INSERT INTO :tablename ('text') VALUES (:post_text)", tablename=userInfo['username'], post_text=post_text)
>>>>>>> bff7908fc0d7db42d527cd06d59a53066f8a76aa
            return redirect("/")
        else:
            score = (ans - 0.4)
            total = "{:.2f}".format((userInfo['total'] + score))
            db.execute("UPDATE users SET total=:total WHERE id=:user_id", total = total, user_id = session["user_id"])
            return redirect("/")
        
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
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

@app.route("/<string:target>")
@login_required
def LookupProfiles(target):
    match = db.execute("SELECT * FROM users WHERE username=:target", target=target)
    if not match:
        return error("Page not found!", 404)
    # DP Search
    dp = "static/dp/" + match[0]['username'] + "." + match[0]['dp']
    if not os.path.exists(dp):
        dp = "../static/dp/"+"default.png"
    else:
        dp = "../static/dp/" + match[0]['username'] + "." + match[0]['dp']
    # Profile Feed
    get_posts = db.execute("SELECT * FROM :tablename", tablename=match[0]['username'])
    if get_posts:
        return render_template("found_profile.html", dp=dp, user=match[0], posts=get_posts, reputation=((match[0]['score']/match[0]['total'])*10))
    else:
        return render_template("found_profile.html", dp=dp, user=match[0], reputation=((match[0]['score']/match[0]['total'])*10))


@app.route("/about", methods=["GET"])
@login_required
def about():
    return render_template("about.html")

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    userInfo, dp = UserInfo()
    if request.method == "GET":
        return render_template("profile.html", userInfo=userInfo, dp=dp, reputation=((userInfo['score']/userInfo['total'])*10))
    else:
        new_bio = request.form.get("bio")
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

