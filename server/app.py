from flask import Flask
from config import Config
from extensions import db, ma, migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    from routes.workout_routes import workout_bp
    from routes.exercise_routes import exercise_bp
    from routes.workout_exercise_routes import workout_exercise_bp

    app.register_blueprint(workout_bp)
    app.register_blueprint(exercise_bp)
    app.register_blueprint(workout_exercise_bp)

    return app