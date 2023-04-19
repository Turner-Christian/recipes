from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask import flash,render_template,redirect,session,request
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/recipes')
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/recipes')
def recipes():
    if 'user_id' not in session:
        return redirect('/')
    data = { 'id' : session['user_id'] }
    user = User.id_in_db(data)
    recipes = Recipe.get_all_recipes()
    return render_template('recipes.html', user=user, recipes=recipes)

@app.route('/register', methods=['POST'])
def register():
    email = { 'email' : request.form['email'] }
    if not User.vald_user_reg(request.form):
        return redirect('/')
    if request.form['password'] != request.form['confirm_password']:
        flash('Passwords do not match', 'register')
        return redirect('/')
    if User.if_user_in_db(email) == True:
        flash('Email is already registered', 'register')
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.register_user(data)
    session['user_id'] = user_id
    return redirect('/recipes')
    
@app.route('/login', methods=['POST'])
def login():
    if not User.vald_user_login(request.form):
        return redirect('/')
    email = { 'email' : request.form['email'] }
    user_in_db = User.user_in_db(email)
    print('user:', user_in_db)
    if not user_in_db:
        flash('Invalid Email/Password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/recipes')