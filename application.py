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
    user_id = session["user_id"]
    name = session["username"]
    return render_template("index.html", name=name)


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
        session["username"] = rows[0]["username"]
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
    user_id = session["user_id"]
    try:
        name = session["username"]
        return render_template("quize.html", name=name)
    except:
        pass


@app.route("/news", methods=["GET", "POST"])
def news():
    name = session["username"]
    return render_template("news.html", name=name)

@app.route("/news1")
def news1():
    name = session["username"]
    return render_template("news1.html", name=name)

@app.route("/news2")
def news2():
    name = session["username"]
    return render_template("news2.html", name=name)

@app.route("/news3")
def news3():
    name = session["username"]
    return render_template("news3.html", name=name)

@app.route("/news4")
def news4():
    name = session["username"]
    return render_template("news4.html", name=name)

@app.route("/news5")
def news5():
    name = session["username"]
    return render_template("news5.html", name=name)

@app.route("/news6")
def news6():
    name = session["username"]
    return render_template("news6.html", name=name)

@app.route("/news7")
def news7():
    name = session["username"]
    return render_template("news7.html", name=name)

@app.route("/news8")
def news8():
    name = session["username"]
    return render_template("news8.html", name=name)


@app.route("/profile", methods=["POST", "GET"])
def profile():
    if request.method == "POST":
        name = session["username"]
        user_id = session["user_id"]

        card_number = request.form.get("card_number")
        card_password = request.form.get("card_password")
        name = db.execute("SELECT username FROM users WHERE id=?", user_id)[0]["username"]


        try:
            db.execute("INSERT INTO credit (name, card_password, card_number, user_id) VALUES (?, ?, ?, ?)", name, card_password, card_number, user_id)
        except:
            return render_template("test1.html")

        return redirect("/")

    else:
        user_id = session["user_id"]
        name = session["username"]
        return render_template("profile.html", name = name)