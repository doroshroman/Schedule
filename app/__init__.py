from flask import Flask
from flask_login import LoginManager
from flask_admin import Admin
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import modelviews
from app.models import Administrator, Group, Teacher, Subject, Lesson

admin = Admin(app, index_view=modelviews.MyAdminIndexView())
admin.add_view(modelviews.AdministratorView(Administrator, db.session))
admin.add_view(modelviews.BaseAdminView(Group, db.session))
admin.add_view(modelviews.BaseAdminView(Teacher, db.session))
admin.add_view(modelviews.BaseAdminView(Subject, db.session))
admin.add_view(modelviews.BaseAdminView(Lesson, db.session))

# To avoid mutual references
from app import routes, models