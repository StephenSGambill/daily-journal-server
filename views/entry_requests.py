import sqlite3
import json
from models import Entry
from models import Mood



def get_all_entries():
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            m.id mood_id,
            m.label mood_label,
            e.date
        FROM Entries e
        JOIN Moods m
            ON e.mood_id = m.id
        """
        )

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(
                row["id"],
                row["concept"],
                row["entry"],
                row["mood_id"],
                row["date"],
            )
            
            mood = Mood(
                row["mood_id"],
                row["mood_label"],
            )

            entry.mood = mood.__dict__
            entries.append(entry.__dict__)

    return entries

def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.id mood_id,
            m.label mood_label,
            e.date
        FROM Entries e
        JOIN Moods m
            ON e.mood_id = m.id
        WHERE e.id = ?
        """,
            (id,),
        )

        row = db_cursor.fetchone()

        entry = Entry(
            row["id"],
            row["concept"],
            row["entry"],
            row["mood_id"],
            row["date"],
        )

        mood = Mood(
            row["mood_id"],
            row["mood_label"],
            )

        entry.mood = mood.__dict__
        return entry.__dict__

def delete_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        DELETE FROM Entries
        WHERE id = ?
        """,
            (id,),
        )

def get_entry_by_search(search_term):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
    """
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date
        FROM Entries e
        WHERE e.entry LIKE ?
    """,
    ('%{}%'.format(search_term), ))
        
    entries = []
    dataset = db_cursor.fetchall()

    for row in dataset:
        entry = Entry(
            row["id"],
            row["concept"],
            row["entry"],
            row["mood_id"],
            row["date"]
        )
        entries.append(entry.__dict__)

    return entries

def create_entry(new_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        INSERT INTO Entries
            ( concept, entry, mood_id, date)
        VALUES
            ( ?, ?, ?, ?);
        """,
            (
                new_entry["concept"],
                new_entry["entry"],
                new_entry["mood_id"],
                new_entry["date"],
            ),
        )

        id = db_cursor.lastrowid
        new_entry["id"] = id

    return new_entry