from flask import Blueprint, jsonify, request, abort
from ..models import Workout, WorkoutExercise
from ..schemas import workout_schema, workouts_schema
from ..extensions import db

workout_bp = Blueprint('workouts', __name__, url_prefix='/workouts')

@workout_bp.route('/', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200

@workout_bp.route('/<int:workout_id>', methods=['GET'])
def get_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    workout_data = workout_schema.dump(workout)

    workout_exercises = WorkoutExercise.query.filter_by(workout_id=workout_id).all()
    workout_data['exercises'] = [
        {
            **we.exercise.to_dict(),
            'reps': we.reps,
            'sets': we.sets,
            'duration_seconds': we.duration_seconds,
            'workout_exercise_id': we.id
        }
        for we in workout_exercises
    ]

    return jsonify(workout_data), 200

@workout_bp.route('', methods=['POST'])
def create_workout():
    json_data = request.get_json()
    if not json_data:
        abort(400, description="No input data provided")

    try:
        data = workout_schema.load(json_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    workout = Workout(**data)
    db.session.add(workout)
    db.session.commit()

    return jsonify(workout_schema.dump(workout)), 201

@workout_bp.route('/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    return jsonify({'message': 'Workout deleted successfully'}), 200