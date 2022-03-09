from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)

from . import routes, models

db.create_all()
db.session.commit()
db.session.close()
