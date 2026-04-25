from flask import Blueprint, jsonify, request, abort
from ..models import Workout, Exercise, WorkoutExercise
from ..schemas import workout_exercise_schema, workout_exercises_schema
from ..extensions import db

workout_exercise_bp = Blueprint('workout_exercises', __name__,
                                url_prefix='/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises')

@workout_exercise_bp.route('/', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get_or_404(workout_id)
    exercise = Exercise.query.get_or_404(exercise_id)

    existing = WorkoutExercise.query.filter_by(workout_id=workout_id, exercise_id=exercise_id).first()
    if existing:
        return jsonify({'error': 'Exercise already added to this workout'}), 400

    json_data = request.get_json() or {}

    try:
        workout_exercise = workout_exercise_schema.load({
            'workout_id': workout_id,
            'exercise_id': exercise_id,
            'reps': json_data.get('reps'),
            'sets': json_data.get('sets'),
            'duration_seconds': json_data.get('duration_seconds')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    db.session.add(workout_exercise)
    db.session.commit()

    return jsonify(workout_exercise_schema.dump(workout_exercise)), 201