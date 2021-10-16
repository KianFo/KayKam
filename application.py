from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from tools import login_required
from tempfile import mkdtemp
from flask_session import Session



app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///barca.db")

@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST","GET"])
def login():

    session.clear()

    if request.method == "POST":

        name = request.form.get("username")
        password = request.form.get("password")

        if not name:
            return render_template("test1.html")
        elif not password:
            return render_template("test1.html")


        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("test1.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")



@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":

        name = request.form.get("username")
        password = request.form.get("password")
        pshash = generate_password_hash(password)
        confirm = request.form.get("confirmation")

        if not name:
            return render_template("test1.html")
        elif not password:
            return render_template("test1.html")
        elif not confirm:
            return render_template("test1.html")
        elif confirm != password:
            return render_template("test1.html")

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", name, pshash)
        except:
            return render_template("test1.html")


        return redirect("/login")

    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/quize", methods=["GET", "POST"])
def quize():
   if request.method == "POST":
       pass

   else:
       return render_template("quize.html")


