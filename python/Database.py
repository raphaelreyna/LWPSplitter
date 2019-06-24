from math import ceil, sin, cos
from random import uniform
import psycopg2
import collections

class DatabaseException(Exception):
        def __init__(self, message):
                super().__init__(message)

class Database:
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
                self.cursor.callproc('maxDegree')
                degree = self.cursor.fetchall()[0][0]
                self.cursor.callproc('maxCode')
                code = self.cursor.fetchall()[0][0]
                return {'Degree': degree, 'CoeffCode': code}

class DatabaseGetter(Database):
        def __init__(self, user, password, host='localhost', port='5432', dbname='lwp_roots'):
                Database.__init__(self, user, password, host=host, port=port, dbname=dbname)
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

class DatabaseSetter(Database):
        def __init__(self, user, password, host='localhost', port='5432', dbname='lwp_roots'):
                Database.__init__(self, user, password, host=host, port=port, dbname=dbname)
                self.insertSQL = {}
                self.getterSQL = {}
                self.getSQLSource()

        def getSQLSource(self):
                srcFile = open("sql/insert/polynomial.sql")
                self.insertSQL['polynomial'] = srcFile.read().rstrip('\n')
                srcFile.close()
                srcFile = open("sql/insert/complex_number.sql")
                self.insertSQL['complex_number'] = srcFile.read().rstrip('\n')
                srcFile.close()
                srcFile = open("sql/insert/random_complex_number.sql")
                self.insertSQL['random'] = srcFile.read().rstrip('\n')
                srcFile.close()
                srcFile = open("sql/insert/root.sql")
                self.insertSQL['root'] = srcFile.read().rstrip('\n')
                srcFile.close()
                srcFile = open("sql/get/complex_number_id.sql")
                self.getterSQL['complex_number_id'] = srcFile.read().rstrip('\n')
                srcFile.close()
                srcFile = open("sql/get/roots_complex_numbers.sql")
                self.getterSQL['roots_complex_number'] = srcFile.read().rstrip('\n')
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
                        raise DatabaseException("Tried to insert a new polynomial but cursor does not exist.")
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
                        raise DatabaseException("Tried to insert a new complex number but cursor does not exist.")
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
                        raise DatabaseException("Tried to insert a new root but cursor does not exist.")
                return True

        def enterNewRandomRoot(self):
                if self.cursor is not None:
                        r = uniform(0.5, 2)
                        theta = uniform(0, 6.2831)
                        real_part = r*cos(theta)
                        imaginary_part = r*sin(theta)
                        sql = self.insertSQL['random'].format(real_part=real_part, imaginary_part=imaginary_part)
                        try:
                                self.cursor.execute(sql)
                        except psycopg2.errors.UniqueViolation:
                                self.enterNewRandomRoot()

        def getComplexNumberID(self, r, i):
                sql = self.getterSQL['complex_number_id'].format(realPart=r, imaginaryPart=i)
                self.cursor.execute(sql)
                return self.cursor.fetchone()[0]

        def polynomialIsComplete(self, id):
                self.cursor.callproc('polynomialIsComplete',[id])
                return self.cursor.fetchall()[0][0]

        def degreeOfPolynomial(self, id):
                self.cursor.callproc('degreeOfPolynomial', [id])
                return self.cursor.fetchall()[0][0]

        def numberOfRootsLogged(self, id):
                self.cursor.callproc('numberOfRootsLogged', [id])
                return self.cursor.fetchall()[0][0]

        def polynomialIsComplete(self, id):
                self.cursor.callproc('polynomialIsComplete', [id])
                return self.cursor.fetchall()[0][0]

        def globalMultiplicityOfRoot(self, id):
                self.cursor.callproc('globalMultiplicityOf', [id])
                return self.cursor.fetchall()[0][0]

        def globalPolynomialCountOfRoot(self, id):
                self.cursor.callproc('globalPolynomialCountOf', [id])
                return self.cursor.fetchall()[0][0]

        def purgePolynomial(self, id):
                self.cursor.callproc('purgePolynomial', [id])
                self.cursor.fetchall()
                return None

