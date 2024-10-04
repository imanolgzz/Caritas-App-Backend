import pymssql
import dotenv
from os import getenv

class MSSQLDB:
    cnx = None

    def __init__(self, host = getenv('DB_HOST_PROD'), DB = getenv('DB_NAME_PROD'), user = getenv('DB_USER_PROD'), password = getenv('DB_PASSWORD_PROD'), port = getenv('DB_PORT_PROD')) -> None:
        # print all the params
        print(host, DB, user, password, port)
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

    def login(self, username = "Adrian", password="Adrian"):
        with self.cnx.cursor(as_dict=True) as cursor:
            cursor.callproc('CheckLogin', (username, password))
            message = (cursor.fetchall()[0]['Message'])
            print(message)
            if message == "Invalid email or password":
                return False
            return True
          
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

DB = MSSQLDB()