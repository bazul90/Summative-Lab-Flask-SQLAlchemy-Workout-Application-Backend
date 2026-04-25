from flask_marshmallow import Marshmallow
from marshmallow import validates, ValidationError, validate
from models import Exercise, Workout, WorkoutExercise

ma = Marshmallow()

class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        load_instance = True

    name = ma.Str(required=True, validate=validate.Length(min=3))
    category = ma.Str(required=True, validate=validate.OneOf(['strength', 'cardio', 'flexibility']))
    equipment_needed = ma.Bool(missing=False)

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

    @validates('reps')
    def validate_reps(self, value):
        if value is not None and value < 0:
            raise ValidationError("reps must be non-negative")

    @validates('sets')
    def validate_sets(self, value):
        if value is not None and value < 0:
            raise ValidationError("sets must be non-negative")

    @validates('duration_seconds')
    def validate_duration_seconds(self, value):
        if value is not None and value < 0:
            raise ValidationError("duration_seconds must be non-negative")

    @validates('reps')
    @validates('sets')
    @validates('duration_seconds')
    def validate_at_least_one(self, value, field, **_):
        rep = self.context.get('reps')
        sets = self.context.get('sets')
        dur = self.context.get('duration_seconds')
        if not any(v is not None for v in [rep, sets, dur]):
            raise ValidationError("At least one of reps, sets, or duration_seconds must be provided")

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)