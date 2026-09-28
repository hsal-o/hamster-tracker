import os
import mariadb
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mariadb.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE")
    )

def insert_run_session(
    hamster_id,
    wheel_id,
    started_at,
    ended_at,
    revolutions,
    distance_miles,
    elapsed_seconds
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO run_session (
            hamster_id,
            wheel_id,
            started_at,
            ended_at,
            revolutions,
            distance_miles,
            elapsed_seconds
        )   
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            hamster_id,
            wheel_id,
            started_at,
            ended_at,
            revolutions,
            distance_miles,
            elapsed_seconds
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

def get_wheel_circumference(wheel_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT circumference_inches
        FROM wheel
        WHERE id = ?
        """,
        (wheel_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is None:
        raise ValueError(f"Wheel with ID {wheel_id} not found")

    return float(row[0])