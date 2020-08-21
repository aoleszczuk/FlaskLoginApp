from flask import Flask, render_template, url_for, request, session, redirect, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

db.create_all()

@app.route("/")
def index():

    return render_template("index.html")


@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session['user'] = user

        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash('You were successfully logged in')
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("You already Logged In!")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/logout")
def logout():
    flash('You were successfully logged out!')
    session.pop("user", None)
    session.pop("email", None)

    return redirect(url_for("index"))


@app.route("/user", methods=["POST", "GET"])
def user():
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email

            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()

            flash("Email saved!")

        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", user=user)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
