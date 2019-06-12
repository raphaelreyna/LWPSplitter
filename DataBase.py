import psycopg2
import collections

class DataBaseException(Exception):
        def __init__(self, message):
                super().__init__(message)

class DataBase:
        def __init__(self, user, password, host='localhost', port='5432', dbname='lwp_roots'):
                self.connectionInfo = {
                        'host': host,
                        'port': port,
                        'dbname': dbname,
                        'user': user,
                        'password': password
                }
                self.connection = None
                self.cursor = None
                self.insertSQL = {}
                self.getterSQL = {}
                self.getSQLSource()

        def getSQLSource(self):
                srcFile = open("sql/enter_polynomial.sql")
                self.insertSQL['polynomial'] = srcFile.read().rstrip('\n')
                srcFile.close()
                srcFile = open("sql/enter_complex_number.sql")
                self.insertSQL['complex_number'] = srcFile.read().rstrip('\n')
                srcFile.close()
                srcFile = open("sql/enter_root.sql")
                self.insertSQL['root'] = srcFile.read().rstrip('\n')
                srcFile.close()
                srcFile = open("sql/get_complex_number_id.sql")
                self.getterSQL['complex_number'] = srcFile.read().rstrip('\n')
                srcFile.close()

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

        def commit(self):
                self.connection.commit()

        def createTables(self):
                if self.cursor is not None:
                        sqlSource = open("sql/create_tables.sql")
                        try:
                                self.cursor.execute(sqlSource.read())
                        except psycopg2.errors.DuplicateTable:
                                sqlSource.close()
                                print("Tables already exist")
                                return
                        else:
                                sqlSource.close()
                else:
                        raise DataBaseException("Tried to create a table but cursor does not exist.")

        def enterNewPolynomial(self, d, c):
                if self.cursor is not None:
                        sql = self.insertSQL['polynomial'].format(degree=d, code=c)
                        try:
                                self.cursor.execute(sql)
                                return self.cursor.fetchone()[0]
                        except psycopg2.errors.UniqueViolation:
                                print("Tried to insert duplicate polynomial; Request ignored.")
                                return None
                else:
                        raise DataBaseException("Tried to insert a new polynomial but cursor does not exist.")
                return None

        def enterNewComplexNumber(self, r, i):
                if self.cursor is not None:
                        sql = self.insertSQL['complex_number'].format(realPart=r, imaginaryPart=i)
                        try:
                                self.cursor.execute(sql)
                                return self.cursor.fetchone()[0]
                        except psycopg2.errors.UniqueViolation:
                                print("Tried to insert duplicate complex number; Request ignored.")
                                return self.getComplexNumberID(r, i)
                else:
                        raise DataBaseException("Tried to insert a new complex number but cursor does not exist.")
                return None

        def enterNewPolynomialRoot(self, polynomial):
                print("Received request to enter polynomial with "+str(len(polynomial["Roots"]))+"\n")
                if self.cursor is not None:
                    polyID = self.enterNewPolynomial(polynomial['Degree'], polynomial['CoeffCode'])
                    if polyID is not None:
                        for root, count in collections.Counter(polynomial['Roots']).items():
                                rootID = self.enterNewComplexNumber(root.real, root.imag)
                                print("Entering polyID: "+str(polyID)+" with rootID: "+str(rootID)+"\n")
                                if rootID is not None:
                                        sql = self.insertSQL['root'].format(polynomial=polyID, complexNumber=rootID, multiplicity=count)
                                        try:
                                                self.cursor.execute(sql)
                                                self.cursor.fetchone()
                                        except psycopg2.errors.UniqueViolation:
                                                print("Tried to insert duplicate root; Request rejected.")
                                                print("This should not have happened. Terminating. \n")
                                                raise
                else:
                        raise DataBaseException("Tried to insert a new root but cursor does not exist.")
                return True


        def getComplexNumberID(self, r, i):
                sql = self.getterSQL['complex_number'].format(realPart=r, imaginaryPart=i)
                self.cursor.execute(sql)
                return self.cursor.fetchone()[0]

