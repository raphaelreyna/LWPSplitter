from PIL import Image, ImageDraw
from Database.Getter import DatabaseGetter

class ImageMaker:
    def __init__(self, user, password, host="localhost", port="5432", dbname="lwp_roots"):
        self.db = DatabaseGetter(user, password, host=host, port=port, dbname=dbname)
        self.db.connect()

    def linearTrans(self, point, a, b):
        x = a*point[0]+b
        y = a*point[1]+b
        return (x,y)

    def makeImageForQuery(self, query, size=1000, backgroundColor=(0,0,0,255)):
        firstpart = "SELECT real_part, imaginary_part FROM polynomial_roots WHERE "
        timesToCall, generatorFunction = self.db.getCountAndGenForQuery(firstpart+query+";")
        gen = generatorFunction()
        image = Image.new('RGBA', (size, size), backgroundColor)
        ctx = ImageDraw.Draw(image)
        for i in range(timesToCall):
            points = next(gen)
            for point in points:
                p = self.linearTrans(point, 200, size/2)
                ctx.point(p, fill=(255,0,0,255))
        return image

    def makeImageForDegree(self, degree, size=1000, backgroundColor=(0,0,0,255)):
        timesToCall, generatorFunction = self.db.execFunc('get_distinct_roots_of_degree_eq', [degree])
        gen = generatorFunction()
        image = Image.new('RGBA', (size, size), backgroundColor)
        ctx = ImageDraw.Draw(image)
        for i in range(timesToCall):
            points = next(gen)
            for point in points:
                p = self.linearTrans(point, size*200/1000, size/2)
                ctx.point(p, fill=(255,0,0,255))
        return image
