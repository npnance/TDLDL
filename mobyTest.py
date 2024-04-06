import sys
import os
import io
import random
import time
import math
import datetime
import traceback
import uuid
import colorsys
import shelve
import logging

import multiprocessing
import queue

from collections import OrderedDict
from operator import itemgetter

from PIL import Image, ImageDraw, ImageFont, ImageFilter #, ImageEnhance
from PIL import ImageOps, ImageChops
from PIL.ImageColor import getrgb

import numpy as np, numpy.random

from io import StringIO, BytesIO

wordListsPath = "/mnt/u/code/pytwit/wordlists/"

wordsMoby = dict()
def getRandomWord_Moby(typeind=""):
##    Noun                            N
##    Plural                          p
##    Noun Phrase                     h
##    Verb (usu participle)           V
##    Verb (transitive)               t
##    Verb (intransitive)             i
##    Adjective                       A
##    Adverb                          v
##    Conjunction                     C
##    Preposition                     P
##    Interjection                    !
##    Pronoun                         r
##    Definite Article                D
##    Indefinite Article              I
##    Nominative                      o

    global rootLogger

    rootLogger.debug("getRandomWord_Moby typeind: " + typeind)
    
    mobyfilepath = wordListsPath + 'mobyposi/mobylf.i'
    global wordsMoby

    if not wordsMoby:
        #with open(mobyfilepath, "rb") as f:
        with open(mobyfilepath, encoding = "cp437") as f:

            for line in f:
                word, typ = line.strip().split("╫")

                for key in typ:
                    if key not in wordsMoby:
                        wordsMoby[key] = []

                    thislist = wordsMoby[key]
                    thislist.append(word)

    random.seed()

    choice = ""
    
    if typeind != "":
        if typeind in wordsMoby:
            thislist = wordsMoby[typeind]

            choice = random.choice(thislist)
    else:
        allkeys = list(wordsMoby.keys())
        keychoice = random.choice(allkeys)

        thislist = wordsMoby[keychoice]

        choice = random.choice(thislist)

    choice = checkWordEncoding(choice)

    rootLogger.debug("getRandomWord_Moby complete: " + choice)

    return choice

def checkWordEncoding(word):
    try:
        word = word.decode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        pass

    return word

rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
rootLogger.addHandler(handler)

getRandomWord_Moby()

getRandomWord_Moby("h")
getRandomWord_Moby("V")
getRandomWord_Moby("!")

print(wordsMoby.keys())