"""Register, login and logout."""
import re
import sqlite3
from functools import wraps

from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import get_db, now_utc

auth_bp = Blueprint("auth", __name__)

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def login_required(view):
    """Put @login_required above a route to block people who are not logged in."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            if request.path.startswith("/api/"):
                return jsonify({"error": "Please log in to continue."}), 401
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("chat.chat_page"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        # Validate the input and show a friendly message for each problem.
        error = None
        if not username or len(username) > 40:
            error = "Please enter a username (up to 40 characters)."
        elif not EMAIL_PATTERN.match(email):
            error = "Please enter a valid email address."
        elif len(password) < 8:
            error = "Your password needs at least 8 characters."
        elif password != confirm:
            error = "The two passwords do not match."

        if error is None:
            try:
                db = get_db()
                cursor = db.execute(
                    "INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                    (username, email, generate_password_hash(password), now_utc()),
                )
                db.commit()
                session.clear()
                session["user_id"] = cursor.lastrowid
                session["username"] = username
                return redirect(url_for("chat.chat_page"))
            except sqlite3.IntegrityError:
                error = "That email is already registered. Try logging in instead."
            except sqlite3.Error:
                error = "Sorry, something went wrong. Please try again."

        flash(error, "error")
        return render_template("register.html", username=username, email=email)

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("chat.chat_page"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        try:
            user = get_db().execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        except sqlite3.Error:
            flash("Sorry, something went wrong. Please try again.", "error")
            return render_template("login.html", email=email)

        # Same message for "no such email" and "wrong password" so we don't leak which emails exist.
        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Wrong email or password.", "error")
            return render_template("login.html", email=email)

        session.clear()
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return redirect(url_for("chat.chat_page"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
