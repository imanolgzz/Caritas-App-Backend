from flask import Blueprint, request, jsonify
from util.jwt import validate_token
from util.db_connection import DB
from util.logs import LOGGER

event_routes = Blueprint("events", __name__)
@event_routes.route("/eventosFuturos", methods=["GET"])
def events():
	"""
	Obtiene los eventos futuros ordenados por fecha.
	---
	parameters: []
	responses:
		200:
			description: Lista de eventos futuros obtenida con éxito.
			content:
				application/json:
					schema:
						type: array
						items:
							type: object
							properties:
								ID_EVENTO:
									type: int
									description: ID del evento
									example: 1
								NOMBRE:
									type: string
									description: Nombre del evento
									example: "Parque de Diversiones"
								FECHA:
									type: string
									format: date
									description: Fecha del evento
									example: "2024-07-15"
								LUGAR:
									type: string
									description: Lugar del evento
									example: "Six Flags"
								DESCRIPCION:
									type: string
									description: Descripción breve del evento
									example: "Día de Parque."
								NUM_MAX_ASISTENTES:
									type: int
									description: Número máximo de asistentes
									example: 200
								CODIGO:
									type: string
									description: Código del evento
									example: "PRK002"
								PUNTAJE:
									type: int
									description: Puntuación única del evento
									example: 120
		400:
			description: Error en la conexión a la base de datos
			content:
				application/json:
					schema:
						type: object
						properties:
							message:
								type: string
								example: "Error en la conexión"
		400:
			description: Error al recibir los eventos próximos
			content:
				application/json:
					schema:
						type: object
						properties:
							message:
								type: string
								example: "No hay eventos próximos"
	"""
	LOGGER.info("Requested events from ip - {} using {}".format(request.remote_addr, request.user_agent))
	events = DB.eventosFuturos()
	if events:
		response = jsonify(events)
		response.status_code = 200
		return response

	else:
		response = jsonify({ "message": "No hay eventos próximos" })
		response.status_code = 400
		return response



@event_routes.route("/eventosDelMes", methods=["GET"])
def events():
	"""
	Obtiene los eventos del mes correspondiente ( Actual).
	---
	parameters: []
	responses:
		200:
			description: Lista de eventos del mes obtenida con éxito.
			content:
				application/json:
					schema:
						type: array
						items:
							type: object
							properties:
								ID_EVENTO:
									type: int
									description: ID del evento
									example: 1
								NOMBRE:
									type: string
									description: Nombre del evento
									example: "Parque de Diversiones"
								FECHA:
									type: string
									format: date
									description: Fecha del evento
									example: "2024-07-15"
								LUGAR:
									type: string
									description: Lugar del evento
									example: "Six Flags"
								DESCRIPCION:
									type: string
									description: Descripción breve del evento
									example: "Día de Parque."
								NUM_MAX_ASISTENTES:
									type: int
									description: Número máximo de asistentes
									example: 200
								CODIGO:
									type: string
									description: Código del evento
									example: "PRK002"
								PUNTAJE:
									type: int
									description: Puntuación única del evento
									example: 120
		400:
			description: Error en la conexión a la base de datos
			content:
				application/json:
					schema:
						type: object
						properties:
							message:
								type: string
								example: "Error en la conexión"
		400:
			description: Error al recibir los eventos del mes
			content:
				application/json:
					schema:
						type: object
						properties:
							message:
								type: string
								example: "No hay eventos este mes"
	"""
	LOGGER.info("Requested events from ip - {} using {}".format(request.remote_addr, request.user_agent))
	events = DB.eventosFuturos()
	if events:
		response = jsonify(events)
		response.status_code = 200
		return response

	else:
		response = jsonify({ "message": "No hay eventos próximos" })
		response.status_code = 400
		return response



'''
3er sprint

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
  '''