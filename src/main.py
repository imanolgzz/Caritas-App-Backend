from flask import Flask
from routes import initialize_app
from util import db_connection

DB = db_connection.MSSQLDB()

if __name__ == '__main__':
	app = initialize_app()
	app.run(host='0.0.0.0', port = 5000, debug=True)
