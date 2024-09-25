from flask import Blueprint, request, jsonify

attendance_routes = Blueprint("attendance", __name__)

@attendance_routes.route("/attendance", methods=["POST"])
def attendance():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    ID_USER = data.get("ID_USER")
    ID_EVENT = data.get("ID_EVENT")

    if ID_USER is None or ID_EVENT is None:
        return jsonify({"error": "Falta ID del evento o de un Usuario Valido"}), 400
    
    if ID_USER == 1:
        return jsonify({"message": "Gracias por registrarte Pedro"}), 200
    else:
        return jsonify({"error": "Error en el registro"}), 400