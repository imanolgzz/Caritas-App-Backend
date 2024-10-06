from flask import Flask
from routes import initialize_app
from os import getenv
from dotenv import load_dotenv

if __name__ == '__main__':
	load_dotenv()
	app = initialize_app()
	app.run(host=getenv("API_HOST_PROD"), port = getenv("API_PORT_PROD"), debug=True)