from datetime import date
from server import create_app, db
from server.models import Exercise, Workout, WorkoutExercise

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    ex1 = Exercise(name='Push-ups', category='strength', equipment_needed=False)
    ex2 = Exercise(name='Running', category='cardio', equipment_needed=False)
    ex3 = Exercise(name='Yoga', category='flexibility', equipment_needed=True)
    ex4 = Exercise(name='Squats', category='strength', equipment_needed=False)
    ex5 = Exercise(name='Deadlift', category='strength', equipment_needed=True)
    ex6 = Exercise(name='Cycling', category='cardio', equipment_needed=True)

    db.session.add_all([ex1, ex2, ex3, ex4, ex5, ex6])
    db.session.commit()

    w1 = Workout(date=date(2025, 4, 20), duration_minutes=30, notes='Morning cardio')
    w2 = Workout(date=date(2025, 4, 21), duration_minutes=45, notes='Strength training')
    w3 = Workout(date=date(2025, 4, 22), duration_minutes=60, notes='Full body workout')

    db.session.add_all([w1, w2, w3])
    db.session.commit()

    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=ex2.id, reps=None, sets=None, duration_seconds=1800)
    we2 = WorkoutExercise(workout_id=w2.id, exercise_id=ex1.id, reps=15, sets=3, duration_seconds=None)
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=ex4.id, reps=20, sets=3, duration_seconds=None)
    we4 = WorkoutExercise(workout_id=w2.id, exercise_id=ex5.id, reps=8, sets=3, duration_seconds=None)
    we5 = WorkoutExercise(workout_id=w3.id, exercise_id=ex6.id, reps=None, sets=None, duration_seconds=3600)
    we6 = WorkoutExercise(workout_id=w3.id, exercise_id=ex1.id, reps=25, sets=4, duration_seconds=None)
    we7 = WorkoutExercise(workout_id=w3.id, exercise_id=ex3.id, reps=None, sets=None, duration_seconds=1200)

    db.session.add_all([we1, we2, we3, we4, we5, we6, we7])
    db.session.commit()

    print("Database seeded successfully!")
    print(f"Created {Exercise.query.count()} exercises")
    print(f"Created {Workout.query.count()} workouts")
    print(f"Created {WorkoutExercise.query.count()} workout-exercise links")
