from Database.Database import Database as DB
from math import ceil

class DatabaseGetter(DB):
    def __init__(self,
                 user,
                 password,
                 host='splitterDB',
                 port='5432',
                 dbname='lwp_roots',
                 blockSize=50):
        DB.__init__(self,
                          user,
                          password,
                          host=host,
                          port=port,
                          dbname=dbname)
        self.transferBlockSize = blockSize

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

    def execFunc(self, funcName, args):
        self.cursor.callproc(funcName, args)
        rowcount = self.cursor.rowcount
        timesToCall = ceil(rowcount/self.transferBlockSize)
        def f():
            timesCalled = 0
            while timesCalled < timesToCall:
                yield self.cursor.fetchmany(self.transferBlockSize)
                timesCalled += 1
        return (timesToCall, f)
