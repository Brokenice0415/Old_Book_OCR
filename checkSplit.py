import os
import cv2

def checkSplit(splitPath):
    count = 0
    isValid = 0
    for root, dirs, files in os.walk(splitPath):
        for file in files:
            img = cv2.imread(root + '\\' + file)
            h, w = img.shape[:2]
            if h < 110 and w < 110:
                isValid += 1
            count += 1
    return isValid, count, isValid / count

if __name__ == "__main__" :
    isValid, count, checkResult = checkSplit("img\\split\\bunko\\")
    print("有效{}个\t总共{}个\t正确率{:.2f}%".format(isValid, count, checkResult*100))