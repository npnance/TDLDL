# -*- coding: utf-8 -*-
from __future__ import with_statement

import sys
import cgi
import os
import random
import math
import datetime
import uuid

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from PIL import ImageOps, ImageChops
from PIL.ImageColor import getrgb

from flask import Flask, request, send_file, send_from_directory
app = Flask(__name__)

#------------------------------------- Supporting functions

def getFileDimensions(inputPath):
    wts = Image.open(inputPath) 
    wts.load()
    height = wts.size[1]
    width = wts.size[0]
    
    return (width, height)

def safetyCheck(*args):
    lst = ()
    if len(args) == 3:
        lst = (args[0], args[1], args[2])
    elif len(args) == 4:
        lst = (args[0], args[1], args[2], args[3])
    elif len(args) == 1:
        lst = args[0]
    else:
        raise TypeError('Either parameter 1 should be a color tuple, or 3 or 4 parameters (r,g,b,a optional) are expected.')
    
    for iSC in range(len(lst)):
        if lst[iSC] < 0:
            lst = replace_at_index(lst, iSC, 0)
        elif lst[iSC] > 255:
            lst = replace_at_index(lst, iSC, lst[iSC] % 255)

    return lst

def safetyCheck_LeaveAtMax(*args):
    lst = ()
    if len(args) == 3:
        lst = (args[0], args[1], args[2])
    elif len(args) == 4:
        lst = (args[0], args[1], args[2], args[3])
    elif len(args) == 1:
        lst = args[0]
    else:
        raise TypeError('Either parameter 1 should be a color tuple, or 3 or 4 parameters (r,g,b,a optional) are expected.')
    
    for iSC in range(len(lst)):
        if lst[iSC] < 0:
            lst = replace_at_index(lst, iSC, 0)
        elif lst[iSC] > 255:
            lst = replace_at_index(lst, iSC, 255)

    return lst

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def lum(r,g,b,a=0):
    return math.sqrt( .241 * r + .691 * g + .068 * b )

def myhsv_to_rgb(hsv):
    p = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
    p = (int(p[0] * 255.0), int(p[1] * 255.0), int(p[2] * 255.0))

    return p
        
def sort_by_lum(choices):
    choices.sort(key=lambda rgb: lum(*rgb))

    return choices

def getInverse(c):
    inverse = (255-c[0],255-c[1],255-c[2])
    return inverse
    
def resizeToMinMax(img, maxW, maxH, minW, minH):
    if img.size[0] > maxW or img.size[1] > maxH or img.size[0] < minW or img.size[1] < minH:
        (w, h) = getSizeByMinMax(img.size[0], img.size[1], maxW, maxH, minW, minH)
        img = img.resize((int(w), int(h)), Image.ANTIALIAS)

    return img

def resizeToMax(img, maxW, maxH):
    if img.size[0] > maxW or img.size[1] > maxH:
        (w, h) = getSizeByMax(img.size[0], img.size[1], maxW, maxH)
        img = img.resize((int(w), int(h)), Image.ANTIALIAS)

    return img

def resizeToTarget(img, targetImg):    
    img = img.resize((targetImg.size[0], targetImg.size[1]), Image.ANTIALIAS)

    return img

def getSizeByMinMax(w, h, maxW, maxH, minW, minH):
    resizedW = w
    resizedH = h

    r = (h * 1.0) / w
    
    while resizedW > maxW or resizedH > maxH:
        resizedW -= 1.0
        resizedH = r * resizedW

    while resizedW < minW or resizedH < minH:
        resizedW += 1.0
        resizedH = r * resizedW

    return (resizedW, resizedH)

def getSizeByMax(w, h, maxW, maxH):
    # resize the image down to <= the original size
    
    resizedW = w
    resizedH = h

    r = (h * 1.0) / w
    
    while resizedW > maxW or resizedH > maxH:
        resizedW -= 1.0
        resizedH = r * resizedW

    return (resizedW, resizedH)

@app.route('/tdl')
def img():
    return root()

@app.route('/')
def root():
    return "<html><body>hello world</body></html>"

if __name__ == "__main__":
    app.run(debug=True)