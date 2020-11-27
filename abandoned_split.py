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
获得两页的文字部分
"""
def findCharPart(img):
    charParts = []
    shadows = getShadow(img, 'y')
    l = len(shadows)
    mean = sum(shadows)/l
    """
    获得截取部分的起始位置
    """
    charPartsRange = getRange(shadows, mean, True)

    maxWidth = 0
    for charPartRange in charPartsRange:
        maxWidth = max(maxWidth, charPartRange[1]-charPartRange[0])

    for charPartRange in charPartsRange:
        if maxWidth / (charPartRange[1]-charPartRange[0]) < 2:
            timg = img[:,charPartRange[0]:charPartRange[1]]
            # cv2.imshow('img', timg)
            # cv2.waitKey()
            charParts.append(timg)

    return charParts

"""
获得文字部分的文字列
"""
def findCharCols(img):
    charCols = []
    shadows = getShadow(img, 'y')
    l = len(shadows)
    mean = sum(shadows)/l
    minShadow = min(shadows)
    mean = (mean + minShadow) / 2
    """
    获得截取部分的起始位置
    """
    charColsRange = getRange(shadows, mean, False)

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
    h, w = img.shape[:2]
    shadows = getShadow(img, 'x')
    l = len(shadows)
    mean = sum(shadows)/l
    minShadow = min(shadows)
    mean = (mean+minShadow)/2

    """
    获取文字的起始位置
    """
    charsRange = getRange(shadows, mean, False)

    """
    利用方块字特性，当切割字长小于字宽时，限定字宽等于字长
    会导致出现重复分割的部分
    在聚类中排除
    
    [2:-1]表示去除上下的黑边
    """
    for charRange in charsRange[1:-1]:
        if w > charRange[1]-charRange[0]:
            if charRange[0] + w > h:
                timg = img[charRange[0]:h, :]
            else:
                timg = img[charRange[0]:charRange[0]+w, :]
        else:
            timg = img[charRange[0]:charRange[1], :]

        # cv2.imshow('image', timg)
        # cv2.waitKey()
        chars.append(timg)

    return chars

"""
分割函数主体封装
imgPath : 图片存储目录
"""
def splitImg_abandoned(imgPath):
    fileName = imgPath.split('\\')[-2]
    imgName = imgPath.split('\\')[-1]
    imgName = imgName[:imgName.find('.')]

    print(fileName + ":\t" + imgName + "开始分割...")

    startTime = time.process_time()
    img = Binarization(imgPath)
    charParts = findCharPart(img)
    charCols = []
    chars = []
    charCount = 0
    """
    从右往左
    """
    for charPart in charParts:
        charCols += findCharCols(charPart)
    for charCol in charCols:
        chars = findChars(charCol) + chars
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
    for root, dirs, files in os.walk("img\\pypdf2\\ha\\"):
        for file in files:
            splitImg("img\\pypdf2\\ha\\" + file)