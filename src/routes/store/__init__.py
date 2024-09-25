from flask import Blueprint, request, jsonify
from util.jwt import write_token, validate_token

auth_routes = Blueprint("store", __name__)

@auth_routes.route("/products", methods=["GET"])
def products():
	# Make request from database
