from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Optional
from datetime import date


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SearchForm(FlaskForm):
    groupname = StringField('Group Name', validators=[DataRequired()])
    from_day = DateField('Date', default=date.today)
    to_day = DateField('Date', default=date.today)
    teacher = StringField('Teacher')

    submit = SubmitField('Search')



    