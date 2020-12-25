from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, login
import datetime as dt


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    surname = db.Column(db.String(45))
    patronymic = db.Column(db.String(45))
    lessons = db.relationship('Lesson', backref='teacher', lazy='dynamic')

    def __str__(self):
        return f'{self.name} {self.surname} {self.patronymic}'

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'patronymic': self.patronymic
            }


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    lessons = db.relationship('Lesson', backref='group', lazy='dynamic')

    def __str__(self):
        return f'{self.name}'

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name
            }


class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    subj_type = db.Column(db.String(45))
    lessons = db.relationship('Lesson', backref='subject', lazy='dynamic')

    def __str__(self):
        return f'{self.title} {self.subj_type}'

    def as_dict(self):
        return {
            'id': self.id,
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

    def as_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'order': self.order,
            'auditory': self.auditory,
            'teacher': self.teacher.as_dict(),
            'group': self.group.as_dict(),
            'subject': self.subject.as_dict()
            }

    def __str__(self):
        return f'{self.id} {self.order} {self.date} {self.auditory} {self.teacher_id} {self.group_id} {self.subject_id}'

@login.user_loader
def load_user(id):
    return Administrator.query.get(int(id))

class Administrator(UserMixin,db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True) 
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

