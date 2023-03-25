import PIL
from PIL import Image, ImageDraw
import math
# import numpy as np

class Stellar:
    def __init__(self):
        self.img = Image.open("em.jpg")
        self.origin = (1895, 510)
        self.px_per_lat = 415 / 90
        self.px_per_lon = 1800 / 390
        self.sc = self.img.crop(box=(1895 - self.px_per_lon * 360, 510 - 415, 1895, 510 + 415))
        # ic.show()
        # self.mat = self.sc.load()
        self.video = None
        self.output = None
        self.sb, self.eb = None, None
        # print(self.sc.width, self.sc.height)
    def getpx(self, lat, lon):
        return self.sc.getpixel((int(self.sc.width - lon * self.px_per_lon - 1), lat * self.px_per_lat))
    def transform(self, radius, beta, view = 90):
        self.radius, self.beta, self.view = radius, beta, view
        self.output = Image.new('RGB', (radius * 2, radius * 2))
        mx, my = radius, radius
        for x in range(-radius, radius):
            for y in range(-radius, radius):
                if x ** 2 + y ** 2 > radius ** 2:
                    continue
                rx, ry = x, -y
                lat = math.sqrt(x ** 2 + y ** 2) / radius * view
                lon = 0
                if x == 0:
                    if ry >= 0:
                        lon = math.pi * .5
                    else:
                        lon = math.pi * 1.5
                else:
                    if x > 0 and ry >= 0:
                        lon = math.atan(ry / rx)
                    elif x < 0 and ry >= 0:
                        lon = math.pi - math.atan(-ry / rx)
                    elif x < 0 and ry < 0:
                        lon = math.pi + math.atan(ry / rx)
                    elif x > 0 and ry < 0:
                        lon = 2 * math.pi - math.atan(-ry / rx)
                lon = lon / math.pi * 180
                # print(mx + x, my + y, int(lat))
                latr = math.acos((math.cos(lat / 180 * math.pi) - beta) / (1 - beta * math.cos(lat / 180 * math.pi))) / math.pi * 180
                self.output.putpixel((mx + x, my + y), self.getpx(latr, lon))
    def newPicture(self, radius, beta, view = 90):
        self.video = None
        self.transform(radius, beta, view)
        self.save()
    def newVideo(self, radius, sb, eb, view = 90):
        self.video = []
        self.radius, self.sb, self.eb, self.view = radius, sb, eb, view
    def addFrame(self, beta):
        self.transform(self.radius, beta, self.view)
        self.video.append(self.output)
    def save(self):
        if self.video is None:
            self.output.save("view[%.1fdegree, radius=%dpx]-%.2fc.jpg" % (self.view, self.radius, self.beta))
            print("Saved as view[%.1fdegree, radius=%dpx]-%.2fc.jpg" % (self.view, self.radius, self.beta))
        else:
            self.video[0].save('view[%fdegree, radius=%dpx]-[%.2f, %.2f]c.gif' % (self.view, self.radius, self.sb, self.eb), save_all = True, append_images = self.video[1:], optimize = False, duration = 10)
            print("Saved as view[%fdegree, radius=%dpx]-[%.2f, %.2f]c.gif" % (self.view, self.radius, self.sb, self.eb))
# print(img.width, img.height)

# radius = 1000
stellar = Stellar()
t = input()
if t == "image":
    print("Generating...")
    beta = float(input())
    stellar.transform(800, beta, 90)
else:
    sb = float(input())
    eb = float(input())
    st = float(input())
    print("Generating...")
    stellar.newVideo(800, sb, eb)
    b, i = sb, 0
    while b <= eb:
        print("Generating frame#%d, beta=%.2f" % (i, b))
        stellar.addFrame(b)
        b += st
        i += 1
    stellar.save()