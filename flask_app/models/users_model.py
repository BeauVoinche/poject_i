# the model will TALK to the DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import database
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+[a-zA-Z]+$')

class User():
    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.favorite_recipes = []

    # ?==========================Create a new user
    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO users ( first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        """
        return connectToMySQL(database).query_db(query, data)
    
    #?==========================Get all Users
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(database).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users
    


    # ? ==========================Get User by ID
    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT * FROM users 
        WHERE users.id = %(id)s;
        """
        results = connectToMySQL(database).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])


    # ? =========================Get User by Email
    @classmethod
    def get_by_email(cls, data):
        query = """
        SELECT * FROM users
        WHERE email = %(email)s
        """
        results = connectToMySQL(database).query_db(query, data)
        # print(results)
        if len(results) < 1:
            return False
        return cls(results[0])


# # ?=============================Add recipe to favorites
#     @classmethod
#     def add_favorite(cls,data):
#         query = "INSERT INTO user_likes (user_id,recipe_id) VALUES (%(user_id)s,%(recipe_id)s);"
#         return connectToMySQL(database).query_db(query,data)

# # ?=============================Delete recipe from favorites
#     @classmethod
#     def delete_favorite(cls,data):
#         query = """
#         DELETE user_likes FROM user_likes 
#         WHERE recipe_id = %(recipe_id)s AND user_id = %(user_id)s;"""
#         return connectToMySQL(database).query_db(query,data)


# ? =============================Validate the user when creating
    @staticmethod
    def validate_user(data):
        is_valid = True
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(database).query_db(query, data)

        # *look through this for specific validations to use if necessary for examples
        if len(data['first_name']) < 2:
            is_valid=False
            flash("Invalid entry, First Name is required", 'first_name')
        elif not data['first_name'].isalpha():
            is_valid=False
            flash("Invalid entry, First Name can only contain letters", 'first_name')

        if len(data['last_name']) < 2:
            is_valid=False
            flash("Invalid entry, Last Name is required", 'last_name')
        elif not data['last_name'].isalpha():
            is_valid=False
            flash("Invalid entry, Last Name can only contain letters", 'last_name')

        if len(data['email']) < 1:
            is_valid=False
            flash("Invalid entry, email is required", 'email')
        elif not EMAIL_REGEX.match(data['email']):
            is_valid=False
            flash("Invalid email address", 'email')
        else:
            email_dict = {
                'email': data['email'],
            }
            potential_user = User.get_by_email(email_dict)
            if potential_user: #! email is already in use
                is_valid=False
                flash("Email already exists", 'email')

        if len(data['password']) < 8:
            is_valid=False
            flash("Invalid entry, must be at least 8 characters long", 'password')
        elif not data['password'] == data['confirm_password']:
            is_valid=False
            flash("Passwords do not match", 'confirm_password')

        return is_valid