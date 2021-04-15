# # -*- coding: utf-8 -*-
# from PCV.tools import imtools
# import pickle
# from scipy import *
# from pylab import *
# from PIL import Image
# from scipy.cluster.vq import *
# from PCV.tools import pca
#
# # Uses sparse pca codepath.
# imlist = imtools.get_imlist('tmp/data/selectedfontimages/a_selected_thumbs/')
#
# # 获取图像列表和他们的尺寸
# im = array(Image.open(imlist[0]))  # open one image to get the size
# m, n = im.shape[:2]  # get the size of the images
# imnbr = len(imlist)  # get the number of images
# print("The number of images is %d" % imnbr)
#
# # Create matrix to store all flattened images
# immatrix = array([array(Image.open(imname)).flatten() for imname in imlist], 'f')
#
# # PCA降维
# V, S, immean = pca.pca(immatrix)
#
# # 保存均值和主成分
# f = open('tmp/data/selectedfontimages/a_pca_modes.pkl', 'wb')
# pickle.dump(immean, f)
# pickle.dump(V, f)
# f.close()
#
# # get list of images
# imlist = imtools.get_imlist('tmp/data/selectedfontimages/a_selected_thumbs/')
# imnbr = len(imlist)
#
# # load model file
# with open('tmp/data/selectedfontimages/a_pca_modes.pkl', 'rb') as f:
#     immean = pickle.load(f)
#     V = pickle.load(f)
# # create matrix to store all flattened images
# immatrix = array([array(Image.open(im)).flatten() for im in imlist], 'f')
#
# # project on the 40 first PCs
# immean = immean.flatten()
# projected = array([dot(V[:40], immatrix[i] - immean) for i in range(imnbr)])
#
# # k-means
# projected = whiten(projected)
# centroids, distortion = kmeans(projected, 4)
# code, distance = vq(projected, centroids)
#
# # plot clusters
# for k in range(4):
#     ind = where(code == k)[0]
#     figure()
#     gray()
#     for i in range(minimum(len(ind), 40)):
#         subplot(4, 10, i + 1)
#         imshow(immatrix[ind[i]].reshape((25, 25)))
#         axis('off')
# show()

#---------------------------------------------------------------------

# -*- coding: utf-8 -*-
from PCV.tools import imtools, pca
from PIL import Image, ImageDraw
from pylab import *
from PCV.clustering import hcluster

imlist = imtools.get_imlist('tmp/test/')
imnbr = len(imlist)

# Load images, run PCA.
immatrix = array([array(Image.open(im)).flatten() for im in imlist], 'f')
V, S, immean = pca.pca(immatrix)

# Project on 2 PCs.
projected = array([dot(V[[0, 1]], immatrix[i] - immean) for i in range(imnbr)])  # P131 Fig6-3左图
# projected = array([dot(V[[1, 2]], immatrix[i] - immean) for i in range(imnbr)])  # P131 Fig6-3右图

# height and width
h, w = 1200, 1200

# create a new image with a white background
img = Image.new('RGB', (w, h), (255, 255, 255))
draw = ImageDraw.Draw(img)

# draw axis
draw.line((0, h / 2, w, h / 2), fill=(255, 0, 0))
draw.line((w / 2, 0, w / 2, h), fill=(255, 0, 0))

# scale coordinates to fit
scale = abs(projected).max(0)
scaled = floor(array([(p / scale) * (w / 2 - 20, h / 2 - 20) + (w / 2, h / 2)
                      for p in projected])).astype(int)

# paste thumbnail of each image
for i in range(imnbr):
    nodeim = Image.open(imlist[i])
    nodeim.thumbnail((25, 25))
    ns = nodeim.size
    box = (scaled[i][0] - ns[0] // 2, scaled[i][1] - ns[1] // 2,
           scaled[i][0] + ns[0] // 2 + 1, scaled[i][1] + ns[1] // 2 + 1)
    img.paste(nodeim, box)

tree = hcluster.hcluster(projected)
hcluster.draw_dendrogram(tree, imlist, filename='fonts.png')

figure()
imshow(img)
axis('off')
img.save('tmp/data/selectedfontimages/pca_font.png')
show()

#--------------------------------------------------------------------------------
#
# # -*- coding: utf-8 -*-
# from PCV.tools import imtools, pca
# from PIL import Image, ImageDraw
# from pylab import *
# from scipy.cluster.vq import *
#
# # imlist = imtools.get_imlist('tmp/data/selectedfontimages/a_selected_thumbs')
# imlist = imtools.get_imlist('tmp/test/')
# imnbr = len(imlist)
#
# # Load images, run PCA.
# immatrix = array([array(Image.open(im)).flatten() for im in imlist], 'f')
# V, S, immean = pca.pca(immatrix)
#
# # Project on 2 PCs.
# projected = array([dot(V[[0, 1]], immatrix[i] - immean) for i in range(imnbr)])  # P131 Fig6-3左图
# # projected = array([dot(V[[1, 2]], immatrix[i] - immean) for i in range(imnbr)])  # P131 Fig6-3右图
#
# n = len(projected)
# # compute distance matrix
# S = array([[sqrt(sum((projected[i] - projected[j]) ** 2))
#             for i in range(n)] for j in range(n)], 'f')
# # create Laplacian matrix
# rowsum = sum(S, axis=0)
# D = diag(1 / sqrt(rowsum))
# I = identity(n)
# L = I - dot(D, dot(S, D))
# # compute eigenvectors of L
# U, sigma, V = linalg.svd(L)
# k = 20
# # create feature vector from k first eigenvectors
# # by stacking eigenvectors as columns
# features = array(V[:k]).T
# # k-means
# features = whiten(features)
# centroids, distortion = kmeans(features, k)
# code, distance = vq(features, centroids)
# # plot clusters
# for c in range(k):
#     ind = where(code == c)[0]
#     figure()
#     gray()
#     for i in range(minimum(len(ind), 39)):
#         im = Image.open(imlist[ind[i]])
#         subplot(4, 10, i + 1)
#         imshow(array(im))
#         axis('equal')
#         axis('off')
# show()