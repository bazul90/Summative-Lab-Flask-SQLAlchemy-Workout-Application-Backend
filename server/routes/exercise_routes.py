from flask import Blueprint, jsonify, request, abort
from ..models import Exercise, WorkoutExercise
from ..schemas import exercise_schema, exercises_schema
from ..extensions import db

exercise_bp = Blueprint('exercises', __name__, url_prefix='/exercises')

@exercise_bp.route('/', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200

@exercise_bp.route('/<int:exercise_id>', methods=['GET'])
def get_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    exercise_data = exercise_schema.dump(exercise)

    workout_exercises = WorkoutExercise.query.filter_by(exercise_id=exercise_id).all()
    exercise_data['workouts'] = [
        {
            'workout_id': we.workout.id,
            'date': we.workout.date.isoformat(),
            'duration_minutes': we.workout.duration_minutes,
            'reps': we.reps,
            'sets': we.sets,
            'duration_seconds': we.duration_seconds,
            'workout_exercise_id': we.id
        }
        for we in workout_exercises if we.workout
    ]

    return jsonify(exercise_data), 200

@exercise_bp.route('/', methods=['POST'])
def create_exercise():
    json_data = request.get_json()
    if not json_data:
        abort(400, description="No input data provided")

    try:
        exercise = exercise_schema.load(json_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    db.session.add(exercise)
    db.session.commit()

    return jsonify(exercise_schema.dump(exercise)), 201

@exercise_bp.route('/<int:exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({'message': 'Exercise deleted successfully'}), 200