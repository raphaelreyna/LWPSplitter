from math import ceil
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
                self.cursor.callproc('getMaxDegree')
                degree = self.cursor.fetchall()[0][0]
                self.cursor.callproc('getMaxCode')
                code = self.cursor.fetchall()[0][0]
                return {'CoeffCode': code, 'Degree': degree}

class DataBaseGetter(DataBase):
        def __init__(self, user, password, host='localhost', port='5432', dbname='lwp_roots'):
                DataBase.__init__(self, user, password, host=host, port=port, dbname=dbname)
                self.sql = {}
                self.getSQLSource()
                self.transferBlockSize = 50

        def getSQLSource(self):
                srcFile = open("sql/get_roots_complex_numbers.sql")
                self.sql['RootsComplexNumbers'] = srcFile.read().rstrip('\n')
                srcFile.close()

        def getCountAndGenForQuery(self, query):
                """
                Passes the query on to the database and returns a tuple with a count and a function f.
                Evaluating f produces a generator that fetches 'count' points the from the database each time and yields them.
                The count is how many times we may call on the generator until we exhaust its data.
                """
                self.cursor.execute(query)
                rowcount = self.cursor.rowcount
                timesToCall = ceil(rowcount/self.transferBlockSize)
                def f():
                        timesCalled = 0
                        while timesCalled < timesToCall:
                                yield self.cursor.fetchmany(self.transferBlockSize)
                                timesCalled += 1
                return (timesToCall, f)

        def getRootsComplexNumbersSingle(self, relation, degree, distinct=True):
                options = {'relation': relation,
                           'degree': degree,
                           'distinct': "DISTINCT" if distinct else ""
                           }
                query = self.sql['RootsComplexNumbers'].format(**options)
                return self.getCountAndGenForQuery(query)


class DataBaseSetter(DataBase):
        def __init__(self, user, password, host='localhost', port='5432', dbname='lwp_roots'):
                DataBase.__init__(self, user, password, host=host, port=port, dbname=dbname)
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

        def commit(self):
                self.connection.commit()

        def enterNewPolynomial(self, d, c):
                if self.cursor is not None:
                        sql = self.insertSQL['polynomial'].format(degree=d, code=c)
                        try:
                                self.cursor.execute(sql)
                                return self.cursor.fetchone()[0]
                        except psycopg2.errors.UniqueViolation:
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
                                return self.getComplexNumberID(r, i)
                else:
                        raise DataBaseException("Tried to insert a new complex number but cursor does not exist.")
                return None

        def enterNewPolynomialRoot(self, polynomial):
                if self.cursor is not None:
                    polyID = self.enterNewPolynomial(polynomial['Degree'], polynomial['CoeffCode'])
                    if polyID is not None:
                        for root, count in collections.Counter(polynomial['Roots']).items():
                                rootID = self.enterNewComplexNumber(root.real, root.imag)
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

def setupDataBase(database):
        dbWasConnected = True
        if database.cursor is None:
                database.connect()
                dbWasConnected = False
        cursor = database.cursor()
        sqlSource = open("sql/create_tables.sql").read().rstrip("\n")
        try:
                cursor.execute(sqlSource)
        except psycopg2.errors.DuplicateTable:
                sqlSource.close()
                return
        else:
                sqlSource.close()
        sqlSource = open("sql/create_functions.sql").read().rstrip("\n")
        try:
                cursor.execute(sqlSource)
        except:
                sqlSource.close()
                raise
        else:
                sqlSource.close()
        if dbWasConnected is False:
                database.disconnect()


