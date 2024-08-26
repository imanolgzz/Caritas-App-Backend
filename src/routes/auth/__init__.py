from flask import Blueprint, request
from routes.middleware import write_token, validate_token

auth_routes = Blueprint("auth", __name__)

@auth_routes.route("/login", methods=["POST"])
def login():
	data = request.get_json()
	if data["username"] == "Pedro":
		return write_token(data=request.get_json())
	
	else:
		response = jsonify({"message": "User not found"})
		response.status_code = 404
		return response

@auth_routes.route("/verify/token")
def verify():
	token = request.headers["Authorization"].split(" ")[1]
	return validate_token(token, output=True)	
