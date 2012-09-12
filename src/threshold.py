#!/usr/bin/env python

import os
import sys

import numpy
import cv2

def make_mask(ifile):
    img = cv2.imread(ifile)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 1)
    dil = cv2.dilate(thresh, None, iterations=5)

    #cv2.imwrite('out.png', dil)

    return dil


def threshold_file(ifile, outfile):
    img = cv2.imread(ifile)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(gray, 255, 1, 0, 107, 1)
    
    er = cv2.erode(thresh, None, iterations=1)

    mask = make_mask(file)

    final = cv2.bitwise_and(er, er, mask=mask)
    
    cv2.imwrite(outfile, final)



def process(input_filename, output_filename):
    threshold_file(input_filename, output_filename)
