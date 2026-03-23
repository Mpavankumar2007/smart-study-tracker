
from flask import Flask, render_template, request, redirect, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

# store users
users = {}

# store data for each user
user_data = {}

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect("/home")

        return "Invalid Login"

    return render_template("login.html")


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]

    users[username] = password

    user_data[username] = {
        "data": [],
        "goal": 0,
        "streak": 0,
        "last_date": ""
    }

    return redirect("/")


@app.route("/home")
def home():

    if "user" not in session:
        return redirect("/")

    username = session["user"]
    user = user_data[username]

    total = sum([x[1] for x in user["data"]])

    return render_template(
        "index.html",
        data=user["data"],
        total=total,
        goal=user["goal"],
        streak=user["streak"]
    )


@app.route("/add", methods=["POST"])
def add():

    username = session["user"]
    user = user_data[username]

    subject = request.form["subject"]
    hours = float(request.form["hours"])
    date = datetime.now().strftime("%Y-%m-%d")

    user["data"].append((subject, hours, date))

    if date != user["last_date"]:
        user["streak"] += 1
        user["last_date"] = date

    return redirect("/home")


@app.route("/delete/<int:index>")
def delete(index):

    username = session["user"]
    user = user_data[username]

    user["data"].pop(index)

    return redirect("/home")


@app.route("/goal", methods=["POST"])
def set_goal():

    username = session["user"]
    user = user_data[username]

    user["goal"] = float(request.form["goal"])

    return redirect("/home")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)