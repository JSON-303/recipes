from flask_app import app, bcrypt
from flask import flash, redirect, render_template, request, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.get("/")
def index():
    """Route renders (index)login/reg page"""

    return render_template("index.html")


@app.post("/register")
def register():
    """Route to process the registration form"""
    if not User.register_form_is_valid(request.form):
        return redirect("/")

    potential_user = User.find_by_email(request.form["email"])

    if potential_user != None:
        flash("Email in use. Please log in.")
        return redirect("/")

    hashed_pw = bcrypt.generate_password_hash(request.form["password"])
    user_data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": hashed_pw,
    }
    user_id = User.register(user_data)
    session["user_id"] = user_id
    return redirect("/recipes")


@app.post("/login")
def login():
    """This route process the login form"""
    if not User.login_form_is_valid(request.form):
        return redirect("/")

    if User.password_validation(request.form):
        user = User.find_by_email(request.form["email"])

        session["user_id"] = user.id
        return redirect("/recipes")

    else:
        flash("Invalid email or passwor.", "login")
        return redirect("/")


@app.get("/recipes")
def user_reciepe_page():
    """This route displays the users dashboard"""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    recipes = Recipe.all_recipes()
    user = User.find_by_id(session["user_id"])
    return render_template("recipes.html", recipes=recipes, user=user)
