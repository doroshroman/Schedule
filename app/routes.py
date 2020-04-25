from app import app
from flask import render_template, flash
from app.forms import AddScheduleForm

@app.route('/')
@app.route('/index')
def hello_world():
    return "Hello World!"

@app.route('/add_schedule', methods=['GET', 'POST'])
def add_schedule():
    form = AddScheduleForm()
    if form.validate_on_submit():
        # Data from form is ready
        pass


    return render_template('add_schedule.html', form=form)
