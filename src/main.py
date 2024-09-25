from flask import Flask
from routes import initialize_app
from os import getenv

if __name__ == '__main__':
	app = initialize_app()
	app.run(host=getenv("API_HOST_PROD"), port = getenv("API_PORT_PROD"), debug=True)
