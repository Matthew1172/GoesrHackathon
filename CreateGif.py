import imageio as iio
from pathlib import Path
import numpy as np
import os

class CreateGif:
    def __init__(self, product, year, startDay, endDay, band, mode, fp="GoesRImages"):
        self.product = product if product else ''
        self.year = year if year else '2020'
        self.startDay = startDay if startDay else 1
        self.endDay = endDay if endDay else 3
        self.band = band if band else "01"
        self.mode = mode if mode else 6

        self.fp = fp
        self.gif_path = os.path.join(os.getcwd(), "Gifs")
        try:
            os.mkdir(self.gif_path)
        except:
            print("Could not create gif folder path: {}".format(self.gif_path))
        self.gif_path = os.path.join(self.gif_path, self.product)
        try:
            os.mkdir(self.gif_path)
        except:
            print("Could not create gif product path: {}".format(self.gif_path))
        self.gif_path = os.path.join(self.gif_path, self.year)
        try:
            os.mkdir(self.gif_path)
        except:
            print("Could not create gif year path: {}".format(self.gif_path))
        self.gif_path = os.path.join(self.gif_path, self.band)
        try:
            os.mkdir(self.gif_path)
        except:
            print("Could not create gif band path: {}".format(self.gif_path))
        self.gif_path = os.path.join(self.gif_path, str(self.mode))
        try:
            os.mkdir(self.gif_path)
        except:
            print("Could not create gif mode path: {}".format(self.gif_path))
        self.gif_path = os.path.join(self.gif_path, str(self.startDay)+"-"+str(self.endDay)+".gif")

    def createGif(self):
        images = []

        path = os.path.join(self.fp, self.product)
        path = os.path.join(path, self.year)
        for i in range(self.startDay, self.endDay):
            if i < 10: d = '00'+str(i)
            elif i < 100: d = '0'+str(i)
            else: d = str(i)
            dayPath = os.path.join(path, d)
            for j in range(24):
                if j < 10: h = '0'+str(j)
                else: h = str(j)
                hourPath = os.path.join(dayPath, h)

                bPath = os.path.join(hourPath, str(self.band))
                mPath = os.path.join(bPath, str(self.mode))

                for file in Path(mPath).iterdir():
                    if not file.is_file(): continue
                    images.append(iio.v2.imread(file))
        if len(images) < 1: return
        frames = np.stack(images, axis=0)
        iio.mimsave(self.gif_path, frames, duration=0.1)


year = "2022"
product = "ABI-L1b-RadF"
startDay = 1
endDay = 3
mode = 6
for i in range(1, 17):
    if i < 10: b = '0'+str(i)
    else: b = str(i)
    cg = CreateGif(product=product, year=year, startDay=startDay, endDay=endDay, band=b, mode=mode)
    cg.createGif()