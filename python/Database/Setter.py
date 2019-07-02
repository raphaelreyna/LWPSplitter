import collections
from Database.Database import Database as DB
from Database.Errors import Error as Error
from psycopg2.errors import UniqueViolation

class DatabaseSetter(DB):
    def __init__(self, user, password, host='splitterDB', port='5432', dbname='lwp_roots'):
        DB.__init__(self, user, password, host=host, port=port, dbname=dbname)

    def enterNewPolynomial(self, d, c):
        try:
            self.cursor.callproc('insert_polynomial', (d, c))
            return self.cursor.fetchone()[0]
        except UniqueViolation:
            return None

    def enterNewComplexNumber(self, r, i, ret=False):
        try:
            self.cursor.callproc('insert_complex_number', (r, i))
            return self.cursor.fetchone()[0]
        except UniqueViolation:
            if ret is True:
                self.cursor.callproc('get_complex_number_id', (r, i))
                return self.cursor.fetchone()[0]
            else:
                return None

    def enterNewPolynomialRoot(self, polynomial):
        if self.cursor is not None:
            polyID = self.enterNewPolynomial(polynomial['Degree'], polynomial['CoeffCode'])
            if polyID is not None:
                for root, count in collections.Counter(polynomial['Roots']).items():
                    rootID = self.enterNewComplexNumber(root.real, root.imag, ret=True)
                    if rootID is not None:
                        try:
                            self.cursor.callproc('insert_root', (polyID, rootID, count))
                            self.cursor.fetchone()
                        except UniqueViolation:
                            print("Tried to insert duplicate root; Request rejected.")
                            print("This should not have happened. Terminating. \n")
                            raise
        else:
            raise Error("Tried to insert a new root but cursor does not exist.")
        return True

    def enterNewRandomComplexNumber(self, r, i):
        """
        Returns -1 if tried to insert a duplicate.
        Returns the id of the newly entered complex number otherwise.
        """
        if self.cursor is not None:
            try:
                self.cursor.callproc('insert_random_complex_number', (r, i))
                return self.cursor.fetchone()[0]
            except UniqueViolation:
                return -1
