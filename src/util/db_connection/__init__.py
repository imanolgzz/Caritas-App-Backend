import pymssql

class MSSQLDB:
    cnx = None

    def __init__(self, host = '100.80.80.7', DB = 'CaritasDB', user = 'SA', password = 'Shakira123.', port = '1433') -> None:
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

    def login(self, user = "Adrian", password="Adrian"):
        with self.cnx.cursor(as_dict=True) as cursor:
            cursor.callproc('CheckLogin', (user, password))
            message = (cursor.fetchall()[0]['Message'])
            if message == "Invalid email or password":
                return False
            return True

    def eventAttendance(self, USER_ID = 1, EVENT_ID = 1):
        with self.cnx.cursor(as_dict=True) as cursor:
            cursor.callproc("AgendarEvento",(USER_ID,EVENT_ID))
            message = (cursor.fetchall()[0]['Message'])
            if message == "ID de usuario o evento no válido":
                return False
            return True
    
DB = MSSQLDB()
