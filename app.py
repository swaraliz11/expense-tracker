import os 
import sqlite3

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

# Create table
with sqlite3.connect("expense.db", check_same_thread=False) as con:
    db = con.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, email VARCHAR NOT NULL, hash TEXT NOT NULL, income NUMERIC NOT NULL)")
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
        password = request.form.get("password")
        
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

@app.route("/budget")
def budget():
    """Show monthly budget and savings"""
    if request.method == "POST":
        budget = request.form.get("budget")
        savings = request.form.get("savings")
        if not budget:
            return apology("must provide budget", 403)
        elif not savings:
            return apology("must provide savings")
        else:
            expenses = budget - savings
            return render_template("budget2.html", monthly_budget=budget, monthly_savings=savings, monthly_expenses=expenses)
    else:
        return render_template("budget.html")
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

if __name__ == "__main__":
    debug=True


    









 