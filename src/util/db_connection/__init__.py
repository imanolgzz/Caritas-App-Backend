import pymssql

class MSSQLDB:
    def __init__(self, Host = '100.80.80.7', DB = 'CaritasDB', User = 'SA', Password = 'Shakira123.', Port = '1433') -> None:
        self.mssql_params = {}
        self.mssql_params['DB_HOST'] = Host
        self.mssql_params['DB_NAME'] = DB
        self.mssql_params['DB_USER'] = User
        self.mssql_params['DB_PASSWORD'] = Password
        self.mssql_params['DB_PORT'] = Port

    def connect(self):
        try:
            cnx = pymssql.connect(
                server=self.mssql_params['DB_HOST'],
                user=self.mssql_params['DB_USER'],
                password=self.mssql_params['DB_PASSWORD'],
                database=self.mssql_params['DB_NAME'],
                port=self.mssql_params['DB_PORT'])
            return cnx
        except Exception as e:
            import sys
            sys.exit("Cannot connect to mssql server!: {}".format(e))