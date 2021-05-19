# -*- coding: utf-8 -*-
from PCV.tools import imtools, pca
from PIL import Image, ImageDraw
from pylab import *
from scipy.cluster.vq import *

imlist = imtools.get_imlist('tmp/test/')
imnbr = len(imlist)

# Load images, run PCA.
immatrix = array([array(Image.open(im)).flatten() for im in imlist], 'f')
V, S, immean = pca.pca(immatrix)

projected = array([dot(V[[0, 1]], immatrix[i] - immean) for i in range(imnbr)])

n = len(projected)
# compute distance matrix
S = array([[sqrt(sum((projected[i] - projected[j]) ** 2))
            for i in range(n)] for j in range(n)], 'f')
# create Laplacian matrix
rowsum = sum(S, axis=0)
D = diag(1 / sqrt(rowsum))
I = identity(n)
L = I - dot(D, dot(S, D))
# compute eigenvectors of L
U, sigma, V = linalg.svd(L)
k = 20
# create feature vector from k first eigenvectors
# by stacking eigenvectors as columns
features = array(V[:k]).T
# k-means
features = whiten(features)
centroids, distortion = kmeans(features, k)
code, distance = vq(features, centroids)
# plot clusters
for c in range(k):
    ind = where(code == c)[0]
    figure()
    gray()
    for i in range(minimum(len(ind), 39)):
        im = Image.open(imlist[ind[i]])
        subplot(4, 10, i + 1)
        imshow(array(im))
        axis('equal')
        axis('off')
    savefig("tmp/cluster/{}.jpg".format(c))
