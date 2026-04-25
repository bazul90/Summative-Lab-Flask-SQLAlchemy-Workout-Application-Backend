# Workout Tracker API

A Flask REST API for tracking workouts, exercises, and their relationships. The API allows users to create, view, and delete workouts and exercises, as well as associate exercises with specific workout sessions.

## Description

This API provides a complete backend solution for a workout tracking application. It features three main resources:

- **Workouts**: Track workout sessions with date, duration, and optional notes
- **Exercises**: Define exercise details including name, category, and equipment needs
- **WorkoutExercises**: Join table that links exercises to workouts with specific rep/set/duration data

The API uses Flask-SQLAlchemy for ORM and database migrations, Marshmallow for serialization/validation, and follows RESTful principles.

## Installation

```bash
pipenv install
pipenv shell
```

## Setup

Initialize and migrate the database (run from the project root):

```bash
flask --app server.app db init
flask --app server.app db migrate -m "initial migration"
flask --app server.app db upgrade
```

Seed the database with sample data (run from the project root):

```bash
python -m server.seed
```

## Run the Application

Option 1: Using Flask (run from the project root):

```bash
flask --app server.app run --debug
```

Option 2: Using the provided runner script:

```bash
python run.py
```

The API will be available at `http://localhost:5000`

## Endpoints

### Workouts

#### GET /workouts
List all workouts.

**Response:**
```json
[
  {
    "id": 1,
    "date": "2025-04-20",
    "duration_minutes": 30,
    "notes": "Morning cardio"
  }
]
```

#### GET /workouts/<id>
Get a specific workout with its associated exercises and join data.

**Response:**
```json
{
  "id": 1,
  "date": "2025-04-20",
  "duration_minutes": 30,
  "notes": "Morning cardio",
  "exercises": [
    {
      "id": 2,
      "name": "Running",
      "category": "cardio",
      "equipment_needed": false,
      "reps": null,
      "sets": null,
      "duration_seconds": 1800,
      "workout_exercise_id": 1
    }
  ]
}
```

#### POST /workouts
Create a new workout.

**Request:**
```json
{
  "date": "2025-04-25",
  "duration_minutes": 45,
  "notes": "Leg day"
}
```

**Response:**
```json
{
  "id": 4,
  "date": "2025-04-25",
  "duration_minutes": 45,
  "notes": "Leg day"
}
```

#### DELETE /workouts/<id>
Delete a workout and all associated workout-exercise links (cascade delete).

**Response:**
```json
{
  "message": "Workout deleted successfully"
}
```

### Exercises

#### GET /exercises
List all exercises.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Push-ups",
    "category": "strength",
    "equipment_needed": false
  }
]
```

#### GET /exercises/<id>
Get a specific exercise with its associated workouts and join data.

**Response:**
```json
{
  "id": 1,
  "name": "Push-ups",
  "category": "strength",
  "equipment_needed": false,
  "workouts": [
    {
      "workout_id": 2,
      "date": "2025-04-21",
      "duration_minutes": 45,
      "reps": 15,
      "sets": 3,
      "duration_seconds": null,
      "workout_exercise_id": 2
    }
  ]
}
```

#### POST /exercises
Create a new exercise.

**Request:**
```json
{
  "name": "Bench Press",
  "category": "strength",
  "equipment_needed": true
}
```

**Response:**
```json
{
  "id": 7,
  "name": "Bench Press",
  "category": "strength",
  "equipment_needed": true
}
```

#### DELETE /exercises/<id>
Delete an exercise and all associated workout-exercise links (cascade delete).

**Response:**
```json
{
  "message": "Exercise deleted successfully"
}
```

### WorkoutExercises

#### POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
Add an existing exercise to a workout with optional reps, sets, or duration data.

**Request:**
```json
{
  "reps": 12,
  "sets": 4,
  "duration_seconds": null
}
```

**Response:**
```json
{
  "id": 8,
  "workout_id": 1,
  "exercise_id": 3,
  "reps": 12,
  "sets": 4,
  "duration_seconds": null,
  "exercise": {
    "id": 3,
    "name": "Yoga",
    "category": "flexibility",
    "equipment_needed": true
  }
}
```

## Error Handling

The API returns appropriate HTTP status codes:

- 200: Success
- 201: Created
- 400: Bad request (validation error)
- 404: Not found
- 500: Internal server error

**Error response format:**
```json
{
  "error": "Description of the error"
}
```

## Validation

### Schema Validations
- `Exercise.name`: minimum 3 characters
- `Exercise.category`: must be one of ["strength", "cardio", "flexibility"]
- `Workout.duration_minutes`: must be greater than 0
- `WorkoutExercise.reps`, `sets`, `duration_seconds`: must be non-negative if provided
- `WorkoutExercise`: at least one of `reps`, `sets`, or `duration_seconds` must be provided

### Model Validations (SQLAlchemy @validates)
- `Exercise.name`: enforced minimum 3 characters
- `Exercise.category`: enforced allowed values
- `Workout.duration_minutes`: enforced > 0
- `WorkoutExercise.reps/sets/duration_seconds`: enforced non-negative

### Database Constraints
- `exercises.name`: UNIQUE constraint
- `workouts.duration_minutes`: CHECK > 0
- `workout_exercises.reps/sets/duration_seconds`: CHECK >= 0
- `workout_exercises`: UNIQUE(workout_id, exercise_id)

## Database Schema

```
exercises
├── id (PK)
├── name (unique, not null)
├── category (not null)
└── equipment_needed (boolean)

workouts
├── id (PK)
├── date (not null)
├── duration_minutes (not null, >0)
└── notes (text)

workout_exercises
├── id (PK)
├── workout_id (FK -> workouts, cascade delete)
├── exercise_id (FK -> exercises, cascade delete)
├── reps (>=0)
├── sets (>=0)
└── duration_seconds (>=0)
```

## Project Structure

```
.
├── Pipfile
├── README.md
├── .gitignore
└── server/
    ├── app.py
    ├── config.py
    ├── extensions.py
    ├── models.py
    ├── schemas.py
    ├── seed.py
    └── routes/
        ├── __init__.py
        ├── exercise_routes.py
        ├── workout_exercise_routes.py
        └── workout_routes.py
```

## Dependencies

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Marshmallow
- Marshmallow
- Marshmallow-SQLAlchemy
- python-dotenv

## Git Workflow

The project follows feature-based commits:

1. Initial structure and configuration
2. Models with relationships and validations
3. Schemas with Marshmallow
4. Workout endpoints
5. Exercise endpoints
6. WorkoutExercise endpoints
7. Seed file
8. Documentation

## Notes

- The API uses SQLite by default for simplicity
- All timestamps are in ISO format (YYYY-MM-DD)
- Deleting a workout/exercise cascades to delete associated WorkoutExercise records
- Responses are prettified JSON for readability
- No update endpoints are required per specification