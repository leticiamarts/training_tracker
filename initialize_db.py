import psycopg2
import os 
from dotenv import load_dotenv

load_dotenv()

# Connection parameters
conn = psycopg2.connect(
    host="localhost",
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)



# Create a cursor object
cur = conn.cursor()

# Create tables
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    );
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS workouts (
        workout_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(user_id),
        workout_date DATE NOT NULL,
        workout_duration INTERVAL NOT NULL
    );
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS exercises (
        exercise_id SERIAL PRIMARY KEY,
        workout_id INTEGER REFERENCES workouts(workout_id),
        exercise_name VARCHAR(100) NOT NULL,
        reps INTEGER NOT NULL,
        weight DECIMAL(5, 2) NOT NULL
    );
''')

# Commit and close connection
conn.commit()
cur.close()
conn.close()
