from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask import flash,render_template,redirect,session,request
from flask_app.controllers import users

@app.route('/recipes/new')
def new():
    user_id = session['user_id']
    return render_template('new_recipe.html', user_id=user_id)

@app.route('/recipes/view/<int:id>')
def view(id):
    if 'user_id' not in session:
        return redirect('/')
    data = { 'id' : id }
    id = { 'id' : session['user_id'] }
    recipe = Recipe.get_one_recipe(data)
    user = User.id_in_db(id)
    return render_template('view_recipe.html', recipe=recipe, user=user)

@app.route('/recipes/new/create', methods=['POST'])
def recipe_create():
    if not Recipe.vald_recipes(request.form):
        flash('All Fields Required', 'recipe')
        return redirect('/recipes/new')
    Recipe.create_recipe(request.form)
    return redirect('/recipes')

@app.route('/recipes/edit/<int:id>')
def recipe_edit(id):
    if 'user_id' not in session:
        return redirect('/')
    data = { 'id' : id }
    recipe = Recipe.get_one_recipe(data)
    if session['user_id'] != recipe.user_id:
        return redirect('/recipes')
    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    data = { 'id' : id }
    Recipe.delete(data)
    return redirect('/recipes')