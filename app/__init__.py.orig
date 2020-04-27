from flask import Flask
from flask_login import LoginManager

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
<<<<<<< HEAD
login = LoginManager(app)
=======
>>>>>>> dd7c9e1af27c01af01d511766398de83f7c4a552

# To avoid mutual references
from app import routes, models