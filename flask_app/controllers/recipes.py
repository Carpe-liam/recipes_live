from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app.controllers import users

@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        flash("please login", "login")
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    user = User.locate_by_id(data)
    return render_template("new_recipe.html", user=user)


@app.route('/recipes/save', methods=["POST"])
def save_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data = {
        "user_id" : request.form["user_id"],
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "under_30" : request.form["under_30"],
        "date_made_on" : request.form["date_made_on"]
    }
    
    print(data)
    Recipe.save_recipe(data)
    return redirect('/dashboard')


@app.route('/recipes/<int:id>')
def view_recipe(id):
    if 'user_id' not in session:
        flash("please login", "login")
        return redirect('/')
    data = {
        "id":id
    }
    recipe = Recipe.get_recipe(data)
    user_data = {
        "id" : session['user_id']
    }
    user = User.locate_by_id(user_data)
    return render_template("show_recipe.html",user=user, recipe=recipe)


@app.route('/recipes/edit/<int:id>')
def show_edit_page(id):
    if 'user_id' not in session:
        flash("please login", "login")
        return redirect('/')
    data = {
        "id":id
    }
    user_data = {
        "id" : session['user_id']
    }
    user = User.locate_by_id(user_data)
    recipe = Recipe.get_recipe(data)
    return render_template("edit_recipe.html", recipe=recipe, user=user)

@app.route("/recipes/update/<int:id>", methods=["POST"])
def update_recipe(id):
    data = {
        "id": id,
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "under_30" : request.form["under_30"],
        "date_made_on" : request.form["date_made_on"]
    }
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{request.form["id"]}')
    Recipe.edit_recipe(request.form)
    return redirect("/dashboard")

@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect("/logout")
    data = {
        "id" : id
    }
    Recipe.delete_recipe(data)
    return redirect('/dashboard')