<<<<<<< HEAD
from flask import render_template, flash, url_for
from flask import request
from flask_login import current_user, login_user
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

import utils
from app import app
from app import db
from app.forms import AddScheduleForm
from app.forms import LoginForm
from app.models import *
from app.models import Admin

=======
from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import AddScheduleForm
import logging
import utils
from app.models import *
>>>>>>> dd7c9e1af27c01af01d511766398de83f7c4a552

@app.route('/')
@app.route('/index')
def index():
    return "Hello World!"


@app.route('/add_schedule', methods=['GET', 'POST'])
def add_schedule():
    form = AddScheduleForm()
    error = None
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
            
            # After successful adding pair
            return redirect(url_for('add_schedule'))
            
        except Exception as e:
            app.logger.info(e)
            error = "Incorrect fields!"
    
    return render_template('add_schedule.html', form=form, error=error)

<<<<<<< HEAD
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin is None or not admin.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(admin, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

=======
>>>>>>> dd7c9e1af27c01af01d511766398de83f7c4a552
