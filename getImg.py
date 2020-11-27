import fitz
import time
import PyPDF4
from PIL import Image
import os


def pdf2img2(pdfPath, imgPath, zoomX, zoomY, rotationAngle):
    startTime = time.process_time()
    pdf = fitz.open(pdfPath)
    len = pdf.pageCount
    for pg in range(len):
        #print("page:{}".format(pg))
        page = pdf[pg]
        trans = fitz.Matrix(zoomX, zoomY).preRotate(rotationAngle)
        pm = page.getPixmap(matrix=trans, alpha=False)
        pm.writePNG(imgPath + "img{}.png".format(pg))
    endTime = time.process_time()
    print("fitz执行时间:\t{}s".format(endTime - startTime))

def pdf2img(pdfPath, imgPath):
    startTime = time.process_time()

    pdf = PyPDF4.PdfFileReader(open(pdfPath, 'rb'))
    len = pdf.numPages
    imgCount = 0
    for pg in range(len):
        #print("page:{}".format(pg))
        page = pdf.getPage(pg)
        xObject = page['/Resources']['/XObject'].getObject()
        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                imgCount += 1
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                data = xObject[obj].getData()
                if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                    mode = "RGB"
                else:
                    mode = "P"
                if '/Filter' in xObject[obj]:
                    filter = xObject[obj]['/Filter']
                    if not os.path.exists(imgPath):
                        os.mkdir(imgPath)
                    if filter == '/FlateDecode':
                        img = Image.frombytes(mode, size, data)
                        img.save(imgPath + "img{}.png".format(imgCount))
                    elif filter == '/DCTDecode':
                        img = open(imgPath + "img{}.jpg".format(imgCount), "wb")
                        img.write(data)
                        img.close()
                    elif filter == '/JPXDecode':
                        img = open(imgPath + "img{}.jp2".format(imgCount), "wb")
                        img.write(data)
                        img.close()
                    elif filter == '/CCITTFaxDecode':
                        img = open(imgPath + "img{}.tiff".format(imgCount), "wb")
                        img.write(data)
                        img.close()
                else:
                    img = Image.frombytes(mode, size, data)
                    img.save(imgPath + "img{}.png".format(imgCount))

    endTime = time.process_time()
    print("PyPDF执行时间:\t{}s".format(endTime - startTime))

if __name__ == "__main__":
	if not os.path.exists("\\img"):
		os.mkdir("\\img")
	if not os.path.exists("\\img\\pypdf2"):
		os.mkdir("\\img\\pypdf2")
    #pdf2img2("pdf\\bunko.pdf", "img\\fitz\\bunko", 5, 5, 0)
    pdf2img("pdf\\bunko.pdf", "img\\pypdf2\\bunko\\")
    pdf2img("pdf\\ha.pdf", "img\\pypdf2\\ha\\")
