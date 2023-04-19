from flask_app.config.mysqlconnection import MySQLConnection
from flask_app import app
from flask_app.models import user
from flask import flash

class Recipe:
    DB = 'recipes_schemas'
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under = data['under']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = data['creator']

    @classmethod
    def create_recipe(cls,data):
        query = """
        INSERT INTO recipes(name, description, instructions, date_made, under, user_id)
        VALUES(%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under)s, %(user_id)s);
        """
        return MySQLConnection(cls.DB).query_db(query,data)

    @classmethod
    def delete(cls, data):
        query = """
        DELETE FROM recipes WHERE id = %(id)s;
        """
        return MySQLConnection(cls.DB).query_db(query,data)

    @classmethod
    def get_one_recipe(cls,data):
        query = """
        SELECT * FROM recipes
        JOIN users on recipes.user_id = users.id
        WHERE recipes.id = %(id)s;
        """
        result = MySQLConnection(cls.DB).query_db(query,data)
        # print(result)
        for row in result:
            posting_user = user.User({
                'id': row['user_id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            })
            new_recipe = Recipe({
                'id': row['id'],
                'name': row['name'],
                'description': row['description'],
                'instructions': row['instructions'],
                'date_made': row['date_made'],
                'under': row['under'],
                'user_id': row['user_id'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'creator': posting_user
            })
        return new_recipe

    @classmethod
    def get_all_recipes(cls):
        query = """
        SELECT * FROM recipes
        JOIN users ON recipes.user_id = users.id
        ORDER BY recipes.created_at DESC
        """
        results = MySQLConnection(cls.DB).query_db(query)
        # print(results)
        all_recipes = []
        for row in results:
            posting_user = user.User({
                'id': row['user_id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            })
            new_recipe = Recipe({
                'id': row['id'],
                'name': row['name'],
                'description': row['description'],
                'instructions': row['instructions'],
                'date_made': row['date_made'],
                'under': row['under'],
                'user_id': row['user_id'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'creator': posting_user
            })
            all_recipes.append(new_recipe)
        return all_recipes

    @staticmethod
    def vald_recipes(input):
        is_valid = True
        if not input['name'] or not input['description'] or not input['instructions'] or not input['date_made']:
            flash('All fields required')
            is_valid = False
        if len(input['name']) < 3:
            flash('Name must be at least 3 characters' ,'recipe')
            is_valid = False
        if len(input['description']) < 3:
            flash('Description must be at least 3 characters' ,'recipe')
            is_valid = False
        if len(input['instructions']) < 3:
            flash('Instructions must be at least 3 characters' ,'recipe')
            is_valid = False
        return is_valid