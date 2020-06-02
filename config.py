import os


class Config():
    # To protect form from attack
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'so-secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+mysqlconnector://root:Chaii2323@localhost/mydb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
