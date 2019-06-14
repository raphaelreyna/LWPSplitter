import numpy as np
import json
import os, sys, argparse

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
        self.loadState()
        self.polysProcessed = 0
        self.finishedDegree = False
        self.db = DataBase.DataBaseSetter(user, password, host=host, port=port, dbname=dbname)
        self.db.connect()
        self.db.createTables()

    def loadState(self):
        stateFileExists = os.path.isfile(
            "state.json"
        )  # state.json stores the last worked polynomials code and degree.
        if stateFileExists == False:
            state = {"Degree": 1, "CoeffCode": 0}
            file = open("state.json", "w")
            json.dump(state, file)
            file.close()
        stateFile = open("state.json")
        self.state = json.load(stateFile)
        stateFile.close()
        self.maxCoeffCode = maxCoeffCodeForDegree(self.state["Degree"])

    def flushState(self):
        stateFile = open("state.json", "w")
        json.dump(self.state, stateFile)
        stateFile.close()

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

    def run(self, count):
        polysProcessed = 0
        while polysProcessed < count:
            rootsData = self.splitNext()
            result = self.db.enterNewPolynomialRoot(rootsData)
            if result is True:
                self.updateState()
                self.flushState()
                polysProcessed += 1
            else:
                raise Exception("Lost Connection to Database!")

    def rootsOf(self, coeffCode, degree):
        degreeCode = "0" + str(degree + 1) + "b"
        coefficientsStringArray = list(format(coeffCode, degreeCode))
        coefficients = [zeroToMinusOne(int(coeff)) for coeff in coefficientsStringArray]
        return np.roots(coefficients)

    def parseArgs(self, args=None):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--progress",
            help="Display the last saved polynomials code and degree",
            action="store_true",
        )
        parser.add_argument(
            "--split", help="Split a given number of blocks.", type=int, nargs=1
        )
        return parser.parse_args(args)

    def processArgs(self, args):
        if args.progress:
            stateFile = open("state.json", "r")
            state = json.load(stateFile)
            stateFile.close()
            outputString = (
                "Last polynomial to be split: Degree = "
                + str(state["Degree"])
                + " ,  Coeff. Code = "
                + str(state["CoeffCode"])
            )
            print(outputString)

        if args.split:
            count = args.split[0]
            print("Preparing to split" + str(count) + " blocks.\n")
            self.run(count)

    def main(self):
        args = self.parseArgs(sys.argv[1:])
        self.processArgs(args)
