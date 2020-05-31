from builtins import range
from datetime import date, timedelta, datetime
from flask import logging
from app.models import *
from app import app, db
from sqlalchemy.orm.session import make_transient

def copy_lesson(lesson, date):
    lesson = Lesson(date=date, order=lesson.order, auditory=lesson.auditory, teacher=lesson.teacher, group=lesson.group, subject=lesson.subject)

    db.session.add(lesson)
    db.session.commit()

def count_days(date_start, date_end):
    if date_start > date_end:
        return -1
    return (date_end - date_start).days + 1

def get_day_index(date, date_start, date_end):
    # date - format datetime.date
    date = datetime(date.year, date.month, date.day)
    if (date > date_end or date < date_start):
        return -1
    else:
        return (date - date_start).days  

def convert_str_to_date(str_date, format):
    return datetime.strptime(str_date, format)

def build_days_range(date_start, date_end):
    count = count_days(date_start, date_end)
    days = []
    for i in range(count):
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

def get_group_by_name(name):
    return db.session().query(Group).filter_by(name=name).one()

def get_teacher(name, surname, patronymic):
    teacher = db.session().query(Teacher).filter(
                        Teacher.name.like(name),
                        Teacher.surname.like(surname),
                        Teacher.patronymic.like(patronymic)).one()
    return teacher
    
def get_random_teacher():
    index = random.randrange(0, db.session.query(Teacher).count())
    return db.session.query(Teacher)[index] 

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
    lessons = utils.convert_lessons_to_dict(lessons_range)
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

# Exceptions
class CannotCreateException(Exception):
    pass

# Filters
@app.template_filter()
def slot_start(order):
    """Convert order to start time"""
    order_to_time = {
        1: '08:30',
        2: '10:05',
        3: '11:55',
        4: '13:30',
        5: '15:05' 
    }
    if order in order_to_time:
        return order_to_time[order]
    else:
        return order_to_time[1]

@app.template_filter()
def slot_end(order):
    """Convert order to end time"""
    order_to_time = {
        1: '09:50',
        2: '11:25',
        3: '13:15',
        4: '14:50',
        5: '16:25'
    }
    if order in order_to_time:
        return order_to_time[order]
    else:
        return order_to_time[1]

if __name__ == "__main__":
    pass
