import psycopg2

class Database:
    def __init__(self, user, password, host='splitterDB', port='5432', dbname='lwp_roots'):
        self.connectionInfo = {
                'host': host,
                'port': port,
                'dbname': dbname,
                'user': user,
                'password': password
        }
        self.connection = None
        self.cursor = None

    def connect(self):
        connectionInfo = ""
        for key, value in self.connectionInfo.items():
                info = key+"='"+value+"' "
                connectionInfo += info
        self.connection = psycopg2.connect(connectionInfo)
        self.cursor = self.connection.cursor()
        self.connection.set_session(autocommit=True)

    def disconnect(self):
        self.connection.close()
        self.cursor = None
        self.connection = None

    def getState(self):
        self.cursor.callproc('get_max_degree')
        degree = self.cursor.fetchall()[0][0]
        self.cursor.callproc('get_max_code')
        code = self.cursor.fetchall()[0][0]
        return {'Degree': degree, 'CoeffCode': code}

