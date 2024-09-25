from flask import Flask
from routes import initialize_app
import os

if __name__ == '__main__':
	app = initialize_app()
	app.run(host=getenv("API_HOST"), port = getenv("API_PORT"), debug=True)
