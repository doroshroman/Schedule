from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from sqlalchemy.exc import SQLAlchemyError

import utils
from app import app
from app.forms import AddScheduleForm
from app.forms import LoginForm
from app.models import *


@app.route('/')
@app.route('/index')
def index():
    return "Hello World!"


@app.route('/add_schedule', methods=['GET', 'POST'])
#@login_required
def add_schedule():
    form = AddScheduleForm()
    errors = []
    if form.validate_on_submit():
        # Grab data from form
        group = form.groupname.data
        day = form.day.data
        PAIRS = 5
        group_record = None

        try:
            group_record = utils.get_group_by_name(group)
        except SQLAlchemyError as e:
            e = "Group not found"
            errors.append(e)
            
        for i in range(PAIRS):
            lesson = utils.read_lesson_data(form, i+1)
            if utils.is_valid_lesson(lesson): 
                # Parse field 
                auditory = lesson["auditory"]
                name, surname, patronymic = lesson["teacher"].split()
                title = lesson["subject"]
                subj_type = lesson["subject_type"]

                try:
                    teacher = utils.get_teacher(name, surname, patronymic)
                    subject = utils.get_subject(title, subj_type)
                    pair = Lesson(date=day, order=i+1, auditory=auditory, teacher=teacher, group=group_record, subject=subject)
                    db.session.add(pair)
                    db.session.commit()

                    return redirect(url_for('index'))

                except SQLAlchemyError as e:
                    app.logger.error(e)
                    e = f"Some fields are incorrect in {i+1} row!"
                    errors.append(e)

    return render_template('add_schedule.html', form=form, errors=errors)

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
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('add_schedule')
        return redirect(next_page)
        # return redirect(url_for('add_schedule'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/groups')
def groups():
    records = Group.query.all()
    group_list = [rec.as_dict() for rec in records]
    return jsonify(group_list)

@app.route('/teachers')
def teachers():
    records = Teacher.query.all()
    teacher_list = [rec.as_dict() for rec in records]
    return jsonify(teacher_list)

@app.route('/subjects')
def subjects():
    records = Subject.query.all()
    subject_list = [rec.as_dict() for rec in records]
    return jsonify(subject_list)

@app.errorhandler(404)
def page_not_found(error):
	app.logger.error(f'Page not found: {request.path}')
	return render_template('404.html'), 404