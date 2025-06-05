from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "supersecret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres@localhost/flask_tasks_db"

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Import models AFTER initializing db
    from app import models  # This triggers the __init__.py in models/ to load all models
    
    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    # Register blueprints
    from app.routes.task_routes import task_bp
    from app.routes.index_routes import index_bp
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(task_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)

    return app
