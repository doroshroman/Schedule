from app import db

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    surname = db.Column(db.String(45))
    patronymic = db.Column(db.String(45))
    lessons = db.relationship('Lesson', backref='teacher_lesson', lazy='dynamic')

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    lessons = db.relationship('Lesson', backref='group_lesson', lazy='dynamic')

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    subj_type = db.Column(db.String(45))
    lessons = db.relationship('Lesson', backref='subject_lesson', lazy='dynamic')

class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    order = db.Column(db.Integer)
    auditory = db.Column(db.String(45))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    