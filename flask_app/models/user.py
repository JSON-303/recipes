from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.recipe import Recipe
from flask_app import bcrypt
import re

EMAIL_REGEX = re.compile((r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$"))


class User:
    _db = "recipes_db"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    """Static Methods: Register/Login"""

    @staticmethod
    def register_form_is_valid(form_data):
        """This method validates the registration form"""
        is_valid = True
        """Name Validators:"""
        if len(form_data["first_name"].strip()) == 0:
            flash("Please enter first_name.", "register")
            is_valid = False
        elif len(form_data["first_name"].strip()) < 2:
            flash("First name must be at least two characters.", "register")
            is_valid = False
        if len(form_data["last_name"].strip()) == 0:
            flash("Please enter last name.", "register")
            is_valid = False
        elif len(form_data["last_name"].strip()) < 2:
            flash("Last name must be at least two characters.", "register")
            is_valid = False
        """Email Validators:"""
        if len(form_data["email"].strip()) == 0:
            flash("Please enter email.", "register")
            is_valid = False
        elif not EMAIL_REGEX.match(form_data["email"]):
            flash("Email address invalid.", "register")
            is_valid = False
        elif User.find_by_email(form_data["email"]) is not None:
            flash(
                "Email already in use. Please us a different email or log in.",
                "register",
            )
            is_valid = False
        """Password Validators:"""
        if len(form_data["password"].strip()) == 0:
            flash("Please enter a password.")
            is_valid = False
        elif len(form_data["password"].strip()) < 8:
            flash("Password must be at least eight characters")
        elif form_data["password"] != form_data["confirm_password"]:
            flash("Passwords do not match.", "register")
            is_valid = False

        return is_valid

    @staticmethod
    def login_form_is_valid(form_data):
        """This method validates the login format"""
        is_valid = True
        if len(form_data["email"].strip()) == 0:
            flash("Please enter your email.", "login")
            is_valid = False
        elif not EMAIL_REGEX.match(form_data["email"]):
            flash("Email address invalid.", "login")
            is_valid = False
        return is_valid

    @staticmethod
    def confirm_account_existence(form_data):
        """This method confirms existence of the email within the database"""
        is_valid = False
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {"email": form_data["email"]}
        result = connectToMySQL(User._db).query_db(query, data)
        if result:
            is_valid = True
        return is_valid

    @staticmethod
    def password_validation(form_data):
        is_valid = False
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {"email": form_data["email"]}
        result = connectToMySQL(User._db).query_db(query, data)

        if result:
            user = result[0]
            if bcrypt.check_password_hash(user["password"], form_data["password"]):
                is_valid = True

        return is_valid

    """Class Methods"""

    @classmethod
    def register(cls, user_data):
        """This method creates a new user in the database"""
        query = """
        INSERT INTO users
        (first_name, last_name, email, password)
        VALUES
        (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        """
        user_id = connectToMySQL(User._db).query_db(query, user_data)
        print(user_id)  # delete this after verifying id is returned in terminal
        return user_id

    @classmethod
    def find_by_email(cls, email):
        """This method finds a user by email"""
        query = """SELECT * FROM users WHERE email = %(email)s;"""
        data = {"email": email}
        list_of_dicts = connectToMySQL(User._db).query_db(query, data)
        if len(list_of_dicts) == 0:
            return None
        user = User(list_of_dicts[0])
        return user

    @classmethod
    def find_by_id(cls, id):
        """This method finds a user by id"""
        query = """SELECT * FROM users WHERE id = %(id)s;"""
        data = {"id": id}
        list_of_dicts = connectToMySQL(User._db).query_db(query, data)
        user = User(list_of_dicts[0])
        return user
