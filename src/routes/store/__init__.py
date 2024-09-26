from flask import Blueprint, request, jsonify
from util.db_connection import DB

store_routes = Blueprint("store", __name__)

@store_routes.route("/products", methods=["GET"])
def products():
    """
    Obtener todos los productos redimibles de la tienda
    ---
    responses:
        200:
          description: Lista de productos obtenida exitosamente
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    ID_PRODUCTO:
                      type: integer
                      description: ID del producto
                      example: 1
                    NOMBRE:
                      type: string
                      description: Nombre del producto
                      example: "Producto A"
                    DESCRIPCION:
                      type: string
                      description: Descripción del producto
                      example: "Descripción del Producto A"
                    PUNTAJE:
                      type: integer
                      description: Puntos necesarios para redimir el producto
                      example: 100
                    CANT_DISPONIBLE:
                      type: integer
                      description: Cantidad disponible del producto
                      example: 50
        400:
          description: Error de conexión
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "Error de conexión"
        404:
          description: No se encontraron productos
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "No se encontraron productos"
    """
    products = DB.store()

    if products:
        response = jsonify(products)
        response.status_code = 200
        return response

    else:
        response = jsonify({ "message": "Error loggin in" })
        response.status_code = 400
        return response


@store_routes.route("/redeem", methods=["POST"])
def redeem():
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

    try:
        status = DB.redeem(data["ID_PRODUCT"])
        messages = {
            0: "Compra realizada con éxito.",
            1: "Puntos insuficientes.",
            2: "Usuario o producto no encontrado."
        }

        response = jsonify({"message": messages.get(status, "Unknown status code.")})
        response.status_code = 200
    except:
        response = jsonify({"message": "ID_PRODUCT not provided or error"})
    
    return response