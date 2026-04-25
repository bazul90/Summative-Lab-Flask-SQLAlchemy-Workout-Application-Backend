from extensions import db
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')

    __table_args__ = (
        CheckConstraint("LENGTH(name) >= 3", name='check_name_length'),
        CheckConstraint("category IN ('strength', 'cardio', 'flexibility')", name='check_category'),
    )

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 3:
            raise ValueError("Exercise name must be at least 3 characters")
        return name.strip()

    @validates('category')
    def validate_category(self, key, category):
        allowed_categories = ['strength', 'cardio', 'flexibility']
        if category.lower() not in allowed_categories:
            raise ValueError(f"Category must be one of: {', '.join(allowed_categories)}")
        return category.lower()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'equipment_needed': self.equipment_needed
        }

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')

    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_positive_duration'),
    )

    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if not duration or duration <= 0:
            raise ValueError("Duration must be greater than 0")
        return duration

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'duration_minutes': self.duration_minutes,
            'notes': self.notes
        }

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id', ondelete='CASCADE'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id', ondelete='CASCADE'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    __table_args__ = (
        CheckConstraint("reps IS NULL OR reps >= 0", name='check_non_negative_reps'),
        CheckConstraint("sets IS NULL OR sets >= 0", name='check_non_negative_sets'),
        CheckConstraint("duration_seconds IS NULL OR duration_seconds >= 0", name='check_non_negative_duration'),
        UniqueConstraint('workout_id', 'exercise_id', name='unique_workout_exercise'),
    )

    @validates('reps', 'sets', 'duration_seconds')
    def validate_non_negative(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f"{key} must be non-negative")
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'workout_id': self.workout_id,
            'exercise_id': self.exercise_id,
            'reps': self.reps,
            'sets': self.sets,
            'duration_seconds': self.duration_seconds,
            'exercise': self.exercise.to_dict() if self.exercise else None
        }
