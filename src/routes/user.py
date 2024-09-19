from flask import Blueprint, request
from routes.middleware.JWT import validate_token

routes_user = Blueprint("routes_user", __name__)

@routes_user.before_request
def verify_token_middleware():
	token = request.headers["Authorization"].split(" ")[1]
	return validate_token(token)

@routes_user.route("/data", methods=["POST"])
def data():
	data = request.get_json()
	return data["country"]
