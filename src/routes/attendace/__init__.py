from flask import Blueprint, request, jsonify
from util.db_connection import DB

attendance_routes = Blueprint("attendance", __name__)

@attendance_routes.route("/attendance", methods=["POST"])
def attendance():
	"""
	Realiza el registro de asistencia de un usuario a un evento determinado.
	---
	parameters:
		- in: body
		  name: ID_USUARIO
		  description: ID_USUARIO 
		  schema:
		  	type: object
			required:
				- ID_USUARIO
				- ID_EVENTO
			properties:
				ID_USUARIO:
					type: int
					description: ID del usuario
					example: 1
				ID_EVENTO:
					type: int
					description: ID del evento al que se estará registrando
					example: 1
	responses:
		200:
		  description: Usuario registrado con éxito
		  content:
			application/json:
			  schema:
			  	type: object
				properties:
					message:
						type: string
						example: Success

		400:
		  description: Error en registrar Asistencia
		  content:
			application/json:
			  schema:
			  	type: object
				properties:
					message:
						type: string
						example: Error en conexión
		
		404:
		  description: El evento ya está registrado
		  content:
			application/json:
			  schema:
			  	type: object
				properties:
					message:
						type: string
						example: ID de usuario o evento no válido
	"""
	data = request.get_json()

	if DB.eventAttendance(data["ID_USUARIO"], data["ID_EVENTO"]):
			try:
					response = jsonify({"message":"Usuario registrado con éxito"})
					response.status_code = 200
					return response
			
			except:
					response = jsonify({"message":"Error en registrar usuario"})
					response.status_code = 400
					return response 
	else:
			response = jsonify({"message":"El evento ya está registrado"})
			response.status_code = 404
			return response