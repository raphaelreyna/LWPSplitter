import threading
from Splitter import Splitter
from Database import DatabaseGetter, DatabaseSetter
from flask import Flask
from flask_restful import Resource, Api

username = 'littlewood'
password = 'JohnEdenson'

app = Flask(__name__)
api = Api(app)

dbGetter = DatabaseGetter(username, password)
dbSetter = DatabaseSetter(username, password)

"""
Returns -1 when invalid input is given, 1 while currently splitting, and 0 after starting a splitting thread.
"""
class Split(Resource):
    def get(self, count):
        c = None
        try:
            c = int(count)
        except:
            return {"RETURN": -1}
        if threading.active_count() != 2:
            return {"RETURN": 1}
        else:
            Splitter(dbSetter, c).start()
            return {"RETURN": 0}

class State(Resource):
    def get(self):
        splitting = "False"
        dbGetter.connect()
        if threading.active_count() != 2:
                splitting = "True"
        state = dbGetter.getState()
        dbGetter.disconnect()
        if state['Degree'] is None:
            state = {'CoeffCode': 0, 'Degree': 1}
        state['splitting'] = splitting
        return state

api.add_resource(Split, '/split/<count>')
api.add_resource(State, '/state')

if __name__ == '__main__':
    app.run(port='5002', host='0.0.0.0')
