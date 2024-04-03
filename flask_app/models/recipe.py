from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from pprint import pprint


class Recipe:
    _db = "recipes_db"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.under = data["under"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_cooked = data["date_cooked"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def new_recipe_validation(form_data):
        """Validates New/Edit Recipe form data"""
        is_valid = True
        """New Recipe Validators"""
        if len(form_data["description"].strip()) == 0:
            flash("Description must not be blank.")
            is_valid = False
        elif len(form_data["description"].strip()) < 3:
            flash("Description must be at least three characters.")
            is_valid = False
        if len(form_data["name"].strip()) == 0:
            flash("Please enter name.")
            is_valid = False
        elif len(form_data["name"].strip()) < 3:
            flash("Name must be at least three characters.")
            is_valid = False
        if len(form_data["instructions"].strip()) == 0:
            flash("Please enter Instructions.")
            is_valid = False
        elif len(form_data["instructions"].strip()) < 3:
            flash("Instructions must be at least three characters.")
            is_valid = False
        if not form_data["date_cooked"].strip():
            flash("Please select a date.")
        if not form_data.get("under"):
            flash("Please select if the recipe is under or over 30 min.")
            is_valid = False

        return is_valid

    @classmethod
    def all_recipes(cls):
        """Finds all the recipes in the database with users"""
        query = """
        Select recipes.*, users.first_name AS user_first_name
        FROM recipes
        LEFT JOIN users ON recipes.user_id = users.id
        """

        list_of_dicts = connectToMySQL(Recipe._db).query_db(query)
        recipes = []
        for each_dict in list_of_dicts:
            user_first_name = each_dict.pop("user_first_name", None)
            user_id = each_dict.pop("user_id", None)
            recipe = Recipe(each_dict)
            recipe.user_first_name = user_first_name
            recipe.user_id = user_id
            recipes.append(recipe)

        return recipes

    @classmethod
    def find_by_id(cls, recipe_id):
        """Finds one recipe by ID"""
        query = "SELECT * FROM recipes WHERE id = %(recipe_id)s;"
        data = {"recipe_id": recipe_id}
        list_of_dicts = connectToMySQL(Recipe._db).query_db(query, data)
        recipe = Recipe(list_of_dicts[0])

        return recipe

    @classmethod
    def new_recipe(cls, recipe_data):
        """This method creates a new recipe in the database"""
        query = """
        INSERT INTO recipes
        (name, under, description, instructions, date_cooked, user_id)
        VALUES
        (%(name)s, %(under)s, %(description)s, %(instructions)s, %(date_cooked)s, %(user_id)s)
        """
        recipe_id = connectToMySQL(Recipe._db).query_db(query, recipe_data)
        return recipe_id

    @classmethod
    def update_recipe(cls, recipe_id, recipe_data):
        query = """
        UPDATE recipes
        SET name = %(name)s, under = %(under)s, description = %(description)s,
        instructions = %(instructions)s, date_cooked = %(date_cooked)s
        WHERE id = %(id)s;"""

        data = {**recipe_data, "id": recipe_id}
        connectToMySQL(Recipe._db).query_db(query, data)
        return

    @classmethod
    def delete_recipe(cls, recipe_id):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        data = {"id": recipe_id}
        return connectToMySQL(Recipe._db).query_db(query, data)
