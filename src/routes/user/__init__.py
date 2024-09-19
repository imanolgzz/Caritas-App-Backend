from flask import Blueprint, request, jsonify
from util.jwt import validate_token

user_routes = Blueprint("user", __name__)

@user_routes.before_request
def verify_jwt_token():
	data = request.get_json()
	token = request.headers["Authorization"].split(" ")[1]
	validation = validate_token(token, True)
	response = None
	try:
		if validation["username"] == data["username"]:
			response = validation
		else:
			response = jsonify({"error": "user is requesting unauthorized information"})
			response.status_code = 401
	except:
		response = jsonify({"error": "anauthorized"})
		response.status_code = 401
	return response

@user_routes.route("/data", methods=["POST"])
def data():
	data = request.get_json()
	return data["country"]
