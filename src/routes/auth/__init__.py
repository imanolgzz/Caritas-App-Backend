from flask import Blueprint, request, jsonify
from util.jwt import write_token, validate_token

auth_routes = Blueprint("auth", __name__)

@auth_routes.route("/login", methods=["POST"])
def login():
	data = request.get_json()
	# Harcodear password también
	if data["username"] == "Pedro":
		try:
			token = write_token(data=request.get_json())
			response = jsonify({"message": "success", "JWT_Token": token.decode("UTF-8")})
			response.status_code = 200
			return response
		except:
			response = jsonify({"message": "error loggin in"})
			response.status_code = 400
			return response	
	else:
		response = jsonify({"message": "User not found"})
		response.status_code = 404
		return response

@auth_routes.route("/verify/token")
def verify():
	token = request.headers["Authorization"].split(" ")[1]
	return validate_token(token, output=True)	
