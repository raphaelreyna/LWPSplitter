from PIL import Image, ImageDraw
from DataBase import DataBaseGetter

class ImageMaker:
    def __init__(self, user, password, host="localhost", port="5432", dbname="lwp_roots"):
        self.db = DataBaseGetter(user, password, host=host, port=port, dbname=dbname)
        self.db.connect()

    def linearTrans(self, point, a, b):
        x = a*point[0]+b
        y = a*point[1]+b
        return (x,y)

    def makeImageForQuery(self, query, size=1000, backgroundColor=(0,0,0,255)):
        timesToCall, generatorFunction = self.db.getCountAndGenForQuery(query)
        gen = generatorFunction()
        image = Image.new('RGBA', (size, size), backgroundColor)
        ctx = ImageDraw.Draw(image)
        for i in range(timesToCall):
            points = next(gen)
            for point in points:
                p = self.linearTrans(point, 200, size/2)
                ctx.point(p, fill=(255,0,0,255))
        return image

    def makeImageForDegree(self, degree, size=1000):
        timesToCall, generatorFunction = self.db.getRootsComplexNumbersSingle("=", degree)
        gen = generatorFunction()
        image = Image.new('RGBA', (size, size), (0,0,0,0))
        ctx = ImageDraw.Draw(image)
        for i in range(timesToCall):
            points = next(gen)
            for point in points:
                p = self.linearTrans(point, 200, size/2)
                ctx.point(p, fill=(255,0,0,255))
        return image
