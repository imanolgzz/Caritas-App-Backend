from flask import Blueprint, request, jsonify
from util.jwt import write_token, validate_token
from util.db_connection import DB

auth_routes = Blueprint("auth", __name__)

@auth_routes.route("/login", methods=["POST"])
def login():
	"""
	Verifica que el usuario exsista en la base de datos y regresa el JWT adecuado
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
	data = request.get_json()
	# Harcodear password también
	if DB.login(data["username"], data["password"]):
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
		response = jsonify({"message": "User not found"})
		response.status_code = 404
		return response


def login(self, user = "Adrian", password="Adrian"):
	with DB.cnx.cursor(as_dict=True) as cursor:
		cursor.callproc('CheckLogin', (user, password))
		message = (cursor.fetchall()[0]['Message'])
		if message == "Invalid email or password":
			return False
		return True
  
def register():
	try:
		data = request.get_json()
		username = data["username"]
		password = data["password"]
		email = data["email"]
		name = data["name"]
		first_lastname = data["first_lastname"]
		second_lastname = data["second_lastname"]

		# validate that all fields are presented
		if not username or not password or not email or not name or not first_lastname or not second_lastname:
			return jsonify({"message": "All fields are required"}), 400

		# validate that the email is not already in use
		alreadyExists = False
		with DB.cnx.cursor(as_dict=True) as cursor:
			cursor.callproc('CheckUserExists', (user, password))
			message = (cursor.fetchall()[0]['Message'])
			if message != "Invalid email or password":
				alreadyExists = True
		
		if alreadyExists:
			return jsonify({"message": "User already exists"}), 400

		# register the user
		with DB.cnx.cursor(as_dict=True) as cursor:
			cursor.callproc('RegisterUser', (username, password, email, name, first_lastname, second_lastname))
			message = (cursor.fetchall()[0]['Message'])
			if message != "User registered":
				return jsonify({"message": "Error registering user"}), 400
		return jsonify({"message": "User registered, successfully"}), 200
	except Exception as e:
		return jsonify({"message": "Error: " + str(e)}), 500

@auth_routes.route("/verify/token")
def verify():
	token = request.headers["Authorization"].split(" ")[1]
	return validate_token(token, output=True)	
