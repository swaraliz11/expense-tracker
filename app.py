import os 
import sqlite3
import datetime

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure system to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Create table for storing information about user
with sqlite3.connect("expense.db", check_same_thread=False) as con:
    db = con.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, email VARCHAR NOT NULL, hash TEXT NOT NULL, income NUMERIC NOT NULL)")
    con.commit()
con.close()

# Create table for storing categories of expenses
with sqlite3.connect("expense.db", check_same_thread=False) as con:
    db = con.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS record (user_id NUMERIC NOT NULL, date VARCHAR NOT NULL, amount NUMERIC, category TEXT NOT NULL)")
    con.commit()
con.close()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    """Show summary of daily expenses"""
    return apology("todo")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        income = request.form.get("income")
        # Ensure name was submitted 
        if not name:
            return apology("must provide name", 403)
        # Ensure email was submitted
        if not email:
            return apology("must provide email address", 403)
        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)
        # Ensure length of password submitted is not less than 5
        elif len(password) < 5:
            return apology("password should be at least 5 characters long")
        # Ensure passwords match
        elif password != confirm_password:
            return apology("passwords do not match", 401)
        # Ensure income was submitted
        elif not income:
            return apology("must provide income", 403)
        
        # Hash user's password
        hash = generate_password_hash(password)

        # Check if user already exists
        with sqlite3.connect("expense.db", check_same_thread=False) as con:
            db = con.cursor()
            db.execute("SELECT COUNT(*) FROM users WHERE email = ?", [email])
            count = db.fetchone()[0]
            if count > 0:
                return apology("user already exists")
            else:
                db.execute("INSERT INTO users (name, email, hash, income) VALUES (?, ?, ?, ?)", [name, email, hash, income])
                con.commit()
                # Redirect to home page
                return redirect("/")
        con.close()

    # User reached the route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure email was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)
        
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        
        email = request.form.get("email")
        
        # Query database for email
        with sqlite3.connect("expense.db", check_same_thread=False) as con:
            con.row_factory = sqlite3.Row
            db = con.cursor()
            db.execute("SELECT * FROM users WHERE email = ?", [email])
            rows = db.fetchall()
            con.commit()
        con.close()

        # Ensure user exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid email and/or password", 403)
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/record", methods=["GET", "POST"])
@login_required
def record():
    """Record expenses"""
    if request.method == "POST":
        user_id = session["user_id"]
        amount = request.form.get("amount")
        category = request.form.get("category")
        date = request.form.get("date")
        if not amount:
            return apology("must enter amount")
        elif not category:
            return apology("must enter category")
        elif not date:
            return apology("must enter date")
        else:
            with sqlite3.connect("database.db", check_same_thread=False) as con:
                db = con.cursor()
                db.execute("INSERT INTO record (user_id, date, amount, category) VALUES (?, ?, ?, ?)", [user_id, amount, date, category])
                con.commit()
            con.close()
            return render_template("/")
    else:
        return render_template("record.html")
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

if __name__ == "__main__":
    debug=True


    









 