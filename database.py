print("✅ NeighborLink database module loaded")

import sqlite3
import os


DB_PATH = "data/neighborlink.db"


def get_connection():

    os.makedirs(
        "data",
        exist_ok=True
    )

    return sqlite3.connect(DB_PATH)


def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        location TEXT,

        skills TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS opportunities (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT,

        description TEXT,

        created_by TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


    conn.commit()

    conn.close()


def get_member_count():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count
