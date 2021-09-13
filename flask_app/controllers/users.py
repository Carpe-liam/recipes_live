from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app.controllers import recipes


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/create', methods=["POST"])
def create():
    if not User.validate_user(request.form):
        return redirect('/')
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email": request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.create_user(data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/login', methods=["POST"])
def login():
    if not User.locate_user(request.form):
        return redirect('/')
    user = User.locate_user(request.form)
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def show_dashboad():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    recipes = Recipe.get_all_recipes()
    user = User.locate_by_id(data)
    return render_template("dashboard.html", user=user, recipes=recipes)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')