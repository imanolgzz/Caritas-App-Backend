from flask import Blueprint, request, jsonify
from util.jwt import write_token, validate_token
from util.db_connection import DB
from util.hashing import hashPassword
from util.logs import LOGGER

auth_routes = Blueprint("auth", __name__)

@auth_routes.route("/login", methods=["POST"])
def login():
	"""
	Verifica que el usuario exista en la base de datos y regresa el JWT adecuado
	---
	parameters:
		- in: body
		  name: Usuario
		  description: Usuario
		  schema:
		  	type: object
			required:
				- username
				- password
			properties:
				username:
					type: string
					description: Correo del usuario
					example: Adrian@mail.com
				password:
					type: string
					description: Contraseña del usuario
					example: Adrian@Pass
	responses:
		200:
		  description: Usuario valido
		  content:
			application/json:
			  schema:
			  	type: object
				properties:
					message:
						type: string
						example: Success
					JWT_Token:
						type: string
						example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
		400:
		  description: Error de conexion
		  content:
			application/json:
			  schema:
			  	type: object
				properties:
					message:
						type: string
						example: Error loggin in
		
		404:
		  description: Usuario o contraña no validos
		  content:
			application/json:
			  schema:
			  	type: object
				properties:
					message:
						type: string
						example: User not found
	"""
	LOGGER.info("Requested login from ip - {} using {}".format(request.remote_addr, request.user_agent))
	data = request.get_json()
	hashedPassword = hashPassword(data["password"])
	if DB.login(data["username"], hashedPassword):
		try:
			token = write_token(data)
			response = jsonify({"message": "Success", "JWT_Token": token.decode("UTF-8")})
			response.status_code = 200
			return response
		
			
		except:
			response = jsonify({"message": "Error loggin in"})
			response.status_code = 400
			return response	
		
	else:
		response = jsonify({"message": "Invalid email or password"})
		response.status_code = 404
		return response
	
	
		


@auth_routes.route("/register", methods=["POST"])
def register():
	"""
	Registra un nuevo usuario en la base de datos
	---
	parameters:
		- in: body
		  name: Usuario
		  description: Datos del usuario a registrar
		  schema:
		  	type: object
			required:
				- username
				- email
				- password
				- name
				- first_lastname
				- second_lastname
				- role
				- address
				- zip
			properties:
				username:
					type: string
					description: Identificador del usuario
					example: user01
				email:
					type: string
					description: Correo Electrónico del usuario
					example: user01@mail.com
				password:
					type: string
					description: Contraseña del usuario
					example: user1234
				name:
					type: string
					description: Nombre del usuario
					example: Imanol
				first_lastname:
					type: string
					description: Primer apellido del usuario
					example: González
				second_lastname:
					type: string
					description: Segundo apellido del usuario
					example: Solís
				role:
					type: string
					description: Rol del usuario
					example: Colaborador
				address:
					type: string
					description: Dirección del usuario
					example: Piedras de San Marcos 202
				zip:
					type: string
					description: Código Postal del usuario
					example: 10429
	responses:
		200:
		  description: Usuario registrado exitosamente
		  content:
			application/json:
			  schema:
			  	type: object
				properties:
					message:
						type: string
						example: User registered successfully
		400:
		  description: Faltan datos requeridos o el usuario ya existe
		  content:
			application/json:
			  schema:
			  	type: object
				properties:
					message:
						type: string
						example: User already exists
		500:
		  description: Error interno en el servidor
		  content:
			application/json:
			  schema:
			  	type: object
				properties:
					message:
						type: string
						example: Error registering user
	"""
	try:
		data = request.get_json()
		username = data["username"]
		email = data["email"]
		password = data["password"]
		name = data["name"]
		first_lastname = data["first_lastname"]
		second_lastname = data["second_lastname"]
		role = data["role"]
		address = data["address"]
		zip = data["zip"]

		# validate that all fields are presented
		if not username or not email or not password or not name or not first_lastname or not second_lastname or not role or not address or not zip:
			return jsonify({"message": "All fields are required"}), 400
		
		if DB.checkUserExists(email):
			return jsonify({"message": "User already exists"}), 400
		
		# register the user
		hashedPassword = hashPassword(password)

		state, message = DB.registerUser(email, hashedPassword, name, first_lastname, second_lastname, address + " CP " + str(zip), zip)
		if state:
			return jsonify({"message":  message}), 200
		else:
			return jsonify({"message":  message}), 500
	except Exception as e:
		return jsonify({"message": "Error: " + str(e)}), 500

@auth_routes.route("/verify/token")
def verify():
	token = request.headers["Authorization"].split(" ")[1]
	return validate_token(token, output=True)	
