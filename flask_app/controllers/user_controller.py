
#! Routing
from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.users_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# ! VIEWS

# ? ================================Main Movie Page
@app.route("/")
def index():
    if 'user_id' not in session:
        return render_template("main_page.html")
    userdata = {
        'id' : session['user_id']
    }
    logged_user = User.get_by_id(userdata)
    return render_template("main_page.html", logged_user=logged_user)


# # ? ================================Login page
@app.route('/newuser')
def show_one_user():
    if 'user_id' in session:
        return redirect('/')
    return render_template('login_page.html')




# ! ACTIONS


# ?=================================== Register User
@app.route("/register", methods=["POST"])
def register():
    if not User.validate_user(request.form):
        return redirect('/newuser')
    data = {
        **request.form,
        'password': bcrypt.generate_password_hash(request.form['password'])
        #* ^^^^^^^ this equals below
        # 'first_name': request.form['first_name'],
        # 'last_name': request.form['last_name'],
        # 'password': hashed_pw,
        # 'email': request.form['email']
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect("/")


#?=================================== Logout User
@app.route("/logout")
def logout():
    # *delete session['user'] and redirect
        # ! routing guard
    if 'user_id' not in session:
        return redirect("/")
    session.clear()
    return redirect("/")


#?=================================== Login User
@app.route("/login", methods=["POST"])
def login():
    potential_user_in_db = User.get_by_email(request.form)
    # * if email not found
    if not potential_user_in_db:
        flash("Email not found", "log")
        return redirect("/newuser")
    # * if password is wrong
    if not bcrypt.check_password_hash(potential_user_in_db.password, request.form['password']):
        flash("Incorrect password", "log")
        return redirect("/newuser")
    # * if password is correct and email is found
    session['user_id'] = potential_user_in_db.id
    return redirect("/")

# # ?===================================Like a recipe
# @app.route('/like/recipe/<int:id>')
# def add_to_likes(id):
#     data = {
#         'user_id': session['user_id'],
#         'recipe_id': id
#     }
#     User.add_favorite(data)
#     return redirect(f"/user/{session['user_id']}")

# # ?===================================UNLike a recipe
# @app.route('/unlike/recipe/<int:id>')
# def delete_from_likes(id):
#     data = {
#         'user_id': session['user_id'],
#         'recipe_id': id
#     }
#     User.delete_favorite(data)
#     return redirect(f"/user/{session['user_id']}")

