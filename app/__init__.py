from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
from app import ansible_facts
bootstrap = Bootstrap(app)