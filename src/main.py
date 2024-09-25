from flask import Flask
from routes import initialize_app
from util.db_connection import MSSQLDB

DB = MSSQLDB()

if __name__ == '__main__':
	app = initialize_app()
	app.run(host='0.0.0.0', port = 5000, debug=True)
