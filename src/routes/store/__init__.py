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
    Canjear un producto para un usuario.
    ---
    parameters:
        - in: body
          name: SolicitudDeCanje
          description: Cuerpo de la solicitud para canjear un producto
          schema:
            type: object
            required:
                - ID_USER
                - ID_PRODUCT
            properties:
                ID_USER:
                    type: string
                    description: ID del usuario
                    example: 12345
                ID_PRODUCT:
                    type: string
                    description: ID del producto
                    example: 67890
    responses:
        200:
          description: Compra exitosa
          content:
            application/json:
              schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Compra exitosa.
        400:
          description: Solicitud incorrecta
          content:
            application/json:
              schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Puntos insuficientes o Cantidad insuficiente.
        404:
          description: Usuario o producto no encontrado
          content:
            application/json:
              schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Usuario o producto no encontrado.
        500:
          description: Error interno del servidor
          content:
            application/json:
              schema:
                type: object
                properties:
                    message:
                        type: string
                        example: ID_PRODUCT o ID_USER no proporcionado o error.
    """

    data = request.get_json()

    try:
        status = DB.redeem(data["ID_USER"], data["ID_PRODUCT"])
        messages = {
            0: "Compra exitosa.",        # Success
            1: "Puntos insuficientes.",  # Insufficient points
            2: "Cantidad insuficiente.", # Not enough quantity
            3: "Usuario o producto no encontrado." # User or product not found
        }
        response = jsonify({"message": messages.get(status, "Código de estado desconocido.")})
    
        # Set the status code based on the DB response
        if status == 0:
            response.status_code = 200  # Success
        elif status == 1:
            response.status_code = 400  # Bad Request for insufficient points
        elif status == 2:
            response.status_code = 400  # Bad Request for not enough quantity
        elif status == 3:
            response.status_code = 404  # Not Found for user or product not found
        else:
            response.status_code = 500  # Internal Server Error for unknown status

    except:
        response = jsonify({"message": "ID_PRODUCT o ID_USER no proporcionado o error"})
        response.status_code = 500  # Internal Server Error for exceptions

    return response