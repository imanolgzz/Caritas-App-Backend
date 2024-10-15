import pymssql
from os import getenv

class MSSQLDB:
    cnx = None

    def __init__(self, host = getenv('DB_HOST_PROD'), DB = getenv('DB_NAME_PROD'), user = getenv('DB_USER_PROD'), password = getenv('DB_PASSWORD_PROD'), port = getenv('DB_PORT_PROD')) -> None:
        # print all the params
        self.mssql_params = {}
        self.mssql_params['DB_HOST'] = host
        self.mssql_params['DB_NAME'] = DB
        self.mssql_params['DB_USER'] = user
        self.mssql_params['DB_PASSWORD'] = password
        self.mssql_params['DB_PORT'] = port

        # Connect to database on start
        self.connect()
        print(self.cnx)

    def connect(self):
        try:
            self.cnx = pymssql.connect(
                server=self.mssql_params['DB_HOST'],
                user=self.mssql_params['DB_USER'],
                password=self.mssql_params['DB_PASSWORD'],
                database=self.mssql_params['DB_NAME'],
                port=self.mssql_params['DB_PORT'])
            print(f"!!!!\nSuccessfully connected to {self.mssql_params['DB_NAME']}")
        
        except Exception as e:
            import sys
            sys.exit(f"Can not connect to mssql server on {self.mssql_params['DB_HOST']}: {e}")

    def login(self, username, password):
        try:
            with self.cnx.cursor(as_dict=True) as cursor:
                cursor.callproc('CheckLogin', (username, password))
                message = (cursor.fetchall()[0]['Message'])            
            if message == "Invalid email or password":
                return False
            return True
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            DB.cnx.commit()

    def eventosEstadisticas(self, user_ID):
        try:
            with self.cnx.cursor(as_dict=True) as cursor:
                cursor.callproc('eventosStats', (user_ID))
                results = cursor.fetchall()
                print(results)
                return results
        except Exception as e:
            print(f"Error: {str(e)}")    
          
    def store(self):
        with self.cnx.cursor(as_dict=True) as cursor:
            cursor.callproc('GetProductosTienda', ())
            results = cursor.fetchall()
        return results
    
    def eventosFuturos(self):
        with self.cnx.cursor(as_dict=True) as cursor:
            cursor.callproc('GetEventosFuturosOrdenadosPorFecha', ())
            results = cursor.fetchall()
        return results

    def eventAttendance(self, ID_USUARIO , ID_EVENTO):
        with self.cnx.cursor(as_dict=True) as cursor:
            cursor.callproc("AgendarEvento",(ID_USUARIO,ID_EVENTO))
            message = (cursor.fetchone()['Message'])
            if message == "ID de usuario o evento no válido" or message == "El usuario ya está registrado":
                return False

            return True
    
    def confirmarAsistencia(self, ID_USUARIO, ID_EVENTO, PASSWORD_EVENTO):
        with self.cnx.cursor(as_dict=True) as cursor:
            cursor.callproc("ConfirmarAsistencia", (ID_USUARIO, ID_EVENTO, PASSWORD_EVENTO))
            message = (cursor.fetchone()['Message'])
            print("Mensaje de la base de datos: " + str(message))
            if message == "El usuario no está registrado para el evento especificado" or message == "El usuario ya está registrado" or message == "ID de usuario no válido" or message == "ID de evento no válido" or message == "El usuario ya está registrado" or message == "Contraseña incorrecta":
                return False, message
            return True, message

    def getRegisteredEvents(self, ID_USUARIO):
        with self.cnx.cursor(as_dict=True) as cursor:
            cursor.callproc("GetEventosAgendadosUsuario", (ID_USUARIO,))
            eventos = cursor.fetchall()
            if not eventos:
                return {"success": False, "message": "El usuario no está registrado en ningún evento"}
            return {"success": True, "events": eventos}

    
    def redeem(self, USER_ID=31, PRODUCT_ID=1):
        try:
            with self.cnx.cursor(as_dict=True) as cursor:
                # Call the stored procedure
                cursor.callproc("RealizarCompra", (USER_ID, PRODUCT_ID))
            
                # Fetch the single result
                result = cursor.fetchone()
                if result is not None:
                    return result['Status']  # Return the Status
                return None  # or some default value if no status was returned
        except Exception as e:
            # Handle exceptions (e.g., log the error, re-raise, etc.)
            print(f"An error occurred: {e}")
            return None  # or some default value or error message 

    def getUsuario(self,CORREO):
        with self.cnx.cursor(as_dict = True) as cursor:
            cursor.callproc("GetUsuario",(CORREO,))
            results = cursor.fetchall()
        return results
    
    def monthlyEvents(self):
        with self.cnx.cursor(as_dict = True) as cursor:
            cursor.callproc("GetEventosMesActual",())
            results = cursor.fetchall()
        return results

DB = MSSQLDB()