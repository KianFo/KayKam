from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash



app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")