## 汉语古籍OCR第一次记录——提取pdf图片

### 提取pdf图片

#### 使用fitz

安装包方法

> pip install PyMuPDF

```python
def pdf2img(pdfPath, imgPath, zoomX, zoomY, rotationAngle):
    startTime = time.process_time()
    pdf = fitz.open(pdfPath)
    len = pdf.pageCount
    for pg in range(1, len):
        print("page:{}".format(pg))
        page = pdf[pg]
        trans = fitz.Matrix(zoomX, zoomY).preRotate(rotationAngle)
        pm = page.getPixmap(matrix=trans, alpha=False)
        pm.writePNG(imgPath + "img{}.png".format(pg))
    endTime = time.process_time()
    print("fitz执行时间:\t{}s".format(endTime - startTime))
```

执行提取66张pdf图片，所花时间很长

<img src="\img\1\fitz_time.png" alt="fitz_time" style="zoom:50%;" />

平均13.6s一张

![fitz_img](\img\1\fitz_img.png)

**其中有黑色的是电脑显示错误，实际图片显示正常**

提取得到的图片66张共1.96GB，平均30MB一张图片，图片属性如下

<img src="\img\1\fitz_detail.png" alt="fitz_detail" style="zoom:50%;" />

#### 使用PyPDF

安装包方法

> pip install pypdf4

```python
def pdf2img2(pdfPath, imgPath):
    startTime = time.process_time()

    pdf = PyPDF4.PdfFileReader(open(pdfPath, 'rb'))
    len = pdf.numPages
    imgCount = 0
    for pg in range(len):
        print("page:{}".format(pg))
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
```

当使用PyPDF2库

会出现`NotImplementedError: unsupported filter /DCTDecode`的报错

**解决方法：卸载PyPDF2库，使用更新后的PyPDF4库**

> pip uninstall pypdf2
>
> pip install pypdf4

同样也是执行提取66张pdf图片，解决问题后执行时间相比fitz是他的4427分之一

<img src="\img\1\pypdf_time.png" alt="pypdf_time" style="zoom:50%;" />

显然PyPDF提取图片在速度上更优

![pypdf_img](\img\1\pypdf_img.png)

但是他读取的都是jpg格式的图片

66张图片共32.6MB，平均一张500KB

<img src="\img\1\pypdf_detail.png" alt="pypdf_detail" style="zoom:50%;" />

可以看到在图片像素上相比fitz差了不少，但是我认为这些像素够用了

因此最后选用PyPDF4