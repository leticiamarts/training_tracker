import streamlit as st
import psycopg2
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection
def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

# Add a new user
def add_user(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username) VALUES (%s) ON CONFLICT DO NOTHING;", (username,))
    conn.commit()
    cur.close()
    conn.close()

# Add a workout
def add_workout(user_id, workout_duration):
    conn = get_connection()
    cur = conn.cursor()
    workout_date = datetime.now().date()
    cur.execute("INSERT INTO workouts (user_id, workout_date, workout_duration) VALUES (%s, %s, %s) RETURNING workout_id;", (user_id, workout_date, workout_duration))
    workout_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return workout_id

# Add an exercise to a workout
def add_exercise(workout_id, exercise_name, reps, weight):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO exercises (workout_id, exercise_name, reps, weight) VALUES (%s, %s, %s, %s);", (workout_id, exercise_name, reps, weight))
    conn.commit()
    cur.close()
    conn.close()

# Retrieve user by username
def get_user_id(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users WHERE username = %s;", (username,))
    user_id = cur.fetchone()
    cur.close()
    conn.close()
    return user_id[0] if user_id else None

# Retrieve workout history
def get_workout_history(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT workout_date, workout_duration, exercise_name, reps, weight
        FROM workouts
        JOIN exercises ON workouts.workout_id = exercises.workout_id
        WHERE workouts.user_id = %s
        ORDER BY workout_date DESC;
    ''', (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# Streamlit app UI
def main():
    st.title("Training Tracker")

    # User input for username
    username = st.text_input("Enter your username:")
    if username:
        add_user(username)
        user_id = get_user_id(username)

        # Add workout details
        with st.form("Workout Form"):
            workout_duration = st.slider("Workout Duration (minutes):", 0, 180, 60)
            exercise_name = st.text_input("Exercise Name:")
            reps = st.number_input("Reps:", min_value=1, value=10)
            weight = st.number_input("Weight (kg):", min_value=0.0, value=10.0, step=0.5)
            submit = st.form_submit_button("Add Workout")

            if submit:
                if exercise_name:
                    workout_duration = timedelta(minutes=workout_duration)
                    workout_id = add_workout(user_id, workout_duration)
                    add_exercise(workout_id, exercise_name, reps, weight)
                    st.success("Workout added!")

        # Display workout history
        st.subheader("Workout History")
        history = get_workout_history(user_id)
        for row in history:
            st.write(f"Date: {row[0]}, Duration: {row[1]}, Exercise: {row[2]}, Reps: {row[3]}, Weight: {row[4]} kg")

if __name__ == "__main__":
    main()
