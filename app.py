"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask
from models import db, connect_db, User, Post, Tag, PostTag

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


@app.route('/users/<user_id>/posts/new')
def create_newpost(user_id):
    """Create a new post """
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('post_form.html', user=user, tags=tags)


@app.route('/users/<user_id>/posts/new', methods=["POST"])
def commit_newpost(user_id):
    """Process the post form"""
    new_post = Post(title=request.form["title"],
                    content=request.form["content"],
                    user_id=user_id)

    db.session.add(new_post)
    db.session.commit()
    all_tags = request.form.getlist('tag_name')
    for eachtag in all_tags:
        tag = Tag.query.get(eachtag)
        new_post.tags.append(tag)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/posts/<post_id>')
def show_post(post_id):
    """Show all the information about the post"""
    post = Post.query.get_or_404(post_id)
    return render_template('show_post.html', post=post)


@app.route('/posts/<post_id>/edit')
def edit_form(post_id):
    """Show a user a form to edit the post"""
    post = Post.query.get(post_id)
    return render_template('edit_post.html', post=post)


@app.route('/posts/<post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Edit the post"""
    post = Post.query.get(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post_id}')


@app.route('/posts/<post_id>/delete')
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/users')


@app.route('/tags')
def list_tags():
    """Lists all tags, with links to the tag detail page."""
    tags = Tag.query.all()
    return render_template('alltags.html', tags=tags)


@app.route('/tags/<tag_id>')
def show_tag(tag_id):
    """Show detail about a tag. Have links to edit form and to delete."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('showtag.html', tag=tag)


@app.route('/tags/new')
def add_newtag():
    """Shows a form to add a new tag"""
    return render_template('form_newtag.html')


@app.route('/tags/new', methods=["POST"])
def process_tags():
    """process add form, add tags and redirect to tag list"""
    tag = Tag(name=request.form["name"])
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')


@app.route('/tags/<tag_id>/edit')
def edit_tag(tag_id):
    """Show edit form for a tag."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag=tag)


@app.route('/tags/<tag_id>/edit', methods=["POST"])
def change_tag(tag_id):
    """Show edit form for a tag."""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["name"]
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')


@app.route('/tags/<tag_id>/delete')
def delete_tag(tag_id):
    """Delete a tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')
