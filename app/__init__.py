from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# To avoid mutual references
from app import routes