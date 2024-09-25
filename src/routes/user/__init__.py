from flask import Blueprint, request, jsonify
from util.jwt import validate_token
from util.db_connection import DB

user_routes = Blueprint("user", __name__)
'''
@user_routes.before_request

def verify_jwt_token():
	data = request.get_json()
	print(data)
	token = request.headers["Authorization"].split(" ")[1]
	print(token)
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
	return response
		response.status_code = 401
'''
@user_routes.route("/eventosFuturos", methods=["GET"])
def eventos():

	try: 
		eventos = None
		with DB.cnx.cursor(as_dict=True) as cursor:
			cursor.callproc('GetEventosFuturosOrdenadosPorFecha')
			eventos = cursor.fetchall()
		return jsonify({"eventosFuturos": eventos}), 201
	except:
		return jsonify({"message": "Error al intentar procesar los eventos futuros"}), 500 
	

@user_routes.route("/cuestionarioPorTipo")
def cuestionario():
	with DB.cnx.cursor(as_dict=True) as cursor:
		cursor.callproc('GetQuestionsBasedOnType', (1))
		eventos = cursor.fetchall()
		print(eventos)
		return eventos

@user_routes.route("/opcionRespuestas")

def respuestas():
	with DB.cnx.cursor(as_dict=True) as cursor:
		cursor.callproc('GetChoices')
		eventos = cursor.fetchall()
		print(eventos)
		return eventos