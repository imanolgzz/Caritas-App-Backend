from flask import Blueprint, request, jsonify
from util.db_connection import DB

attendance_routes = Blueprint("attendance", __name__)

@attendance_routes.route("/asistencia", methods=["POST"])
def asistencia():
    """
	Realiza el registro de asistencia de un usuario a un evento determinado.
	---
	parameters:
		- in: body
		  name: Datos
		  description: Datos
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
		
		400:
		  description: Evento o usuario no válido
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

    try:
        if DB.eventAttendance(data["ID_USUARIO"], data["ID_EVENTO"]):
            response = jsonify({"message": "Usuario registrado con éxito"})
            response.status_code = 200
        else:
            response = jsonify({"message": "ID de usuario o evento no válido"})
            response.status_code = 400

        return response
        
    except Exception as e:
        response = jsonify({"message": f"Error en registrar asistencia: {str(e)}"})
        response.status_code = 400
        return response

    finally:
        DB.cnx.commit()

@attendance_routes.route("/confirmarAsistencia", methods=["POST"])
def confirmarAsistencia():
    """
	Realiza el registro de asistencia de un usuario a un evento determinado.
	---
	parameters:
		- in: body
		  name: Datos
		  description: Datos
		  schema:
		  	type: object
			required:
				- ID_USUARIO
				- ID_EVENTO
				- PASSWORD_EVENTO
			properties:
				ID_USUARIO:
					type: int
					description: ID del usuario
					example: 2
				ID_EVENTO:
					type: int
					description: ID del evento al que se estará registrando
					example: 2
				PASSWORD_EVENTO:
					type: string
					description: Contraseña del evento
					example: "PRK002"
	responses:
		200:
		  description: Asistencia confirmada exitosamente 
		  content:
			application/json:
			  schema:
			  	type: object
				properties:
					message:
						type: string
						example: Success

		400:
		  description: Error al registrar Asistencia
		  content:
			application/json:
			  schema:
			  	type: object
				properties:
					message:
						type: string
						example: Error en conexión
		
		400:
		  description: Evento o usuario no válido
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

    try:
				state, message = DB.confirmarAsistencia(data["ID_USUARIO"], data["ID_EVENTO"], data["PASSWORD_EVENTO"])
        if state:
            response = jsonify({"message": "Asistencia confirmada exitosamente"})
            response.status_code = 200
        else:
            response = jsonify({"message": "ID de usuario o evento no válido"})
            response.status_code = 400

        return response
        
    except Exception as e:
        response = jsonify({"message": f"Error al validar la asistencia: {str(e)}"})
        response.status_code = 400
        return response

    finally:
        DB.cnx.commit()

@attendance_routes.route("/estadisticas/<usuario>", methods=["GET"])
def estadisticas(usuario):
    """
	Obtiene el numero de eventos registrados y eventos asistidos.
	---
	responses:
		200:
		  description: Estadisticas Obtenidas
		  content:
			application/json:
			  schema:
			  	type: object
				properties:
					asistencia:
						type: int
						example: 0
                    
					falta:
						type: int
						example: 0
		400:
		  description: Error Inesperado
		  content:
			application/json:
			  schema:
			  	type: object
				properties:
					message:
						type: string
						example: No se pudieron obtener las asistencias

		401:
		  description: Error
		  content:
			application/json:
			  schema:
			  	type: object
				properties:
					message:
						type: string
						example: No se obtuvo un usuario
        
		404:
			description: Error en obtener asistencias
			content:
			application/json:
				schema:
				type: object
				properties:
					message:
						type: string
						example: ID de usuario no válido
		
	"""
    print(usuario)
    if usuario == '{usuario}' or not usuario:
        response = jsonify({"message": f"No se obtuvo un usuario"})
        response.status_code = 401
        return response

    try:
        stats = DB.eventosEstadisticas(usuario)
        print(stats)
        if stats:
            response = jsonify(stats)
            response.status_code = 200
        else:
            response = jsonify({"message": "ID de usuario inválido"})
            response.status_code = 404

        return response
        
    except Exception as e:
        response = jsonify({"message": f"Error en obtener asistencias: {str(e)}"})
        response.status_code = 400
        return response

    finally:
        DB.cnx.commit()

