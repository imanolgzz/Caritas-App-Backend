'''
  El middleware es el código que se ejecuta antes de cada petición a una ruta

  La funcionalidad será la siguiente:
    Recibir el JWT desde un header
    Decodificar el JWT
    Enviar un mensaje de error 401 si:
      - El JWT recibido es inválido
      - El JWT recibido está vencido
    Proceder retornando vacío en caso contrario, enviando como parámetro el usuario decodificado del JWT
    a las rutas con el nombre de parámetro JWT_User, con el fin de que cada una pueda validar que se les
    estén enviando solicitudes válidas para su token 
'''