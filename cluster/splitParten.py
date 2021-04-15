import cv2
from Binarization import *
import numpy as np
import matplotlib.pyplot as plt
import time
import os

"""
投影
"""
def getShadow(img, axis):
    if axis == 'y':
        img = img.T
    pt = []
    for row in img:
        pt.append(sum(row))
    return pt

"""
绘出投影图像
"""
def pltShadow(shadows):
    # 投影
    x1 = np.linspace(0, 1, len(shadows))
    plt.plot(x1, shadows)

    plt.show()

"""
获得起止范围
"""
def getRange(shadows, mean):
    t = 0
    start, end = -1, -1
    Range = []
    for i in shadows:
        if i < mean:
            if (start >= 0) and (end == -1):
                end = t
                Range.append([start, end])
                start = -1
                end = -1
        else:
            if start == -1:
                start = t
        t += 1
    return Range

"""
获得文字部分的文字列
"""
def findCharCols(img):
    charCols = []
    shadows = getShadow(img, 'y')
    mean = sum(shadows) / len(shadows) / 2

    """
    获得截取部分的起始位置
    """
    charColsRange = getRange(shadows, mean)

    maxWidth = 0
    for charColRange in charColsRange:
        maxWidth = max(maxWidth, charColRange[1]-charColRange[0])

    for charColRange in charColsRange:
        if maxWidth / (charColRange[1]-charColRange[0]) < 2:
            timg = img[:,charColRange[0]:charColRange[1]]
            # cv2.imshow('img', timg)
            # cv2.waitKey()
            charCols.append(timg)

    return charCols


"""
获取每个文字
"""
def findChars(img):
    chars = []
    shadows = getShadow(img, 'x')
    mean = sum(shadows) / len(shadows) / 4.5

    """
    获取文字的起始位置
    """
    charsRange = getRange(shadows, mean)

    for charRange in charsRange:
        timg = img[charRange[0]:charRange[1], :]
        # cv2.imshow('image', timg)
        # cv2.waitKey()
        chars.append(timg)

    return chars



"""
分割函数主体封装
imgPath : 图片存储目录
"""
def splitImg(imgPath):
    fileName = imgPath.split('\\')[-2]
    imgName = imgPath.split('\\')[-1]
    imgName = imgName[:imgName.find('.')]

    print(fileName + ":\t" + imgName + "开始分割...")

    startTime = time.process_time()
    img = Binarization(imgPath)
    charCols = findCharCols(img)
    chars = []
    charCount = 0
    for charCol in charCols:
        chars = findChars(charCol) + chars
    for char in chars:
        """
        反转颜色
        """
        char = 255 - char
        cv2.imwrite("tmp\\split\\" + str(charCount) + ".jpg", char)
        charCount += 1
    endTime = time.process_time()
    print("分割执行时间:\t{}s".format(endTime - startTime))


if __name__ == "__main__":
    for root, dirs, files in os.walk("tmp\\origin\\"):
        for file in files:
            splitImg("tmp\\origin\\" + file)