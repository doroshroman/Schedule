from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Optional
from datetime import date

class AddScheduleForm(FlaskForm):
    groupname = StringField('Group Name', validators=[DataRequired()])
    day = DateField('Date', default=date.today, validators=[DataRequired()])

    auditory1 = StringField('Auditory')
    teacher1 = StringField('Teacher')
    subject1 = StringField('Subject')
    subject_type1 = SelectField('Type',default='',validators=[Optional()], choices=[('lec', 'Lecture'), ('lab', 'Practise')])
    
    auditory2 = StringField('Auditory')
    teacher2= StringField('Teacher')
    subject2 = StringField('Subject')
    subject_type2 = SelectField('Type',default='',validators=[Optional()], choices=[('lec', 'Lecture'), ('lab', 'Practise')])
    
    auditory3 = StringField('Auditory')
    teacher3 = StringField('Teacher')
    subject3 = StringField('Subject')
    subject_type3 = SelectField('Type',default='',validators=[Optional()], choices=[('lec', 'Lecture'), ('lab', 'Practise')])
    
    auditory4 = StringField('Auditory')
    teacher4 = StringField('Teacher')
    subject4 = StringField('Subject')
    subject_type4 = SelectField('Type',default='',validators=[Optional()], choices=[('lec', 'Lecture'), ('lab', 'Practise')])
    
    auditory5 = StringField('Auditory')
    teacher5 = StringField('Teacher')
    subject5 = StringField('Subject')
    subject_type5 = SelectField('Type',default='',validators=[Optional()], choices=[('lec', 'Lecture'), ('lab', 'Practise')])

    submit = SubmitField('Add')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SearchForm(FlaskForm):
    groupname = StringField('Group Name', validators=[DataRequired()])
    from_day = DateField('Date', default=date.today)
    to_day = DateField('Date', default=date.today)
    teacher_name = StringField('Teacher')

    submit = SubmitField('Search')