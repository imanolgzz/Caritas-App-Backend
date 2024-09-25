from flask import Flask
from routes import questionnaire_routes  # Import the routes blueprint

app = Flask(__name__)

# Register the blueprint (this connects the routes to your app)
app.register_blueprint(questionnaire_routes)

if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True)
