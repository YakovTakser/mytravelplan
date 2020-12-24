from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from mytravelplan.config import Config
from flask_mail import Mail


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()


# Create app start the web app
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Modules import
    from mytravelplan.todolists.routes import todolists
    from mytravelplan.messages.routes import messages
    from mytravelplan.users.routes import users
    from mytravelplan.posts.routes import posts
    from mytravelplan.main.routes import main
    from mytravelplan.errors.handlers import errors

    # Create new data base if there is no data base exists
    with app.app_context():
        db.create_all()



    # Registering the imported modules to make them usable in the web app
    app.register_blueprint(todolists)
    app.register_blueprint(messages)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
