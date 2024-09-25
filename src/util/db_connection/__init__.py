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

    def connect(self):
        try:
            self.cnx = pymssql.connect(
                server=self.mssql_params['DB_HOST'],
                user=self.mssql_params['DB_USER'],
                password=self.mssql_params['DB_PASSWORD'],
                database=self.mssql_params['DB_NAME'],
                port=self.mssql_params['DB_PORT'])
            
        
        except Exception as e:
            import sys
            sys.exit("Cannot connect to mssql server!: {}".format(e))

    def login(self, user = "Adrian", password="Adrian"):
        with self.cnx.cursor(as_dict=True) as cursor:
            cursor.callproc('CheckLogin', (user, password))
            print(cursor)