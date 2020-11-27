import cv2
import numpy as np

def Binarization(imgPath):
    img = cv2.imread(imgPath)
    grayedImg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    h, w = grayedImg.shape[:2]
    m = np.reshape(grayedImg, [1, h*w])
    mean = m.sum() / (h*w)
    retval, dst = cv2.threshold(grayedImg, mean, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    binarizedImg = np.array(dst)
    """
    降噪与腐蚀
    """
    binarizedImg = cv2.blur(binarizedImg, (5, 5))
    # binarizedImg = cv2.dilate(binarizedImg, None)
    # cv2.imshow('img', binarizedImg)
    # cv2.waitKey()
    return binarizedImg

if __name__ == "__main__":
    img = Binarization("img\\pdf2img\\img1.png")
    cv2.imwrite("img\\binarize\\img1.png", img)
    # cv2.imshow('img', img)
    # cv2.waitKey()