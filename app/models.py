from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db, login
import datetime as dt
import utils
import random
import copy

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    surname = db.Column(db.String(45))
    patronymic = db.Column(db.String(45))
    lessons = db.relationship('Lesson', backref='teacher', lazy='dynamic')

    def as_dict(self):
        return {
            'name': self.name,
            'surname': self.surname,
            'patronymic': self.patronymic
            }

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    lessons = db.relationship('Lesson', backref='group', lazy='dynamic')

    def as_dict(self):
        return {'name': self.name}


class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    subj_type = db.Column(db.String(45))
    lessons = db.relationship('Lesson', backref='subject', lazy='dynamic')

    def as_dict(self):
        return {
            'title': self.title,
            'subj_type': self.subj_type
            }

class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    order = db.Column(db.Integer)
    auditory = db.Column(db.String(45))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)

class Admin(UserMixin,db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return Admin.query.get(int(id))

class Timetable():
    def __init__(self, group, total_hours, date_from, date_to):
        self.group = group
        self.total_hours = total_hours
        self.date_from = dt.datetime.strptime(date_from, '%Y-%m-%d')
        self.date_to = dt.datetime.strptime(date_to, '%Y-%m-%d')
        
    def generate_random_timetable(self, subjects=None):
        # Insert into random day and in random order
        # 1. Choose random day
        # 2. Choose random number from 1 to 5(inclusive)
        # 3. Choose random auditory
        # 4. Choose random teacher
        # 5. Choose random subject and update hours
        # 6. We have group
        # Create lesson
        days = utils.count_days(self.date_from, self.date_to)
        index = random.randrange(0, days)
        random_day = self.date_from + dt.timedelta(days=index)
        
        pairs = 5
        number = random.randrange(1, pairs + 1)

        auditory = random.randrange(300, 400)

        index = random.randrange(0, db.session.query(Teacher).count())
        teacher = db.session.query(Teacher)[index] 
        
        subjects = copy.deepcopy(subjects)
        index = random.randrange(0, len(subjects))
        random_subject = subjects[index]
        subject_title = random_subject.get('subject', '')
        subject_type = random_subject.get('subj_type', '')
        
        subject = utils.get_subject(subject_title, subject_type)
        group = utils.get_group_by_name(self.group)

        lesson = Lesson(date=random_day, order=number, auditory=auditory, teacher=teacher, group=group, subject=subject)
        db.session.add(lesson)
        db.session.commit()
        

