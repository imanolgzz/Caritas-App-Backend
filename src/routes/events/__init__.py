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

@event_routes.route("/eventosRegistrados", methods=["GET"])
def registeredEvents():
    """
    Obtiene los eventos registrados por un usuario.
    ---
    parameters:
      - name: ID_USUARIO
        in: query
        type: integer
        required: true
        description: ID del usuario para obtener los eventos registrados
        example: 1
    responses:
      200:
        description: Lista de eventos registrados obtenida con éxito.
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  ID_EVENTO:
                    type: integer
                    description: ID del evento
                    example: 1
                  NOMBRE:
                    type: string
                    description: Nombre del evento
                    example: "Conferencia de Bienestar"
                  FECHA:
                    type: string
                    format: date
                    description: Fecha del evento
                    example: "2024-07-15"
                  LUGAR:
                    type: string
                    description: Lugar del evento
                    example: "Centro de Convenciones"
                  DESCRIPCION:
                    type: string
                    description: Descripción breve del evento
                    example: "Una conferencia sobre bienestar mental y físico."
                  NUM_MAX_ASISTENTES:
                    type: integer
                    description: Número máximo de asistentes
                    example: 200
                  CODIGO:
                    type: string
                    description: Código del evento
                    example: "CONF2024"
                  PUNTAJE:
                    type: integer
                    description: Puntuación del evento
                    example: 150
      400:
        description: Error en la solicitud o en la conexión a la base de datos
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Error al obtener los eventos registrados"
      400:
        description: El usuario no está registrado en ningún evento
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "El usuario no está registrado en ningún evento"
    """
    # Obtener el ID_USUARIO del query parameter
    user_id = request.args.get('ID_USUARIO')

    # Validar que se haya pasado el parámetro ID_USUARIO
    if not user_id:
        return jsonify({"message": "ID_USUARIO es requerido"}), 400

    try:
        # Conexión a la base de datos para llamar al stored procedure
        with DB.cnx.cursor(as_dict=True) as cursor:
            cursor.callproc('GetEventosAgendadosUsuario', (user_id,))
            eventos = cursor.fetchall()

            # Si hay eventos, devolver la lista
            if eventos:
                return jsonify(eventos), 200
            else:
                # Si no hay eventos registrados, devolver un error 400
                return jsonify({"message": "El usuario no está registrado en ningún evento"}), 400

    except Exception as e:
        return jsonify({"message": f"Error en la conexión a la base de datos: {str(e)}"}), 400


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