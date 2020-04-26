from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import AddScheduleForm
import logging
import utils
from app.models import *

@app.route('/')
@app.route('/index')
def index():
    return "Hello World!"


@app.route('/add_schedule', methods=['GET', 'POST'])
def add_schedule():
    form = AddScheduleForm()

    if form.validate_on_submit():
        # Grab data from form
        try:
            group = form.groupname.data
            group_record = db.session().query(Group).filter_by(name=group).one()
            day = form.day.data
            PAIRS = 5

            for i in range(PAIRS):
                lesson = utils.read_lesson_data(form, i+1)
                if utils.is_valid_lesson(lesson):
                    
                    name, surname, patronymic = lesson["teacher"].split()
                    teacher = db.session().query(Teacher).filter(
                        Teacher.name.like(name),
                        Teacher.surname.like(surname),
                        Teacher.patronymic.like(patronymic)
                    ).one()
                    title = lesson["subject"]
                    subj_type = lesson["subject_type"]
                    subj_record = db.session.query(Subject).filter(
                        Subject.title.like(title),
                        Subject.subj_type.like(subj_type)
                    ).one()
                    pair = Lesson(date=day, order=i+1, auditory=lesson["auditory"], teacher=teacher, group=group_record, subject=subj_record)
                    db.session.add(pair)
                    db.session.commit()

        except Exception as e:
            app.logger.info(e)
            pass

    return render_template('add_schedule.html', form=form)

