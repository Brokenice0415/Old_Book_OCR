import numpy as np
import os.path
from PIL import Image

def ResizeImage(path, savePath, width, height, type):
    img = Image.open(path)
    img = np.array(img)
    h, w = img.shape

    if h > w:
        timg = np.ones((h,h))*255
        timg[:h, :w] = img
    else:
        timg = np.ones((w, w))*255
        timg[:h, :w] = img

    img = Image.fromarray(timg)
    out = img.resize((width, height), Image.ANTIALIAS)
    out.convert('RGB').save(savePath, type)

if __name__ == "__main__":
    width = 25
    height = 25
    type = 'jpeg'
    for root, dirs, files in os.walk("tmp\\split\\"):
        for file in files:
            path = root + file
            savePath = "tmp\\test\\" + file[:file.rindex('.')+1] + "jpg"
            if "jpg" in file:
                print(path)
                ResizeImage(path, savePath, width, height, type)