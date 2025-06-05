from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    # title = StringField("Title", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired(message="Please fill in title field")])
    description = TextAreaField("Description")
