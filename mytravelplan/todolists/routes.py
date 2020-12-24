import flask
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from mytravelplan import db
from mytravelplan.main.routes import like_to_post
from mytravelplan.messages.routes import messages_counters
from mytravelplan.models import Post, Comment, Image, Country, Todolist, ImageToDoList, Postintodolist
from mytravelplan.posts.forms import PostForm, CommentForm, LikeForm
from mytravelplan.posts.utils import save_picture
from mytravelplan.todolists.forms import ToDoListForm, AddToDoListForm

todolists = Blueprint('todolists', __name__)


# In that file all the routes of the posts at the website, here is all the logic and functionality of the posts
# and here is the templates that user sees that belong to posts


@todolists.route('/todolists/<int:post_id>/<int:to_do_list_id>', methods=['GET', 'POST'])
@login_required
def to_do_lists(post_id, to_do_list_id):
    # Generic functionality
    # Messages counters
    msg_counters = messages_counters()

    add_to_do_list_form = AddToDoListForm()
    to_do_list_id = add_to_do_list_form.id.data
    to_do_lists_and_their_posts = []
    page = request.args.get('page', 1, type=int)
    to_do_lists = Todolist.query.filter_by(user_id=current_user.id).order_by(Todolist.date_posted.desc()).paginate(page=page, per_page=5)

    if add_to_do_list_form.validate_on_submit():
        if post_id != 0 and to_do_list_id != 0:
            to_do_list = Todolist.query.filter_by(id=to_do_list_id).first()
            post_in_to_do_list = Postintodolist(to_do_list_id=to_do_list_id, post_id=post_id,
                                                name_of_to_do_list=to_do_list.title)
            db.session.add(post_in_to_do_list)
            db.session.commit()
            return redirect(url_for('posts.post', post_id=post_id))
    elif post_id != 0:
        return render_template('to_do_lists.html', to_do_lists=to_do_lists,
                               legend='Choose To do list where to add post', post_id=post_id,
                               add_to_do_list_form=add_to_do_list_form, to_do_lists_and_their_posts=to_do_lists_and_their_posts,msg_counters=msg_counters)

    return render_template('to_do_lists.html', legend='Your to do lists', to_do_lists=to_do_lists,
                           add_to_do_list_form=add_to_do_list_form, post_id=post_id,msg_counters =msg_counters)


# Shows clicked post or entered post in the url
@todolists.route("/todolist/<int:todolist_id>", methods=['GET', 'POST'])
def to_do_list(todolist_id):
    to_do_list = Todolist.query.get_or_404(todolist_id)
    # to_do_list = Todolist.query.filter_by(id=todolist_id).first()
    # Generic functionality
    # Messages counters
    msg_counters = messages_counters()
    images = ImageToDoList.query.filter_by(to_do_list_id=to_do_list.id)
    posts = []
    dictionary_of_lists_of_pics_of_posts = []

    if to_do_lists is not None:
        print('here')
        # Taking all posts of every to do list
        posts_in_to_do_list = Postintodolist.query.filter_by(to_do_list_id=to_do_list.id)
        for post_in_to_do_list in posts_in_to_do_list:
            post = Post.query.filter_by(id=post_in_to_do_list.post_id).first()
            posts.append(post)
    return render_template('to_do_list.html', title=to_do_list.title, to_do_list=to_do_list, legend='Your Trip',
                           images=images, dictionary_of_lists_of_pics_of_posts=dictionary_of_lists_of_pics_of_posts, posts=posts, msg_counters=msg_counters)


# Shows form for creation a new post
@todolists.route("/todolist/new/", methods=['GET', 'POST'])
@login_required
def new_to_do_list():
    form = ToDoListForm()
    # Generic functionality
    # Messages counters
    msg_counters = messages_counters()

    if form.validate_on_submit():
        to_do_list = Todolist(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(to_do_list)
        db.session.commit()

        uploaded_imgs = flask.request.files.getlist("file[]")
        db.session.commit()

        for upload_img in uploaded_imgs:
            if upload_img:
                image_file_path = save_picture(upload_img)
                new_img = ImageToDoList(to_do_list_id=to_do_list.id, image_file_path=image_file_path)
                db.session.add(new_img)
        db.session.commit()
        flash('Your To Do List has been created!', 'success')
        return redirect(url_for('todolists.to_do_lists', post_id=0, to_do_list_id=0))
    return render_template('create_to_do_list.html', form=form, legend='Create Your Trip',msg_counters=msg_counters)


# Form for update a post
@todolists.route("/todolist/<int:todolist_id>/update", methods=['GET', 'POST'])
@login_required
def update_to_do_list(todolist_id):
    to_do_list = Todolist.query.get_or_404(todolist_id)
    # Generic functionality
    # Messages counters
    msg_counters = messages_counters()

    if to_do_list.author != current_user and current_user.admin_permissions != 1:
        abort(403)
    form = ToDoListForm()
    if form.validate_on_submit():
        to_do_list.title = form.title.data
        to_do_list.content = form.content.data
        db.session.commit()
        flash('Your to do list has been updated!', 'success')
        return redirect(url_for('todolists.to_do_list', todolist_id=todolist_id))
    elif request.method == 'GET':
        form.title.data = to_do_list.title
        form.content.data = to_do_list.content
    return render_template('create_to_do_list.html', title='Update To do list', form=form, legend='Update To do list', msg_counters=msg_counters)


# Deleting a to do list
@todolists.route("/todolist/<int:todolist_id>/delete", methods=['POST'])
@login_required
def delete_to_do_list(todolist_id):
    to_do_list = Todolist.query.get_or_404(todolist_id)
    if to_do_list.author != current_user and current_user.admin_permissions != 1:
        abort(403)
    images = ImageToDoList.query.filter_by(to_do_list_id=to_do_list.id)
    # Deleting all images of to do list
    for image in images:
        db.session.delete(image)

    # Deleting all added posts to do list
    posts_in_to_do_list = Postintodolist.query.filter_by(to_do_list_id=to_do_list.id)
    for post_in_to_do_list in posts_in_to_do_list:
        db.session.delete(post_in_to_do_list)
    db.session.delete(to_do_list)
    db.session.commit()
    flash('Your to do list has been deleted!', 'success')
    return redirect(url_for('todolists.to_do_lists', post_id=0, to_do_list_id=0))