from flask_app.config.mysqlconnection import MySQLConnection
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
import re
bcrypt = Bcrypt(app)
CHAR_REGEX = re.compile(r'^[a-zA-Z]')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = 'recipes_schemas'
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def register_user(cls,data):
        query = """
        INSERT INTO users(first_name, last_name, email, password)
        VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return MySQLConnection(cls.DB).query_db(query,data)

    @classmethod
    def id_in_db(cls,data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = MySQLConnection(cls.DB).query_db(query,data)
        return cls(result[0])

    @classmethod
    def if_user_in_db(cls,data):
        query = 'SELECT * from users WHERE email = %(email)s'
        result = MySQLConnection(cls.DB).query_db(query,data)
        print(result)
        if len(result) < 1:
            return False
        else:
            return True

    @classmethod
    def user_in_db(cls,data):
        query = 'SELECT * from users WHERE email = %(email)s'
        result = MySQLConnection(cls.DB).query_db(query,data)
        print(result)
        return cls(result[0])

    @staticmethod
    def vald_user_login(input):
        is_valid = True
        if not input['email'] or not input['password']:
            flash('All fields required', 'login')
            is_valid = False
        return is_valid

    @staticmethod
    def vald_user_reg(input):
        is_valid = True
        if not input['first_name'] or not input['last_name'] or not input['email'] or not input['password'] or not input['confirm_password']:
            flash('All fields required', 'register')
            is_valid = False
        if len(input['first_name']) < 2:
            flash('First Name must be at least 2 characters', 'register')
            is_valid = False
        if not CHAR_REGEX.match(input['first_name']):
            flash('First Name must be alphabetic letters', 'register')
            is_valid = False

        if len(input['last_name']) < 2:
            flash('Last Name must be at least 2 characters', 'register')
            is_valid = False
        if not CHAR_REGEX.match(input['last_name']):
            flash('Last Name must be alphabetic letters', 'register')
            is_valid = False
        
        if not EMAIL_REGEX.match(input['email']):
            flash('Email is not valid', 'register')
            is_valid = False

        if len(input['password']) < 8:
            flash('Password must be at least 8 characters', 'register')
            is_valid = False
        return is_valid