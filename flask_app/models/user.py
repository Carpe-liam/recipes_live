from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM users ;
        """
        result = connectToMySQL(DATABASE).query_db(query)
        return result
    
    @classmethod
    def get_others(cls, data):
        query = """
        SELECT * FROM users
        WHERE NOT users.id = %(id)s
        ORDER BY users.first_name ASC ;
        """
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result 

    @classmethod
    def create_user(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (  %(first_name)s, %(last_name)s, %(email)s, %(password)s  );
        """
        return connectToMySQL(DATABASE).query_db(query, data) # returns id


    @classmethod
    def locate_user(cls, data):
        query = """
        SELECT * FROM users
        WHERE users.email = %(email)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)

        if len(result) <1:
            return False
        return cls(result[0])

    @classmethod
    def locate_by_id(cls, data):
        query = """
        SELECT * FROM users
        WHERE users.id = %(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)

        if len(result) <1:
            return False
        return cls(result[0])


    @staticmethod
    def validate_user(user): #request form
        errors = {}
        if len(user['first_name']) < 2:
            errors['first_name'] = 'Name should be at least 2 characters.'

        if len(user['last_name']) < 2:
            errors['last_name'] = 'Name should be at least 2 characters.'

        if len(user['password']) < 8 :
            errors['password'] = 'Password should be at least 8 characters.'

        if user['password'] != user['password_check']:
            errors['password_check'] = 'Passwords do not match'

        if user['password'] != user['password_check']:
            errors['password_check'] = 'Passwords do not match'

        query = "SELECT * FROM users WHERE users.email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,user)
        if len(results) >= 1:
            errors['email'] = "Email already taken."

        if not EMAIL_REGEX.match(user['email']): 
            errors['invalid_email'] = "Invalid email address!"

        for category,message in errors.items():
            flash(message,category)
        return len(errors) == 0
