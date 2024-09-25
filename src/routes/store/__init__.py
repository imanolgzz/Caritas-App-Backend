from flask import Blueprint, request, jsonify
from util.db_connection import DB

auth_routes = Blueprint("store", __name__)

@auth_routes.route("/products", methods=["GET"])
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