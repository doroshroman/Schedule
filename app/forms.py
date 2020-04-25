from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired

class AddScheduleForm(FlaskForm):
    groupname = StringField('Group Name', validators=[DataRequired()])
    date_from = DateField('Date From', format='%d/%m/%Y', validators=[DataRequired()])
    date_to = DateField('Date To', format='%d/%m/%Y', validators=[DataRequired()])
    submit = SubmitField("Create Schedule")