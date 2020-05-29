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
    #lessons = db.relationship('Lesson', backref='teacher', lazy='dynamic')

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
    #lessons = db.relationship('Lesson', backref='group', lazy='dynamic')

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
    #lessons = db.relationship('Lesson', backref='subject', lazy='dynamic')

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
    teacher = db.relationship(Teacher, backref='lessons')
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    group = db.relationship(Group, backref='lessons_groups')
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    subject = db.relationship(Subject, backref='lessons_subjects')

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

    def __init__(self, group, date_from, date_to, subjects):
        self.group = utils.get_group_by_name(group)
        
        self.date_from, self.date_to, self._days = self._init_dates(date_from, date_to)

        self.subjects = subjects
        self._pairs = 5
        self._lesson_in_db = {}
        self.calendar = self._init_timetable()
        
    
    def _init_dates(self, date_from, date_to):
        date_from = utils.convert_str_to_date(date_from, '%Y-%m-%d')
        date_to = utils.convert_str_to_date(date_to, '%Y-%m-%d')
        days = utils.count_days(date_from, date_to)
        
        if days == -1:
            raise utils.CannotCreateException("Incorrect dates")

        return date_from, date_to, days

    def _init_timetable(self):
        
        calendar = []
        for i in range(self._pairs):
            row = [None for j in range(self._days)]
            calendar.append(row)

        lessons = utils.get_lessons_range(self.group, self.date_from, self.date_to)
        
        for date, pairs in lessons.items():
            day_index = utils.get_day_index(date, self.date_from, self.date_to)
            for pair in pairs:
                self.update_subjects(pair.subject)
                pair_order = pair.order
                if pair_order:
                    calendar[pair_order - 1][day_index] = pair
                    self._lesson_in_db[pair] = True
        return calendar
    
    def update_subjects(self, subject):
        if not self.subjects:
            raise utils.CannotCreateException("Set up the subjects")

        for sub in self.subjects:
            title = sub.get("subjects", None)
            sub_type = sub.get("subj_type", None)
            hours = sub.get("hours", 0)
            if title == subject.title and sub_type == subject.subj_type:
                sub["hours"] = int(hours) - 1

    def _create_random_lesson(self, group_record):

        day_index = random.randrange(0, self._days)
        random_day = self.date_from + dt.timedelta(days=day_index)
        # To store in db that's why pairs + 1
        number = random.randrange(1, self._pairs + 1)

        auditory = random.randrange(300, 400)

        teacher_index = random.randrange(0, db.session.query(Teacher).count())
        teacher = db.session.query(Teacher)[teacher_index]

        subject_index = random.randrange(0, len(self.subjects))
        random_subject = self.subjects[subject_index]
        subject_title = random_subject.get('subject', '')
        subject_type = random_subject.get('subj_type', '')
        subject_hours = random_subject.get('hours', 0)

        subject = utils.get_subject(subject_title, subject_type)

        # Insert into timetable calendar
        order_pos = number - 1
        day_pos = day_index

        if self.calendar[order_pos][day_pos] is None:
            if subject_hours:
                lesson = Lesson(date=random_day, order=number, auditory=auditory, teacher=teacher, group=group_record, subject=subject)
                random_subject['hours'] = int(subject_hours) - 1
                self.calendar[order_pos][day_pos] = lesson
            
    
    def generate_random_timetable(self):
        error_msg = None
        if(not self._can_create()):
            error_msg = 'Too much hours for this period'
        else:
            # Create random lessons
            while(self._is_hours_remains() and self._get_free_position() > 0):
                self._create_random_lesson(self.group)

        if error_msg:
            raise utils.CannotCreateException(error_msg)
            
    def _get_free_position(self):
        return sum(row.count(None) for row in self.calendar)

    def _is_hours_remains(self):
        for subject in self.subjects:
            hours = subject.get('hours', 0)
            if hours and int(hours) > 0:
                return True

        return False
    
    def _get_total_hours(self):
        return sum(int(sub.get('hours', 0)) for sub in self.subjects)
    
    def _can_create(self):
        return self._pairs * self._days >= self._get_total_hours()

    def display_timetable(self):
        app.logger.info(self.calendar)

    def insert_into_db(self):
        for i in range(self._pairs):
            for j in range (self._days):
                lesson = self.calendar[i][j]
                if lesson and lesson not in self._lesson_in_db:
                    db.session.add(lesson)
                    db.session.commit()