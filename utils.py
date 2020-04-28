from builtins import range
from datetime import date, timedelta
from flask import logging
from app.models import *
from app import app, db

def count_days(date_start, date_end):
    return (date_end - date_start).days + 1

def is_weekend(day):
    SATURDAY = 5
    SUNDAY = 6
    return (day.weekday() == SATURDAY or day.weekday() == SUNDAY)  

def build_days_range(date_start, date_end):
    count = count_days(date_start, date_end)
    days = []
    for i in range(count):
        if not is_weekend(date_start):
            days.append(date_start)
        date_start = date_start + timedelta(1)
    return days

# For form utils and validation
def read_lesson_data(form, order):
    inputs = ["auditory", "teacher", "subject", "subject_type"]
    fields = list(map(lambda x: x + str(order),inputs))
    lesson = {}
    for i, f in zip(inputs,fields):
        lesson[i] = form[f].data
    return lesson

def is_valid_lesson(lesson):
    return not('' in lesson.values() or None in lesson.values())

# Db queries
def get_group_by_name(name):
    return db.session().query(Group).filter_by(name=name).one()

def get_teacher(name, surname, patronymic):
    teacher = db.session().query(Teacher).filter(
                        Teacher.name.like(name),
                        Teacher.surname.like(surname),
                        Teacher.patronymic.like(patronymic)).one()
    return teacher

def get_subject(title, subj_type):
    subj_record = db.session.query(Subject).filter(
                        Subject.title.like(title),
                        Subject.subj_type.like(subj_type)).one()
    return subj_record

def get_lessons(group, date):
    lessons_per_day = db.session.query(Lesson).filter_by(group=group, date=date).order_by(Lesson.order).all()
    return lessons_per_day 

def get_lessons_range(group, date_from, date_to):
    lessons_range = db.session.query(Lesson).filter_by(group=group).filter(Lesson.date.between(date_from, date_to)).all()
    lessons = convert_lessons_to_dict(lessons_range)
    return lessons

def convert_lessons_to_dict(lessons):
    lessons_dict = {}
    for lesson in lessons:
        key = lesson.date
        if key in lessons_dict:
            lessons_dict[key].append(lesson)
        else:
            lessons_dict[key] = [lesson]
    return lessons_dict

if __name__ == "__main__":
    pass
