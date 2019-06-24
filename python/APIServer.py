from Splitter import Splitter
from Database import DatabaseGetter, DatabaseSetter
from flask import Flask, request
from flask_restful import Resource, Api

username = 'littlewood'
password = 'JohnEdenson'

app = Flask(__name__)
api = Api(app)

dbGetter = DatabaseGetter(username, password)
dbSetter = DatabaseSetter(username, password)
dbGetter.connect()

splittingthread = Splitter(dbSetter, 0)
splittingthread.start()

class Split(Resource):
    def get(self, count):
        c = None
        try:
            c = int(count)
        except:
            return {"RETURN": -1}
        if c is not None:
            if splittingthread.is_alive() is True:
                return {"RETURN": 0}
            else:
                splittingthread = Splitter(dbSetter, c)
                splittingthread.start()
                return {"RETURN": 1}
        else:
                splittingthread = Splitter(dbSetter, c)
                splittingthread.start()
                return {"RETURN": 1}

class State(Resource):
    def get(self):
        splitting = "False"
        if splittingthread is not None:
            if splittingthread.is_alive() is True:
                splitting = "True"
        state = dbGetter.getState()
        if state['Degree'] is None:
            state = {'CoeffCode': 0, 'Degree': 1}
        state['splitting'] = splitting
        return state

api.add_resource(Split, '/split/<count>')
api.add_resource(State, '/state')

if __name__ == '__main__':
    app.run(port='5002', host='0.0.0.0')
