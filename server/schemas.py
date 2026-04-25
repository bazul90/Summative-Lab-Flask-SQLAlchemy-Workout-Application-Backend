from flask_marshmallow import Marshmallow
from marshmallow import validates, ValidationError, validate, validates_schema
from .models import Exercise, Workout, WorkoutExercise

ma = Marshmallow()

class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        load_instance = True

    name = ma.Str(required=True, validate=validate.Length(min=3))
    category = ma.Str(required=True, validate=validate.OneOf(['strength', 'cardio', 'flexibility']))
    equipment_needed = ma.Bool(load_default=False)

class WorkoutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        load_instance = True
        include_fk = True

    date = ma.Date(required=True)
    duration_minutes = ma.Int(required=True, validate=validate.Range(min=1))
    notes = ma.Str(allow_none=True)

class WorkoutExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        load_instance = True
        include_fk = True

    workout_id = ma.Int(required=True)
    exercise_id = ma.Int(required=True)
    reps = ma.Int(allow_none=True, validate=validate.Range(min=0))
    sets = ma.Int(allow_none=True, validate=validate.Range(min=0))
    duration_seconds = ma.Int(allow_none=True, validate=validate.Range(min=0))

    @validates_schema
    def validate_at_least_one_value(self, data, **kwargs):
        """Ensure at least one of reps, sets, or duration_seconds is provided"""
        reps = data.get('reps')
        sets = data.get('sets')
        duration_seconds = data.get('duration_seconds')

        if not any(v is not None for v in [reps, sets, duration_seconds]):
            raise ValidationError("At least one of reps, sets, or duration_seconds must be provided")

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)