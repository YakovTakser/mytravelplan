from datetime import datetime
from mytravelplan import db, login_manager, config
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


# Get the logged in user from the data base with @login_manager.user_loader decorator
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# User Class (Object)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=True)
    messageReceived = db.relationship('Message', backref='receiverUser', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    admin_permissions = db.Column(db.Integer, default=0)
    posts = db.relationship('Post', backref='author', lazy=True)
    to_do_list = db.relationship('Todolist', backref='author', lazy=True)
    amount_of_posts = db.Column(db.Integer, default=0)
    level_of_user = db.Column(db.String(100), default='New')
    verified = db.Column(db.Boolean, default=False)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    def get_verification_token(self, expires_sec=86400):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}'), {self.email}', {self.image_file}'"

    @staticmethod
    def verify_verification_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None

        user = User.query.get(user_id)
        user.verified = True
        db.session.commit()
        return user

    def __repr__(self):
        return f"User('{self.username}'), {self.email}', {self.image_file}'"


# Post Class (Object)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)  # Foreign Key to make a relationship with the user by 'user_id' field
    comments = db.relationship('Comment', backref='belong', lazy=True)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100))
    place = db.Column(db.String(100))
    rate = db.Column(db.Integer)
    likes = db.relationship('PostLikes', backref='belong', lazy=True)
    imgs = db.relationship('Image', backref='belong', lazy=True)
    amount_of_likes = db.Column(db.Integer, default=0)
    amount_of_comments = db.Column(db.Integer, default=0)
    reported = db.Column(db.Boolean, default=False)
    find_friends = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return f"Post('{self.title}'), {self.date_posted}''"


# Comment Class (Object)
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),
                        nullable=False)  # Foreign Key to make a relationship with the Post by 'post_id' field
    username = db.Column(db.String(100), db.ForeignKey('user.username'),
                         nullable=False)  # Foreign Key to make a relationship with the User by 'user_id' field

    def __repr__(self):
        return f"Post('{self.username}'), {self.date_posted}, {self.content}''"


class Country(db.Model):
    country_name = db.Column(db.String(120), primary_key=True, unique=True, nullable=False)
    visit_count = db.Column(db.Integer, default=0)
    rate_total = db.Column(db.Integer, default=0)
    rate_avg = db.Column(db.Float)


# Message Class (Object)
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    owner = db.Column(db.String, nullable=False)
    receiver = db.Column(db.String, db.ForeignKey('user.username'),
                         nullable=False)  # Foreign Key to make a relationship with the user by 'user_id' fieldset
    readed = db.Column(db.Boolean, default=False)
    deletedByOwner = db.Column(db.Boolean, default=False)
    deletedByReceiver = db.Column(db.Boolean, default=False)


class PostLikes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),
                        nullable=False)  # Foreign Key to make a relationship with the user by 'user_id' field
    username = db.Column(db.String, nullable=False)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),
                        nullable=False)  # Foreign Key to make a relationship with the post by 'user_id' field
    image_file_path = db.Column(db.String(20), nullable=False)


# Post Class (Object)
class Todolist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)  # Foreign Key to make a relationship with the user by 'user_id' field
    imgs = db.relationship('ImageToDoList', backref='belong', lazy=True)
    post_in_to_do_list = db.relationship('Postintodolist', backref='belong', lazy=True)


class ImageToDoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to_do_list_id = db.Column(db.Integer, db.ForeignKey('todolist.id'),
                              nullable=False)  # Foreign Key to make a relationship with the user by 'user_id' field
    image_file_path = db.Column(db.String(20), nullable=False)


class Postintodolist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to_do_list_id = db.Column(db.Integer, db.ForeignKey('todolist.id'),
                              nullable=False)  # Foreign Key to make a relationship with the user by 'user_id' field
    post_id = db.Column(db.Integer, nullable=False)
    name_of_to_do_list = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)