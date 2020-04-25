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
    groupname = None
    date_from = None
    date_to = None
    if form.validate_on_submit():
        # Data from form is ready
        groupname = form.groupname.data
        date_from = form.date_from.data
        date_to = form.date_to.data
    return render_template('add_schedule.html', form=form, group=groupname, date_from=date_from, date_to=date_to)
