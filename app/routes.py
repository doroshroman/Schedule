from flask import render_template, flash, redirect, url_for, request, jsonify, make_response
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from sqlalchemy.exc import SQLAlchemyError
from datetime import date, timedelta
from app import app
from app import utils
from app import db
from app.forms import AddScheduleForm
from app.forms import LoginForm
from app.forms import SearchForm
from app.models import Teacher, Group, Lesson, Subject, Administrator


@app.route('/index4update/', methods=['GET', 'POST'])
@login_required
def index4update():
    form = SearchForm()
    error = None
    from_day = None
    to_day = None 
    teacher = None
    lessons = {}
    
    if form.validate_on_submit():
        group = form.groupname.data
        from_day = form.from_day.data
        to_day = form.to_day.data
        teacher = form.teacher.data

        try:
            group_record = Group.query.filter_by(name=group).first()
            lessons = utils.get_lessons_range(group_record, from_day, to_day)
            app.logger.info(lessons)
        except SQLAlchemyError as e:
            error = "Incorrect input data!"

    return render_template('admin_index.html', form=form, day_schedules=lessons, error=error)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    message = None
    lessons = {}
    if form.validate_on_submit():
        
        group = form.groupname.data
        from_day = form.from_day.data
        to_day = form.to_day.data
        teacher = form.teacher.data

        group = Group.query.filter_by(name=group).first()
        if not group:
            flash(f'Group {group} not found', 'info')
            return redirect(url_for('index'))

        lessons = utils.get_lessons_range(group, from_day, to_day)

    return render_template('index.html', form=form, day_schedule=lessons)


@app.route('/add_schedule/', methods=['GET', 'POST'])
@login_required
def add_schedule():
    data = request.get_json()
    print(data)
    message = None
    success = True

    if data and len(data):
        try:
            group = data['groupname']
            date = data['date']
            order = data['order']
            auditory = data['auditory']
            teacher = data['teacher']['name']
            teacher_surname = data['teacher']['surname']
            teacher_patronymic = data['teacher']['patronymic']
            subject_title = data['subject']['title']
            subject_type = data['subject']['subj_type']
            

            group = Group.query.filter_by(name=group).first()
            teacher = utils.get_teacher(teacher, teacher_surname, teacher_patronymic)
            subject = utils.get_subject(subject_title, subject_type)
        
            date = utils.convert_str_to_date(date, '%Y-%m-%d')
            order = int(order)
            lesson = Lesson(date=date, order=order, auditory=auditory, teacher=teacher, group=group, subject=subject)

            db.session.add(lesson)
            db.session.commit()
            
            
        except ValueError as ve:
            app.logger.info(ve)
            message = "Incorrect order!"
            success = False
        except KeyError as ke:
            app.logger.info(ke)
            success = False
            message = "Caught empty lesson"
        except SQLAlchemyError as se:
            app.logger.info(se)
            success = False
            message = "Incorrect data or busy lesson for this time"

        return jsonify(success=success, message=message)
    else:
        return render_template('add_schedule.html')


@app.route('/copy_schedule/', methods=['POST'])
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

            group = Group.query.filter_by(name=group).first()
            lessons = utils.get_lessons(group, date)
            print(lessons)
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
                for i in range(first_day_index, len(days), step):
                    for lesson in lessons:
                        utils.copy_lesson(lesson, days[i])
                        
        except ValueError as ve:
            app.logger.info(ve)
        
    return jsonify(success=True)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        admin = Administrator.query.filter_by(username=form.username.data).first()
        if admin is None or not admin.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(admin, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('add_schedule')
        return redirect(next_page)
        
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/groups/')
def groups():
    records = Group.query.all()
    group_list = [rec.as_dict() for rec in records]
    return jsonify(group_list)

@app.route('/teachers/')
def teachers():
    records = Teacher.query.all()
    teacher_list = [rec.as_dict() for rec in records]
    return jsonify(teacher_list)

@app.route('/subjects/')
def subjects():
    records = Subject.query.all()
    subject_list = [rec.as_dict() for rec in records]
    return jsonify(subject_list)

@app.errorhandler(404)
def page_not_found(error):
	app.logger.error(f'Page not found: {request.path}')
	return render_template('404.html'), 404


@app.route('/delete', methods=["POST"])
@login_required
def delete():
    id = request.json
    if id:
        Lesson.query.filter_by(id=int(id)).delete()
        db.session.commit()
        return jsonify(success=True)
    else:
        return jsonify(success=False)

@app.route('/update/lesson/<int:lesson_id>', methods=["POST"])
@login_required
def update(lesson_id):
    data = request.get_json()
    
    if data and len(data):
        # Read without validation
        order = data['order']
        auditory = data['auditory']
        teacher = data['teacher']['name']
        teacher_surname = data['teacher']['surname']
        teacher_patronymic = data['teacher']['patronymic']
        subject_title = data['subject']['title']
        subject_type = data['subject']['subj_type']

        teacher = None
        subject = None
        try:
            # Get teacher record
            teacher = utils.get_teacher(teacher, teacher_surname, teacher_patronymic)
            
            # Get subject record
            subject = utils.get_subject(subject_title, subject_type)
        except SQLAlchemyError as se:
            app.logger.info(se)
            message = "Incorrect teacher or subject!"
            return jsonify(success=False, message=message)
        
        try:
            lesson = Lesson.query.get(lesson_id)
            # Update lesson
            order = int(order)
            lesson.order = order if order <= 5 else 5
            lesson.auditory = auditory

            lesson.teacher = teacher
            lesson.subject = subject

            db.session.commit()

        except (ValueError, SQLAlchemyError):
            message = "Busy auditory or order"
            return jsonify(success=False, message=message)

    message = f'Successfully updated lesson with id: {lesson_id}' 
    return jsonify(success=True, message=message)

@app.route('/lesson/<int:lesson_id>', methods=["GET"])
def show_lesson(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    return jsonify(lesson.as_dict())

