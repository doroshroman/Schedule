from app import app
from flask import render_template, flash
from app.forms import AddScheduleForm
import logging

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
        data = {
            "groupname" : form.groupname.data,
            "date_from" : form.date_from.data,
            "date_to" : form.date_to.data
        }
        # To log your testing data 
        #app.logger.info(date_from)
        # Validate correct date
    else:
        error = "Start date is greater than End date"
    
    return render_template('add_schedule.html', form=form, error=error, data=data)
