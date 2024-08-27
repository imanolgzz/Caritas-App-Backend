from flask import Blueprint, request
import util.jwt

user_routes = Blueprint("user", __name__)

@user_routes.before_request
def verify_jwt_token():
	token = request.headers["Authorization"].split(" ")[1]
	return validate_token(token)

@user_routes.route("/data", methods=["POST"])
def data():
	data = request.get_json()
	return data["country"]
