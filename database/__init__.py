"""Database package for AI Learning Companion."""

from .schema import (
    initialize_database,
    add_file_record,
    add_summary,
    add_flashcard,
    add_mcq,
    add_important_question,
    get_file_records,
    get_summaries_by_file,
    get_flashcards_by_file,
    get_mcqs_by_file,
    get_important_questions_by_file,
    delete_file_and_data,
    get_connection
)

__all__ = [
    'initialize_database',
    'add_file_record',
    'add_summary',
    'add_flashcard',
    'add_mcq',
    'add_important_question',
    'get_file_records',
    'get_summaries_by_file',
    'get_flashcards_by_file',
    'get_mcqs_by_file',
    'get_important_questions_by_file',
    'delete_file_and_data',
    'get_connection'
]
