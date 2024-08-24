from flask import Blueprint, request, jsonify

auth = Blueprint("auth", __name__)

'''
  Las rutas de autenticación no utilizarán el middleware 
'''
@auth.route("/login", methods=["POST"])
def login():
  '''
    Input:
    {
      "user": string,
      "password": string
    }
    Output exitoso:
    {
      "msg": "success",
      "JWT_Token": string 
    }, 200

    Output de error en credenciales:
    {
      "error": "user or password incorrect"
    }, 401

    Output de error en el servidor:
    {
      "error": "internal server error"
    }, 500
  '''

  pass