from flask_wtf import FlaskForm, validators
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, FileField, IntegerField, RadioField, SelectField
from wtforms.validators import DataRequired



# Post Form for creation and update of Post Object
class ToDoListForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Description')
    submit = SubmitField('Create')

class AddPostForm(FlaskForm):
    id = IntegerField('id')
    addPost = StringField('Title')
    add = SubmitField('Add into to do list')

class AddToDoListForm(FlaskForm):
    id = IntegerField('id')
    addToToDoList = StringField('Title')
    add = SubmitField('Add Here')


