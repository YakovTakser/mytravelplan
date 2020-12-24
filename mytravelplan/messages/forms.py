from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired



# Message Form for creation of Message Object
class MessageForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    content = TextAreaField('Content')
    receiver = StringField('Receiver', validators=[DataRequired()])
    submit = SubmitField('Send Message')

# Message Form for creation of Message Object
class MessageAllForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    content = TextAreaField('Content')
    submit = SubmitField('Send Message')

# Message button in account show
class MessageClickForm(FlaskForm):
    submit = SubmitField('Send Message')