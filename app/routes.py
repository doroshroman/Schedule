from flask import render_template, flash, redirect, url_for, request, jsonify, make_response
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from sqlalchemy.exc import SQLAlchemyError
from datetime import date, timedelta
import utils
from app import app
from app.forms import AddScheduleForm
from app.forms import LoginForm
from app.forms import SearchForm
from app.models import *

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    error = None
    from_day = None
    to_day = None 
    teacher_name = None
    lessons = {}
    
    if form.validate_on_submit():
        group = form.groupname.data
        from_day = form.from_day.data
        to_day = form.to_day.data
        teacher_name = form.teacher_name.data

        try:
            group_record = utils.get_group_by_name(group)
            lessons = utils.get_lessons_range(group_record, from_day, to_day)
            app.logger.info(lessons)
        except SQLAlchemyError as e:
            error = "Incorrect input data!"

    return render_template('show_schedule.html', form=form, day_schedules=lessons, error=error)

@app.route('/add_schedule', methods=['GET', 'POST'])
@login_required
def add():
    data = request.get_json()
    message = None
    success = True

    if data and len(data):
    
        teacher = None
        subject = None
        
        try:
            group = data['groupname']
            date = data['date']
            order = data['order']
            auditory = data['auditory']
            teacher_name = data['teacher']['name']
            teacher_surname = data['teacher']['surname']
            teacher_patronymic = data['teacher']['patronymic']
            subject_title = data['subject']['title']
            subject_type = data['subject']['subj_type']
            # Get teacher record
            group = utils.get_group_by_name(group)
            teacher = utils.get_teacher(teacher_name, teacher_surname, teacher_patronymic)
            
            # Get subject record
            subject = utils.get_subject(subject_title, subject_type)
        except SQLAlchemyError as se:
            app.logger.info(se)
            success = False
            message = "Incorrect teacher or subject!"
        
        except KeyError as ke:
            pass

        try:
            date = utils.convert_str_to_date(date, '%Y-%m-%d')
            order = int(order)
            lesson = Lesson(date=date, order=order, auditory=auditory, teacher=teacher, group=group, subject=subject)

            db.session.add(lesson)
            db.session.commit()
            
            
        except ValueError as ve:
            app.logger.info(ve)
            message = "Incorrect order!"
            success = False

        except SQLAlchemyError as se:
            app.logger.info(se)
            success = False
            message = str(se)

        return jsonify(success=success, message=message)
    else:
        return render_template('add_schedule.html')

@app.route('/copy_schedule', methods=['POST'])
def copy():
    data = request.get_json()
    if data and len(data):
        group = data['groupname']
        date = data['date']
        date_from = data['date_from']
        date_to = data['date_to']
        week_type = data['week_type']
        day_type = data['day_type']
        try:
            date = utils.convert_str_to_date(date,'%Y-%m-%d')
            date_from = utils.convert_str_to_date(date_from,'%Y-%m-%d')
            date_to = utils.convert_str_to_date(date_to,'%Y-%m-%d')

            group = utils.get_group_by_name(group)
            lessons = utils.get_lessons(group, date)
            days = utils.build_days_range(date_from, date_to)
            
            step = 7
            if week_type == 'odd':
                step = 14

            first_day_index = -1

            for i, day in enumerate(days):
                if day_type == day.strftime("%A"):
                    first_day_index = i
                    break
            if first_day_index != -1:
                for i in range(first_day_index, len(days), step ):
                    for lesson in lessons:
                        utils.copy_lesson(lesson, days[i])
                        
        except ValueError as ve:
            app.logger.info(ve)
        
    return "sex"
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

@app.route('/create', methods=["GET", "POST"])
def create():
    # Creating schedule for one semester
    schedule_meta = request.json
    app.logger.info(schedule_meta)
    flash_msg = None

    if schedule_meta:
        group = schedule_meta.get('groupname', None)
        date_from = schedule_meta.get('date_from', None)
        date_to = schedule_meta.get('date_to', None)
        subjects = schedule_meta.get('subjects', None)
        
        try:
            timetable = Timetable(group, date_from, date_to, subjects)
            timetable.generate_random_timetable()
            timetable.display_timetable()
            timetable.insert_into_db()

        except ValueError as ve:
            flash_msg = str(ve)

        except utils.CannotCreateException as exp:
            flash_msg = str(exp)

        except SQLAlchemyError as sqle:
            app.logger.info(sqle)
            flash_msg = str(sqle)
            
    if flash_msg:
        return jsonify({
            'flash': flash_msg
            })
    
    response = make_response(render_template('semester.html'))
    response.headers['Content-type'] = 'text/html; charset=utf-8'
    return response


@app.route('/add', methods=["GET", "POST"])
def add_shedule():
    pass
@app.route('/delete', methods=["POST"])
def delete():
    id = request.json
    if id:
        Lesson.query.filter_by(id=int(id)).delete()
        db.session.commit()
        return jsonify(success=True)
    else:
        return jsonify(success=False)

@app.route('/update/lesson/<int:lesson_id>', methods=["POST"])
def update(lesson_id):
    data = request.get_json()
    message = None
    success = True

    if data and len(data):
        # Read without validation
        order = data['order']
        auditory = data['auditory']
        teacher_name = data['teacher']['name']
        teacher_surname = data['teacher']['surname']
        teacher_patronymic = data['teacher']['patronymic']
        subject_title = data['subject']['title']
        subject_type = data['subject']['subj_type']

        teacher = None
        subject = None
        try:
            # Get teacher record
            teacher = utils.get_teacher(teacher_name, teacher_surname, teacher_patronymic)
            
            # Get subject record
            subject = utils.get_subject(subject_title, subject_type)
        except SQLAlchemyError as se:
            app.logger.info(se)
            success = False
            message = "Incorrect teacher or subject!"

        try:
            lesson = Lesson.query.get(lesson_id)
            # Update lesson
            order = int(order)
            lesson.order = order if order <= 5 else 5
            lesson.auditory = auditory

            lesson.teacher = teacher
            lesson.subject = subject

            db.session.commit()
            
            message = f'Successfully updated lesson with id: {lesson_id}' 
            
        except ValueError as ve:
            app.logger.info(ve)
            message = "Incorrect order!"
            success = False

        except SQLAlchemyError as se:
            app.logger.info(se)
            success = False
            message = str(se)

    return jsonify(success=success, message=message)

@app.route('/lesson/<int:lesson_id>', methods=["GET"])
def show_lesson(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    return jsonify(lesson.as_dict())

