import imageio as iio
from pygifsicle import optimize
from pathlib import Path
import numpy as np
import os


class GoesRGifCreator:
    def __init__(self, product, year, startDay, endDay, band, mode, fp="GoesRImages"):
        self.product = product if product else ''
        self.year = year if year else '2020'
        self.startDay = startDay if startDay else 1
        self.endDay = endDay if endDay else 3
        self.band = band if band else "01"
        self.mode = mode if mode else 6

        self.fp = fp
        self.gif_path = os.path.join(os.getcwd(), "Gifs")
        self.gif_path = os.path.join(self.gif_path, self.product)
        self.gif_path = os.path.join(self.gif_path, self.year)
        self.gif_path = os.path.join(self.gif_path, self.band)
        self.gif_path = os.path.join(self.gif_path, str(self.mode))
        try:
            os.makedirs(self.gif_path)
        except:
            print("Couldn't create directory: {}".format(self.gif_path))
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
        optimize(self.gif_path)
