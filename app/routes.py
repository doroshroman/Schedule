from app import app
from flask import render_template, flash
from app.forms import AddScheduleForm
import logging
import utils

@app.route('/')
@app.route('/index')
def hello_world():
    return "Hello World!"

@app.route('/add_schedule', methods=['GET', 'POST'])
def add_schedule():
    form = AddScheduleForm()
    data = {}
    error = None
    if form.validate_on_submit():
        # Data from form is ready
        group = form.groupname.data
        date_from = form.date_from.data
        date_to = form.date_to.data

        days = utils.build_days_range(date_from, date_to)
        app.logger.info(days)
        
        data = {
            "groupname" : group,
            "days": days
            }

    else:
        error = "Start date is greater than End date"
    
    return render_template('add_schedule.html', form=form, error=error, data=data)
