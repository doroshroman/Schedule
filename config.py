import os

class Config():
    # To protect form from attack
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'so-secret'
