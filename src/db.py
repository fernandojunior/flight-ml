import sqlite3


DATABASE = "predictions.db"


def setup_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER,
        month INTEGER,
        day INTEGER,
        dep_time INTEGER,
        sched_dep_time INTEGER,
        dep_delay REAL,
        air_time REAL,
        distance REAL,
        hour INTEGER,
        minute INTEGER,
        predicted_arrival_delay REAL
    )
    """
    )
    conn.commit()
    conn.close()


def test_database_connection():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    conn.close()


def store_prediction(data, predicted_delay):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """
    INSERT INTO predictions (
        year, month, day, dep_time, sched_dep_time, dep_delay, air_time,
        distance, hour, minute, predicted_arrival_delay
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            data.year,
            data.month,
            data.day,
            data.dep_time,
            data.sched_dep_time,
            data.dep_delay,
            data.air_time,
            data.distance,
            data.hour,
            data.minute,
            predicted_delay,
        ),
    )
    conn.commit()
    conn.close()


def get_prediction_history():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """
    SELECT year, month, day, dep_time, sched_dep_time, dep_delay, air_time,
           distance, hour, minute, predicted_arrival_delay
    FROM predictions
    """
    )
    rows = cursor.fetchall()
    conn.close()

    history = []
    for row in rows:
        history.append(
            {
                "year": row[0],
                "month": row[1],
                "day": row[2],
                "dep_time": row[3],
                "sched_dep_time": row[4],
                "dep_delay": row[5],
                "air_time": row[6],
                "distance": row[7],
                "hour": row[8],
                "minute": row[9],
                "predicted_arrival_delay": row[10],
            }
        )

    return history
