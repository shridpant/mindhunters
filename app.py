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

from flask import Flask
from flask_session import Session
from werkzeug.exceptions import HTTPException, InternalServerError
from src.auth import auth, login_required
from src.helpers import UserInfo, error
from src.profile import profile
from src.search import search
from src.home import home

app = Flask(__name__)
app.config.from_object("config")

app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(profile, url_prefix="/")
app.register_blueprint(home, url_prefix="/")
app.register_blueprint(search, url_prefix="/")

Session(app)
        
@app.errorhandler(Exception)
def errorhandler(e):
    print(str(e))
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return error(e.name, e.code)

if __name__ == "__main__":
    app.run()