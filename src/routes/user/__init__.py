from flask import Blueprint, request
import routes.middleware

user_routes = Blueprint("user", __name__)

@user_routes.before_request
def verify_token_middleware():
	token = request.headers["Authorization"].split(" ")[1]
	return validate_token(token)

@user_routes.route("/data", methods=["POST"])
def data():
	data = request.get_json()
	return data["country"]
