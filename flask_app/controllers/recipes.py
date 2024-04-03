from flask_app import app
from flask import flash, redirect, render_template, request, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.get("/recipes")
def recipes_page():
    """This route renders all recipes"""
    recipes = Recipe.all_recipes()
    user = User.find_by_id(session["user_id"])
    return render_template("recipes.html", recipes=recipes, user=user)


@app.get("/recipes/new")
def new_recipe():
    if "user_id" not in session:
        flash("Pleas log in to submit a recipe.")
        return redirect("/")
    return render_template("recipe_new.html")


@app.post("/recipes/submit")
def add_recipe():

    if "user_id" not in session:
        flash("Pleas log in to submit a recipe.")
        return redirect("/")

    recipe_data = {
        "name": request.form["name"],
        "under": request.form.get("under"),
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_cooked": request.form["date_cooked"],
        "user_id": session["user_id"],
    }

    if not Recipe.new_recipe_validation(recipe_data):
        return redirect("/recipes/new")

    recipe_id = Recipe.new_recipe(recipe_data)
    session["recipe_id"] = recipe_id

    return redirect(f"/recipes")


@app.get("/recipes/edit/<int:recipe_id>")
def edit_recipe(recipe_id):
    if "user_id" not in session:
        flash("Pleas log in to edit a recipe.")
        return redirect("/")

    recipe = Recipe.find_by_id(recipe_id)
    return render_template("recipe_edit.html", recipe=recipe)


@app.post("/recipes/update/<int:recipe_id>")
def update_recipe(recipe_id):

    if "user_id" not in session:
        flash("Pleas log in to submit a recipe.")
        return redirect("/")

    recipe_data = {
        "name": request.form["name"],
        "under": request.form.get("under"),
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_cooked": request.form["date"],
        "user_id": session["user_id"],
    }

    if not Recipe.new_recipe_validation(recipe_data):
        flash
        return redirect(f"/recipes/edit/{recipe_id}")

    Recipe.update_recipe(recipe_id, recipe_data)
    session["recipe_id"] = recipe_id

    return redirect(f"/recipes")


@app.post("/recipes/delete/<int:recipe_id>")
def delete_recipe(recipe_id):
    """This route deletes a recipe from the database"""
    Recipe.delete_recipe(recipe_id)
    return redirect("/recipes")


@app.get("/recipes/view/<int:recipe_id>")
def view_recipe(recipe_id):
    if "user_id" not in session:
        flash("Pleas log in to submit a recipe.")
        return redirect("/")

    recipe = Recipe.find_by_id(recipe_id)
    user = User.find_by_id(session["user_id"])
    return render_template(
        "recipe_view.html", recipe_id=recipe_id, recipe=recipe, user=user
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
