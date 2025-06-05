from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description")
    start_date = DateField("Start Date", format='%Y-%m-%d')
    due_date = DateField("Due Date", format='%Y-%m-%d')
    priority = SelectField("Priority", choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    status = SelectField("Status", choices=[('1', 'To Do'), ('2', 'Doing'), ('3', 'Done')])
