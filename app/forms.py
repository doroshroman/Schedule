from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from datetime import date

class AddScheduleForm(FlaskForm):
    groupname = StringField('Group Name', validators=[DataRequired()])
    date_from = DateField('Date From', default=date.today, validators=[DataRequired()])
    date_to = DateField('Date To', default=date.today, validators=[DataRequired()])
    submit = SubmitField("Create Schedule")

    def validate_on_submit(self):
        result = super(AddScheduleForm, self).validate()
        if self.date_from.data > self.date_to.data:
            return False
        else:
            return result 