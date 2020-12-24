from flask_wtf import FlaskForm, validators
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, FileField, IntegerField, RadioField, SelectField
from wtforms.validators import DataRequired



# Post Form for creation and update of Post Object
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Description')
    country = StringField('Country', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    rate = SelectField('Rate', choices=[('1', '✩'), ('2', '✩✩'), ('3', '✩✩✩'), ('4', '✩✩✩✩'), ('5', '✩✩✩✩✩')], validators=[DataRequired()])
    find_friends = SelectField('Find Friends', choices=[('False', 'No'), ('True', 'Yes')], validators=[DataRequired()])
    place = StringField('Place', validators=[DataRequired()])
    submit = SubmitField('Post')


# Comment Form for creation of Comment Object
class CommentForm(FlaskForm):
    content = TextAreaField('New Comment:', validators=[DataRequired()], render_kw={"placeholder": "Write your comment here.."})
    submit = SubmitField('Comment')

# Search Form
class SearchForm(FlaskForm):
    user = StringField('User')
    country = StringField('Country')
    city = StringField('City')
    place = StringField('Place')
    submit = SubmitField('Search')

class LikeForm(FlaskForm):
    id = IntegerField('id')
    like_or_unlike = StringField('like_or_unlike')
    like = SubmitField('Like')
    unlike = SubmitField('Unlike')

class ReportForm(FlaskForm):
    id = IntegerField('id')
    report = SubmitField('Report Post')
