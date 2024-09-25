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

    def login(self, user = "Adrian", password="Adrian"):
        with self.cnx.cursor(as_dict=True) as cursor:
            cursor.callproc('CheckLogin', (user, password))
            message = (cursor.fetchall()[0]['Message'])
            if message == "Invalid email or password":
                return False
            return True

DB = MSSQLDB()
