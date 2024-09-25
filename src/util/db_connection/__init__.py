import pymssql

class MSSQLDB:
    # Connect to mssql dB from start
    mssql_params = {}
    mssql_params['DB_HOST'] = '100.80.80.7'
    mssql_params['DB_NAME'] = 'CaritasDB'
    mssql_params['DB_USER'] = 'SA'
    mssql_params['DB_PASSWORD'] = 'Shakira123.'

    def connect(self):
        try:
            cnx = pymssql.connect(
                server=self.mssql_params['DB_HOST'],
                user=self.mssql_params['DB_USER'],
                password=self.mssql_params['DB_PASSWORD'],
                database=self.mssql_params['DB_NAME'])
            return cnx
        except Exception as e:
            import sys
            sys.exit("Cannot connect to mssql server!: {}".format(e))