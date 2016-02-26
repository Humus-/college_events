from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = 'myverylongsecretkey'

# Flask-Login setup
from flask.ext.login import LoginManager
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.session_protection = "strong"
login_manager.setup_app(app)

bootstrap = Bootstrap(app)

# MySQL DB setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/evento'

# Echo all the sql queries
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

from models import User
db.create_all()
db.session.commit()

# Register blueprints
from .views.dashboard import dashboard
from .views.profile import profile
from .views.home import home
app.register_blueprint(home)
app.register_blueprint(dashboard)
app.register_blueprint(profile)

