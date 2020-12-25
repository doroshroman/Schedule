from flask_admin import AdminIndexView
from flask_login import current_user
from flask import redirect, url_for, request, flash
from flask_admin.contrib.sqla import ModelView
import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin.form import rules
from wtforms import PasswordField


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        req = re.findall(r'(/\w+/.*)', request.url)[0]
        return redirect(url_for('login', next=req))


class BaseAdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        req = re.findall(r'(/\w+/.*)', request.url)[0]
        return redirect(url_for('login', next=req))


class AdministratorView(BaseAdminView):
    
    form_edit_rules = (
        'username',
        rules.Header('Reset Password'),
        'new_password', 'confirm'
    )

    form_create_rules = (
        'username', 'email', 'password'
    )

    def scaffold_form(self):
        form_class = super(AdministratorView, self).scaffold_form()
        form_class.password = PasswordField('Password')
        form_class.new_password = PasswordField('New Password')
        form_class.confirm = PasswordField('Confirm')
        return form_class
    
    def create_model(self, form):
        password_hash = generate_password_hash(form.password.data)
        model = self.model(
            username=form.username.data, email=form.email.data,
            password_hash=password_hash
        )
        form.populate_obj(model)
        self.session.add(model)
        self._on_model_change(form, model, True)
        self.session.commit()
    
    def update_model(self, form, model):
        form.populate_obj(model)
        if form.new_password.data:
            if form.new_password.data != form.confirm.data:
                flash('Passwords must match', 'warning')
                return
            model.password_hash = generate_password_hash(form.new_password.data)
        self.session.add(model)
        self._on_model_change(form, model, False)
        self.session.commit()

