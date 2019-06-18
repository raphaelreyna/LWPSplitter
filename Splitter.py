import numpy as np
import DataBase

def zeroToMinusOne(x):
    if x == 0:
        return -1
    else:
        return x

def maxCoeffCodeForDegree(degree):
    return (2 ** (degree + 1)) - 1

class Splitter:
    def __init__(
        self, user, password, host="localhost", port="5432", dbname="lwp_roots"
    ):
        self.finishedDegree = False
        self.db = DataBase.DataBaseSetter(user, password, host=host, port=port, dbname=dbname)
        self.db.connect()
        DataBase.setupDataBase(self.db)
        self.state = self.db.getState()
        self.maxCoeffCode = maxCoeffCodeForDegree(self.state['Degree'])
        self.updateState()

    def updateState(self):
        self.state["CoeffCode"] += 1
        if self.state["CoeffCode"] > self.maxCoeffCode:
            self.nextDegree()

    def nextDegree(self):
        self.state['Degree'] += 1
        self.state['CoeffCode'] = 0
        self.maxCoeffCode = maxCoeffCodeForDegree(self.state['Degree'])

    def prepData(self, rootsData):
        return {
            "CoeffCode": self.state["CoeffCode"],
            "Degree": self.state["Degree"],
            "Roots": rootsData
        }

    def splitCurrent(self):
        degree = self.state['Degree']
        code = self.state['CoeffCode']
        return self.rootsOf(code, degree)

    def splitNext(self):
        if self.state['CoeffCode'] > self.maxCoeffCode:
            self.nextDegree()
        rootsData = self.splitCurrent()
        return self.prepData(rootsData)

    def rootsOf(self, coeffCode, degree):
        degreeCode = "0" + str(degree + 1) + "b"
        coefficientsStringArray = list(format(coeffCode, degreeCode))
        coefficients = [zeroToMinusOne(int(coeff)) for coeff in coefficientsStringArray]
        return np.roots(coefficients)

    def run(self, count):
        polysProcessed = 0
        while polysProcessed < count:
            rootsData = self.splitNext()
            result = self.db.enterNewPolynomialRoot(rootsData)
            if result is True:
                self.updateState()
                polysProcessed += 1
            else:
                raise Exception("Lost Connection to Database!")
