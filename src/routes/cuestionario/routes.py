import pyodbc
from flask import Blueprint, request, jsonify

# Define the blueprint for your questionnaire routes
questionnaire_routes = Blueprint("questionnaire", __name__)

# Connection string to your database
CONNECTION_STRING = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=10.14.255.61;'
    'DATABASE=master;'
    'UID=SA;'
    'PWD=Shakira123.;'
)

# Establish the database connection
def get_db_connection():
    conn = pyodbc.connect(CONNECTION_STRING)
    return conn

# Route to get questions by questionnaire ID
@questionnaire_routes.route("/get-questions/<int:questionnaire_id>", methods=["GET"])
def get_questions(questionnaire_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL query to get the questions and their choices
    query = """
        SELECT q.question_id, q.question_text, c.choice_id, c.choice_text, c.choice_value
        FROM Questions q
        JOIN Choices c ON q.question_id = c.question_id
        WHERE q.questionnaire_id = ?
    """
    cursor.execute(query, questionnaire_id)
    results = cursor.fetchall()

    questions = {}
    for row in results:
        question_id, question_text, choice_id, choice_text, choice_value = row
        if question_id not in questions:
            questions[question_id] = {
                "question_id": question_id,
                "question_text": question_text,
                "choices": []
            }
        questions[question_id]["choices"].append({
            "choice_id": choice_id,
            "choice_text": choice_text,
            "choice_value": choice_value
        })

    cursor.close()
    conn.close()

    return jsonify(list(questions.values())), 200
