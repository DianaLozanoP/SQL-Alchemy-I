"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "amarillos"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


app.app_context().push()
connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    return redirect('/users')


@app.route('/users')
def users_page():
    """Display all users"""
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/new')
def form_page():
    """Form to create a new user"""
    return render_template('user_form.html')


@app.route('/users/new', methods=["POST"])
def create_newuser():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["img-url"]

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<user_id>')
def show_userinfo(user_id):
    """Show details about user"""
    user = User.query.get_or_404(user_id)
    return render_template('userpage.html', user=user)


@app.route('/users/<user_id>/edit')
def edit_userpage(user_id):
    """Edit user information"""
    user = User.query.get_or_404(user_id)
    return render_template('edituser.html', user=user)


@app.route('/users/<user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Process the edit-form user information"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["img-url"]
    current_User = User.query.get(user_id)
    current_User.update_information(first_name, last_name, image_url)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<user_id>/delete')
def delete_userdb(user_id):
    """Delete the user from database"""
    User.delete_user(user_id)
    db.session.commit()
    return redirect('/users')
