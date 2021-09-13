from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.date_made_on = data['date_made_on']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_all_recipes(cls):
        query = """
        SELECT * FROM recipes;
        """
        return connectToMySQL(DATABASE).query_db(query)
    
    @classmethod
    def get_recipe(cls, data):
        query = """
        SELECT * FROM recipes
        WHERE id = %(id)s ;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        return cls(results[0])


    @classmethod
    def save_recipe(cls, data):
        query = """
        INSERT INTO recipes (user_id, name, description, instructions, under_30, date_made_on)
        VALUES (  %(user_id)s, %(name)s, %(description)s, %(instructions)s, %(under_30)s, %(date_made_on)s  )  ;
        """
        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def edit_recipe(cls, data):
        query = """
        UPDATE recipes 
        SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_30=%(under_30)s, date_made_on = %(date_made_on)s 
        WHERE recipes.id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)


    @classmethod
    def delete_recipe(cls, data):
        query = """
        DELETE FROM recipes
        WHERE recipes.id = %(id)s ;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @staticmethod
    def validate_recipe(recipe):
        errors = {}
        if len(recipe['name']) < 3:
            errors['name'] = 'Name should be at least 3 characters.'

        if len(recipe['description']) < 3:
            errors['description'] = 'Descriptions should be 3 or more characters.'

        if len(recipe['instructions']) < 3:
            errors['instructions'] = 'Instructions should be 3 or more characters.'

        if recipe['date_made_on'] == "":
            errors['date_made_on'] = "Please enter date recipe was last made"

        if recipe['under_30'] == "":
            errors['date_made_on'] = "Please enter if over or under 30 minutes to cook"

        for category,message in errors.items():
            flash(message,category)
        return len(errors) == 0
