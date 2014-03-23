#!/usr/bin python

from digits import digits as ocr
from os.path import basename
import glob
import numpy as np
import cv2

SZ = 20 # size of each digit is SZ x SZ
        
np.set_printoptions(threshold='nan')
def load_train_digits():
    cells = []
    labels = []
    for file in glob.glob('./train/learn/*.png'):
        img = cv2.imread(file, 0)
        h, w = img.shape[:2] 
        c = [np.hsplit(img, w//SZ)]
        c = np.array(c)
        cells.extend(c.reshape(-1, SZ, SZ))
        labels.extend(get_labels_for_filename(file))
    return cells, np.array(labels)

def get_labels_for_filename(fn):
    """ dostring"""
    s = basename(fn)[:-4]
    return np.array([int(x) for x in s])


def split2d(img, cell_size, flatten=True):
    h, w = img.shape[:2] 
    sx, sy = cell_size
    cells = [np.hsplit(row, w//sx) for row in np.vsplit(img, h//sy)]
    cells = np.array(cells)
    if flatten:
        cells = cells.reshape(-1, sy, sx)
    return cells

if __name__ == '__main__':
    digits, labels = load_train_digits()
    samples = ocr.preprocess_hog(digits)
    model = ocr.SVM()
    model.train(samples, labels)
    model.save('../src/digits/own_digits_svm.dat')