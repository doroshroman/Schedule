from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import AddScheduleForm
import logging
import utils

@app.route('/')
@app.route('/index')
def index():
    return "Hello World!"


@app.route('/add_schedule', methods=['GET', 'POST'])
def add_schedule():
    form = AddScheduleForm()
    
    if form.validate_on_submit():
        group = form.groupname.data
        day = form.day.data
        
        if utils.is_weekend(day):
            return redirect(url_for('add_schedule')) 


    return render_template('add_schedule.html', form=form)

