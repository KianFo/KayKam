from flask import Flask, redirect, render_template, request, session
from flask.scaffold import F
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
            error = "Please enter a username"
            return render_template("login.html", error=error)
        if not password:
            error_pas = "Please enter a password"
            return render_template("login.html", error_pas=error_pas)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            error_pas = "Your password is not correct !"
            return render_template("login.html", error_pas=error_pas)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        session["first_name"] = rows[0]["first_name"]
        session["last_name"] = rows[0]["last_name"]
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
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")


        if not first_name:
            error_first = "Please enter first name"
            return render_template("register.html", error_first=error_first)

        if not last_name:
            error_last = "Please enter lastname"
            return render_template("register.html", error_last=error_last)

        if not name:
            error = "Please enter a username"
            return render_template("register.html", error=error)

        if not password:
            error_pas = "Please enter a password"
            return render_template("register.html", error_pas=error_pas)

        if not confirm:
            error_confirm = "Please enter confirmation"
            return render_template("register.html", error_confirm=error_confirm)


        length = len(str(db.execute("SELECT * FROM users WHERE username =? ", name)))
        if length > 2:
            error = "This username has been already taken"
            return render_template("register.html", error=error)


        pas_length = len(str(password))
        if pas_length < 4:
            error_pas = "Your password should be at least 4 letters or numbers"
            return render_template("register.html", error_pas=error_pas)


        if confirm != password:
            error_confirm = "Your confirmation in not the same as your password"
            return render_template("register.html", error_confirm = error_confirm)


        try:
            db.execute("INSERT INTO users (username, hash, first_name, last_name) VALUES (?, ?, ?, ?)", name, pshash, first_name, last_name)
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
        first = session["first_name"]
        last = session["last_name"]

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
        first = session["first_name"]
        last = session["last_name"]
        return render_template("profile.html", name = name, first=first, last=last)


@app.route("/changepass", methods=["POST","GET"])
def changepass():
    if request.method == "POST":
        name_new = request.form.get("pass_new")
        confirm_new = request.form.get("pass_confirm")
        hashnew = generate_password_hash(name_new)
        user_id = session["user_id"]

        if not name_new:
            error_pass = "Please enter New Password"
            return render_template("change_pass.html", error_pass=error_pass)

        if not confirm_new:
            error_confirm = "Please enter confirmation"
            return render_template("change_pass.html", error_confirm=error_confirm)

        try:
            db.execute("UPDATE users SET hash=? WHERE id=?", hashnew, user_id)
        except:
            return render_template("test1.html")

        session.clear()

        return redirect("/login")

    else:
        return render_template("change_pass.html")


@app.route("/change_F_L", methods=["GET","POST"])
def change_F_L():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        user_id = session["user_id"]
        
        try:
            db.execute("UPDATE users SET first_name=? WHERE id=?", first_name, user_id)
        except:
            return render_template("test1.html")

        try:
            db.execute("UPDATE users SET last_name=? WHERE id=?", last_name, user_id)
        except:
            return render_template("test1.html")

        session.clear()

        return redirect("/login")
    else:
        return render_template("change_F_L.html")





@app.route("/credit", methods=["POST", "GET"])
def credit():
    if request.method == "POST":
    
        try:
            card_number = request.form.get("credit_number")
        except:
            card_numbere = "Please enter card number"
            return render_template("credit.html", card_numbere=card_numbere)


        try:
            card_password = (request.form.get("password"))
        except:
            passworde = "Please enter your password"
            return render_template("credit.html", passworde=passworde)

        
        if not card_number:
            card_numbere = "Please enter card number"
            return render_template("credit.html", card_numbere=card_numbere)

        
        if not card_password:
            passworde = "Please enter your password"
            return render_template("credit.html", passworde=passworde)

        card_number = request.form.get("credit_number")
        card_password = (request.form.get("password"))
        owner = session["username"]
        user_id = session["user_id"]
        pas = generate_password_hash(card_password)

        
        name2 = session["username"]

        test_length = len(db.execute("SELECT name FROM credit WHERE card_number=?", card_number))

        if test_length > 0:
            card_numbere = "Card_number has already been taken"
            return render_template("credit.html", card_numbere=card_numbere)


        try:
            db.execute("INSERT INTO credit (user_id, name, card_number, card_password) VALUES (?, ?, ?, ?)", user_id, owner, card_number, pas)
        except:
            return render_template("test1.html")

        message = "You successfully created an account, by deffault you have an amount of"

        cash = 150

        return render_template("raw.html", message=message, cash=cash)

    else:
        return render_template("credit.html")


@app.route("/charge", methods=["POST", "GET"])
def charge():
    if request.method == "POST":
        try:
            card_number = request.form.get("card_number")
        except:
            card_numbere = "Please enter your card number"
            return render_template("charge.html", card_numbere=card_numbere)


        try:
            password = request.form.get("password")
        except:
            passworde = "Please enter your password"
            return render_template("charge.html", passworde=passworde)


        if not card_number:
            card_numbere = "Please enter your card number"
            return render_template("charge.html", card_numbere=card_numbere)

        if not password:
            passworde = "Please enter your password"
            return render_template("charge.html", passworde=passworde)

        card_number = request.form.get("card_number")
        password = request.form.get("password")
        

        name2 = session["username"]

        test_length = len(db.execute("SELECT card_number FROM credit WHERE name=?", name2))

        if test_length == 1:
            card_numbere = "Card_number invalid"
            return render_template("charge.html", card_numbere=card_numbere)

        try:
            cash = int(request.form.get("cash"))
        except:
            cashe = "Please insert amount of cash you want"
            return render_template("charge.html", cashe=cashe)


        try:
            user = db.execute("SELECT * FROM credit WHERE card_number=?", card_number)
            passw = user[0]["card_password"]
            cash1 = int(user[0]["cash"])
            newcash = cash + cash1
        except:
            message = "Wrong input values!"
            return render_template("charge.html", cashe=message) ##################



        if len(user) != 1 or not check_password_hash(passw, request.form.get("password")):
            return render_template("test1.html")

        try:
            db.execute("UPDATE credit SET cash=? WHERE card_number=?", newcash, card_number)
        except:
            return render_template("test.html")

        message = "Your card is successfully charged by"

        return render_template("raw.html", message=message, cash=cash)

    else:
        return render_template("charge.html")



@app.route("/shop", methods=["POST", "GET"])
def shop():
    if request.method == "POST":
        user_id = session["user_id"]
        name = session["user_name"]
        return render_template("test1")
    
    else:
        name = session["username"]
        return render_template("shop.html", name=name)




#\@app.route("/product1", methods=["GET", "POST"])
#def product1():
    #if request.method == "POST":

        #id = request.form.get("id")
        #user_id = session["user_id"]

        
        #test_length = len(db.execute("SELECT number FROM cart WHERE pid=? AND user_id=?", id, user_id))
        
        #if test_length == 0:

            #try:
                #db.execute("INSERT INTO cart (user_id, pid, number) VALUES (?, ?, ?)", user_id, id, 1)
            #except:
                #return render_template("test1")

        #else:
            #try:
                #number1 = db.execute("SELECT number FROM cart WHERE pid=? AND user_id=?", id, user_id)
                #number1 += 1
                #db.execute("UPDATE cart SET number=? WHERE user_id=? AND pid=?", number1, user_id, id)
            #except:
                #return render_template("test1.html")

        #return redirect









@app.route("/product1", methods=["GET", "POST"])
def product1():
    if request.method == "POST":

        user_id = session["user_id"]
        number = request.form.get("number")
        pid = request.form.get("id")
        name = session["username"]
        price = db.execute("SELECT price FROM products WHERE pid=1")[0]["price"]
        pname = db.execute("SELECT pname FROM products WHERE pid=1")[0]["pname"]


#        return render_template("iner.html", a=pname, b=price)

        if request.form.get("number") == "none":
            return render_template("product1.html")     ################

#        return render_template("iner.html", a=user_id, b=number, c=pid, d=name)


        # db.execute("INSERT INTO credit (user_id, name, card_number, card_password) VALUES (?, ?, ?, ?)", user_id, owner, card_number, pas)

        kiankhar = 64

        cart_length = len(db.execute("SELECT * FROM cart WHERE user_id=? AND pid=?", user_id, pid))

#        return render_template("iner.html", a=user_id, b=number, c=pid, d=cart_length)
        if cart_length != 0:
            try:
                db.execute("UPDATE cart SET number=? WHERE user_id=? AND pid=?", number, user_id, pid)
            except:
                return render_template("test1.html")

            return redirect("/shop")
#        return render_template("iner.html")
        try:
            db.execute("INSERT INTO cart (user_id, pid, number, price, pname) VALUES (?, ?, ?, ?, ?)", user_id, pid, number, price, pname)
        except:
            return render_template("test1.html")
#        try:
 #           db.execute("INSERT INTO cart (user_id, pid, number) VALUES (?, ?, ?)", user_id, pid, number)
#        except:
        return redirect("/shop")
#            return render_template("test1.html")

#        return redirect("/")

    else:
        name = session["username"]
        return render_template("product1.html", name=name)          ###################











@app.route("/product2", methods=["GET", "POST"])
def product2():
    if request.method == "POST":

        user_id = session["user_id"]
        number = request.form.get("number")
        pid = request.form.get("id")
        name = session["username"]
        price = db.execute("SELECT price FROM products WHERE pid=2")[0]["price"]
        pname = db.execute("SELECT pname FROM products WHERE pid=2")[0]["pname"]


        if request.form.get("number") == "none":
            return render_template("product2.html")     ################

#        return render_template("iner.html", a=user_id, b=number, c=pid, d=name, e=price, f=pname)


        # db.execute("INSERT INTO credit (user_id, name, card_number, card_password) VALUES (?, ?, ?, ?)", user_id, owner, card_number, pas)

        kiankhar = 64

        cart_length = len(db.execute("SELECT * FROM cart WHERE user_id=? AND pid=?", user_id, pid))

#        return render_template("iner.html", a=user_id, b=number, c=pid, d=cart_length)
        if cart_length != 0:
            try:
                db.execute("UPDATE cart SET number=? WHERE user_id=? AND pid=?", number, user_id, pid)
            except:
                return render_template("test1.html")

            return redirect("/shop")
#        return render_template("iner.html")
        try:
            db.execute("INSERT INTO cart (user_id, pid, number, price, pname) VALUES (?, ?, ?, ?, ?)", user_id, pid, number, price, pname)
        except:
            return render_template("test1.html")
#        try:
 #           db.execute("INSERT INTO cart (user_id, pid, number) VALUES (?, ?, ?)", user_id, pid, number)
#        except:
        return redirect("/shop")
#            return render_template("test1.html")

#        return redirect("/")

    else:
        name = session["username"]
        return render_template("product2.html", name=name)          ###################












@app.route("/product3", methods=["GET", "POST"])
def product3():
    if request.method == "POST":

        user_id = session["user_id"]
        number = request.form.get("number")
        pid = request.form.get("id")
        name = session["username"]
        price = db.execute("SELECT price FROM products WHERE pid=3")[0]["price"]
        pname = db.execute("SELECT pname FROM products WHERE pid=3")[0]["pname"]


        if request.form.get("number") == "none":
            return render_template("product3.html")     ################

#        return render_template("iner.html", a=user_id, b=number, c=pid, d=name)


        # db.execute("INSERT INTO credit (user_id, name, card_number, card_password) VALUES (?, ?, ?, ?)", user_id, owner, card_number, pas)

        kiankhar = 64

        cart_length = len(db.execute("SELECT * FROM cart WHERE user_id=? AND pid=?", user_id, pid))

#        return render_template("iner.html", a=user_id, b=number, c=pid, d=cart_length)
        if cart_length != 0:
            try:
                db.execute("UPDATE cart SET number=? WHERE user_id=? AND pid=?", number, user_id, pid)
            except:
                return render_template("test1.html")

            return redirect("/shop")
#        return render_template("iner.html")
        try:
            db.execute("INSERT INTO cart (user_id, pid, number, price, pname) VALUES (?, ?, ?, ?, ?)", user_id, pid, number, price, pname)
        except:
            return render_template("test1.html")
#        try:
 #           db.execute("INSERT INTO cart (user_id, pid, number) VALUES (?, ?, ?)", user_id, pid, number)
#        except:
        return redirect("/shop")
#            return render_template("test1.html")

#        return redirect("/")

    else:
        name = session["username"]
        return render_template("product3.html", name=name)          ###################












@app.route("/product4", methods=["GET", "POST"])
def product4():
    if request.method == "POST":

        user_id = session["user_id"]
        number = request.form.get("number")
        pid = request.form.get("id")
        name = session["username"]

        price = db.execute("SELECT price FROM products WHERE pid=4")[0]["price"]
        pname = db.execute("SELECT pname FROM products WHERE pid=4")[0]["pname"]



        if request.form.get("number") == "none":
            return render_template("product4.html")     ################

#        return render_template("iner.html", a=user_id, b=number, c=pid, d=name)


        # db.execute("INSERT INTO credit (user_id, name, card_number, card_password) VALUES (?, ?, ?, ?)", user_id, owner, card_number, pas)

        kiankhar = 64

        cart_length = len(db.execute("SELECT * FROM cart WHERE user_id=? AND pid=?", user_id, pid))

#        return render_template("iner.html", a=user_id, b=number, c=pid, d=cart_length)
        if cart_length != 0:
            try:
                db.execute("UPDATE cart SET number=? WHERE user_id=? AND pid=?", number, user_id, pid)
            except:
                return render_template("test1.html")

            return redirect("/shop")
#        return render_template("iner.html")
        try:
            db.execute("INSERT INTO cart (user_id, pid, number, price, pname) VALUES (?, ?, ?, ?, ?)", user_id, pid, number, price, pname)

        except:
            return render_template("test1.html")
#        try:
 #           db.execute("INSERT INTO cart (user_id, pid, number) VALUES (?, ?, ?)", user_id, pid, number)
#        except:
        return redirect("/shop")
#            return render_template("test1.html")

#        return redirect("/")

    else:
        name = session["username"]
        return render_template("product4.html", name=name)          ###################










@app.route("/product5", methods=["GET", "POST"])
def product5():
    if request.method == "POST":

        user_id = session["user_id"]
        number = request.form.get("number")
        pid = request.form.get("id")
        name = session["username"]
        price = db.execute("SELECT price FROM products WHERE pid=5")[0]["price"]
        pname = db.execute("SELECT pname FROM products WHERE pid=5")[0]["pname"]


        if request.form.get("number") == "none":
            return render_template("product5.html")     ################

#        return render_template("iner.html", a=user_id, b=number, c=pid, d=name)


        # db.execute("INSERT INTO credit (user_id, name, card_number, card_password) VALUES (?, ?, ?, ?)", user_id, owner, card_number, pas)

        kiankhar = 64

        cart_length = len(db.execute("SELECT * FROM cart WHERE user_id=? AND pid=?", user_id, pid))

#        return render_template("iner.html", a=user_id, b=number, c=pid, d=cart_length)
        if cart_length != 0:
            try:
                db.execute("UPDATE cart SET number=? WHERE user_id=? AND pid=?", number, user_id, pid)
            except:
                return render_template("test1.html")

            return redirect("/shop")
#        return render_template("iner.html")
        try:
            db.execute("INSERT INTO cart (user_id, pid, number, price, pname) VALUES (?, ?, ?, ?, ?)", user_id, pid, number, price, pname)
        except:
            return render_template("test1.html")
#        try:
 #           db.execute("INSERT INTO cart (user_id, pid, number) VALUES (?, ?, ?)", user_id, pid, number)
#        except:
        return redirect("/shop")
#            return render_template("test1.html")

#        return redirect("/")

    else:
        name = session["username"]
        return render_template("product5.html", name=name)          ###################










@app.route("/product6", methods=["GET", "POST"])
def product6():
    if request.method == "POST":

        user_id = session["user_id"]
        number = request.form.get("number")
        pid = request.form.get("id")
        name = session["username"]
        price = db.execute("SELECT price FROM products WHERE pid=6")[0]["price"]
        pname = db.execute("SELECT pname FROM products WHERE pid=6")[0]["pname"]


        if request.form.get("number") == "none":
            return render_template("product6.html")     ################

#        return render_template("iner.html", a=user_id, b=number, c=pid, d=name)


        # db.execute("INSERT INTO credit (user_id, name, card_number, card_password) VALUES (?, ?, ?, ?)", user_id, owner, card_number, pas)

        kiankhar = 64

        cart_length = len(db.execute("SELECT * FROM cart WHERE user_id=? AND pid=?", user_id, pid))

#        return render_template("iner.html", a=user_id, b=number, c=pid, d=cart_length)
        if cart_length != 0:
            try:
                db.execute("UPDATE cart SET number=? WHERE user_id=? AND pid=?", number, user_id, pid)
            except:
                return render_template("test1.html")

            return redirect("/shop")
#        return render_template("iner.html")
        try:
            db.execute("INSERT INTO cart (user_id, pid, number, price, pname) VALUES (?, ?, ?, ?, ?)", user_id, pid, number, price, pname)
        except:
            return render_template("test1.html")
#        try:
 #           db.execute("INSERT INTO cart (user_id, pid, number) VALUES (?, ?, ?)", user_id, pid, number)
#        except:
        return redirect("/shop")
#            return render_template("test1.html")

#        return redirect("/")

    else:
        name = session["username"]
        return render_template("product6.html", name=name)          ###################


@app.route("/cart", methods=["POST","GET"])
def cart():
    if request.method == "POST":
        pass
    else:
        user_id = session["user_id"]


        num1 = 0
        num2 = 0
        num3 = 0
        num4 = 0
        num5 = 0
        num6 = 0

        price1 = 0
        price2 = 0
        price3 = 0
        price4 = 0
        price5 = 0
        price6 = 0

        try:
            num1 = db.execute("SELECT number FROM cart WHERE user_id=? AND pid=1", user_id)[0]["number"]
            price1 = db.execute("SELECT price FROM products WHERE pid=1")[0]["price"]
        except:
            pass

        try:
            num2 = db.execute("SELECT number FROM cart WHERE user_id=? AND pid=2", user_id)[0]["number"]
            price2 = db.execute("SELECT price FROM products WHERE pid=2")[0]["price"]
        except:
            pass

        try:
            num3 = db.execute("SELECT number FROM cart WHERE user_id=? AND pid=3", user_id)[0]["number"]
            price3 = db.execute("SELECT price FROM products WHERE pid=3")[0]["price"]
        except:
            pass

        try:
            num4 = db.execute("SELECT number FROM cart WHERE user_id=? AND pid=4", user_id)[0]["number"]
            price4 = db.execute("SELECT price FROM products WHERE pid=4")[0]["price"]
        except:
            pass

        try:
            num5 = db.execute("SELECT number FROM cart WHERE user_id=? AND pid=5", user_id)[0]["number"]
            price5 = db.execute("SELECT price FROM products WHERE pid=5")[0]["price"]
        except:
            pass

        try:
            num6 = db.execute("SELECT number FROM cart WHERE user_id=? AND pid=6", user_id)[0]["number"]
            price6 = db.execute("SELECT price FROM products WHERE pid=6")[0]["price"]
        except:
            pass


        all1 = 0
        all2 = 0
        all3 = 0
        all4 = 0
        all5 = 0
        all6 = 0


        try:
            all1 = float(num1) * float(price1)
        except:
            pass

        try:
            all2 = float(num2) * float(price2)
        except:
            pass

        try:
            all3 = float(num3) * float(price3)
        except:
            pass           

        try:
            all4 = float(num4) * float(price4)
        except:
            pass          

        try:
            all5 = float(num5) * float(price5)
        except:
            pass

        try:
            all6 = float(num6) * float(price6)
        except:
            pass

        allnum = num1 + num2 + num3 + num4 + num5 + num6


        allprice = float(all1) + float(all2) + float(all3) + float(all4) + float(all5) + float(all6)

#        return render_template("iner.html", a=all1, b=all2, c=all3, d=allprice, e=all4, f=all5, g=all6)

        user_id = session["user_id"]
        products = db.execute("SELECT * FROM cart WHERE user_id = ?", user_id)

        if len(products) == 0:
            main = "You haven't add anything to your cart!"
            message = "by going to shop page, you can add sth to your cart!" 
            return render_template("fail.html", main=main, message=message)

        name = session["username"]
        return render_template("cart.html", products=products, allprice=round(allprice), name=name, all1=all1, all2=all2, all3=all3, all4=all4, all5=all5, all6=all6, allnum=allnum)


@app.route("/delete", methods=["POST", "GET"])
def delete():
    if request.method == "POST":
        pid = request.form.get("id")
        user_id = session["user_id"]

#        return render_template("iner.html", a=pid, b=user_id)


        try:
            db.execute("DELETE FROM cart WHERE pid=? AND user_id=?", pid, user_id)
        except:
            return render_template("test1.html")

        return redirect("/cart")


    else:
        return render_template("cart.html")
    


@app.route("/buy", methods=["POST","GET"])
def buy():
    if request.method == "POST":
        user_id = session["user_id"]


        card_number = request.form.get("credit_number")
        password = request.form.get("password")


        #errors
        if not card_number:
            card_numbere = "Please enter your card number"
            return render_template("buy.html", card_numbere=card_numbere)
        
        if not password:
            passworde = "Please enter your password"
            return render_template("buy.html", passworde=passworde)

        try:
            data = db.execute("SELECT * FROM credit WHERE card_number=?", card_number)
        except:
            card_numbere = "Card number invalid!"
            return render_template("buy.html", card_numbere=card_numbere)

        try:
            passhash = data[0]["card_password"]
        except:
            passworde = "Password incorrect!"
            return render_template("buy.html", passworde=passworde)


        if len(data) != 1 or not check_password_hash(passhash, password):
            return render_template("test1.html")


        num1 = 0
        num2 = 0
        num3 = 0
        num4 = 0
        num5 = 0
        num6 = 0

        price1 = 0
        price2 = 0
        price3 = 0
        price4 = 0
        price5 = 0
        price6 = 0

        try:
            num1 = db.execute("SELECT number FROM cart WHERE user_id=? AND pid=1", user_id)[0]["number"]
            price1 = db.execute("SELECT price FROM products WHERE pid=1")[0]["price"]
        except:
            pass

        try:
            num2 = db.execute("SELECT number FROM cart WHERE user_id=? AND pid=2", user_id)[0]["number"]
            price2 = db.execute("SELECT price FROM products WHERE pid=2")[0]["price"]
        except:
            pass

        try:
            num3 = db.execute("SELECT number FROM cart WHERE user_id=? AND pid=3", user_id)[0]["number"]
            price3 = db.execute("SELECT price FROM products WHERE pid=3")[0]["price"]
        except:
            pass

        try:
            num4 = db.execute("SELECT number FROM cart WHERE user_id=? AND pid=4", user_id)[0]["number"]
            price4 = db.execute("SELECT price FROM products WHERE pid=4")[0]["price"]
        except:
            pass

        try:
            num5 = db.execute("SELECT number FROM cart WHERE user_id=? AND pid=5", user_id)[0]["number"]
            price5 = db.execute("SELECT price FROM products WHERE pid=5")[0]["price"]
        except:
            pass

        try:
            num6 = db.execute("SELECT number FROM cart WHERE user_id=? AND pid=6", user_id)[0]["number"]
            price6 = db.execute("SELECT price FROM products WHERE pid=6")[0]["price"]
        except:
            pass

 #       return render_template("iner.html", a=num1, b=price1, c=num2, d=price2, e=num3, f=price3)

        all1 = 0
        all2 = 0
        all3 = 0
        all4 = 0
        all5 = 0
        all6 = 0


        try:
            all1 = num1 * price1
        except:
            pass

        try:
            all2 = num2 * price2
        except:
            pass

        try:
            all3 = num3 * price3
        except:
            pass           

        try:
            all4 = num4 * price4
        except:
            pass          

        try:
            all5 = num5 * price5
        except:
            pass

        try:
            all6 = num6 * price6
        except:
            pass


        allprice = all1 + all2 + all3 + all4 + all5 + all6

#        return render_template("iner.html", a=all1, b=all2, c=all3, d=all4, e=all5, f=all6, g=allprice)

        cashin = db.execute("SELECT cash FROM credit WHERE card_number=?", card_number)[0]["cash"]


        if allprice > cashin:
            return render_template("notmoney.html", cashin=cashin)

        NewCashin = cashin - allprice

        db.execute("UPDATE credit SET cash=? WHERE card_number=?", NewCashin, card_number)
        db.execute("DELETE FROM cart WHERE user_id=?", user_id)

        return redirect("/cart")
            
    else:
        user_id = session["user_id"]

        num1 = 0
        num2 = 0
        num3 = 0
        num4 = 0
        num5 = 0
        num6 = 0

        price1 = 0
        price2 = 0
        price3 = 0
        price4 = 0
        price5 = 0
        price6 = 0

        try:
            num1 = db.execute("SELECT number FROM cart WHERE user_id=? AND pid=1", user_id)[0]["number"]
            price1 = db.execute("SELECT price FROM products WHERE pid=1")[0]["price"]
        except:
            pass

        try:
            num2 = db.execute("SELECT number FROM cart WHERE user_id=? AND pid=2", user_id)[0]["number"]
            price2 = db.execute("SELECT price FROM products WHERE pid=2")[0]["price"]
        except:
            pass

        try:
            num3 = db.execute("SELECT number FROM cart WHERE user_id=? AND pid=3", user_id)[0]["number"]
            price3 = db.execute("SELECT price FROM products WHERE pid=3")[0]["price"]
        except:
            pass

        try:
            num4 = db.execute("SELECT number FROM cart WHERE user_id=? AND pid=4", user_id)[0]["number"]
            price4 = db.execute("SELECT price FROM products WHERE pid=4")[0]["price"]
        except:
            pass

        try:
            num5 = db.execute("SELECT number FROM cart WHERE user_id=? AND pid=5", user_id)[0]["number"]
            price5 = db.execute("SELECT price FROM products WHERE pid=5")[0]["price"]
        except:
            pass

        try:
            num6 = db.execute("SELECT number FROM cart WHERE user_id=? AND pid=6", user_id)[0]["number"]
            price6 = db.execute("SELECT price FROM products WHERE pid=6")[0]["price"]
        except:
            pass


        all1 = 0
        all2 = 0
        all3 = 0
        all4 = 0
        all5 = 0
        all6 = 0


        try:
            all1 = float(num1) * float(price1)
        except:
            pass

        try:
            all2 = float(num2) * float(price2)
        except:
            pass

        try:
            all3 = float(num3) * float(price3)
        except:
            pass           

        try:
            all4 = float(num4) * float(price4)
        except:
            pass          

        try:
            all5 = float(num5) * float(price5)
        except:
            pass

        try:
            all6 = float(num6) * float(price6)
        except:
            pass


        allprice = all1 + all2 + all3 + all4 + all5 + all6

#        return render_template("iner.html", a=all1, b=all2, c=all3, d=allprice, e=all4, f=all5, g=all6)

        return render_template("buy.html", allrpice=round(allprice))