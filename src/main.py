from flask import Flask
from routes.auth.login import routes_auth
from routes.user import routes_user 
from dotenv import load_dotenv

app = Flask(__name__)

app.register_blueprint(routes_auth, url_prefix="/api")
app.register_blueprint(routes_user, url_prefix="/api/user")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
	load_dotenv()
	app.run(host='0.0.0.0', port = 5000, debug=True)
