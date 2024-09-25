from flask import Flask
from routes import initialize_app

if __name__ == '__main__':
    app = initialize_app()
    app.run(host='0.0.0.0', port = 5500, debug=True)