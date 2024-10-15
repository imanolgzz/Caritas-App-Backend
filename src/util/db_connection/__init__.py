import pymssql
from os import getenv

class MSSQLDB:
    
    def __init__(self, host=getenv('DB_HOST_PROD'), DB=getenv('DB_NAME_PROD'), 
                 user=getenv('DB_USER_PROD'), password=getenv('DB_PASSWORD_PROD'), 
                 port=getenv('DB_PORT_PROD')) -> None:
        # Store connection parameters
        self.mssql_params = {
            'DB_HOST': host,
            'DB_NAME': DB,
            'DB_USER': user,
            'DB_PASSWORD': password,
            'DB_PORT': port
        }

    def connect(self):
        """Open a new connection for each request."""
        try:
            return pymssql.connect(
                server=self.mssql_params['DB_HOST'],
                user=self.mssql_params['DB_USER'],
                password=self.mssql_params['DB_PASSWORD'],
                database=self.mssql_params['DB_NAME'],
                port=self.mssql_params['DB_PORT']
            )
        except Exception as e:
            import sys
            sys.exit(f"Cannot connect to MSSQL server on {self.mssql_params['DB_HOST']}: {e}")

    def login(self, username, password):
        """Use a new connection for every request to avoid conflicts."""
        try:
            with self.connect() as conn:
                with conn.cursor(as_dict=True) as cursor:
                    cursor.callproc('CheckLogin', (username, password))
                    message = cursor.fetchall()[0]['Message']
                conn.commit()
            return message != "Invalid email or password"
        except Exception as e:
            print(f"Error: {str(e)}")
            return False

    def eventosEstadisticas(self, user_ID):
        """Get statistics for events."""
        try:
            with self.connect() as conn:
                with conn.cursor(as_dict=True) as cursor:
                    cursor.callproc('eventosStats', (user_ID,))
                    results = cursor.fetchall()
                return results
        except Exception as e:
            print(f"Error: {str(e)}")
            return []

    def store(self):
        """Fetch products for the store."""
        with self.connect() as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.callproc('GetProductosTienda', ())
                results = cursor.fetchall()
            return results

    def eventosFuturos(self):
        """Fetch future events ordered by date."""
        with self.connect() as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.callproc('GetEventosFuturosOrdenadosPorFecha', ())
                results = cursor.fetchall()
            return results

    def eventAttendance(self, ID_USUARIO, ID_EVENTO):
        """Schedule an event for a user."""
        with self.connect() as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.callproc("AgendarEvento", (ID_USUARIO, ID_EVENTO))
                message = cursor.fetchone()['Message']
            conn.commit()
            return message not in ["ID de usuario o evento no válido", "El usuario ya está registrado"]

    def confirmarAsistencia(self, ID_USUARIO, ID_EVENTO, PASSWORD_EVENTO):
        """Confirm attendance for an event."""
        with self.connect() as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.callproc("ConfirmarAsistencia", (ID_USUARIO, ID_EVENTO, PASSWORD_EVENTO))
                message = cursor.fetchone()['Message']
            conn.commit()
            return message not in ["El usuario no está registrado", "Contraseña incorrecta"], message

    def getRegisteredEvents(self, ID_USUARIO):
        """Fetch events a user is registered for."""
        with self.connect() as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.callproc("GetEventosAgendadosUsuario", (ID_USUARIO,))
                eventos = cursor.fetchall()
            if not eventos:
                return {"success": False, "message": "El usuario no está registrado en ningún evento"}
            return {"success": True, "events": eventos}

    def redeem(self, USER_ID=31, PRODUCT_ID=1):
        """Redeem a product for a user."""
        try:
            with self.connect() as conn:
                with conn.cursor(as_dict=True) as cursor:
                    cursor.callproc("RealizarCompra", (USER_ID, PRODUCT_ID))
                    result = cursor.fetchone()
                conn.commit()
                return result['Status'] if result else None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def getUsuario(self, CORREO):
        """Fetch user information based on email."""
        with self.connect() as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.callproc("GetUsuario", (CORREO,))
                results = cursor.fetchall()
            return results

    def monthlyEvents(self):
        """Fetch events for the current month."""
        with self.connect() as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.callproc("GetEventosMesActual", ())
                results = cursor.fetchall()
            return results

    def cuestionario(self):
        with self.connect() as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.callproc('GetQuestionsBasedOnType', (1))
                eventos = cursor.fetchall()
                eventos
            return eventos

    def respuestas(self):
        with self.connect() as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.callproc('GetChoices')
                eventos = cursor.fetchall()
                return eventos
        
    def getUsuario(self, correo):
        with self.connect() as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.callproc("GetUsuario", (correo,))
                user = cursor.fetchall()
                return user
            
    def eventosFuturos(self):
        with self.connect() as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.callproc('GetEventosFuturosOrdenadosPorFecha')
                eventos = cursor.fetchall()
                return eventos

# Initialize DB object
DB = MSSQLDB()
