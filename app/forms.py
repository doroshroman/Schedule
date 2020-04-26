from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Optional
from datetime import date

class AddScheduleForm(FlaskForm):
    groupname = StringField('Group Name', validators=[DataRequired()])
    day = DateField('Date', default=date.today, validators=[DataRequired()])

    auditory_first = StringField('Auditory')
    teacher_first = StringField('Teacher')
    subject_first = StringField('Subject')
    subject_type_first = SelectField('Type',default='',validators=[Optional()], choices=[('lec', 'Lecture'), ('lab', 'Practise')])
    
    auditory_second = StringField('Auditory')
    teacher_second= StringField('Teacher')
    subject_second = StringField('Subject')
    subject_type_second = SelectField('Type',default='',validators=[Optional()], choices=[('lec', 'Lecture'), ('lab', 'Practise')])
    
    auditory_third = StringField('Auditory')
    teacher_third = StringField('Teacher')
    subject_third = StringField('Subject')
    subject_type_third = SelectField('Type',default='',validators=[Optional()], choices=[('lec', 'Lecture'), ('lab', 'Practise')])
    
    auditory_fourth = StringField('Auditory')
    teacher_fourth = StringField('Teacher')
    subject_fourth = StringField('Subject')
    subject_type_fourth = SelectField('Type',default='',validators=[Optional()], choices=[('lec', 'Lecture'), ('lab', 'Practise')])
    
    auditory_fifth = StringField('Auditory')
    teacher_fifth = StringField('Teacher')
    subject_fifth = StringField('Subject')
    subject_type_fifth = SelectField('Type',default='',validators=[Optional()], choices=[('lec', 'Lecture'), ('lab', 'Practise')])

    submit = SubmitField('Add')
