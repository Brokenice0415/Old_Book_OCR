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
获得起止范围
"""


def getRange(shadows, mean, isGT):
    t = 0
    start, end = -1, -1
    Range = []
    if isGT:
        for i in shadows:
            if i > mean:
                if (start >= 0) and (end == -1):
                    end = t
                    Range.append([start, end])
                    start = -1
                    end = -1
            else:
                if start == -1:
                    start = t
            t += 1
    else:
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
判断是否是白块
"""
def isSpace(img):
    ptSum = 0
    h, w = img.shape[:2]
    for row in img:
        ptSum += sum(row)
    """
    空白数大于90%
    """
    if ptSum < h*w*25:
        return True
    return False

"""
获得两页的文字部分
"""


def findCharPart(img):
    charParts = []
    rowShadows = getShadow(img, 'x')
    colShadows = getShadow(img, 'y')
    rowMean = sum(rowShadows) / len(rowShadows)
    rowMean = (rowMean + max(rowShadows)) / 2
    colMean = sum(colShadows) / len(colShadows)
    """
    获得截取部分的起始位置
    """
    rowsRange = getRange(rowShadows, rowMean, True)
    colsRange = getRange(colShadows, colMean, True)

    maxRowWidth = 0
    maxColWidth = 0
    for rowRange in rowsRange:
        maxRowWidth = max(maxRowWidth, rowRange[1] - rowRange[0])

    for colRange in colsRange:
        maxColWidth = max(maxColWidth, colRange[1] - colRange[0])

    for colRange in colsRange:
        if maxColWidth / (colRange[1] - colRange[0]) < 2:
            for rowRange in rowsRange:
                if maxRowWidth / (rowRange[1] - rowRange[0]) < 2:
                    timg = img[rowRange[0]:rowRange[1], colRange[0]:colRange[1]]
                    # cv2.namedWindow('img', cv2.WINDOW_AUTOSIZE)
                    # cv2.imshow('img', timg)
                    # cv2.waitKey()
                    charParts.append(timg)

    return charParts


"""
获得文字部分的文字
若需截取文字部分则也是该函数
"""


def findChars(img):
    chars = []
    rowShadows = getShadow(img, 'x')
    colShadows = getShadow(img, 'y')
    rowMean = sum(rowShadows) / len(rowShadows)
    rowMean = (rowMean + min(rowShadows)) / 2
    colMean = sum(colShadows) / len(colShadows)
    colMean = (colMean + min(colShadows)) / 2
    """
    获得截取部分的起始位置
    """
    rowsRange = getRange(rowShadows, rowMean, False)
    colsRange = getRange(colShadows, colMean, False)

    maxColWidth = 0
    meanColWidth = 0

    for colRange in colsRange:
        maxColWidth = max(maxColWidth, colRange[1] - colRange[0])
        meanColWidth += colRange[1] - colRange[0]
    meanColWidth /= len(colsRange)

    for colRange in colsRange:
        if maxColWidth / (colRange[1] - colRange[0]) < 2:
            charCol = []
            for rowRange in rowsRange:
                if meanColWidth / (rowRange[1] - rowRange[0]) < 1.5:
                    timg = img[rowRange[0]:rowRange[1], colRange[0]:colRange[1]]
                    # cv2.namedWindow('img', cv2.WINDOW_AUTOSIZE)
                    # cv2.imshow('img', timg)
                    # cv2.waitKey()
                    if not isSpace(timg):
                        charCol.append(timg)

            chars = charCol + chars

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
    charParts = findCharPart(img)
    chars = []
    charCount = 0
    """
    从右往左
    """
    for charPart in charParts:
        chars = findChars(charPart) + chars
    for char in chars:
        """
        反转颜色
        """
        char = 255 - char
        saveFilePath = "img\\split\\" + fileName
        saveImgPath = saveFilePath + "\\" + imgName
        if not os.path.exists(saveFilePath):
            os.mkdir(saveFilePath)
        if not os.path.exists(saveImgPath):
            os.mkdir(saveImgPath)
        cv2.imwrite(saveImgPath + "\\img" + str(charCount) + ".png", char)
        charCount += 1
    endTime = time.process_time()
    print("分割执行时间:\t{}s".format(endTime - startTime))


if __name__ == "__main__":
    for root, dirs, files in os.walk("img\\pypdf2\\bunko\\"):
        for file in files:
            splitImg("img\\pypdf2\\bunko\\" + file)