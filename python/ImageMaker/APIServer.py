from ImageMaker import ImageMaker
from flask import Flask, send_file
from flask_restful import Resource, Api, request
import os, sys

username = 'littlewood'
password = 'JohnEdenson'

app = Flask(__name__)
api = Api(app)

imagemaker = ImageMaker(username, password)
oldImagePath = None

"""
Returns -1 when invalid input is given, 1 while currently splitting, and 0 after starting a splitting thread.
"""
class imageForDegEq(Resource):
    def get(self, degree):
        d = None
        try:
            d = int(degree)
        except:
            return {"RETURN": -1}
        im = imagemaker.makeImageForDegree(d)
        path = sys.path[0]+"/tmp/"
        name = "lwp_roots_degree_"+str(d)+".png"
        path += name
        try:
            os.remove(oldImagePath)
        except:
            pass
        im.save(path, 'png')
        oldImagePath = path
        return send_file(path)

class imageForQuery(Resource):
    def get(self):
        args = request.args
        sql = args['sql']
        size = int(args['size'])
        im = imagemaker.makeImageForQuery(sql, size=size)
        path = sys.path[0]+"/tmp/"
        name = "lwp_roots_query.png"
        path += name
        try:
            os.remove(oldImagePath)
        except:
            pass
        im.save(path, 'png')
        oldImagePath = path
        return send_file(path)

api.add_resource(imageForDegEq, '/imageForDegEq/<degree>')
api.add_resource(imageForQuery, '/imageForQuery')

if __name__ == '__main__':
    app.run(port='5003', host='0.0.0.0')
