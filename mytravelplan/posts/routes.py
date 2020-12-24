import flask
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from mytravelplan import db
from mytravelplan.main.routes import like_to_post
from mytravelplan.messages.routes import messages_counters
from mytravelplan.models import Post, Comment, Image, Country, Todolist, Postintodolist, User
from mytravelplan.posts.forms import PostForm, CommentForm, LikeForm, ReportForm
from mytravelplan.posts.utils import save_picture
from mytravelplan.todolists.forms import AddPostForm

posts = Blueprint('posts', __name__)

# In that file all the routes of the posts at the website, here is all the logic and functionality of the posts
# and here is the templates that user sees that belong to posts



# Number of posts that user need to upload to get to the next level
NEXT_LEVEL = 2


# Shows clicked post or entered post in the url
@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    form = CommentForm()
    # Generic functionality
    # Messages counters
    msg_counters = messages_counters()
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post.id)
    images = []
    images = Image.query.filter_by(post_id=post.id)
    formLikes = LikeForm()
    post = Post.query.filter_by(id=post_id).first()
    add_post_form = AddPostForm()
    if current_user.is_authenticated:
        if request.method == 'POST':
            form_name = flask.request.form['form-name']
            if form_name == 'add_post_form':
                if add_post_form.validate_on_submit():
                    print('here')
                    post_add_id = add_post_form.id.data
                    # Maybe here is a problemmmmmmm
                    return redirect(url_for('todolists.to_do_lists', post_id=post_add_id, to_do_list_id=0))
            if form_name == 'form':
                # Comment functionality if the form of comment was submitted
                if form.validate_on_submit():
                    # text = how to split
                    comment = Comment(content=form.content.data, author=current_user, post_id=post_id)
                    post.amount_of_comments += 1
                    db.session.add(post)
                    db.session.add(comment)
                    db.session.commit()
                    flash('Your comment has been created!', 'success')
                    return redirect(url_for('posts.post', post_id=post_id))
            if form_name == 'formLikes':
                # If like or unlike button were pressed
                if formLikes.validate_on_submit():
                    like_or_unlike = formLikes.like_or_unlike.data
                    id_of_post_to_like = formLikes.id.data
                    like_to_post(id_of_post_to_like, like_or_unlike)
                    return redirect(url_for('posts.post', post_id=post_id))

        # Generic functionality
        # Messages counters
        msg_counters = messages_counters()
        print('jasnjcksancs')
    return render_template('post.html', title=post.title, post=post, comments=comments, formLikes=formLikes, form=form, images=images, add_post_form=add_post_form, msg_counters=msg_counters)



# Shows form for creation a new post
@posts.route("/post/new/<string:username>/", methods=['GET', 'POST'])
@login_required
def new_post(username):
    form = PostForm()
    # Generic functionality
    # Messages counters
    msg_counters = messages_counters()

    if form.validate_on_submit():
        country_name = form.country.data.lower()
        country_name = country_name.capitalize()
        country = Country.query.get(country_name)
        if country != None:
            if form.find_friends.data == 'True':
                find_friends = True
            else:
                find_friends = False
            post = Post(title=form.title.data, content=form.content.data, author=current_user, country=country_name, city=form.city.data, place=form.place.data, rate=form.rate.data, find_friends=find_friends)
            db.session.add(post)
            db.session.commit()
            country.visit_count += 1
            country.rate_total = country.rate_total + post.rate
            country.rate_avg = country.rate_total/country.visit_count
            uploaded_imgs = flask.request.files.getlist("file[]")

            user = User.query.filter_by(username=username).first_or_404()

            user.amount_of_posts += 1
            if user.level_of_user == 'New' and user.amount_of_posts >= NEXT_LEVEL * 1:
                user.level_of_user = 'Nov'
            elif user.level_of_user == 'Nov' and user.amount_of_posts >= NEXT_LEVEL * 2:
                user.level_of_user = 'Inter'
            elif user.level_of_user == 'Inter' and user.amount_of_posts >= NEXT_LEVEL * 3:
                user.level_of_user = 'Adv'
            elif user.level_of_user == 'Adv' and user.amount_of_posts >= NEXT_LEVEL * 4:
                user.level_of_user = 'Exp'
            db.session.commit()

            for upload_img in uploaded_imgs:
                if upload_img:
                    image_file_path = save_picture(upload_img)
                    new_img = Image(post_id=post.id, image_file_path=image_file_path)
                    db.session.add(new_img)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Country you entered is not exist!', 'danger')
    return render_template('create_post.html', form=form, legend='New Post', msg_counters=msg_counters)


# Form for update a post
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # Generic functionality
    # Messages counters
    msg_counters = messages_counters()

    if post.author != current_user and current_user.admin_permissions != 1:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.city = form.city.data
        post.place = form.place.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.country.data = post.country
        form.city.data = post.city
        form.place.data = post.place
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post', msg_counters=msg_counters)


# Deleting a post
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post.id)
    if post.author != current_user and current_user.admin_permissions != 1:
        abort(403)

    for comment in comments:
        db.session.delete(comment)
        db.session.commit()
    images = Image.query.filter_by(post_id=post.id)
    for img in images:
        db.session.delete(img)
        db.session.commit()
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))