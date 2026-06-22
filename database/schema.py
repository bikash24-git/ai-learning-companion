"""
Database schema and initialization for AI Learning Companion.
"""
import sqlite3
from pathlib import Path
from datetime import datetime

DATABASE_PATH = Path("database/learning_companion.db")
DATABASE_PATH.parent.mkdir(exist_ok=True)


def get_connection():
    """Get or create SQLite database connection."""
    conn = sqlite3.connect(str(DATABASE_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    """Initialize database with required tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table for uploaded files
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL UNIQUE,
            file_type TEXT NOT NULL,
            upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            file_size INTEGER,
            content_preview TEXT
        )
    """)
    
    # Table for summaries
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER NOT NULL,
            summary_type TEXT NOT NULL,
            content TEXT NOT NULL,
            generated_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
        )
    """)
    
    # Table for flashcards
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            generated_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
        )
    """)
    
    # Table for MCQs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mcqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            generated_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
        )
    """)
    
    # Table for important questions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS important_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            question_type TEXT NOT NULL,
            answer TEXT NOT NULL,
            generated_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    conn.close()


def add_file_record(filename: str, file_type: str, file_size: int, content_preview: str = "") -> int:
    """Add a file record to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO files (filename, file_type, file_size, content_preview)
            VALUES (?, ?, ?, ?)
        """, (filename, file_type, file_size, content_preview))
        conn.commit()
        file_id = cursor.lastrowid
        return file_id
    finally:
        conn.close()


def add_summary(file_id: int, summary_type: str, content: str):
    """Add a summary record to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO summaries (file_id, summary_type, content)
            VALUES (?, ?, ?)
        """, (file_id, summary_type, content))
        conn.commit()
    finally:
        conn.close()


def add_flashcard(file_id: int, question: str, answer: str):
    """Add a flashcard record to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO flashcards (file_id, question, answer)
            VALUES (?, ?, ?)
        """, (file_id, question, answer))
        conn.commit()
    finally:
        conn.close()


def add_mcq(file_id: int, question: str, option_a: str, option_b: str, option_c: str, option_d: str, correct_answer: str):
    """Add an MCQ record to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO mcqs (file_id, question, option_a, option_b, option_c, option_d, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (file_id, question, option_a, option_b, option_c, option_d, correct_answer))
        conn.commit()
    finally:
        conn.close()


def add_important_question(file_id: int, question: str, question_type: str, answer: str):
    """Add an important question record to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO important_questions (file_id, question, question_type, answer)
            VALUES (?, ?, ?, ?)
        """, (file_id, question, question_type, answer))
        conn.commit()
    finally:
        conn.close()


def get_file_records():
    """Retrieve all file records from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM files ORDER BY upload_timestamp DESC")
        records = cursor.fetchall()
        return records
    finally:
        conn.close()


def get_summaries_by_file(file_id: int):
    """Retrieve all summaries for a specific file."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM summaries WHERE file_id = ? ORDER BY generated_timestamp DESC", (file_id,))
        records = cursor.fetchall()
        return records
    finally:
        conn.close()


def get_flashcards_by_file(file_id: int):
    """Retrieve all flashcards for a specific file."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM flashcards WHERE file_id = ? ORDER BY generated_timestamp DESC", (file_id,))
        records = cursor.fetchall()
        return records
    finally:
        conn.close()


def get_mcqs_by_file(file_id: int):
    """Retrieve all MCQs for a specific file."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM mcqs WHERE file_id = ? ORDER BY generated_timestamp DESC", (file_id,))
        records = cursor.fetchall()
        return records
    finally:
        conn.close()


def get_important_questions_by_file(file_id: int):
    """Retrieve all important questions for a specific file."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM important_questions WHERE file_id = ? ORDER BY generated_timestamp DESC", (file_id,))
        records = cursor.fetchall()
        return records
    finally:
        conn.close()


def delete_file_and_data(file_id: int):
    """Delete a file record and all associated data."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM files WHERE id = ?", (file_id,))
        conn.commit()
    finally:
        conn.close()
