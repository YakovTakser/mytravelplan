from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from mytravelplan.models import User

# Here are all the forms that belonmg to users

# Registration form for the user
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "confirm password"})
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "first name"})
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "last name"})
    date_of_birth = DateField('Date Of Birth', format='%d/%m/%Y', validators=[validators.Optional()], render_kw={"placeholder": "dd/mm/YYYY"})
    # Admin Permissions
    admin_permissions = IntegerField('Admin Permissions', validators=[validators.Optional()])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email already exist.')

# Login form for the user
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "First name"})
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Last name"})
    date_of_birth = DateField('Date Of Birth', format='%d/%m/%Y', validators=[validators.Optional()], render_kw={"placeholder": "dd/mm/YY"})
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    # Admin Permissions
    admin_permissions = IntegerField('Admin Permisssions', validators=[validators.Optional()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('This email already exist. Please choose a different one.')


# View user form, for admin use only
class ViewUser(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('View')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "email"})
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is now account with that email. you must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')],
                                     render_kw={"placeholder": "confirm password"})
    submit = SubmitField('Reset Password')