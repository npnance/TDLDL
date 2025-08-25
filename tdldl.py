# -*- coding: utf-8 -*-

from multiprocessing.managers import DictProxy
import base64
import colorsys
import configparser
import datetime
import hashlib
import json
import logging
import math
import multiprocessing
from numba import jit, njit
import os
import queue
import random
import re
import shelve
import string
import sys
import time
import traceback
import uuid

from collections import OrderedDict
from operator import itemgetter

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageSequence, ImageOps, ImageChops, ExifTags
from PIL.ImageColor import getrgb
import PIL.GifImagePlugin as pilGif

import numpy as np, numpy.random
import emoji

from flask import Flask, jsonify, request, send_file, send_from_directory, render_template
from werkzeug.routing import BaseConverter
from io import BytesIO

from tdlColorPrint import ColorPrint
from tdlState import TdlState
from tdlState import TdlValues

#from werkzeug.middleware.profiler import ProfilerMiddleware

app = Flask(__name__)
#app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[50], profile_dir='/home/nn/flaskdev/_profiled/')

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

# path params. change as needed --------------------------- @~-------

fontPath = "/mnt/c/windows/fonts/"
fontNameMono = "Cour.ttf"
fontNameSansSerif = "Verdana.ttf"
fontNameImpact = "Impact.ttf"
fontNameWordGrid = "track.ttf"
fontNameWordReg = "AlteHaasGroteskBold.ttf"
fontNameArcade = "ARCADEPI.TTF"

fontPathSansSerif = fontPath + fontNameSansSerif

publicDomainImagePath = "/mnt/u/code/python/commons/download/"

# insert paths. remove what you don't have and add your image insert directories here
allPaths = [
    "/mnt/u/code/python/commons/download/",
    "/mnt/u/code/python/commons/download1/",
    "./sourceimages/special/",
    r"/mnt/u/My Webs/tooinside/universemdwiki/_private/",
    "./sourceimages/style/",
    "./sourceimages/orangeblocks/",
    "/mnt/t/Pictures/tweeter/",
    "/mnt/t/Pictures/sa archive/",
    "/mnt/t/Pictures/sa/",
    "/mnt/t/Pictures/sa2/",
    "/mnt/t/Pictures/sa3/",
    "/mnt/t/Pictures/",
    "/mnt/u/code/python/commons/tiffsOnly/",
    "/mnt/t/Pictures/From Lumia920White/Camera roll/",
    "/mnt/t/Pictures/From_iPhone6/",
    "./imagesExported/",
    "/mnt/t/Pictures/stupidshit/",
    "/mnt/t/Pictures/stupidshit/no/"
]

ollamaHost = 'http://192.168.1.30:11434'

wordListsPath = "/mnt/u/code/pytwit/wordlists/"
mobyfilepath = wordListsPath + 'mobyposi/mobylf.i' # path to Moby Project files: https://en.wikipedia.org/wiki/Moby_Project . check the References section for a download site

palettesPath = "./sourceimages/palettes"
stampPath = "./sourceimages/stamps"

shelfFileName = "tdlshelf.log"
pathFunctionDoc = "./tdldl.json"
pathTelemetry = "./tdldl_stats.json"
pathOperations = "./logOperations/"
pathSourceImages = "./sourceimages/"
pathLabelSquares = "./sourceimages/gsp_1inch_squares.png"

pathBootstrapCSS = """<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">"""
pathBootstrapJS = """<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js" integrity="sha384-QJHtvGhmr9XOIpI6YVutG+2QOK9T+ZnN4kzFN1RtK3zEFEIsxhlmWl5/YESvpZ13" crossorigin="anonymous"></script>"""

pathWebFonts = """<link href="https://fonts.googleapis.com/css?family=Bungee" rel="stylesheet"> 
    <link href="https://fonts.googleapis.com/css?family=Amiko" rel="stylesheet">"""

defaultInsertExtensions = ('.jpg','.gif','.png','.tif')

def getCurrentStandardWidth():
    return 1024

def getCurrentStandardHeight():
    return 1024

timeOutDefault = 30

# ---------- logging params ---------------------------

rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
rootLogger.addHandler(handler)

pilLogger = logging.getLogger("PIL")
pilLogger.setLevel(logging.WARNING)

print (f'PIL Logger level set to: {pilLogger.level}')

numba_logger = logging.getLogger('numba')
numba_logger.setLevel(logging.WARNING)

colorPrint = ColorPrint(rootLogger)

def colorEsc(x):
    return f'\x1b[38;5;{x}m'

def colorBg(x):
    return f'\x1b[{x}m'

def random_standard_emoji():
    """
    Return a random standard emoji (single glyph, no skin tone or flag variations).
    """
    all_emojis = list(emoji.EMOJI_DATA.keys())

    # Filter out flags (many are 2-character sequences) and skin tone variants
    filtered = [
        e for e in all_emojis
        if len(e) == 1 and "skin tone" not in emoji.EMOJI_DATA[e]["en"]
    ]

    return random.choice(filtered)

this_runs_emoji = random_standard_emoji()

# here be dragons
colorPrint.print_custom_palette(147, f"--{colorEsc(148)}--{colorEsc(155)}-{colorEsc(160)}-{colorEsc(170)}-{colorEsc(190)}-{colorEsc(194)}-> {colorEsc(196)}h{colorEsc(198)}e{colorEsc(200)}r{colorEsc(202)}e {colorEsc(204)}b{colorEsc(206)}e {colorEsc(207)}d{colorEsc(208)}r{colorEsc(209)}a{colorEsc(210)}g{colorEsc(211)}o{colorEsc(212)}n{colorEsc(208)}s {colorEsc(148)}---{colorEsc(112)} GROWL 🐲🔥 {colorEsc(148)}-{colorEsc(149)}-{colorEsc(159)}-{colorEsc(147)}-> {this_runs_emoji} MODE {colorEsc(142)}-->")

#----------- font blacklist. will not be chosen -------

fontBlacklist = ["LilyPond",
                 "marlett",
                 "segmdl2",
                 "Swkeys1",
                 "SWMacro",
                 "symbol",
                 "teamviewer",
                 "webdings", # looks bad todd
                 "wingding",
                 "CoolS-Regular",
                 "Hollywood Capital Hills",
                 "Hollywood Capital",
                 "Embossed Germanica",
                 "Fluted Germanica",
                 "Shadowed Germanica",
                 "Plain Germanica",
                 "holomdl2",
                 "REFSPCL",
                 "VISITOR",
                 "BNJDigital",
                 "WINGDNG2", # Wing Dongs
                 "WINGDNG3",
                 "romantic",
                 "mtextra",
                 "OUTLOOK",
                 "HARLOWSI",
                 "PARCHM",
                 "Gottlieb"
                 ]

#----------- color, palette and iAlg definitions. best not to change. --------

cocoColors = ["00FF00", "0000FF", "FFFFFF", "FF00FF", "FFFF00", "FF0000", "00FFFF", "FF8000", "000000"]
atariColors = ["000000","404040","6C6C6C","909090","B0B0B0","C8C8C8","DCDCDC","ECECEC","444400","646410","848424","A0A034","B8B840","D0D050","E8E85C","FCFC68","702800","844414","985C28","AC783C","BC8C4C","CCA05C","DCB468","ECC878","841800","983418","AC5030","C06848","D0805C","E09470","ECA880","FCBC94","880000","9C2020","B03C3C","C05858","D07070","E08888","ECA0A0","FCB4B4","78005C","8C2074","A03C88","B0589C","C070B0","D084C0","DC9CD0","ECB0E0","480078","602090","783CA4","8C58B8","A070CC","B484DC","C49CEC","D4B0FC","140084","302098","4C3CAC","6858C0","7C70D0","9488E0","A8A0EC","BCB4FC","000088","1C209C","3840B0","505CC0","6874D0","7C8CE0","90A4EC","A4B8FC","00187C","1C3890","3854A8","5070BC","6888CC","7C9CDC","90B4EC","A4C8FC","002C5C","1C4C78","386890","5084AC","689CC0","7CB4D4","90CCE8","A4E0FC","003C2C","1C5C48","387C64","509C80","68B494","7CD0AC","90E4C0","A4FCD4","003C00","205C20","407C40","5C9C5C","74B474","8CD08C","A4E4A4","B8FCB8","143800","345C1C","507C38","6C9850","84B468","9CCC7C","B4E490","C8FCA4","2C3000","4C501C","687034","848C4C","9CA864","B4C078","CCD488","E0EC9C","442800","644818","846830","A08444","B89C58","D0B46C","E8CC7C","FCE08C"]

primaryColors = [(255,0,0), (0,255,0), (0,0,255)]

wackyColors = [(255,255,0),
               (0,255,0),
               (255,0,255)]

randoFillList = [18, 19, 20, 21, 24, 26, 33, 34, 36, 37, 38, 39, 42, 43, 44, 45, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 68, 69, 70, 73, 74, 77, 79, 82, 84, 85, 86, 88, 90, 91, 92, 93]

iAlgNames = [
    "none",
    "random", 
    "the tipping point", 
    "night random",
    "dark noise", 
    "bar grid",
    "EGA noise",
    "long bars",
    "the color of a tv tuned to a dead channel",
    "green noise",
    "bar john",
    "diamond hatch",
    "wacky noise", 
    "T_H_E__S_H_U_F_F_L_E_R", 
    "lil bars", 
    "FLANNEL GRID", 
    "ever changing", 
    "soldiers", 
    "child soldiers", 
    "horizontal bars",
    "small flannel", 
    "vertical bars", 
    "D E A D N I G H T S K Y", 
    "D E A D N I G H T G R O U N D", 
    "F U Z Z Y _ F L A N N E L", ""
    "T I M E _ L I M I T", 
    "8 0 S  T R I P", 
    "D_E_A_D__M_A_L_L__H_A_U_N_T_I_N_G", 
    "BIG ___ GRID", 
    "8 bit sq outline",
    "P_I_G__G_R_I_D", 
    "M_E_L_T_I_N_G__P_O_T", 
    "SOUTHEAST CRUMBO", 
    "TODDLER SOLDIERS", 
    "U_N_I_F_O_R_M", "S_L_O_W__C_H_A_N_G_E_S", "B_A_R__S_C_R_E_W", 
    "AND MOD", 
    "OR MOD", 
    "EXP MOD",
    "MODDLEDEE/MODDLEDUM", 
    "mark at the boon", 
    "HIGH INDIAN", 
    "MUSHROOM EXPRESS", 
    "LUIGI IN THE SKY WITH DIAMONDS", 
    "KNEE FOLDER BURIED IN THE TUNDRA", 
    "ARC EXPLOSION", 
    "SATURN'S BIRTHDAY", 
    "CIRCLE 8", 
    "4D FLANNEL",
    "PUSH WALLPAPER", 
    "CRAYON NUKE", 
    "THE SMELL OF BLUEBERRY MARKERS", 
    "HEROIN FROM TOPANGA", 
    "RESOGROVE FINISH", 
    "NATIVE BLANKET",
    "TRY BALL MEAT", 
    "TURN THE KNOB", 
    "X MARKS THE X", 
    "JUTTING URANUS",
    "TINY DECO", 
    "ONCE I SHOT GOD ON BROADWAY", 
    "YEAH", 
    "ARKY BARKY", 
    "DIRTY CARPET", 
    "UNIQUE VAN FIBER", 
    "?_??_???_????_?????", 
    "PLAYING THE STAR", 
    "THE FEELINGS NEVER TOLD", 
    "Nice.",
    "EL DITHERO", 
    "CUBE 5: THE FINAL CUBING", 
    "HOW COULD IT ALL FALL ONE DAY", 
    "SHE NEVER NOTICED", 
    "AEROPLANE IN THE SEA WITH DARKNESS", 
    "BIG SQUARE PUSSY", 
    "SCOOL FENCE", 
    "the echo of silence reverberates off the walls of my being but no one can hear it out there it's sad and dark and lonely in your casket when there are no nail marks on the inside and two miles of dirt above i lived on a pile of rocks where i'll die after the final reckoning when the life drains from your body and the earth's, and the universe implodes", 
    "RIBBED SQUARES NO TOE", 
    "ALONE ON A FRIDAY NIGHT",
    "SWAPPER WHOPPER", 
    "DIGITAL OPULENCE", 
    "THAT PROBABLY LOOKS INSANE", 
    "GAME CRASH FOREST", 
    "15 DISCONTINUED SODAS", 
    "PLUTO TAILOR", 
    "DEMIURGE OVERKILL", 
    "idk yet", 
    "no men no bears no women",
    "binders full of women",
    "90",
    "i don't remember",
    "SEDUCING MEDUSAS",
    "84-2",
    "circle grid",
    "95",
    "96",
    "97",
    "98",
    "99",
    "100",
    "101",
    "102",
    "103",
    "PUDDLE KINK",
    "CIRCLE CIRCLES",
    "106",
    "107",
    "108",
    "109",
    "110",
    "111",
    "112",
    "113",
    "114",
    "115",
    "BADPERSON WHAMMY",
    "117",
    "ZIGZAG FEAST",
    "119"    
]

maxFloodFillArg = len(iAlgNames) - 1

# ---- okay, you can change fourColorPalettes. IF you promise to be careful.

fourColorPalettes = (('000000','ffffff','ff0000','00ff00','0000ff'),
                 ('082B2D','069498','73AC7F','C9FA9E','ffffff'),
                 ('ECD078','D95B43','C02942','542437','53777A'),
                 ('D9CEB2','948C75','D5DED9','7A6A53','99B2B7'),
                 ('951DF8','030105','CD1E1E','E48B19','E92581'),
                 ('4D454F','ffffff','FA1330','B3B5A7','2A1330'),
                 ('000000','D95B43','C02942','542437','2A1330'),
                 ('6feae6','f6a3ef','000000','eecd69','dd6dfb','50d8ec'),
                 ('951DF8','740b3c','620f0f','eb8500','cc7400','f9bed9'))

# --- safe funcs ---------------------------------------------

imageoplist = ["adaptive", "adaptive_dither", "adaptive_mediancut", "adaptive_quant", "fourit", "twoit", "invert", "hueshift", "edge", "contour", "detail", 
               "pixelate", "fourcolorTDL", "godcolor", "fourblend", "redit", "greenit", "blueit", "colorit", "colorize", "colorizeerize", "coloritup", "garlic",
               "findfaces", "grayscale", "minfilter", "maxfilter", "medianfilter",
               "remixed", "remix_blend", "doublediff", "linepainter_inv", "fullfill_diff",
               "copydiff", "colorhatch_diff", "colorhatch_bw_diff", "fullgradient_diff", "canny_inv", "canny_color", "weirderator", 
               "cornerharris", "kmeans", "xanny", "topographica", "autocontrast"]

def getSafeFuncs():
    safeFuncs = [altWorld,
                         ctrlWorld,
                         gritty,
                         vaguetransfer,
                         fullFill,
                         hardLandscape,
                         fourdotsRemixed,                         
                         radioFill,
                         colorHatch,
                         subtlyWrong,
                         nightgrid,
                         nightgridStars,
                         gradientSquares,
                         hsvTesting,
                         paletteSquares,
                         atariripples,
                         diagonal4Way,
                         sigilGrid]

    return safeFuncs

def getOneSafeFunc():
    key = random.choice(getSafeFuncs())
    colorPrint.print_custom_palette(191, f"[--------> getOneSafeFunc ---- {key} --------->")

    return key

# globals ---------------------------------------------- @~-------

config = False
functionDocs = False
telemetry = False
extParams = []
input_palette = []
possibleFonts = []
current_imgtype = None
currentUID = "0"

timeStart = time.time()
manager = multiprocessing.Manager()
wrapperData = manager.dict()
wrapperData["xannies"] = manager.dict()
wrapperData["inserts_used"] = manager.dict()
wrapperData["function_states"] = manager.dict()

words = []
wordsPositive = []
wordsNegative = []
wordsVerb = []
wordsNoun = []
wordsAdjective = []
wordsJargon = []
wordsMoby = dict()

palettelist = [
    (1, "1 (VAPORWAVE)"),
    (2, "2 (PRIMARY)"),
    (3, "3 (WACKY)"),
    (4, "4 (COCO)"),
    (5, "5 (ATARI)"),
    (6, "6 (grylteal)"),
    (7, "7 (dare to dream)"),
    (8, "8 (godfilter)"),
    (9, "9 (hot dog stand)"),
    (10, "10 (AAP-DGA16 - CGA/EGA Edit)"),
    (11, "11 (CGA MODE 4 1 HIGH - cyan/pink)"),
    (12, "12 (CGA MODE 4 0 HIGH - red/green)"),
    (13, "13 (HELLDEATH)"),
    (14, "14 (PICO-8)"),
    (15, "15 (8-BIT HANDHELD)"),
    (16, "16 (RESURRECT JUPITER)"),
    (17, "17 (YOUR FRIEND'S CHAMBER)"),
    (18, "18 (THE BRANE OF EQUINOX)"),
    (19, "19 (pastels)"),
    (20, "20 (rainbow)"),
    (21, "21 (hsv)"),
    (22, "22 (light text)"),
    (23, "23 (ALL CGA)"),
    (24, "24 (CGA++)"),
    (25, "25 (CHASM)"), # courtesy of: https://lospec.com/palette-list/chasm
    (26, "26 (defective)"),
    (27, "27 (8-BIT HVC)"),
    (28, "28 (LIMEDEATH)"),
    (29, "29 (BLUEDEATH)"),
    (30, "30 (DEATHDEATH)"),
    (31, "31 (OUTRUN)"),
    (32, "32 (sunset)"),
    (33, "33 (cappuchino)"),
    (34, "34 (solemn bob)"),
    (35, "35 (radical)"),
    (36, "36 (Mystic Nights)"),
    (37, "37 (ice cream lambo (LAMBO!) )"),
    (38, "38 (ice cream metal)"),
    (39, "39 (ice cream mental)"),
    (40, "40 (dare to nightmare)"),
    (41, "41 (beachy peach)"),
    (42, "42 (42)"),
    (43, "43 (BOATS AND HOES)"),
    (44, "44 (You and Me)"),
    (45, "45 (bosdox coobbrack)"),
    (46, "46 (boyngirl)"),
    (47, "47 (metatronWorld)"),
    (48, "48 (synthwave)"),
    (49, "49 (TWILIGHT 5)"), # https://lospec.com/palette-list/twilight-5
    (50, "50 (city sunset)"),
    (51, "51 (Amber CRT)"),
    (52, "52 (Thermal Camera)"),
    (53, "53 (Forest Canopy)"),
    (54, "54 (Ocean Waves)"),
    (55, "55 (Bauhaus Print)"),
    (56, "56 (Corporate '90s)"),
    (57, "57 (Cyberpunk Alley)"),
    (58, "58 (Solarized Variant)"),
    (59, "59 (jazz cup)"),
    (60, "60 (portland carpet)"),
    (61, "61 (arcade carpet)"),
    (62, "62 (trapper keeper)"),
    (63, "63 (ZEDDY SPECCY)"),
    (64, "64 (MOS6510)"),
    (65, "65 (Desert Sun)"),
    (66, "66 (Tropical Fruit)"),
    (67, "67 (glitchwave)"),
    (68, "68 (BLUELIFE)"),
    (69, "69 (CYANLIFE)"),
    (70, "70 (CYANDEATH)"),
    (71, "71 (Green CRT)"),
    (72, "72 (Blue CRT)"),
    (73, "73 (Rust and Patina)"),
    (74, "74 (Memphis Design)"),
    (75, "75 (Corporate 2000s)"),
    (76, "76 (Neon Tubes)"),
    (77, "77 (Plastic Toys)"),
    (78, "78 (CRAYON 8)"),
    (79, "79 (CRAYON PEOPLE)"),
    (80, "80 (CRAYON 64)"),
    (81, "81 (Pastel Goth)"), 
    (82, "82 (Modern SaaS/Corporate Pastel)"),
    (83, "83 (Aurora Borealis)"),
    (84, "84 (Renaissance Fresco)"),
    (85, "85 (Japanese Woodblock)"),
    (86, "86 (Pop Art CMYK)"),
    (87, "87 (Woodgrain MOS6502)"),
    (88, "88 (Toxic Earth)"),
    (89, "89 (Alice in Wonderland)"),
    (90, "90 (Bird Cry)"),
    (91, "91 (Cotton Candy Rainbow)"),
    (92, "92 (Ice Cream)"),
    (93, "93 (Loud Amplifiers)"),
    (94, "94 (Vocaloid Girl)"),
    (95, "95 (Lawful Evil Contractor)"),
    (96, "96 (distant 4)"),
    (97, "97 (distant 6)"),
    (98, "98 (palette from dir)"),
    (99, "99 (GEN|ERA|TED)"),
    (100, "100 (Braided Carrot)"),
    (101, "101 (vaporwave+)"),
    (102, "102 (primary+)"),
    (103, "103 (wacky+)"),
    (104, "104 (COCO+)"),
    (105, "105 (Atari+)"),
    (106, "106 (grynteal+)"),
    (107, "107 (dare to dreeeeeam)"),
    (108, "108 (fodgilter)"),
    (109, "109 (hot dog stand+)"),
    (110, "110 (EGA Edit-er)"),
    (111, "111 (CGA MODE 4 1 HIGH+)"),
    (112, "112 (CGA MODE 4 0 HIGH+)"),
    (113, "113 (HELLDEATH+)"),
    (114, "114 (PICO-8+)"),
    (115, "115 (8-BIT HANDHELD+)"),
    (116, "116 (RESURRECT JUPITER+)"),
    (117, "117 (YOUR FRIEND'S CHAMBER+)"),
    (118, "118 (THE BRANE OF EQUINOX+)"),
    (119, "119 (pastels+)"),
    (120, "120 (rainbow+)"),
    (121, "121 (hsv+)"),
    (122, "122 (light text+)"),
    (123, "123 (ALL CGA+)"),
    (124, "124 (CGA+++)"),
    (125, "125 (CHASM+)"),
    (126, "126 (defectivejunk)"),
    (226, "226 (defectivejunk++)"),
    (300, "300 (Autumn Glow)"),
    (301, "301 (Autumn Harvest)")
    ]

# code begins here -- multiproc // timeout ------------- @~-------

# TODOs ---~ we define the magick to become the magick ~----------

# * put tdldl on a vps
# * have fun
# * remap_palette
# * EXIGENT MIDNIGHT

# Cryptomeld: Unlocks encrypted memories, revealing forgotten secrets.
# Voidweave: Tears a rift in reality, allowing passage to hidden realms.
# Nexthex: Bends time, altering the course of events with a whisper.
# Soulforge: Fuses consciousness with machine, blurring the boundaries.
# Neuroshade: Cloaks thoughts, shielding them from prying algorithms.
# Chromebane: Corrodes cybernetic implants, rendering them useless.
# Synthblood: Infuses veins with synthetic life, granting unnatural vitality.
# Wraithwire: Threads through firewalls, stealing forbidden data.
# Cortexhex: Rewrites neural pathways, rewriting destiny itself.
# Viraluxe: Spreads digital contagion, infecting networks with chaos.
# Quantumwhisper: Speaks to quantum particles, altering probabilities.
# Holothren: Summons holographic constructs, illusions with teeth.
# Nanoshroud: Wraps the body in nanobots, granting ethereal form.
# Echodark: Echoes the screams of erased memories, haunting the present.
# Aetherpulse: Disrupts reality grids, unraveling the fabric of existence.

# CASINO DEMENTIA
# STYLIZED TIMECLOCK
# GONE MEANTIME
# ETERNAL CONVERSION
# EXPIRATION MOISTENER
# ALKALINE PHOTO
# EMPTIED MACHINE
# GELATIN WHIRRING

# logging ---------------------------------------------- @~-------

def writeWrapperToLog(data: DictProxy):    
    output = '---wrapperData    ---\n'

    output += 'keys:\n'
    for d in data.keys():
        output += str(d) + "\n"

    # ColorPrint.logger_info("wrapperData: " + str(wrapperData))

    output += 'items:\n'
    for did in data.items():        
        output += '\t' + str(did) + '\n'
        output += '\t' + str(did[0]) + '\n'
        output += '\t' + str(did[1]) + '\n'

    output += '---wrapperData end---\n'

    return output

def timeoutWrapper(queue, bob, wordChoice, palette, extParamsPassed, uid, key):
    global input_palette
    input_palette = processPalette(palette)

    global extParams
    extParams = extParamsPassed    

    global wrapperData
    global rootLogger
    global colorPrint

    #ColorPrint.logger_info("wrapperData as timeoutWrapper starts: " + writeWrapperToLog(wrapperData))

    loadConfiguration()

    colorPrint.print_custom_palette(191, f"[--------▶ timeoutWrapper ---- {key} ---------▶")
    colorPrint.print_custom_palette(191, f"| uid: {str(uid)}       ---▶")

    startTimeCheck()
    colorPrint.print_custom_palette(198, f"[          bob starts -------▶ {writeTimeCheck()}-----▶")

    if not isinstance(bob, dict) and bob.__name__ == "textGrid":
        result = bob(wordChoice)
    elif not isinstance(bob, dict):
        result = bob()
    else:
        result = bob["f"]()    

    colorPrint.print_custom_palette(198, f"---------▶ bob done   -------▶ {writeTimeCheck()}-----]")

    # ColorPrint.logger_info("wrapperData: " + writeWrapperToLog(wrapperData))    
    # ColorPrint.logger_info("telemetry: " + writeWrapperToLog(telemetry))

    outputPath = "tempImages/" + uid + ".gif"

    if isinstance(result, pilGif.GifImageFile):
        result.save(outputPath, format="GIF", save_all=True)
        wrapperData[uid] = outputPath
    else:
        wrapperData[uid] = result

    saveConfiguration()

    queue.put(uid)
    queue.close()

    colorPrint.print_custom_palette(191, f"---------▶ timeoutWrapper done ----------------]")

def writeTimeCheck():
    x = round(getTimeCheck()[1], 5)
    return colorPrint.get_custom_rgb(x)

def callWithTimeout(doThisThing, TIMEOUT, wordChoice="ALONE", palette="", key=""):
    global extParams
    global currentUID

    uid = uuid.uuid4()
    currentUID = str(uid)

    global wrapperData
    wrapperData["xannies"][currentUID] = manager.list()
    wrapperData["inserts_used"][currentUID] = manager.list()
    wrapperData["function_states"][currentUID] = manager.list()

    queueueueueue = multiprocessing.Queue(1) # Maximum size is 1
    proc = multiprocessing.Process(target=timeoutWrapper, args=(queueueueueue, doThisThing, wordChoice, palette, extParams, currentUID, key))
    proc.start()

    # Wait for TIMEOUT seconds
    try:
        result = queueueueueue.get(True, TIMEOUT)
    except queue.Empty as exEmp:
        colorPrint.print_custom_palette(171, f"---------▶ callWithTimeout ----   empty   ---------▶")
        colorPrint.print_custom_palette(171, f"{exEmp}")
        colorPrint.print_custom_palette(171, f"{proc} / {dir(proc)}")
        result = None
    except Exception as e:
        colorPrint.print_custom_palette(171, f"---------▶ callWithTimeout ---- exception ---------▶")
        colorPrint.print_custom_palette(171, f"{e}")
        rootLogger.error(proc)
        raise
    finally:
        colorPrint.print_custom_palette(171, f"---------▶ callWithTimeout: {colorBg(41)}{colorEsc(0)}killing bob. {colorEsc(238)}{colorBg(40)}don't tell -----⇥]") 
        proc.kill()

    # Process data here, not in try block above, otherwise your process keeps running
    return result

def startTimeCheck():
    global timeStart
    timeStart = time.time()
    return

def getTimeCheck():
    global timeStart
    t1 = time.time()

    return (t1, t1-timeStart)

def doTimeCheck(otherInfo="", i=0):
    global timeStart
    t1 = time.time()

    global colorPrint

    if i == 0:
        colorPrint.print_warn("elapsed: " + str(t1-timeStart) + " " + otherInfo)
    else:
        colorPrint.logger_whatever("elapsed: " + str(t1-timeStart) + " " + otherInfo)

    return

def logException(e):
    tback = traceback.format_exc()
    fstack = traceback.format_stack()
    
    rootLogger.error(str(datetime.datetime.now()))
    rootLogger.error(tback)
    rootLogger.error(str(fstack))
    rootLogger.error("---------------------")
    
# utility/supporting functions ------------------------- @~-------

def getParam(i):
    global extParams
   
    result = ""
    
    if extParams != []:
        if i >= 0 and len(extParams) >= (i+1) and extParams[i] != "":
            result = extParams[i]
        elif i < 0 and extParams[i] != "":
            result = extParams[i]
        
    return result

def getIntParams(defaultP1=250, defaultP2=100):
    p1 = getParam(0)
    p2 = getParam(1)
    p1 = int(p1) if p1.isdecimal() else defaultP1
    p2 = int(p2) if p2.isdecimal() else defaultP2

    return (p1, p2)

def getTextPosFromImgAndTextSize(img_size, text_size):
    # |                 |                 |
    # |          |             |          |
    # x = midpoint minus (half the text/2)

    midpoint = int(img_size // 2)
    half_text = int(text_size // 2)
    z = midpoint - half_text if midpoint - half_text >= 0 else 0
        
    return z

def getRandomFloodFill():
    global maxFloodFillArg

    iAlg = random.randint(1, maxFloodFillArg)
    
    return iAlg

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
    x = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    
    if len(x) > 4:
        rootLogger.debug(f'value: {value} output: {x}')
        
    return x

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def calculate_luminace(color_code):
    index = float(color_code) / 255 

    if index < 0.03928:
        return index / 12.92
    else:
        return ( ( index + 0.055 ) / 1.055 ) ** 2.4
    
def calculate_relative_luminance(rgb):
    return 0.2126 * calculate_luminace(rgb[0]) + 0.7152 * calculate_luminace(rgb[1]) + 0.0722 * calculate_luminace(rgb[2]) 

def calcContrastRatio(color1, color2):
    light = color1 if sum(color1) > sum(color2) else color2
    dark = color1 if sum(color1) < sum(color2) else color2

    contrast_ratio = ( calculate_relative_luminance(light) + 0.05 ) / ( calculate_relative_luminance(dark) + 0.05 )

    return contrast_ratio

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

def getRandomColorRGB():
    rgba = getRandomColor()
    return (rgba[0], rgba[1], rgba[2])

def getRandomColor(alpha=-1):
    if alpha == -1:
        alpha = random.randint(0, 255)
        
    random.seed()
    r = random.randint(0, 255)

    random.seed()
    g = random.randint(0, 255)

    random.seed()
    b = random.randint(0, 255)

    return (r, g, b, alpha)

# Sum of the min & max of (a, b, c)
def hilo(a, b, c):
    if c < b: b, c = c, b
    if b < a: a, b = b, a
    if c < b: b, c = c, b
    return a + c

def getColorComplement(c):
    (r, g, b) = c
    k = hilo(r, g, b)
    return tuple(k - u for u in (r, g, b))
    
def resizeToMinMax(img, maxW, maxH, minW, minH):
    doTimeCheck("resizeToMinMax starts")

    img = resizeToMin(img, maxW, maxH, minW, minH)

    z = resizeToMax(img, maxW, maxH)
    
    doTimeCheck("resizeToMinMax complete")

    return z

def resizeToMin(img, maxW, maxH, minW, minH):
    doTimeCheck("resizeToMin starts")

    if img.size[0] > maxW or img.size[1] > maxH or img.size[0] < minW or img.size[1] < minH:
        (w, h) = getSizeByMinMax(img.size[0], img.size[1], maxW, maxH, minW, minH)
        img = img.resize((int(w), int(h)), Image.LANCZOS)

    doTimeCheck("resizeToMin complete")

    return img

def resizeToMax(img, maxW, maxH):
    doTimeCheck("resizeToMax starts")

    if img.size[0] > maxW or img.size[1] > maxH:
        (w, h) = getSizeByMax(img.size[0], img.size[1], maxW, maxH)
        img = img.resize((int(w), int(h)), Image.LANCZOS)

    doTimeCheck("resizeToMax complete")

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

def resizeToMatch(img1, img2):
    outputW = 0
    outputH = 0

    if(img1.size[0] >= img2.size[0]):
        outputW = int(img1.size[0])
        outputH = int(img1.size[1])
    else:
        outputW = int(img2.size[0])
        outputH = int(img2.size[1])
        
    img1 = img1.resize((outputW, outputH))
    img2 = img2.resize((outputW, outputH))

    return (img1, img2)

def getTempFile(tempDir="./"):
    import tempfile
   
    return tempfile.NamedTemporaryFile(dir=tempDir)

def writeImageException(e):
    global fontPathSansSerif
    exc_type, exc_obj, exc_tb = sys.exc_info()

    rootLogger.error(sys.exc_info())

    logException(e)

    colorPrint.print_custom_palette(141, f"{e}")
    colorPrint.print_custom_palette(141, f"{dir(e)}")
            
    img = Image.new("RGBA", (1024, 768), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    
    fon = ImageFont.truetype(fontPathSansSerif, 18)
    debugFillColor = (0, 0, 0, 255)
    textY = 0
    
    outputMsg = str(e)
    
    draw.text((5, textY), outputMsg, font=fon, fill=debugFillColor)

    outputMsg = "at line: " + str(exc_tb.tb_lineno)
    
    draw.text((5, textY+24), outputMsg, font=fon, fill=debugFillColor)

    return img

def getGoodRanges(pixels, rangeCount):
    pixCounts = {}

    totalCount = 0

    for pixel in pixels:
        if pixel not in pixCounts:
            pixCounts[pixel] = 1
        else:
            pixCounts[pixel] += 1

        totalCount += 1

    splitCount = totalCount // rangeCount

    range = []

    thisRange = 0
    lastI = 0
    for i in sorted(pixCounts.keys()):
        if pixCounts[i] + thisRange > splitCount:
            rootLogger.debug("i: " + str(i) + " count: " + str(thisRange))
            range.append(lastI)
            thisRange = pixCounts[i] + 0

            if len(range) == rangeCount - 1:
                range.append(255)
                break
        else:
            thisRange += pixCounts[i]

        lastI = i

    if(len(range) < rangeCount):
        range.append(lastI)

    #rootLogger.debug("pixCounts: " + str(sorted(pixCounts.keys())))
    rootLogger.debug("pixCounts: " + str(pixCounts))
    rootLogger.debug("totalCount: " + str(totalCount))
    rootLogger.debug("range: " + str(range))
    rootLogger.debug("splitCount: " + str(splitCount))

    return range

def _lerp(a, b, t): 
    return int(a + (b - a) * t)

def _lerp_color(c1, c2, t):
    return tuple(_lerp(a, b, t) for a, b in zip(c1, c2))

def dropin_text_size(draw, text, font):
    # To get the bounding box of the text:
    left, top, right, bottom = draw.textbbox((0, 0), text, font)
    width = right - left
    height = bottom - top
    return (width, height)

# ---- end utility functions -------------------- @~-------
# image operations ------------------------------ @~-------

def check_image_operation(img, imageop, palette):
    for iopx in imageop.split(','):
        iop = iopx.lower()
        
        if iop == "fourit":
            img = imageop_four_it(img)

        if iop == "twoit":
            img = imageop_two_it(img)

        if iop == "invert":
            img = imageop_invert(img)

        if iop == "hueshift":
            img = imageop_hueshift(img)

        if iop == "edge":
            img = imageop_edge(img)

        if iop == "contour":
            img = imageop_contour(img)

        if iop == "detail":
            img = imageop_detail(img)

        if iop == "adaptive_mediancut":
            img = imageop_adaptive_palette(img, palette, quantOption=0)

        if iop == "adaptive":
            img = imageop_adaptive_palette(img, palette, quantOption=2)

        if iop == "adaptive_dither":
            img = imageop_adaptive_palette(img, palette, quantOption=2, dither=1)

        if iop == "adaptive_quant":
            img = imageop_adaptive_palette(img, palette, quantOption=3)
            
        if iop == "pixelate":
            img = imageop_pixelate(img)

        if iop == "redit":
            img = imageop_redit(img)

        if iop == "greenit":
            img = imageop_greenit(img)

        if iop == "blueit":
            img = imageop_blueit(img)

        if iop == "colorit":
            whichop = random.randint(0, 2)
            img = imageop_colorit(img, whichop)

        if iop == "fourcolortdl":
            img = imageop_fourcolor(img, palette)

        if iop == "godcolor":
            img = imageop_godcolor(img, palette)

        if iop == "fourblend":
            img = imageop_fourcolorBlend(img, palette)

        if iop == "colorize":
            img = imageop_colorize(img, palette)

        if iop == "colorizerize":
            img = imageop_colorizerize(img, palette)

        if iop == "coloritup":
            img = imageop_colorItUp(img, palette)

        if iop == "garlic":
            img = imageop_garlic(img, palette)

        if iop == "findfaces":
            img = imageop_findfaces(img)

        if iop == "grayscale":
            img = imageop_grayscale(img)

        if iop == "minfilter":
            img = imageop_minfilter(img)

        if iop == "maxfilter":
            img = imageop_maxfilter(img)

        if iop == "medianfilter":
            img = imageop_medianfilter(img)

        if iop == "remixed":
            img = imageop_remixed(img)

        if iop == "remix_blend":
            img = imageop_remixed_blended(img)

        if iop == "doublediff":
            img = imageop_doublediff(img)

        if iop == "linepainter_inv":
            img = imageop_linepainter_inv(img)

        if iop == "fullfill_diff":
            img = imageop_fullFill_diff(img)

        if iop == "copydiff":
            img = imageop_copydiff(img)

        if iop == "colorhatch_diff":
            img = imageop_colorHatch_diff(img)

        if iop == "colorhatch_bw_diff":
            img = imageop_colorHatch_bw_diff(img)

        if iop == "fullgradient_diff":
            img = imageop_fullGradient_diff(img)

        if iop == "canny_inv":
            img = imageop_canny_inv(img)

        if iop == "canny_color":
            img = imageop_canny_color(img)

        if iop == "weirderator":
            img = imageop_weirderator(img)

        if iop == "cornerharris":
            img = imageop_cornerHarris(img)

        if iop == "kmeans":
            img = imageop_kmeans(img)
        
        if iop == "xanny":
            img = imageop_xanny(img)

        if iop == "topographica":
            img = imageop_topographica(img)

        if iop == "autocontrast":
            img = imageop_autocontrast(img)

    return img

def imageop_pixelate(img):
    sqX = random.randint(2, 10)
    sqY = random.randint(2, 10)

    draw = ImageDraw.Draw(img)
    pixdata = img.load()

    for y in range(img.size[1]-1, -1, -sqY):
        for x in range(img.size[0]-1, -1, -sqX):
            c = pixdata[x, y]
            draw.rectangle(((x, y),(x+sqX, y+sqY)), fill=c)
            
    return img

def imageop_adaptive(img, palette="", quantOption=2, dither=0):
    # MEDIANCUT = 0
    # MAXCOVERAGE = 1
    # FASTOCTREE = 2
    # LIBIMAGEQUANT = 3

    img = img.convert("RGB")

    if palette == "":
        palette = getInputPalette()
        
    pal = generatePalette(palette)
    pal = pal.convert("P", palette=Image.ADAPTIVE)

    img.load()
    img = img.quantize(method=quantOption, palette=pal, dither=dither)

    return img

def imageop_adaptive_palette(img, palette=1, quantOption=2, dither=0):
    choices = getPaletteSpecific(palette)

    return imageop_adaptive(img, choices, quantOption, dither)

def imageop_grayscale(img):
    img = img.convert("RGB")
    img = img.convert("L")    
    img.load()    

    return img

def imageop_detail(img):
    img = img.convert("RGB")
    img = img.filter(ImageFilter.DETAIL)
    return img

def imageop_contour(img):
    img = img.convert("RGB")
    img = img.filter(ImageFilter.CONTOUR)
    return img
    
def imageop_edge(img):
    img = img.convert("RGB")
    img = img.filter(ImageFilter.EDGE_ENHANCE)
    return img

def imageop_hueshift(img):
    img = img.convert("RGB")
    
    pixdata = img.load()

    version = random.randint(0, 4)
    
    for x in range(0, img.size[0]):
        for y in range(0, img.size[1]):
            c = pixdata[x, y]

            if version == 0:
                pixdata[x, y] = (c[2], c[1], c[0])
            elif version == 1:
                pixdata[x, y] = (c[2], c[0], c[1])
            elif version == 2:
                pixdata[x, y] = (c[1], c[0], c[2])
            elif version == 3:
                pixdata[x, y] = (c[1], c[2], c[0])
            elif version == 4:
                pixdata[x, y] = (c[0], c[2], c[1])

    return img

def imageop_redit(img):
    return imageop_colorit(img, 0)
def imageop_greenit(img):
    return imageop_colorit(img, 1)
def imageop_blueit(img):
    return imageop_colorit(img, 2)

def imageop_colorit(img, ci):
    pixdata = img.load()

    for x in range(0, img.size[0]):
        for y in range(0, img.size[1]):
            c = pixdata[x, y]
            cl = [c[0], c[1], c[2]]
            cl.sort(reverse=True)

            cother1 = random.choice([1, 2])
            cother2 = 2 if cother1 == 1 else 1
                
            if ci == 0:
                c = (cl[0], cl[cother1], cl[cother2])
            elif ci == 1:
                c = (cl[cother2], cl[0], cl[cother1])
            elif ci == 2:
                c = (cl[cother1], cl[cother2], cl[0])

            pixdata[x, y] = c
                  
    return img

def imageop_fourcolor(inputFile, palette=0, choices=[]):
    global rootLogger
    rootLogger.info("imageop_fourcolor")
    
    (w, h) = getSizeByMax(inputFile.size[0], inputFile.size[1], 1280, 1024)    
    inputFile = inputFile.resize((int(w), int(h)), Image.LANCZOS)
    
    p1 = getParam(0)
    p2 = getParam(1)   

    if choices != []:
        colors = choices
    elif palette != 0:
        try:
            intpalette = int(palette)
            colors = getPaletteSpecific(intpalette)
        except:
            colors = random.choice(fourColorPalettes)
    else:
        colors = random.choice(fourColorPalettes)
    
    return fourColorWithPalette(inputFile, colors)

def fourColorWithPalette(inputImg, colors):
    inputImg = inputImg.convert("RGB")

    pixels = ImageOps.grayscale(inputImg).getdata()

    ranges = getGoodRanges(pixels, len(colors))

    img2 = Image.new(inputImg.mode, inputImg.size,)
    img2.putdata(colorfun(pixels, colors, ranges))

    img2.load()
    
    return img2

def imageop_godcolor(inputFile, palette=0, choices=[]):
    return imageop_fourcolor(inputFile, palette=palette, choices=getPaletteGenerated(paletteLength=random.randint(12, 20)))    

def imageop_fourcolorBlend(inputFile, palette=0, choices=[]):
    result = imageop_fourcolor(inputFile, palette=palette, choices=choices)

    global rootLogger

    result = result.convert("RGBA")
    inputFile = inputFile.convert("RGBA")
    
    if(inputFile.size != result.size):
        rootLogger.warning(inputFile.size)
        rootLogger.warning(result.size)

        result = result.resize((int(inputFile.size[0]), int(inputFile.size[1])), Image.LANCZOS)

    blendAmount = random.randint(30, 88) * 0.01
    
    addState(f"blendAmount: {blendAmount}", None)

    img = Image.blend(inputFile, result, blendAmount)

    return img

def imageop_colorize(inputFile, palette=0, choices=[]):    
    global rootLogger
    rootLogger.info("imageop_colorize")
    
    (w, h) = getSizeByMax(inputFile.size[0], inputFile.size[1], 1280, 1024)    
    inputFile = inputFile.resize((int(w), int(h)), Image.LANCZOS)
    
    p1 = getParam(0)
    p2 = getParam(1)   

    if choices != []:
        colors = choices
    elif palette != 0:
        try:
            intpalette = int(palette)
            colors = getPaletteSpecific(intpalette)
        except:
            colors = random.choice(fourColorPalettes)
    else:
        colors = random.choice(fourColorPalettes)
    
    inputFile = inputFile.convert("RGB")

    gry = ImageOps.grayscale(inputFile)

    result = ImageOps.colorize(gry, get_rgb(colors, 0), get_rgb(colors, 1))

    return result

def imageop_colorizerize(inputFile, palette=0, choices=[]):
    # TODO: change this to use colorizerize
    return imageop_colorize(inputFile, palette, choices)

def imageop_colorItUp(inputFile, palette=0, choices=[]):
    img = colorItUp(inputFile, version=2, palnum=palette)
    return img

def imageop_garlic(inputFile, palette=0, choices=[]):
    img = garlic(inputFile)
    return img

def imageop_findfaces(inputFile):
    timeStart = time.time()
    timeLimit = 30

    currentCascade = "haarcascade_frontalface_default.xml"
    #currentCascade = "haarcascade_fullbody.xml"

    import cv2

    inputFile = inputFile.convert("RGBA")
    
    open_cv_image = numpy.array(inputFile) # cv2.cvtColor(numpy.array(inputFile), cv2.COLOR_RGB2BGR)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + currentCascade)
    
    gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

    i = 0
    faces = [i for i in range(9999)]

    while len(faces) > 4:
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.05, minNeighbors=i)

        t1 = time.time()
        print ("elapsed: " + str(t1-timeStart) + " length: " + str(len(faces)))

        # timeLimit

        i += 1

    while len(faces) < 1:
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.05, minNeighbors=i)

        t1 = time.time()
        print ("elapsed: " + str(t1-timeStart) + " length: " + str(len(faces)))

        i -= 1
    
    rectColor = getRandomColor()

    for x,y,w,h in faces:
        open_cv_image = cv2.rectangle(open_cv_image, (x,y), (x+w, y+h), rectColor, 1)            

    im_pil = Image.fromarray(open_cv_image)
    im_pil = im_pil.convert("RGBA")

    cv2.destroyAllWindows()

    return im_pil
        
def imageop_weirderator(inputFile):
    import cv2

    inputFile = inputFile.convert("RGBA")

    open_cv_image = numpy.array(inputFile)

    retries = 0

    while retries < 10:
        try:
            open_cv_image = cv2.cvtColor(open_cv_image, random.randint(0, 143))
            retries = 10
        except Exception as e:
            rootLogger.debug(e)
            retries += 1
            pass

    try:
        open_cv_image = open_cv_image[:, ::-1, ::].copy()
    except:
        pass

    im_pil = Image.fromarray(open_cv_image)
    im_pil = im_pil.convert("RGBA")

    cv2.destroyAllWindows()

    return im_pil

def imageop_cornerHarris(inputFile):
    import cv2 as cv
    
    # img - Input image. It should be grayscale and float32 type.
    # blockSize - It is the size of neighbourhood considered for corner detection
    # ksize - Aperture parameter of the Sobel derivative used.
    # k - Harris detector free parameter in the equation.

    blockSize = 4
    ksize = 5
    k = 0.04

    inputFile = inputFile.convert("RGBA")

    img = numpy.array(inputFile)

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = numpy.float32(gray)
    dst = cv.cornerHarris(gray, blockSize, ksize, k)

    c = getRandomColor()

    # marking the corners
    #dst = cv.dilate(dst, None)

    img[dst > 0.01 * dst.max()] = c

    im_pil = Image.fromarray(img)
    im_pil = im_pil.convert("RGBA")

    return im_pil

def imageop_kmeans(inputFile):
    import cv2 as cv

    K = 8
    attempts = 10

    inputFile = inputFile.convert("RGB")

    img = numpy.array(inputFile)

    shape = (-1,3)

    colorPrint.print_custom_palette(197, f"current shape: {numpy.shape(img)}")

    Z = img.reshape(shape)
    
    colorPrint.print_custom_palette(197, f"new shape: {numpy.shape(Z)}")
    
    # convert to np.float32
    Z = np.float32(Z)
    
    # define criteria, number of clusters(K) and apply kmeans()
    # criteria: `( type, max_iter, epsilon )`
    # The algorithm termination criteria, that is, the maximum number of iterations and/or the desired accuracy. 
    # The accuracy is specified as criteria.epsilon. As soon as each of the cluster centers moves by less than criteria.epsilon on some iteration, the algorithm stops. 

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, attempts, 1.0)    
    ret,label,center=cv.kmeans(Z,K,None,criteria,attempts,cv.KMEANS_RANDOM_CENTERS)
    
    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))

    im_pil = Image.fromarray(res2)
    im_pil = im_pil.convert("RGBA")

    return im_pil

def imageop_xanny(inputFile):
    global wrapperData
    global currentUID

    uid = currentUID   

    doTimeCheck("xanny queue check: " + str(len(wrapperData["xannies"][uid])) + " image(s)")

    if uid not in wrapperData["xannies"]:
        saveForXanny(inputFile)
    else:
        if len(wrapperData["xannies"][uid]) <= 0:
            saveForXanny(inputFile)

    doTimeCheck("xanny queue check: " + str(len(wrapperData["xannies"][uid])) + " image(s)")

    xi = xannyImage(wrapperData["xannies"][uid])

    return xi

def imageop_invert(img):
    img = img.convert("RGB")
    img = ImageChops.invert(img)
    img.load()
    
    return img

def imageop_two_it(img):
    mirror1 = img.transpose(Image.FLIP_LEFT_RIGHT)
    
    blendAmount = .50   
   
    img = Image.blend(img, mirror1, blendAmount)

    return img

def imageop_four_it(img):
    mirror1 = img.transpose(Image.FLIP_LEFT_RIGHT)
    rot1 = img.rotate(180)
    mirror2 = mirror1.rotate(180)
    
    blendAmount = .50
    
    img = Image.blend(img, rot1, blendAmount)
    mirror = Image.blend(mirror1, mirror2, blendAmount)
    
    img = Image.blend(img, mirror, blendAmount)

    return img

def imageop_minfilter(img):
    img = img.convert("RGB")
    img = img.filter(ImageFilter.MinFilter)
    return img

def imageop_medianfilter(img):
    img = img.convert("RGB")
    img = img.filter(ImageFilter.MedianFilter)
    return img

def imageop_maxfilter(img):
    img = img.convert("RGB")
    img = img.filter(ImageFilter.MaxFilter)
    return img

def imageop_remixed(img):
    img = remixer("", img)
    return img

def imageop_remixed_blended(img):
    try:
        blendAmount = random.uniform(0.2, 0.8)
       
        imgRemix = img.copy()
        imgRemix = remixer("", imgRemix)

        imgRemix = imgRemix.convert("RGBA")
        img = img.convert("RGBA")

        if img.size != imgRemix.size:
            img = img.resize(imgRemix.size, Image.LANCZOS)
            
        img = Image.blend(img, imgRemix, blendAmount)

    except Exception as e:
        print(img.mode, img.size)
        print(imgRemix.mode, imgRemix.size)
        
        img = writeImageException(e)
    
    return img

def imageop_doublediff(img):
    try:
        global current_imgtype
        global tdlTypes      
        
        img2 = current_imgtype()

        img = ImageChops.difference(img, img2)        
        
    except Exception as e:
        img = writeImageException(e)

    return img

def imageop_linepainter_inv(img):
    try:
        width = img.size[0]
        height = img.size[1]

        img = img.convert("RGBA")
        img.load()
        
        img2 = linePainter(width=width, height=height)

        img3 = ImageChops.difference(img, img2) 
        img3.load()
        
        img = img3.convert("RGB")
        img.load()

    except Exception as e:
        img = writeImageException(e)

    return img

def imageop_canny_inv(img):
    
    try:
        import cv2
        
        width = img.size[0]
        height = img.size[1]

        img = img.convert("RGBA")
        img.load()

        open_cv_image = numpy.array(img) 
        # Convert RGB to BGR 
        open_cv_image = open_cv_image[:, :, ::-1].copy() 
    
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        
        gray = cv2.GaussianBlur(gray, (7,7), 1.5)
        gray = cv2.Canny(gray, 0, 50)

        img2 = Image.fromarray(gray)

        img2 = img2.convert("RGB")
        img2 = ImageChops.invert(img2)
        img2.load()
        
        img2 = img2.convert("RGBA")
        
        #img2 = linePainter(width=width, height=height)

        img3 = ImageChops.darker(img, img2)

        #img3 = ImageChops.difference(img, img2) 
        img3.load()
        
        img = img3.convert("RGB")
        img.load()

    except Exception as e:
        img = writeImageException(e)

    cv2.destroyAllWindows()

    return img

def imageop_canny_color(img):
    
    try:
        import cv2
        
        width = img.size[0]
        height = img.size[1]

        img = img.convert("RGBA")
        img.load()

        open_cv_image = numpy.array(img) 
        # Convert RGB to BGR 
        open_cv_image = open_cv_image[:, :, ::-1].copy() 
    
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        
        gray = cv2.GaussianBlur(gray, (7,7), 1.5)
        gray = cv2.Canny(gray, 0, 50)        
        
        img2 = Image.fromarray(gray)        

        img2 = img2.convert("RGB")        
        img2 = ImageChops.invert(img2)
        img2.load()

        pixdata = img2.load()

        ctarg = (0,0,0)
        crepl = getRandomColor()

        for x in range(0, img2.size[0]-1):
            for y in range(0, img2.size[1]-1):
                if pixdata[x, y] == ctarg:
                    pixdata[x, y] = crepl               
        
        img2 = img2.convert("RGBA")
        
        op = random.randint(0, 2)

        if op == 0:
            img3 = ImageChops.darker(img, img2)
        elif op == 1:
            img3 = ImageChops.multiply(img, img2)
        elif op == 2:
            img3 = ImageChops.difference(img, img2)

        print(op)
        
        img3.load()
        
        img = img3.convert("RGB")
        img.load()

    except Exception as e:
        img = writeImageException(e)

    cv2.destroyAllWindows()

    return img

def imageop_fullFill_diff(img):
    try:
        width = img.size[0]
        height = img.size[1]

        img = img.convert("RGBA")
        img.load()
        
        img2 = fullFill(w=width, h=height)

        img3 = ImageChops.difference(img, img2) 
        img3.load()

        img4 = Image.blend(img, img3, .3)
        
        img = img4.convert("RGB")
        img.load()

    except Exception as e:
        img = writeImageException(e)

    return img

def imageop_colorHatch_diff(img):
    try:
        width = img.size[0]
        height = img.size[1]

        img = img.convert("RGBA")
        img.load()
        
        img2 = colorHatch(width=width, height=height)

        img3 = ImageChops.difference(img, img2) 
        img3.load()
        
        img = img3.convert("RGB")
        img.load()

    except Exception as e:
        img = writeImageException(e)

    return img

def imageop_colorHatch_bw_diff(img):
    try:
        width = img.size[0]
        height = img.size[1]

        img = img.convert("RGBA")
        img.load()

        squareX = random.randint(5, 50)
        squareY = random.randint(5, 50)
        
        img2 = colorHatch(width=width, height=height, bw=1, doFF=0, squareX=squareX, squareY=squareY)

        img3 = ImageChops.difference(img, img2) 
        img3.load()
        
        img = img3.convert("RGB")
        img.load()

    except Exception as e:
        img = writeImageException(e)

    return img

def imageop_fullGradient_diff(img):
    try:
        width = img.size[0]
        height = img.size[1]

        img = img.convert("RGBA")
        img.load()

        img2 = fullGradient(width=width, height=height)

        img3 = ImageChops.difference(img, img2) 
        img3.load()
        
        img = img3.convert("RGB")
        img.load()

    except Exception as e:
        img = writeImageException(e)

    return img

def imageop_copydiff(img):
    try:
        width = img.size[0]
        height = img.size[1]

        img = img.convert("RGBA")
        img.load()

        img2 = img.copy()
        img2 = img2.convert("RGB")
        img2 = img2.convert("L")    
        img2.load()
        img2 = img2.convert("RGBA")
        
        img3 = ImageChops.difference(img, img2) 
        img3.load()
        
        img = img3.convert("RGB")
        img.load()

    except Exception as e:
        img = writeImageException(e)

    return img

def imageop_autocontrast(img):
    try:
        cutoff = 0.4
        img = img.convert("RGB")
        img = ImageOps.autocontrast(img, cutoff=cutoff)

    except Exception as e:
        img = writeImageException(e)

    return img

def imageop_topographica(
    img,
    *,
    levels=20,                # number of contour thresholds
    contour_stride=1,         # draw every Nth contour (1 = all)
    line_width=2,             # contour stroke thickness (px)
    line_alpha=210,           # contour opacity
    blur_before=0.6,          # pre-blur luminance for smoother bands (0=off)
    hillshade=True,           # cheap relief shading
    hill_gain=0.45,           # strength of hillshade (0..1)
    invert=False,             # flip elevation (dark = high)
    gradient=None,            # base terrain colors: [(pos, (r,g,b)), ...]
    line_gradient=None        # optional contour color ramp (defaults to dark gray)
):
    """
    Convert an input Pillow image into a pseudo-topographic plate with
    colored elevation bands and contour lines. Returns an RGBA Image.
    """

    # ---------- inline helpers

    def _lerp(a, b, t):  # scalar lerp
        return a + (b - a) * t

    def _lerp_rgb(c0, c1, t):  # color lerp (RGB only)
        return tuple(int(_lerp(a, b, t)) for a, b in zip(c0, c1))

    def _gradient_color(grad, t):
        """
        grad: sorted list like [(pos0, (r,g,b)), (pos1, (r,g,b)), ...]
        t: float in [0,1] -> returns (r,g,b)
        """
        if t <= grad[0][0]:
            return grad[0][1]
        if t >= grad[-1][0]:
            return grad[-1][1]
        for (p0, c0), (p1, c1) in zip(grad, grad[1:]):
            if p0 <= t <= p1:
                # avoid divide-by-zero on identical stops
                span = (p1 - p0) if (p1 - p0) != 0 else 1e-9
                return _lerp_rgb(c0, c1, (t - p0) / span)
        return grad[-1][1]

    def _apply_gradient_LUT(gray_img, grad):
        """
        Map 8-bit grayscale directly to RGB via a 256-color palette LUT.
        No quantize/k-means—every L value maps 1:1 to a color.
        """
        # build 256*3 = 768-length palette (RGB only)
        pal = []
        for i in range(256):
            pal.extend(_gradient_color(grad, i / 255.0))
        # create a palette image using the grayscale bytes as indices
        p = Image.frombytes('P', gray_img.size, gray_img.tobytes())
        p.putpalette(pal)  # exactly 768 values
        return p.convert('RGB')

    # ---------- normalize input

    if img.mode not in ("L", "RGB", "RGBA"):
        img = img.convert("RGB")

    # luminance heightmap
    gray = ImageOps.grayscale(img)
    if invert:
        gray = ImageOps.invert(gray)
    if blur_before and blur_before > 0:
        gray = gray.filter(ImageFilter.GaussianBlur(float(blur_before)))

    # default terrain gradient
    if gradient is None:
        # deep → shoal → lowland → upland → scree → snow
        gradient = [
            (0.00, (14, 30, 66)),
            (0.25, (34, 92, 152)),
            (0.38, (72, 140, 104)),
            (0.58, (160, 182, 120)),
            (0.78, (182, 162, 134)),
            (0.90, (214, 210, 210)),
            (1.00, (246, 246, 246)),
        ]

    # base color bands
    base = _apply_gradient_LUT(gray, gradient).convert("RGBA")

    # hillshade (fast Sobel-ish fake)
    if hillshade:
        gx = gray.filter(ImageFilter.Kernel((3,3), [-1,0,1,-2,0,2,-1,0,1], scale=1))
        gy = gray.filter(ImageFilter.Kernel((3,3), [-1,-2,-1,0,0,0,1,2,1], scale=1))
        gx = ImageOps.autocontrast(gx)
        gy = ImageOps.autocontrast(gy)
        # combine to a light mask and blur slightly
        shade = ImageChops.multiply(gx.convert("L"), ImageOps.invert(gy).convert("L"))
        shade = ImageOps.autocontrast(shade).filter(ImageFilter.GaussianBlur(1.2))
        # mix via multiply with adjustable alpha
        alpha = Image.new("L", img.size, int(255 * max(0.0, min(1.0, hill_gain))))
        shade_rgba = Image.merge("RGBA", (shade, shade, shade, alpha))
        base = ImageChops.multiply(base, shade_rgba)

    # contour lines
    L = max(2, int(levels))
    stride = max(1, int(contour_stride))
    contours = Image.new("RGBA", img.size, (0, 0, 0, 0))

    for i in range(0, L, stride):
        t = int(255 * (i / (L - 1)))
        # binary threshold at this level
        mask = gray.point(lambda v, th=t: 255 if v >= th else 0).convert("L")
        # edges of the thresholded region
        edge = mask.filter(ImageFilter.FIND_EDGES)
        # thicken/solidify edges
        if line_width > 1:
            edge = edge.filter(ImageFilter.MaxFilter(size=max(3, (line_width | 1))))
        edge = edge.point(lambda v: 255 if v > 64 else 0)

        # choose line color
        if line_gradient is None:
            lc = (20, 20, 20, int(line_alpha))
        else:
            rgb = _gradient_color(line_gradient, i / (L - 1))
            lc = (*rgb, int(line_alpha))

        layer = Image.new("RGBA", img.size, lc)
        contours = Image.composite(layer, contours, edge)

    # composite
    out = base.copy()
    out.alpha_composite(contours)
    return out

# random word generation ---------------------- @~-------

def getTDL(primer="tdl"):
    commonWordList = wordListsPath + 'commonwords.txt'
    wards = [line for line in open(commonWordList)]   

    outputs = []

    for z in primer:
        outputs.append([])
    
    for line in wards:
        c = line.strip()[0].lower()
        
        for i in range(len(primer)):
            if c == primer[i]:
                outputs[i].append(line)
        
    random.seed()

    word = ""

    for z in outputs:
        word += "\n" + random.choice(z).upper()

    return word.strip()

def checkWordEncoding(word):
    try:
        word = word.decode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        pass

    return word

def getRandomWordSpecial(wordtype="positive", prefx=""):
    global rootLogger    

    wlPositive = wordListsPath + 'positive-words.txt'
    wlNegative = wordListsPath + 'negative-words.txt'
    wlVerb = wordListsPath + 'dictionary/verbs.txt'
    wlNoun = wordListsPath + 'dictionary/nouns.txt'
    wlAdjective = wordListsPath + 'dictionary/adjectives.txt'
    wlJargon = wordListsPath + 'jargon.txt'
    
    global wordsPositive
    global wordsNegative
    global wordsVerb
    global wordsNoun
    global wordsAdjective
    global wordsJargon
    
    if wordsPositive == []:
        wl = wlPositive
        wards = [line for line in open(wl, encoding = "ISO-8859-1")]        

        for line in wards:
            wordsPositive.append(checkWordEncoding(line))

    if wordsNegative == []:
        wl = wlNegative
        wards = [line for line in open(wl, encoding = "ISO-8859-1")]        

        for line in wards:
            wordsNegative.append(checkWordEncoding(line))

    if wordsVerb == []:
        wl = wlVerb
        wards = [line for line in open(wl, encoding = "ISO-8859-1")]

        for line in wards:
            wordsVerb.append(checkWordEncoding(line))

    if wordsNoun == []:
        wl = wlNoun
        wards = [line for line in open(wl, encoding = "ISO-8859-1")]

        for line in wards:
            wordsNoun.append(checkWordEncoding(line))

    if wordsAdjective == []:
        wl = wlAdjective
        wards = [line for line in open(wl, encoding = "ISO-8859-1")]

        for line in wards:
            wordsAdjective.append(checkWordEncoding(line))

    if wordsJargon == []:
        wl = wlJargon
        wards = [line for line in open(wl, encoding = "ISO-8859-1")]

        for line in wards:
            wordsJargon.append(checkWordEncoding(line))
            
    random.seed()

    zonk = ""

    if wordtype == "positive":
        zonk = wordsPositive
    elif wordtype == "negative":
        zonk = wordsNegative
    elif wordtype == "verb":
        zonk = wordsVerb
    elif wordtype == "noun":
        zonk = wordsNoun
    elif wordtype == "adjective":
        zonk = wordsAdjective
    elif wordtype == "jargon":
        zonk = wordsJargon
    else:
        zonk = wordsPositive

    if prefx == "":
        z = random.choice(zonk).strip()
    else:        
        zyx = list(filter(lambda x: x.startswith(prefx), zonk))

        if len(zyx) > 0:
            z = random.choice(zyx).strip()
        else:
            z = random.choice(zonk).strip()

    return z

def loadWordsFrom(filepath):
    wordsThis = []

    wards = [line for line in open(filepath, encoding = "ISO-8859-1")]

    for line in wards:
        l = checkWordEncoding(line).strip()
        l = ''.join(char for char in l if char.isalnum() or char.isspace())
        l = l.split()

        for xl in l:
            wordsThis.append(xl)
            
    random.seed()

    return wordsThis
    
def getRandomWord_Moby(typeind="", choice=""):
    global rootLogger   
    global mobyfilepath
    global wordsMoby

    if not wordsMoby:
        with open(mobyfilepath, encoding = "cp437") as f:

            for line in f:
                word, typ = line.strip().split("╫")

                for key in typ:
                    if key not in wordsMoby:
                        wordsMoby[key] = []

                    thislist = wordsMoby[key]
                    thislist.append(word)

    random.seed()

    choiceChoiced = ""
    
    # TODO: use choice
    
    if typeind != "":
        if typeind in wordsMoby:
            thislist = wordsMoby[typeind]

            choiceChoiced = random.choice(thislist)
    else:
        allkeys = list(wordsMoby.keys())
        keychoice = random.choice(allkeys)

        thislist = wordsMoby[keychoice]

        choiceChoiced = random.choice(thislist)

    choiceChoiced = checkWordEncoding(choiceChoiced)

    return choiceChoiced

def getRandomWord(match=""):
    wlCommon = [wordListsPath + 'commonwords.txt',
                wordListsPath + 'jargon.txt']
       
    global words

    if words == []:
        wordLists = wlCommon

        for wl in wordLists:
            wards = [line for line in open(wl)]        

            for line in wards:
                words.append(line)

    random.seed()

    word = ""
        
    word = random.choice(words).strip()

    if match != "":
        # TODO: fix match
        while word[0].lower() != match[0]:
            word = random.choice(words).strip()            

    return word

def get_random_unicode(length):
    get_char = chr

    # Update this to include code point ranges to be sampled
    include_ranges = [
        ( 0x0021, 0x0021 ),
        ( 0x0023, 0x0026 ),
        ( 0x0028, 0x007E ),
        ( 0x00A1, 0x00AC ),
        ( 0x00AE, 0x00FF ),
        ( 0x0100, 0x017F ),
        ( 0x0180, 0x024F ),
        ( 0x2C60, 0x2C7F ),
        ( 0x16A0, 0x16F0 ),
        ( 0x0370, 0x0377 ),
        ( 0x037A, 0x037E ),
        ( 0x0384, 0x038A ),
        ( 0x038C, 0x038C ),
    ]

    include_ranges = [
        ( 0x13A0, 0x13FF )
        ]
    
    alphabet = [
        get_char(code_point) for current_range in include_ranges
            for code_point in range(current_range[0], current_range[1] + 1)
    ]
    
    return ''.join(random.choice(alphabet) for i in range(length))

# flood fill section ----------------------------------- @~-------

############################################################################
########### DAMMERUNG CLASS COGNITOHAZARD ##################################
############################################################################
                                                                                
#                                  @@ (                                           
#                                @@/ @@                                           
#                                    @@@                                          
#                                   @%@,@  /@,(@ (                                
#                             &@@@@@@@@@@    *@&                                  
#                           @& @@@#    *@@@@@                                     
#                           @ @@ *(* @#  @##@@                                    
#                            @@@#.&@ @(@@%@/@.                                    
#                               @@@@@ **@@@                                       
#                                       @@@@@@                                    
#                                    @@@@@@@@@@@@(                    @@          
#                                   @@@@@@@@@@@@@@@                #  ,@@         
#                                 &@@   @@@@@   @@@                   @@          
#                                 @@ O  @@@@  O @(           @@@/  @@@@@*    #@  
#               /@@@@@@@@@@@@@    @@    @@@@   @@          @ (@@@@@@@@@@   ,@@@@  
#          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@          @%@@@      &@@@@  @ @@  
#       @@@@@@@.@  ,@@@@@@@@@@@@@@@@XXXXXXXXX@@@             @@ /#& @   .@ @@       
#     @@@@ /    @@@@@@@@@@@@@@@@@@@@@@XXXXXX@@@@@.         .@#@((@@(@@@&@@       
#    @@@@@   @@@@@@@@@@@@,@% &%@&@@@@@*@@@@@@@@@@@@@@@          @, @@@.@@         
#   @@@@   @@@@@@@@@@##                * (@@@@@@@@@@@@@@(                         
#  @@@   @@@@@@@@@@.                     @  @@@@@@@@@@@@@@                        
#  @@@. @@@@@@@@@@@@   *   &               @ @@@@@#@@@@@@@@%                      
#   @@( @@@@@@@.@@% .@      @                 @@@@ @ @@@@@@@*                     
#    @@ @@@@@@    @@.@    ,@    @             .@@@@ @ @@@@@@@                     
#     @@@@@@@@,    &@*     @@  @    @@       @@@@@@  /@@@@@@@                     
#        @@@@@@@@@@  @ @@ @@@ %@@@  ,@@@@@# /@@@@@@  @&@@@@@@                     
#         @@@@@@         @.@@  @@#@@&@@@ @@@@ *@@@@  *@@@@@@@                     
#           @@@@@       @@@,   @@/@   @# #   @@@@@  @%@@@@@@                      
#              @@@@@@@@@@@@ .@@,  @*  @@.  %@@@@@  @@@@@@@/                       
#                 @@@@@@@@@@@     ,@@@  @@(@@@@   @@@@@@                          
#                          @@@@& @ @ @@@@@@@@@@@@@@@                              
#                               @@@@@@                                            
def getAlgName(iAlg):
    global iAlgNames
    algDict = {i:iAlgNames[i] for i in range(len(iAlgNames))}
   
    return algDict.get(iAlg, str(iAlg))

# TODO: from enum import Enum

# 0: ready
# 1: needs processing
# 2: is processing
# 9: processing complete
# 255: locked, take no further action

@njit
def canBeTouched(bitboard, x, y):
    if x >= bitboard.shape[0]:
        return False
    elif y >= bitboard.shape[1]:
        return False
    elif bitboard[x,y] == 255:
        return False
    else:
        return True

@njit
def canChange(bitboard, x, y, newValue):
    if canBeTouched(bitboard, x, y):
        # return True if the newValue can overwrite the old one

        oldValue = bitboard[x,y]

        if oldValue == newValue:
            return False
        elif oldValue <= 0:
            return True
        elif oldValue == 255:
            return False
        elif newValue > oldValue:
            return True
        elif newValue <= 0:
            return True
        
        return False

@njit
def touchThatBit(bitboard, x, y, value):
    if canChange(bitboard, x, y, value):
        bitboard[x,y] = value

    return bitboard

@njit
def getTouchState(bitboard, x, y):
    if canBeTouched(bitboard, x, y):
        return bitboard[x,y]
    
    return -2

@njit
def find_first_numba(vec):
    """return the index of the first occurence of item in vec"""
    for i in range(len(vec)):
        if vec[i]:
            return i
    return None

@njit
def getBitboardNext(bitboard, value=1):
    # x = np.where(bitboard == value)
    # y = np.transpose(x)

    # for k in y:
    #     return (k[0],k[1])
        
    # return None

    # for idx, val in np.ndenumerate(bitboard):
    #     if val == value:
    #         return idx

    for i in range(len(bitboard)):
        for j in range(len(bitboard[i])):
            if bitboard[i][j] == value:
                return (i,j)
            
    return None

@njit
def createNumPyArray(width, height):
    return np.zeros(shape=(width,height), dtype=np.uint8)

# ASPARTAME STEPCHILD

def floodfill(img, xystart, 
              targetcolour, 
              newcolour, 
              dumpEvery=0,
              randomIt=0,
              sizeLimit=(0,0),
              choices=[],
              maxStackDepth=0,
              tippingPoint=25,
              defaultTip=True,
              compFunc=0,
              stamp=None,
              stampTrans=None,
              disobey=0,
              variantOverride=None):

    startTimeCheck()
    colorPrint.print_custom_palette(7, f'[   floodfill starts ------ {writeTimeCheck()} ---->') # {getDecree("","")}')

    width = img.size[0]
    height = img.size[1]

    showFloodedBoxes = getParam(5)

    p3 = getParam(6)
    variant = int(p3) if p3.isdecimal() else 1

    if variantOverride != None:
        variant = variantOverride

    global telemetry    

    (startx, starty) = xystart
    debugMode = False
    resetFloodfillStates()
   
    #from collections import deque
    workpile = []
    getpoint = workpile.pop

    global primaryColors
    global wackyColors
    global cocoColors
    global atariColors
    global currentUID

    iAlgOrig = randomIt

    choicesChosen = True

    # set some default colors for this algorithm
    if choices == []:
        choicesChosen = False

        if randomIt == 7:
            choices = primaryColors
        elif randomIt == 13:
            for wc in wackyColors:
                choices.append(wc)
        elif randomIt == 33:
            for c in cocoColors:
                choices.append(hex_to_rgb(c))

            for c in primaryColors:
                choices.append(c)

            for c in atariColors:
                choices.append(hex_to_rgb(c))

            random.shuffle(choices)
        else:
            for c in cocoColors:
                choices.append(hex_to_rgb(c))           

    if defaultTip:
        tippingPoint = getTippingPoint(randomIt)

    # paramState = dict(xystart=xystart, 
    #           targetcolour=targetcolour, 
    #           newcolour=newcolour, 
    #           dumpEvery=dumpEvery,
    #           randomIt=randomIt,
    #           sizeLimit=sizeLimit,
    #           choices=choices,
    #           maxStackDepth=maxStackDepth,
    #           tippingPoint=tippingPoint,
    #           defaultTip=defaultTip,
    #           compFunc=compFunc,
    #           stamp=stamp,
    #           stampTrans=stampTrans,
    #           disobey=disobey,
    #           variantOverride=variantOverride)

    # colorPrint.print_custom_palette(223, f"[{paramState}]")

    # del paramState
    
    minX = startx
    maxX = startx
    minY = starty
    maxY = starty
    maxCount=0
    count=0
    i = 0
    switcher = 0
    colorsKept = {}
    timesUsed = {}
    conseq = 0
    last_z = 0
    zCol = []
    mod_alg_value = 0

    pixdata = img.load()
    stmpdata = None

    if stamp != None:
        stmpdata = stamp.load()
        
    #bitboard = createNumPyArray(width, height)
    touched = {}
   
    workpile.append((startx,starty,0))
    #touchThatBit(bitboard, startx, starty, 1)

    addState(f"op: floodfill, iAlg: {randomIt} - {getAlgName(randomIt)}, tippingPoint: {tippingPoint}, x: {startx}, y: {starty}, maxStackDepth: {maxStackDepth}, variant: {variant}", None)    

    iPoint = 0
    
    emotion = getRandomWordSpecial("positive", "")

    #honk = getBitboardNext(bitboard, 1)

    stackDepth = 1

    while len(workpile) > 0 and (count < maxCount or maxCount == 0):
        # if honk != None:
        #     (x,y) = honk

        if isItTimeToDump(dumpEvery, iPoint):
            colorPrint.print_custom_rgb(f"workpile: {len(workpile)} -- {writeTimeCheck()} ----->", 255, 0, 88)

        x,y,stackDepth=getpoint()
        pointHash = hash((x,y))

        #bitState = getTouchState(bitboard, x, y)        

        if isItTimeToDump(dumpEvery, iPoint):
            colorPrint.print_custom_rgb(f"now: {(x,y)} ----- {writeTimeCheck()} ----->", 255, 0, 88)
            colorPrint.print_custom_rgb(f"x: {x} y: {y}, count: {count}, maxCount: {maxCount}", 255, 0, 188)
        
        skipItObviously = False
        
        # if bitState == 1:
        #     touchThatBit(bitboard, x, y, 2)
        # elif bitState == 2:
        #     pass
        # elif bitState == 9:
        #     pass
        # elif bitState == 255:
        #     pass

        if isItTimeToDump(dumpEvery, iPoint):            
            colorPrint.print_custom_palette(13, f"| floodfill: workpile loop begin @ {iPoint} --- {writeTimeCheck()} ---->")
            colorPrint.print_custom_palette(113, f"| x: {x}, y: {y}, count: {count}, maxCount: {maxCount} ---->")
            colorPrint.print_custom_palette(77, f"| feeling: {emotion} -------------------- ---->")

        if x < minX: minX = x
        if x > maxX: maxX = x
        if y < minY: minY = y
        if y > maxY: maxY = y
        
        if "floodfill" not in telemetry:
            telemetry['floodfill'] = {}

        if "max_stack_depth" not in telemetry['floodfill']:
            telemetry['floodfill']['max_stack_depth'] = {}        

        if iAlgOrig == -1:
            # now watch this drive
            randomIt = random.randint(1, maxFloodFillArg)

        if disobey > 0:
            uhahah = random.uniform(0, 1)

            if uhahah > disobey:
                # emotion = getRandomWordSpecial("negative", "")
                skipItObviously = True

        if maxStackDepth > 0 and stackDepth > maxStackDepth:
            skipItObviously = True

        # if isItTimeToDump(dumpEvery, iPoint):
        #     colorPrint.print_custom_rgb(f"bitboard[x,y]: {getTouchState(bitboard, x, y)}", 255, 0, 188)
        #     colorPrint.print_custom_rgb(f"canChange(bitboard, x, y, 9): {canChange(bitboard, x, y, 9)}", 255, 0, 188)

        # if not canChange(bitboard, x, y, 9):
        #     skipItObviously = True

        if pointHash in touched or skipItObviously:
            # if isItTimeToDump(dumpEvery, iPoint):
            #     colorPrint.print_custom_palette(119, f"| touched: {getTouchState(bitboard, x, y)}   |")
            pass
        elif (sizeLimit[0] == 0 or abs(x-startx) < sizeLimit[0]) and (sizeLimit[1] == 0 or abs(y-starty) < sizeLimit[1]):
            try:
                if isItTimeToDump(dumpEvery, iPoint):
                    colorPrint.print_custom_palette(33, f"| floodfill: touchy loop begin @ {iPoint} --- {writeTimeCheck()} ---->")
                    colorPrint.print_custom_palette(67, f"| x: {x}, y: {y}, count: {count}, maxCount: {maxCount}, compFunc: {compFunc} ---->")
                    colorPrint.print_custom_palette(37, f"| sizeLimit: {sizeLimit}, your mom's sizeLimit: infinity ---->")
                    colorPrint.print_custom_palette(47, f"| abs(x-startx): {abs(x-startx)}, abs(y-starty): {abs(y-starty)} ---->")
                    colorPrint.print_custom_palette(57, f"| x < img.size[0]: {x < img.size[0]}, y < img.size[1]: {y < img.size[1]} ---->")
                    colorPrint.print_custom_rgb(f"tc: {targetCheck(pixdata,x,y, targetcolour, compFunc)}", 255, 88, 111)

                #if randomIt != 2:
                    # 2 relies on this broken behavior of filling points multiple times
                    # touchThatBit(bitboard, x, y, 9)
                touched[pointHash] = 1
                
                if x < img.size[0] and y < img.size[1] and targetCheck(pixdata,x,y, targetcolour, compFunc):
                    # ---------- floodfill randomIt iAlgs begin here ----- switch statement tdlIdFloodfill --> 

                    newcolour, choices, x, y, switcher = floodFillDetail(randomIt, choices, tippingPoint, stamp, stampTrans, width, height, variant, startx, starty, choicesChosen, count, i, switcher, colorsKept, timesUsed, conseq, last_z, zCol, mod_alg_value, pixdata, stmpdata, x, y, newcolour)
                        
                    #writeOperationToDisk(currentUID, f"x: {x} y: {y} stackDepth: {stackDepth} maxStackDepth: {maxStackDepth} newcolour: {newcolour}")
                    pixdata[x,y] = newcolour
                        
                    count += 1
                    stackDepth += 1

                    if maxStackDepth == 0 or stackDepth < maxStackDepth:
                        # if canChange(bitboard, x-1, y, 1):
                        #     if x-1 >= 0 and x-1 < img.size[0] and y < img.size[1] and targetCheck(pixdata,x-1,y, targetcolour, compFunc):
                        #         touchThatBit(bitboard, x-1, y, 1)

                        # if canChange(bitboard, x+1, y, 1):
                        #     if x+1 < img.size[0] and y < img.size[1] and targetCheck(pixdata,x+1,y, targetcolour, compFunc):
                        #         touchThatBit(bitboard, x+1, y, 1)

                        # if canChange(bitboard, x, y-1, 1):
                        #     if y-1 >= 0 and x < img.size[0] and y-1 < img.size[1] and targetCheck(pixdata,x,y-1, targetcolour, compFunc):
                        #         touchThatBit(bitboard, x, y-1, 1)

                        # if canChange(bitboard, x, y+1, 1):
                        #     if x < img.size[0] and y+1 < img.size[1] and targetCheck(pixdata,x,y+1, targetcolour, compFunc):
                        #         touchThatBit(bitboard, x, y+1, 1)

                        if x-1 >= 0 and x-1 < img.size[0] and y < img.size[1] and hash((x-1,y)) not in touched and targetCheck(pixdata,x-1,y, targetcolour, compFunc):
                            workpile.append((x-1,y,stackDepth))

                        if x+1 < img.size[0] and y < img.size[1] and hash((x+1,y)) not in touched and targetCheck(pixdata,x+1,y, targetcolour, compFunc):
                            workpile.append((x+1,y,stackDepth))

                        if y-1 >= 0 and x < img.size[0] and y-1 < img.size[1] and hash((x,y-1)) not in touched and targetCheck(pixdata,x,y-1, targetcolour, compFunc):
                            workpile.append((x,y-1,stackDepth))

                        if x < img.size[0] and y+1 < img.size[1] and hash((x,y+1)) not in touched and targetCheck(pixdata,x,y+1, targetcolour, compFunc):
                            workpile.append((x,y+1,stackDepth))

                    if isItTimeToDump(dumpEvery, iPoint):
                        colorPrint.print_custom_palette(143, f"\t[ff dump: {writeTimeCheck()} --> ")
                        colorPrint.print_custom_palette(144, f"\tx: {x}, y: {y}")
                        colorPrint.print_custom_palette(149, f"\tstackDepth: {stackDepth}, maxStackDepth: {maxStackDepth}")
                        #colorPrint.print_custom_palette(141, f"\tbitboard[x,y]: {bitboard[x,y]}")
                        colorPrint.print_custom_palette(148, f"\tdump done ----------------------]")

            except Exception as e:
                logException(e)
        
        if isItTimeToDump(dumpEvery, iPoint):            
            colorPrint.print_custom_palette(7, f"| floodfill: workpile loop end @ {iPoint} --- {writeTimeCheck()} ---->")            
            colorPrint.print_custom_palette(229, f"| point: {[x,y,stackDepth]}, stackDepth: {stackDepth}, maxStackDepth: {maxStackDepth}")
            colorPrint.print_custom_palette(217, f"| ------------------ {writeTimeCheck()} ------------------")

        iPoint += 1

        #honk = getBitboardNext(bitboard, 1)

    if showFloodedBoxes == True or showFloodedBoxes in ["True", "true"]:
        for zX in range(minX, maxX):
            pixdata[zX, minY] = (0,255,0)
            pixdata[zX, maxY] = (0,0,255)

        for zY in range(minY, maxY):
            pixdata[minX, zY] = (255,255,0)
            pixdata[maxX, zY] = (255,0,0)

    # addState(f'colorsKept: {colorsKept}')

    colorPrint.print_custom_palette(228, f"| floodfill complete ------ {writeTimeCheck()} ----]")

    return count

ffSpecificState = 0
ffSpecificState2 = 0
ffSpecificState3 = 0
ffSpecificState4 = 0
ffSpecificState5 = 0

def resetFloodfillStates():
    global ffSpecificState
    global ffSpecificState2
    global ffSpecificState3
    global ffSpecificState4
    global ffSpecificState5

    ffSpecificState = 0
    ffSpecificState2 = 0
    ffSpecificState3 = 0
    ffSpecificState4 = 0
    ffSpecificState5 = 0

def floodFillDetail(randomIt, choices, tippingPoint, stamp, stampTrans, width, height, variant, startx, starty, choicesChosen, count, i, switcher, colorsKept, timesUsed, conseq, last_z, zCol, mod_alg_value, pixdata, stmpdata, x, y, newcolour):
    global ffSpecificState
    global ffSpecificState2
    global ffSpecificState3
    global ffSpecificState4
    global ffSpecificState5

    if stamp != None:
        # take the color from the stamp (map it somehow)
        xOff = x % (stamp.size[0])
        yOff = y % (stamp.size[1])

        newcolour = stmpdata[xOff, yOff]

        if stampTrans != None:
            if stampTrans == newcolour:
                newcolour = pixdata[x,y]
    elif randomIt == 0:
        pass
    elif randomIt == 1:
        # random
        if variant == 1 or variant > 15:
            if choices == []:
                newcolour = (random.randint(0,255),
                                            random.randint(0,255),
                                            random.randint(0,255))
            else:
                newcolour = random.choice(choices)                  
        elif variant < 5:
            z = (y << variant) + x

            (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
        elif variant < 10:
            z = x & y & variant

            (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
        elif variant <= 15:
            z = (x | y) & variant

            (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
                        
    elif randomIt == 2:
        # the tipping point
        if choices == []:
            newcolour = primaryColors[switcher]
        else:
            newcolour = choices[switcher]
                            
        ffSpecificState += 1

        if ffSpecificState % tippingPoint == 0:
            switcher += 1

        if choices == []:    
            if switcher > len(primaryColors) - 1:
                switcher = 0
        else:
            if switcher > len(choices) - 1:
                switcher = 0
                                
    elif randomIt == 3:
        # night random
        
        newcolour = (random.randint(0,128),
                     random.randint(0,50),
                     random.randint(0,100))
        
        i += 1
        if i % tippingPoint == 0:
            switcher += 1

        if switcher > len(primaryColors) - 1:
            switcher = 0

        if random.randint(0, 100) < (1 if variant == 0 else variant):
            newcolour = (random.randint(0,255),
                         random.randint(0,255),
                         random.randint(0,255))

            if choices != []:
                (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, i)

    elif randomIt == 4:
        # dark noise
        
        if variant >= 1:
            newcolour = random.choice(choices)
        else:
            newcolour = (random.randint(0,100),
                                     random.randint(0,128),
                                     random.randint(0,128))
    elif randomIt == 5:
        # bar grid
        if count == 0:
            ffSpecificState = [random.choice(choices),random.choice(choices),random.choice(choices)]
            random.shuffle(ffSpecificState)
                        
        if x % (3) == 0 or x % (7) == 0:
            newcolour = ffSpecificState[0]
        elif y % (5) == 0:
            newcolour = ffSpecificState[1]
        elif x % 5 == 0:
            newcolour = random.choice(choices)
        else:
            newcolour = ffSpecificState[2]
    elif randomIt == 6:
        # EGA noise
        if choicesChosen:
            newcolour = random.choice(choices)
        else:
            newcolour = random.choice(primaryColors)
    elif randomIt == 7:
        # long bars
        if variant == 1:
            mod_x = (count % tippingPoint == 0)
        elif variant == 0:
            mod_x = (count % (tippingPoint//2) == 0)
        else:
            mod_x = count % variant == 0

        if mod_x:
            newcolour = random.choice(choices)
    elif randomIt == 8:
        # the color of a tv tuned to a dead channel
        newcolour = (200, random.randint(0, 255), 200)
        newclist = [newcolour[0],newcolour[1],newcolour[2]]                        
        random.shuffle(newclist)
        newcolour = (newclist[0],newclist[1],newclist[2])
    elif randomIt == 9:
        # green noise
        if random.randint(0,2) == 1:
            if choicesChosen:
                newcolour = random.choice(choices)
            else:                            
                newcolour = (random.randint(0, 25),
                                             random.randint(128, 200),
                                             random.randint(0, 225))
    elif randomIt == 10:
        # bar john
        if variant == 1:
            mod_x = x & y
            mod_y = y

            if count == mod_x or x % tippingPoint == mod_x or mod_y % tippingPoint == mod_x:
                newcolour = random.choice(choices)
        elif variant == 0:
            mod_x = 1
            mod_y = random.randint(0, tippingPoint)

            if count == mod_x or x % tippingPoint == mod_x or mod_y % tippingPoint == mod_x:
                newcolour = random.choice(choices)
        elif variant < 6:
            mod_x = variant - 1
            mod_y = y

            if count == mod_x or x % tippingPoint == mod_x or mod_y % tippingPoint == mod_x:
                newcolour = random.choice(choices)
        else:
            mod_x = x - (x % 3)
            mod_y = y - (y % (variant * 10))

            z = (mod_y << 8) | mod_x

            mod_xond1 = (count == 0 or count % variant == 0)
            mod_xond2 = (x % variant == 0)
            mod_xond3 = (y % variant == 0)

            if mod_xond1 or mod_xond2 or mod_xond3:
                z = count
                            
            (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 11:
        # diamond hatch
        newcolour = choices[ffSpecificState2]

        if x % 3 == 0:
            ffSpecificState += 1

        if ffSpecificState % tippingPoint == 0:
            ffSpecificState2 += 1
            
        if ffSpecificState2 > len(choices) - 1:
            ffSpecificState2 = 0
    elif randomIt == 12:
        # wacky noise
        if x % (4) == 0 or x % (6) == 0:
            newcolour = choices[0]                            
        elif y % (3) == 0:
            newcolour = choices[1]                            
        else:
            newcolour = choices[2]

        if x % 5 == 0 or y % 5 == 0:
            random.shuffle(choices)
    elif randomIt == 13:
        # T_H_E__S_H_U_F_F_L_E_R______________________________________________
        if count % tippingPoint == 0 or (y % tippingPoint == 0):
            if len(choices) == 0:
                nclist = list(newcolour)
                random.shuffle(nclist)
                newcolour = (nclist[0], nclist[1], nclist[2])
            else:
                newcolour = random.choice(choices)
    elif randomIt == 14:
        # lil bars
        if count == 0:
            ffSpecificState = 0

        if count % 5 == 0:
            ffSpecificState += 1

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, ffSpecificState)
    elif randomIt == 15:
        # FLANNEL GRID
        if count % 2 == 0:                            
            switcher = 1
        else:
            switcher = -1

        tippingPoint = tippingPoint if variant == 0 else variant

        (mod_x, mod_y) = get_grid_vals(x, y, tippingPoint)
                        
        z = mod_y + (mod_x * switcher)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 16:
        # ever changing

        if variant == 1:
            mod_q = tippingPoint
        elif variant == 0:
            mod_q = random.randint(1, tippingPoint)
        else:
            mod_q = variant

        mod_x = x - (x % mod_q)
        mod_y = y - (y % mod_q)
        
        if count % 2 == 0:
            z = int(abs(math.hypot(mod_x, mod_y)))
        else:
            z = int(abs(math.hypot(mod_y, mod_x)))

        z = z - (z % mod_q)
        
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 17:
        # soldiers
        if count == 0:
            if len(choices) == 0:
                choices = [primaryColors[0], primaryColors[1], primaryColors[2]]
                                
            random.shuffle(choices)
        else:
            if y % 20 == 0:
                random.shuffle(choices)
                            
        newcolour = choices[0]
    elif randomIt == 18:
        # child soldiers
        mod_x = x - (x % 10)
                        
        if y % 8 == 0 or (x % 10 == 0 and y % 8 != 0):
            random.shuffle(choices)
            newcolour = choices[0]
            colorsKept[str(mod_x)] = newcolour
        else:                            
            (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 19:
        # horizontal bars
        mod_y = y - (y % (5 if variant == 0 else variant))
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_y)
    elif randomIt == 20:
        # small flannel
        if ffSpecificState == 0:
            z = y
            ffSpecificState = 1
        else:
            z = x
            ffSpecificState = 0
                            
        mod_x = z - (z % (tippingPoint if variant == 0 else variant))
                        
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 21:
        # vertical bars
        mod_x = x - (x % (5 if variant == 0 else variant))
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 22:
        # D E A D N I G H T S K Y ____________________________
        # copy of 3 initially
        if count == 0:
            ffSpecificState = 0

        if ffSpecificState == 0:
            newcolour = random.choice(choices)
            
            ffSpecificState2 += 1
            if ffSpecificState2 % tippingPoint == 0:
                switcher += 1

            if switcher > len(primaryColors) - 1:
                switcher = 0

            x3 = random.randint(0, 100)
            
            if x3 == 1:
                newcolour = (0,0,random.randint(0,150))
            elif x3 > 75:
                newcolour = random.choice(choices)

            for jj in range(0, 3):
                if newcolour[jj] > 150:
                    newcolour = replace_at_index(newcolour, jj, newcolour[jj] - 100)

            ffSpecificState = 1
        else:
            newcolour = random.choice(choices)
            ffSpecificState = 0
    elif randomIt == 23:
        # D E A D N I G H T G R O U N D ______________________
        if variant == 1:
            variant_d1 = 50
            variant_d2 = -3
            variant_d3 = -1
        elif variant == 0:
            variant_d1 = random.randint(1, 100)
            variant_d2 = -3
            variant_d3 = -2
        else:
            variant_d1 = int(variant * 3)
            variant_d2 = abs(variant_d1) * -1
            variant_d3 = abs(variant) * -1

        switcher = random.randint(0, 2)
        amount = 1 if random.randint(0, 1) == 1 else -1
                        
        if amount == 1 and newcolour[switcher] > variant_d1:
            amount = -1

        conseq += amount

        # don't keep going the same direction all the time
        if conseq < variant_d2 or conseq > abs(variant_d2):
            amount = amount * variant_d3
            conseq = amount
                        
        if variant == 1:
            newcolour = replace_at_index(newcolour, switcher, newcolour[switcher] + amount)
            a = [newcolour[0], newcolour[1], newcolour[2]]
            random.shuffle(a)
            newcolour = (a[0], a[1], a[2])
        else:
            if variant < 5:
                zzz = amount + conseq
                (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, zzz)
            else:
                zzz = amount + (conseq % tippingPoint)
                (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, zzz)
    elif randomIt == 24:
        # F U Z Z Y _ F L A N N E L __________________________
        if last_z == 0:
            z = y
            zz = x
            last_z = 1
        else:
            z = x
            zz = y
            last_z = 0
                            
        i24 = tippingPoint if variant == 0 else tippingPoint // 2 if variant == 1 else variant // 2

        mod_x = z - (z % i24)
        mod_y = zz - (zz % i24)
                        
        zqq = mod_x if variant % 2 == 0 else mod_y
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, zqq)                
    elif randomIt == 25:
        # T I M E _ L I M I T ________________________________
        mod_x = x - (x % tippingPoint)
        if str(mod_x) not in colorsKept:
            if len(choices) == 0:
                newcolour = (random.randint(0,255),
                                             random.randint(0,255),
                                             random.randint(0,255))
            else:
                newcolour = random.choice(choices)

            colorsKept[str(mod_x)] = newcolour
            timesUsed[str(mod_x)] = 1
        else:
            times = timesUsed[str(mod_x)]

            if times > tippingPoint:
                if len(choices) == 0:
                    newcolour = (random.randint(0,255),
                                             random.randint(0,255),
                                             random.randint(0,255))
                else:
                    newcolour = random.choice(choices)

                colorsKept[str(mod_x)] = newcolour

                timesUsed[str(mod_x)] = 1
            else:
                newcolour = colorsKept[str(mod_x)]
                timesUsed[str(mod_x)] = (times + 1)
    elif randomIt == 26:
        # 8 0 S  T R I P
        z = abs(x % tippingPoint - y % tippingPoint)
                        
        if str(z) not in colorsKept:
            newcolour = random.choice(choices)
                            
            colorsKept[str(z)] = newcolour
        else:
            newcolour = colorsKept[str(z)]
    elif randomIt == 27:
        # D_E_A_D__M_A_L_L__H_A_U_N_T_I_N_G______
        mod_y = y % tippingPoint                       
        mod_x = x % tippingPoint

        if count % tippingPoint == 0:
            newcolour = random.choice(choices)
            colorsKept[str(mod_y)] = newcolour
            colorsKept[str(mod_x)] = newcolour
        elif str(mod_y) not in colorsKept:
            newcolour = random.choice(choices)
            colorsKept[str(mod_y)] = newcolour
            colorsKept[str(mod_x)] = newcolour
        elif str(mod_x) not in colorsKept:
            newcolour = random.choice(choices)
            colorsKept[str(mod_y)] = newcolour
            colorsKept[str(mod_x)] = newcolour
        else:                            
            newcolour = random.choice([colorsKept[str(mod_y)], colorsKept[str(mod_x)]])
    elif randomIt == 28:
        # BIG ___ GRID __________________________________________________
        if count == 0:                            
            switcher = random.choice([1, -1])

        tippingPoint = tippingPoint if variant == 0 else variant

        (mod_x, mod_y) = get_grid_vals(x, y, tippingPoint)
                        
        mod_z = mod_y + (mod_x * switcher)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_z)
    elif randomIt == 29:
        # 8 bit sq outline
        if x % 5 == 0 or y % 5 == 0:
            newcolour = (0,0,0)
        else:
            mod_x = x + y - (y % tippingPoint) - (x % tippingPoint)
                            
            if str(mod_x) not in colorsKept:
                if len(choices) == 0:
                    r = random.randint(1, 255)
                    g = random.randint(r-1, 255)
                    b = random.randint(0, g)
                    rgb = [r, g, b]
                                
                    newcolour = (random.choice(rgb), random.choice(rgb), random.choice(rgb))
                else:
                    newcolour = random.choice(choices)
                                
                colorsKept[str(mod_x)] = newcolour
            else:
                newcolour = colorsKept[str(mod_x)]
    elif randomIt == 30:
        # P_I_G__G_R_I_D_______________________________________________________________________
        if count == 0:
            ffSpecificState2 = random.randint(5, 15)
            ffSpecificState = random.choice([1, -1])
            ffSpecificState3 = random.choice([2, 3, 4])

        (mod_x, mod_y) = get_grid_vals(x, y, ffSpecificState2)
                        
        mod_z = mod_y + (mod_x * ffSpecificState)

        if x % (ffSpecificState2 * ffSpecificState3) == 0 or y % (ffSpecificState2 * ffSpecificState3) == 0:
            mod_z = 999
                        
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_z)
    elif randomIt == 31:
        # M_E_L_T_I_N_G__P_O_T_________________________________________________________________
        x3 = x - (x % 8)
        y3 = y - (y % 8)
        z31 = x3 & y3
                        
        if count == 0:
            ffSpecificState2 = random.randint(5, 10)
            ffSpecificState = 0
        elif random.randint(0, ffSpecificState2) == 0:
            ffSpecificState = random.randint(0, len(choices))

        mod_x = str(ffSpecificState) + "_" + str(z31)
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 32:
        # SOUTHEAST CRUMBO                        
        mod_x = x - y + (x % tippingPoint//2) + (y % tippingPoint//2)                        

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 33:
        # TODDLER SOLDIERS
        if count == 0:
            ffSpecificState2 = random.randint(1, 5) * 5

        mod_x = y - (y % ffSpecificState2)
                        
        if count == 0:
            ffSpecificState = 0
            newcolour = random.choice(choices)
        else:
            if ffSpecificState != mod_x:
                newcolour = random.choice(choices)

        ffSpecificState = mod_x
    elif randomIt == 34:
        # U_N_I_F_O_R_M____________________________________________________________________________
        if count == 0:
            for c in choices:
                if str(c) not in timesUsed:
                    timesUsed[str(c)] = 0
                            
        newcolour = random.choice(choices)
        if str(newcolour) not in timesUsed:
            timesUsed[str(newcolour)] = 0
                                
        thisused = timesUsed[str(newcolour)]

        minUsed = thisused                        

        for p in timesUsed:
            if timesUsed[p] < minUsed:
                minUsed = timesUsed[p]
                newcolour = eval(p)

        timesUsed[str(newcolour)] += 1
    elif randomIt == 35:
        # S_L_O_W__C_H_A_N_G_E_S_________________________________________________________--__-_____

        # Determine step size
        ffSpecificState2 = variant if variant > 1 else (1 if variant == 0 else 5)

        mod_y = abs(y - starty) - (abs(y - starty) % ffSpecificState2)

        if not choicesChosen:
            if count == 0:
                direction = 1
                newcolour = random.choice(choices)
            else:
                iThis = random.randint(0, 2)
                if not (0 <= newcolour[iThis] + direction <= 255):
                    direction *= -1
                newcolour = replace_at_index(newcolour, iThis, newcolour[iThis] + direction)
        else:
            mod_x = x - (x % ffSpecificState2)
            mod_x2 = (x - ffSpecificState2) - ((x - ffSpecificState2) % ffSpecificState2)
            mod_x += mod_y

            prev_color = colorsKept.get(str(mod_x2))
            if str(mod_x) in colorsKept:
                newcolour = colorsKept[str(mod_x)]
            else:
                newcolour = random.choice(choices)
                while newcolour == prev_color:
                    newcolour = random.choice(choices)
                colorsKept[str(mod_x)] = newcolour
    elif randomIt == 36:
        # B_A_R__S_C_R_E_W________________________________________________________
        if count % 10 == 0:
            ffSpecificState = random.randint(-2, 2)

        mod_x = x - (x % tippingPoint) + (ffSpecificState * tippingPoint)

        if mod_x < 0:
            mod_x = 0
                            
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 37:
        # AND MOD
        mod_x = x & y

        if variant >= 1:
            mod_x = mod_x + (variant - (variant % tippingPoint))

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 38:
        # OR MOD
        mod_x = x | y

        if variant >= 1:
            mod_x = mod_x + (variant - (variant % tippingPoint))

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 39:
        # EXP MOD
        mod_x = x ^ y

        if variant >= 1:
            mod_x = mod_x + (variant - (variant % tippingPoint))
                        
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 40:
        # MODDLEDEE / MODDLEDUM
        if variant > 1:
            tippingPoint = variant

        if variant < 10:
            if variant % 2 == 1:
                mod_x = (x - (x % tippingPoint)) & (y - (y % tippingPoint))
            else:
                mod_x = (x - (x % tippingPoint)) | (y - (y % tippingPoint))

        else:
            if count % 2 == 0:
                mod_x = (x - (x % tippingPoint)) & (y - (y % tippingPoint))
            else:
                mod_x = (x - (x % tippingPoint)) | (y - (y % tippingPoint))

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 41:
        # mark at the boon
        if variant > 1:
            tippingPoint = variant

        if count % 2 == 0:
            ffSpecificState = abs(x - y)
        else:
            ffSpecificState = abs((y ^ x) & (x ^ y))

        mod_x = ffSpecificState - (ffSpecificState % tippingPoint)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 42:
        # HIGH INDIAN
        mod_x = int(abs(math.sin(x) + math.sin(y)) * 100)
        mod_x = mod_x - (mod_x % tippingPoint)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 43:
        # MUSHROOM EXPRESS
        mod_x = int(abs(math.sin(x) + math.cos(y)) * 100)
        mod_x = mod_x - (mod_x % tippingPoint)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 44:
        # LUIGI IN THE SKY WITH DIAMONDS
        mod_x = int(abs(math.cos(x) + math.sin(y)) * 100)
        mod_x = mod_x - (mod_x % tippingPoint)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 45:
        # KNEE FOLDER BURIED IN THE TUNDRA
        mod_x = int(abs(math.sin(x) + math.cos(y)) * 100)
        mod_y = int(abs(math.cos(x) + math.sin(y)) * 100)
        mod_z = random.choice([mod_x, mod_y])
        mod_z = mod_z - (mod_z % tippingPoint)                        

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_z)
    elif randomIt == 46:
        # ARC EXPLOSION
        ffSpecificState = tippingPoint if variant == 0 else variant

        x2 = abs(startx - x)
        y2 = abs(y - starty)

        mod_x = int(abs(math.hypot(x2, y2)))
        mod_x = mod_x - (mod_x % ffSpecificState)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 47:
        # SATURN'S BIRTHDAY
        ffSpecificState = 250 if variant == 0 else abs(250 - (variant*5))
        mod_x = int(abs(math.log1p(x) + math.log1p(y)) * ffSpecificState)
                        
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 48:
        # CIRCLE 8
        mod_x = int(abs(math.exp(x % tippingPoint))) + int(abs(math.exp(y % tippingPoint)))
        mod_x = mod_x - (mod_x % tippingPoint)
                        
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 49:
        # 4D FLANNEL
        if count == 0:
            ffSpecificState = 0

        if ffSpecificState == 0:
            if y > x:
                if y == 0:
                    y = 1
                mod_x = (x % y) ^ len(choices)
            elif y == x:
                if y == 0:
                    y = 1
                mod_x = (x+1 % y) ^ len(choices)
            else:
                if x == 0:
                    x = 1
                mod_x = (y % x) ^ len(choices)

            ffSpecificState = 1
        elif ffSpecificState == 1:
            mod_x = x ^ y
            ffSpecificState = 2
        elif ffSpecificState == 2:
            mod_x = int(abs(math.hypot(x, y)))
            ffSpecificState = 0
            
        mod_x = mod_x - (mod_x % tippingPoint)
                        
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 50:
        # PUSH WALLPAPER 
        mod_x = (x ^ y) % len(choices)
                        
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 51:
        # CRAYON NUKE
        mod_x = int(abs(math.hypot(startx-x, starty-y)))
        mod_x = mod_x - (mod_x % tippingPoint)

        mod_y = int(abs(math.log1p(x) - math.log1p(y)) * abs(math.log1p(x) + math.log1p(y)))

        if count % 2 == 0:
            mod_z = mod_x
        else:
            mod_z = mod_y
                        
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_z)
    elif randomIt == 52:
        # THE SMELL OF BLUEBERRY MARKERS
        mod_x = x ^ y ^ count
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 53:
        # HEROIN FROM TOPANGA                        
        (mod_x, mod_y) = get_grid_vals(x, y, tippingPoint)

        mod_x = ((y ^ x) % 25) & (mod_y | mod_x)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 54:
        # RESOGROVE FINISH
        ffSpecificState = 150 if variant == 0 else variant
        mod_x = ((x ^ y) & (int(time.time() * ffSpecificState) % 10))
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 55:
        # N_A_T_I_V_E___B_L_A_N_K_E_T____________________
        mod_x = int(abs(math.hypot(x, y))) ^ x
        mod_x = mod_x - (mod_x % tippingPoint)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 56:
        # TRY BALL MEAT

        if variant > 1:
            tippingPoint = variant
        elif variant == 0:
            tippingPoint = random.randint(1, tippingPoint)

        if y > x:
            mod_x = int(abs(math.hypot(y, x))) | x
        else:
            mod_x = int(abs(math.hypot(x, y))) | y
                            
        mod_x = mod_x - (mod_x % tippingPoint)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 57:
        # TURN THE KNOB
        z = random.choice([x, y])
        mod_x = int(abs(math.hypot(x, y))) | z
        mod_x = mod_x - (mod_x % tippingPoint)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 58:
        # X MARKS THE X
        mod_x = x ^ y
        mod_x = mod_x - (mod_x % tippingPoint)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 59:
        # JUTTING URANUS
        mod_x = int(abs(math.hypot(x, y)) * math.pi)                        
        i59 = tippingPoint if variant == 0 else variant
                        
        z = mod_x ^ y
        z = z - (z % i59)
                        
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 60:
        # TINY DECO
        if y > x:
            mod_x = int(abs(math.hypot(y, x)) * math.pi)                        
                            
            z = mod_x ^ x
        else:
            mod_x = int(abs(math.hypot(x, y)) * math.pi)                        
                        
            z = mod_x ^ y
                            
        z = z - (z % tippingPoint)
                        
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 61:
        # ONCE I SHOT GOD ON BROADWAY
        if random.randint(0, 1) == 0:
            mod_x = x & y
        else:
            mod_x = x | y

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 62:
        # YEAH
        z = random.randint(0, 1)
                        
        if (y > x and z == 0) or (x > y and z == 1):
            mod_x = x & y
        else:
            mod_x = x | y

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 63:
        # ARKY BARKY
        if count == 0:
            ffSpecificState = 0

        if ffSpecificState == 0:
            mod_x = int(abs(math.hypot(x, y)))
            mod_x = mod_x - (mod_x % tippingPoint)
            ffSpecificState = 1
        elif ffSpecificState == 1:
            mod_x = int(abs(math.log1p(x) - math.log1p(y)) * 25)
            ffSpecificState = 2
        elif ffSpecificState == 2:
            mod_x = x ^ y
            ffSpecificState = 3
        elif ffSpecificState == 3:
            mod_x = x & y
            ffSpecificState = 0
                        
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 64:
        # D_I_R_T_Y___C_A_R_P_E_T_________________________
        if count == 0:
            ffSpecificState = 1
            ffSpecificState2 = tippingPoint

        if ffSpecificState >= (5 if variant == 0 else variant):
            mod_x = x ^ y if variant != 15 else x | y
                        
            (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)                            
            ffSpecificState = 1                           
        else:
            tippingPoint = ffSpecificState2 * ffSpecificState
            mod_x = x + y - (x % tippingPoint) - (y % tippingPoint)
                        
            (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
            ffSpecificState += 1
    elif randomIt == 65:
        # UNIQUE VAN FIBER
        if count == 0:
            ffSpecificState = 0
            ffSpecificState3 = 5
            ffSpecificState2 = tippingPoint

        if ffSpecificState3 <= 0:
            ffSpecificState3 = 5
                            
        tippingPoint = ffSpecificState2 * ffSpecificState3
                        
        if ffSpecificState == 0:
            mod_x = (x - (x % tippingPoint)) & (y - (y % tippingPoint))
            ffSpecificState = 1
        else:
            mod_x = (x - (x % tippingPoint)) | (y - (y % tippingPoint))
            ffSpecificState = 0
            ffSpecificState3 -= 1
                        
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 66:
        # ?_??_???_????_?????________________________________
        mod_x = int(x * math.pi) | int(y * math.pi)
        mod_y = int(x * math.e) | int(y * math.e)

        z = mod_x & mod_y
        z = z - (z % tippingPoint)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 67:
        # P_L_A_Y_I_N_G___T_H_E____S_T_A_R______________________
        if count == 0:
            zchoices = [2, 3, 5, 7, 11, 47]
            z3choices = [1, 2, 4, 8, 16]
            
            ffSpecificState = random.choice(zchoices)
            ffSpecificState2 = ffSpecificState

            while ffSpecificState2 == ffSpecificState:
                ffSpecificState2 = random.choice(zchoices)

            ffSpecificState3 = random.choice(z3choices)
            ffSpecificState4 = ffSpecificState3
            ffSpecificState5 = ffSpecificState3

            while ffSpecificState4 == ffSpecificState3:
                ffSpecificState4 = random.choice(z3choices)

            while ffSpecificState5 == ffSpecificState3:
                ffSpecificState5 = random.choice(z3choices)
                
        if count % 2 == 0:
            mod_x = math.sqrt(ffSpecificState)
        else:
            mod_x = math.sqrt(ffSpecificState2)
            
        z8 = int(x * mod_x) ^ int(y * mod_x)
        z9 = int(x * mod_x) | int(y // mod_x)
        z7 = x & y

        z = (z8 & z9) | z7 | ffSpecificState3 | ffSpecificState4 | ffSpecificState5
        z = z - (z % tippingPoint)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 68:
        # T_H_E_ F_E_E_L_I_N_G_S_ N_E_V_E_R_ T_O_L_D__________-__________---_____                        
        if count % 2 == 0:
                            # 66
            mod_x = int(x * math.pi) | int(y * math.pi)
            mod_y = int(x * math.e) | int(y * math.e)

            z = mod_x & mod_y
            z = z - (z % tippingPoint)                            
        else:
            z = x ^ y                            
                            
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 69:
        # NICE.
        if count % 2 == 0:
            mod_x = int(x * 6.969) | int(y * 6.969)
            mod_y = int(x // 6.969) | int(y // 6.969)
        else:
            mod_x = int(x * 6.969) & int(y * 6.969)
            mod_y = int(x // 6.969) & int(y // 6.969)
                        
        z = mod_x | mod_y | 69
        z = z - (z % tippingPoint)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 70:
        # EL DITHERO ___________________________________
        if count % 2 == 0:
            mod_x = int(abs(math.hypot(x, y))) ^ x                        
        else:
            mod_x = x ^ y

        mod_x = mod_x - (mod_x % tippingPoint)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 71:
        # CUBE 5: THE FINAL CUBING               
        if len(zCol) <= 0:
            for i71 in range(0, len(choices)):
                zCol.append(i71)
                            
            random.shuffle(zCol)

        mod_x2 = x - (x % 2)
        mod_y2 = y - (y % 2)
                           
        z = zCol.pop()

        zz71 = count % 4
                        
        if zz71 == 0 or zz71 == 2:
            mod_x = (z ^ (mod_x2 | mod_y2) ^ (mod_x2 & mod_y2)) % len(choices)
        elif zz71 == 1:
            mod_x = (x & y) % len(choices)
        else:
            mod_x = (x | y) % len(choices)
                        
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 72:
        # HOW_COULD_IT_ALL_FALL_ONE_DAY______________________________72_____________                      
        if count == 0:
            ffSpecificState = random.randint(10, 100)

        i72 = 2 if variant == 0 else variant

        if count % i72 == 0:
            bg1 = x
            bg2 = y
                            
            if x > bg2:
                bg1 = y
                bg2 = x

            qz = random.randint(bg1, bg2)

            zl = [x, y, qz]

            zl.sort(reverse=True)
                           
            z3 = int(abs(math.hypot(zl[0], zl[1])) * math.pi)
            zz = z3 | random.choice(zl)
            z = zz - (zz % ffSpecificState)

            (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
        else:
            z = x + y - (x % ffSpecificState) - (y % ffSpecificState) 
            (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 73:
        # SHE NEVER NOTICED
        if count % 2 == 0:
            mod_y = int(x * math.pi) | int(y * math.pi)
            mod_x = int(x * math.e) | int(y * math.e)

            z = mod_x & mod_y
            z = z - (z % tippingPoint)
        else:
            mod_y = int(x * math.e) | int(y * math.pi)
            mod_x = int(x * math.e) | int(y * math.pi)

            z = mod_x & mod_y
            z = z - (z % tippingPoint)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 74:
        # AEROPLANE IN THE SEA WITH DARKNESS
        x74 = x - (x%4)
        y74 = y - (y%4)

        if count % 2 == 0:
            mod_y = int(x74 * math.pi) | int(y74 * math.pi)
            mod_x = int(x74 * math.e) | int(y74 * math.e)

            z = mod_x & mod_y
            z = z - (z % tippingPoint)
        else:
            mod_y = int(x74 * math.e) | int(y74 * math.pi)
            mod_x = int(x74 * math.e) | int(y74 * math.pi)

            z = mod_x & mod_y
            z = z - (z % tippingPoint)                  

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 75:
        # BIG SQUARE PUSSY
        i75 = tippingPoint if variant <= 1 else variant

        if x % i75 == 0 or y % i75 == 0:
            z = variant
        else:
            mod_y = y - (y % i75)
            mod_x = x - (x % i75)

            z = (mod_y << 4) + mod_x

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 76:
        # SCOOL FENCE
        if variant == 1:
            tippingPoint = 20
        elif variant == 2:
            tippingPoint = 10
        elif variant > 1:
            tippingPoint = variant
        elif variant == 0 and count == 0:
            ffSpecificState = random.randint(5, 25)
            tippingPoint = ffSpecificState
        else:
            tippingPoint = ffSpecificState

        i76 = random.randint(0, 125)
        skool = (i76,i76,i76)

        y76 = y - (y % tippingPoint)
        x76 = x - (x % tippingPoint)

        z = random.randint(1, len(choices))

        mod_y2 = abs(height - y) % tippingPoint
        mod_x = abs(x - y) % tippingPoint
        mod76 = tippingPoint // 2

        if abs(mod_x - mod76) < 1:
            z = 0
            (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, [skool], z)
        elif abs((x % tippingPoint) - mod_y2) < 1:
            z = 0
            (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, [skool], z)
        else:
            (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 77:
        # the echo of silence reverberates off the walls of my being
        # but no one can hear it out there
        # it's sad and dark and lonely in your casket
        # when there are no nail marks on the inside
        # and two miles of dirt above
        # i lived on a pile of rocks
        # where i'll die after the final reckoning
        # when the life drains from your body
        # and the earth's, and the universe
        # implodes

        ffSpecificState = tippingPoint if variant == 0 else variant

        if i % ffSpecificState == 0:
            switcher = 1 - switcher

        if switcher == 0:                            
            mod_x = int(abs(math.hypot(x, y)))
            mod_x = mod_x - (mod_x % ffSpecificState)                            
        else:
            mod_x = x + y - (x % ffSpecificState) - (y % ffSpecificState)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 78:
        # RIBBED SQUARES NO TOE
        mod_y = y - (y % tippingPoint)
        mod_x = x - (x % tippingPoint)

        if count % 4 == 0:
            z = (mod_y << 8) + mod_x
        elif count % 2 == 0:
            z = (mod_y << 4) + mod_x
        else:
            z = (mod_x << 4) + mod_y

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 79:
        # ALONE ON A FRIDAY NIGHT

        if variant == 1:
            if switcher == 0 or i % tippingPoint * 5 == 0:
                switcher = random.randint(1, 8)
        else:
            switcher = variant

        if switcher == 1:
            mod_x = x + y - (x % tippingPoint) - (y % tippingPoint)
        elif switcher == 2:
            mod_x = x + y - (x % tippingPoint) + (y % tippingPoint)
        elif switcher == 3:
            mod_x = x + y + (x % tippingPoint) - (y % tippingPoint)
        elif switcher == 4:
            mod_x = x + y + (x % tippingPoint) + (y % tippingPoint)
        elif switcher == 5:
            mod_x = x - y - (x % tippingPoint) - (y % tippingPoint)
        elif switcher == 6:
            mod_x = x - y - (x % tippingPoint) + (y % tippingPoint)
        elif switcher == 7:
            mod_x = x - y + (x % tippingPoint) - (y % tippingPoint)
        else:
            mod_x = x - y + (x % tippingPoint) + (y % tippingPoint)                 
                                                
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 80:
        # SWAPPER WHOPPER
        if mod_alg_value == 0:
            mod_alg_value = random.uniform(3,8)

        dx, dy = x - startx, y - starty
        ang = (math.atan2(dy, dx) + math.pi) / (2*math.pi)  # 0..1
        r = math.hypot(dx, dy)

        mod_z = x - y + (x % tippingPoint) + (y % tippingPoint)
        mod_x2 = x if y != 0 else width - x

        if variant == 1:
            if count % 2 == 0:
                mod_x = int(mod_x2 * mod_alg_value) | int(y * mod_alg_value)
                mod_y = int(mod_x2 // mod_alg_value) | int(y // mod_alg_value)
            else:
                mod_x = int(mod_x2 * mod_alg_value) & int(y * mod_alg_value)
                mod_y = int(mod_x2 // mod_alg_value) & int(y // mod_alg_value)

            z = mod_x | mod_y | tippingPoint
            z = z - (z % tippingPoint)
        elif variant == 2:
            mod_x = int(mod_x2 * mod_alg_value) | int(y * mod_alg_value)
            mod_y = int(mod_x2 // mod_alg_value) | int(y // mod_alg_value)
                            
            z = mod_x | mod_y | tippingPoint
            z = z - (z % tippingPoint)
        elif variant == 3:
            mod_x = int(mod_x2 * mod_alg_value) & int(y * mod_alg_value)
            mod_y = int(mod_x2 // mod_alg_value) & int(y // mod_alg_value)
                            
            z = mod_x | mod_y | tippingPoint
            z = z - (z % tippingPoint)
        elif variant == 4:
            mod_x = int(mod_x2 * mod_alg_value) ^ int(y * mod_alg_value)
            mod_y = int(mod_x2 // mod_alg_value) ^ int(y // mod_alg_value)
                            
            z = mod_x | mod_y | tippingPoint
            z = z - (z % tippingPoint)
        elif variant == 14:
            mod_x = int(mod_x2 * mod_alg_value) ^ int(y * mod_alg_value)
            mod_y = int(mod_x2 // mod_alg_value) ^ int(y // mod_alg_value)
                            
            z = mod_x & mod_y & tippingPoint
            z = z - (z % tippingPoint)
        else:
            zz = (variant % 10)
            zz = zz if zz != 0 else tippingPoint

            if count % zz == 0:
                mod_x = int(mod_x2 * mod_alg_value) | int(y * mod_alg_value)
                mod_y = int(mod_x2 // mod_alg_value) | int(y // mod_alg_value)
            else:
                mod_x = int(mod_x2 * mod_alg_value) & int(y * mod_alg_value)
                mod_y = int(mod_x2 // mod_alg_value) & int(y // mod_alg_value)

            z = mod_x | mod_y | tippingPoint
            z = z - (z % tippingPoint)

        if count % 5 == 0:
            z = int(r)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 81:
        # DIGITAL OPULENCE
        if count == 0:
            ffSpecificState = random.randint(2, 12)
            ffSpecificState2 = random.randint(2, 12)            

        variantState = 16
        
        if variant > 1:
            variantState = variant

        mod_x = x - (x % ffSpecificState)
        mod_y = y - (y % ffSpecificState2)
                        
        z = (mod_x << variantState) | mod_y

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 82:
        # THAT PROBABLY LOOKS INSANE
        if count == 0:
            switcher = random.choice([1, -1])

        mod_x = int(x * math.pi) | int(x * math.pi)
        mod_y = int(y * math.e) | int(y * math.e)

        z = mod_x | mod_y
        #z = z - (z % tippingPoint)

        (mod_q, mod_r) = get_grid_vals(x, y, tippingPoint)
        mod_s = mod_q + (mod_r * switcher)
                        
        i82 = y % tippingPoint
        i82_2 = x % tippingPoint

        i82_3 = (tippingPoint // 2)                        

        if (i82 <= i82_3 and i82_2 < i82_3) or ((i82 > (i82_3 + 1)) and (i82_2 >= (i82_3 + 1))):
            z = mod_s

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 83:
        # GAME CRASH FOREST

        if count == 0:
            ffSpecificState = random.randint(2, variant+3)
            ffSpecificState2 = random.randint(2, variant+3)

            while ffSpecificState == ffSpecificState2:
                ffSpecificState2 = random.randint(2, 12)

        variantState = 2

        mod_x = x - (x % ffSpecificState)
        mod_y = y - (y % ffSpecificState2)
                        
        if count % 2 == 0:
            z = (mod_x << variantState) | mod_y
        else:
            z = (mod_y << variantState) | mod_x

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 84:
        # 15 DISCONTINUED SODAS                
                                       
        # | 0 | 1 |
        # |---+---|
        # | 2 | 3 |        

        # Align to tippingPoint grid
        mod_y = y - (y % tippingPoint)
        mod_x = x - (x % tippingPoint)
        z = (mod_y << 4) + mod_x

        # Variant handling
        if variant == 0:
            mod_84 = random.randint(1, 25)
        elif variant == 1:
            mod_84 = 25
        else:
            mod_84 = variant

        # 3×3 grid position
        mod_ff_x = (x // mod_84) % 3
        mod_ff_y = (y // mod_84) % 3

        # Distance and sum, floored to tippingPoint multiples
        mod_z = int(math.hypot(x, y)) - (int(math.hypot(x, y)) % tippingPoint)
        mod_q = x + y - (x % tippingPoint) - (y % tippingPoint)

        # Lookup table for final value
        outcomes = {
            (0, 0): z,
            (0, 1): mod_z,
            (0, 2): x ^ y,
            (1, 0): mod_q,
            (1, 1): x & y,
            (1, 2): x | y,
            (2, 0): mod_q - mod_z,
            (2, 1): mod_q & mod_z,
            (2, 2): mod_q | mod_z
        }
        mod_84 = outcomes[(mod_ff_x, mod_ff_y)]

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_84)
    elif randomIt == 85:
        # PLUTO TAILOR
        if count == 0:
            ffSpecificState = random.randint(5, 15)
            ffSpecificState2 = random.randint(4, ffSpecificState + 10)
            ffSpecificState3 = random.randint(2, 8)
                            
        mod_c = count % ffSpecificState3
                        
        mod_x = x - (x % ffSpecificState - mod_c)
        mod_y = y - (y % ffSpecificState2 + mod_c)
                        
        mod_z = ( mod_x << 2 ) | mod_y
                        
        newcolour = get_kept_color_avoid_sides(colorsKept, choices, mod_z, limit=5)
                        
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_z)
    elif randomIt == 86:
        # DEMIURGE OVERKILL
        if count == 0:
            ffSpecificState = random.random() * 10

        if count % 4 == 0:
            mod_x = int(x * ffSpecificState) | int(y * ffSpecificState)
            mod_y = int(x // ffSpecificState) | int(y // ffSpecificState)
            z = mod_x | mod_y | int(ffSpecificState)
            z = z - (z % tippingPoint)
            (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
        elif count % 2 == 0:
            mod_x = int(x * ffSpecificState) & int(y * ffSpecificState)
            mod_y = int(x // ffSpecificState) & int(y // ffSpecificState)
            z = mod_x | mod_y | int(ffSpecificState)
            z = z - (z % tippingPoint)
            (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
        else:
            if ffSpecificState2 == 0:
                z = y
                zz = x
                ffSpecificState2 = 1
            else:
                z = x
                zz = y
                ffSpecificState2 = 0
                                
            mod_x = z - (z % tippingPoint)
            mod_y = zz - (zz % tippingPoint)

            (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_x)
            (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_y)
    elif randomIt == 87:
        # idk yet
        if ffSpecificState == 0:
            ffSpecificState = random.uniform(3,8)   

        mod_y = y - (y % tippingPoint)
        mod_x = x - (x % tippingPoint)

        z = ((mod_y << 2) + (mod_x << 4)) | random.randint(0,8)

                        # mod_z = x - y + (x % tippingPoint) + (y % tippingPoint)
                        # mod_x2 = x if y != 0 else width - x
                        # mod_tp = tippingPoint if variant == 1 else variant

                        # if count % 2 == 0:
                        #     mod_x = int(mod_x2 * ffSpecificState) | int(y * ffSpecificState)
                        #     mod_y = int(mod_x2 // ffSpecificState) | int(y // ffSpecificState)
                        # else:
                        #     mod_x = int(mod_x2 * ffSpecificState) & int(y * ffSpecificState)
                        #     mod_y = int(mod_x2 // ffSpecificState) & int(y // ffSpecificState)
                        
                        # z = mod_x | mod_y | tippingPoint
                        # z = z - (z % tippingPoint)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 88:
        # no men no bears no women
        if y % 2 == 0:
            z = abs(x + y)
        else:
            z = abs(y - x)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 89:
        # binders full of women and bears

        ffSpecificState = ((y % 6) + (x % 6)) % 6

        outcomes = {
            (0): 0,
            (1): int(abs(math.log1p(x) - math.log1p(y)) * 25),
            (2): x ^ y,
            (3): x & y,
            (4): x + y,
            (5): x | y,
            (6): x - y
        }

        z = outcomes[(ffSpecificState)]

        if ffSpecificState == 0:
            mod_x = int(abs(math.hypot(x, y)))
            z = mod_x - (mod_x % tippingPoint)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 90:
        vr = variant if variant != 0 else 20

        if count % 2 == 0:
            # Distance from origin
            dist = math.hypot(x, y)

            # Angle in radians, normalized to 0..1
            angle = (math.atan2(y, x) + math.pi) / (2 * math.pi)

            # Create spiral index (z) — distance influences base color, angle offsets it
            z = int((dist / 5) + (angle * len(choices))) % len(choices)
        elif count % 3 == 0:
            a = (x % vr) + (y % vr)
            b = (x % vr + 5) ^ (y % vr + 10)
            z = (a * b) % len(choices)
        else:
            tide_x = math.sin(x / 7.0) * len(choices) / 2
            tide_y = math.cos(y / 9.0) * len(choices) / 2
            z = int((tide_x + tide_y + len(choices)) % len(choices))
            
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 91:
        # i don't remember which this is a mix of
        z1 = int(abs(math.hypot(x, y))) ^ x
        z2 = int(abs(math.hypot(x, y))) ^ y
        z1 = z1 - (z1 % tippingPoint)
        z2 = z2 - (z2 % tippingPoint)

        z = z1 | z2

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 92:
        # SEDUCING MEDUSAS
        if abs(startx - x) < 2 and (count % 2 == 0):
            z = random.randint(0, len(choices)-1)
        elif abs(starty - y) < 2:
            z = 0
        elif abs(startx - x) < 2:
            z = 1
        elif abs(startx - x) < 5:
            z = 0
        elif abs(starty - y) < 5:
            z = 1
        elif x < startx and y < starty and (count % 2 == 0):
            z = 2
        elif x > startx and y > starty and (count % 2 == 0):
            z = 3
        elif y % tippingPoint == 0:
            z = random.randint(2, 3)
        elif count % 16 == 0:
            z = (x ^ y) | (x & y) | tippingPoint
        elif count % 8 == 0:
            if x < y:
                z = tippingPoint << (count % 8)
            else:
                z = tippingPoint << (count % 3)
        elif count % 2 == 0:
            z = (variant + 1) * (count % 4)        
            z = z // tippingPoint
        else:
            z = int(abs(math.hypot(x,y)) * variant)
                        
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 93:
        # 84-2
        # Align to tippingPoint grid
        mod_y = y - (y % tippingPoint)
        mod_x = x - (x % tippingPoint)
        z = (mod_y << 4) + mod_x

        # Variant handling
        if variant == 0:
            mod_84 = 12
        elif variant == 1:
            mod_84 = 25
        elif variant == 25:
            mod_84 = random.randint(1, 25)
        else:
            mod_84 = variant

        # grid position
        mod_ff_x = (x // mod_84) % 4
        mod_ff_y = (y // mod_84) % 4

        # Distance and sum, floored to tippingPoint multiples
        mod_z = int(math.hypot(x, y)) - (int(math.hypot(x, y)) % tippingPoint)
        mod_q = x + y - (x % tippingPoint) - (y % tippingPoint)

        # Lookup table for final value
        outcomes = {
            (0, 0): z,
            (0, 1): mod_z,
            (0, 2): x ^ y,
            (0, 3): y ^ x,
            (1, 0): mod_q,
            (1, 1): x & y,
            (1, 2): x | y,
            (1, 3): (x & y) | mod_q,
            (2, 0): mod_q - mod_z,
            (2, 1): mod_q & mod_z,
            (2, 2): mod_q | mod_z,
            (2, 3): (y | x) & z,
            (3, 0): mod_q << mod_z,
            (3, 1): mod_q >> mod_z,
            (3, 2): x + y,
            (3, 3): x - y
        }

        if count % 4 == 0:
            mod_84 = outcomes[(mod_ff_x, mod_ff_x)]
        elif count % 3 == 0:
            mod_84 = outcomes[(mod_ff_y, mod_ff_y)]
        elif count % 2 == 0:
            mod_84 = outcomes[(mod_ff_x, mod_ff_y)]
        else:
            mod_84 = outcomes[(mod_ff_y, mod_ff_x)]

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, mod_84)
    elif randomIt == 94:
        # circle grid

        cell = variant + 5 if variant > 0 else 15

        # circle geometry
        r = int(cell * 0.38)                 # circle radius (≈ 76% of cell width)
        band = max(1, cell // 12)            # ring thickness

        # center of the current cell
        cx = (x // cell) * cell + cell // 2
        cy = (y // cell) * cell + cell // 2

        # distance from pixel to cell center
        d = math.hypot(x - cx, y - cy)

        # optional checkerboard parity to add variation between cells
        parity = ((x // cell) + (y // cell)) & 1

        # pick palette index by region: background / ring / interior
        if d <= r - band:
            # inside the circle
            # z = (2 * parity) % len(choices)
            shade = int((d / max(1, r)) * len(choices))
            z = (shade + 2 * parity) % len(choices)
        elif r - band < d < r + band:
            # ring band
            z = (2 * parity + 1) % len(choices)
        else:
            # background
            z = (2 * parity + 2) % len(choices)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 95:
        # 95
        cell = variant + 5
        cx = (x // cell) * cell + cell // 2
        cy = (y // cell) * cell + cell // 2
        d = max(abs(x - cx), abs(y - cy))           # Chebyshev distance
        band = max(1, cell // 8)
        ring = (d // band) % len(choices)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, ring)
    elif randomIt == 96:
        # 96
        cx, cy = startx, starty
        dx, dy = x - cx, y - cy
        ang = (math.atan2(dy, dx) + math.pi) / (2*math.pi)  # 0..1
        r = math.hypot(dx, dy)
        k_ang = 16 if variant == 0 else max(4, variant)
        k_rad = 10
        a_id = int(ang * k_ang)
        r_id = int(r / max(1.0, (width+height) / (2*k_rad)))
        z = (a_id + r_id) % len(choices)
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 97:
        # 97
        w = variant if variant > 0 else 32
        h = max(8, w // 2)
        row = y // h
        col = (x + (w//2 if (row & 1) else 0)) // w
        z = (row + 3*col) % len(choices)
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 98:
        # 98
        sx = (x / 23.0); sy = (y / 19.0)
        v = math.sin(sx) + math.sin(1.7*sy + 0.6*math.sin(sx*0.7))
        idx = int(((v + 2.0) * 0.25) * len(choices)) % len(choices)
        z = idx
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 99:
        # 99
        # interleave lower 10 bits
        xx, yy = x & 1023, y & 1023
        m = 0
        for b in range(10):
            m |= ((xx >> b) & 1) << (2*b)
            m |= ((yy >> b) & 1) << (2*b+1)
        z = (m // 128) % len(choices)
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 100:
        # 100
        cell = variant + 10 if variant > 0 else 40
        u = (x % cell) < (cell//2)
        v = (y % cell) < (cell//2)
        over = (u ^ v)
        band = max(2, cell//10)
        near_h = (y % cell) < band or (y % cell) > cell - band
        near_v = (x % cell) < band or (x % cell) > cell - band
        z = (2*over + near_h + 2*near_v) % len(choices)
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 101:
        # 101
        cell = variant + 10 if variant > 0 else 64
        gx, gy = x // cell, y // cell
        # random center inside this cell
        rnd = _hash2(gx, gy)
        cx = gx*cell + (rnd & (cell-1))
        cy = gy*cell + ((rnd>>16) & (cell-1))
        d = int(math.hypot(x - cx, y - cy))
        z = (d // max(1, cell//6)) % len(choices)
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 102:
        # 102
        cell = variant + 10 if variant > 0 else 48
        gx, gy = x // cell, y // cell
        lx, ly = x % cell, y % cell
        diag = (lx + ly) < cell
        z = ( (gx + gy) + (1 if diag else 0) ) % len(choices)
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 103:
        # 103
        cell = variant + 10 if variant > 0 else 56
        gx, gy = x // cell, y // cell
        orient = _hash2(gx, gy) & 1      # 0=horiz, 1=vert
        band = max(2, cell // 10)
        stripe = ((x if orient else y) % (2*band)) < band
        z = ( (gx + 2*gy) + (1 if stripe else 0) ) % len(choices)
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 104:
        # PUDDLE KINK
        if count == 0:
            switcher = random.choice([-1,1])

        sectors = 12 if variant == 0 else max(8, variant)
        dx, dy = x - startx, y - starty
        ang = (math.atan2(dy, dx) + math.pi) / (2*math.pi)   # 0..1        
        r = math.hypot(dx, dy)
        sec = int(ang * sectors)
        z = sec % len(choices)

        z += int(r // 5) * switcher

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 105:
        # CIRCLE CIRCLES

        if count % 2 == 0:
            dx, dy = x - startx, y - starty
            r = math.hypot(dx, dy)
            freq = 0.08 if variant == 0 else 0.02 + 0.004*variant
            v = 0.5 * (1 + math.sin(r * 2*math.pi*freq))
            z = int(v * (len(choices)-1))
        else:
            ffSpecificState = tippingPoint if variant == 0 else variant

            x2 = abs(startx - x)
            y2 = abs(y - starty)

            mod_x = int(abs(math.hypot(x2, y2)))
            z = mod_x - (mod_x % ffSpecificState)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 106:
        # 106
        cell = variant + 10 if variant > 0 else 24
        gx, gy = x // cell, y // cell
        n = _hash2(gx, gy) % len(choices)
        # add small intra-cell wobble so edges aren’t too crisp
        wob = ((x % cell) + (y % cell)) // max(1, cell//6)
        z = (n + wob) % len(choices)
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 107:
        s = variant if variant > 0 else 36
        q = (math.sqrt(3)/3 * (x - startx) - 1/3 * (y - starty)) / s
        r = (2/3 * (y - starty)) / s
        qi, ri = int(round(q)), int(round(r))
        z = (qi + 2*ri) % len(choices)
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 108:
        k = 5
        acc = 0.0
        for i in range(k):
            a = i * (2*math.pi/5)
            acc += math.cos((x*math.cos(a)+y*math.sin(a)) / (12 if variant==0 else max(6,variant)))
        z = int(((acc/k)+1)*0.5 * (len(choices)-1)) % len(choices)
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 109:
        # map to 9 bits square (512)
        xx, yy = x & 511, y & 511
        def _rot(n, x, y, rx, ry):
            if ry == 0:
                if rx == 1:
                    x = n-1 - x; y = n-1 - y
                x, y = y, x
            return x, y
        def hilbert_idx(n, x, y):
            d = 0; s = n//2
            while s>0:
                rx = 1 if (x & s) else 0
                ry = 1 if (y & s) else 0
                d += s*s*((3*rx) ^ ry)
                x, y = _rot(s, x, y, rx, ry)
                s //= 2
            return d
        h = hilbert_idx(512, xx, yy)
        z = (h // 2048) % len(choices)
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 110:
        gx = x ^ (x >> 1)
        gy = y ^ (y >> 1)
        z = ((gx ^ gy) // 128) % len(choices)
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 111:
        dx, dy = x - startx, y - starty
        r = math.hypot(dx, dy)
        ang = math.atan2(dy, dx)
        a = (r * 0.12) + (ang * 3.0)   # tune gains
        z = int((a % (2*math.pi)) / (2*math.pi) * len(choices))
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 112:
        sx0, sy0 = width//4, height//3
        sx1, sy1 = 3*width//4, 2*height//3
        d0 = int(math.hypot(x - sx0, y - sy0))
        d1 = int(math.hypot(x - sx1, y - sy1))
        z = ((d0 ^ d1) // 9)
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 113:
        s = 120.0 if variant==0 else max(40.0, float(variant)*10.0)
        u = math.sin(y/s) + 0.5*math.sin((x+y)/(s*0.7))
        v = math.sin(x/s) - 0.5*math.sin((x-y)/(s*0.9))
        t = math.sin(6.28318*(u*0.5+v*0.5))
        z = int(((t+1)*0.5) * (len(choices)-1))
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 114:
        n = 8 if variant==0 else max(3, variant%16)
        dx, dy = x - startx, y - starty
        ang = (math.atan2(dy, dx) + math.pi) % (2*math.pi)
        wedge = (ang % (2*math.pi/n))
        # mirror within wedge
        if wedge > math.pi/n: wedge = (2*math.pi/n) - wedge
        r = math.hypot(dx, dy)
        z = int((r*0.05 + wedge*(n/3.0)) % len(choices))
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 115:
        cell = variant + 10 if variant > 0 else 24
        gx, gy = x//cell, y//cell
        # carve either east or south per cell deterministically
        carve_east = (((gx*73856093) ^ (gy*19349663)) & 1) == 0
        in_corridor = ((x % cell) < 3) or ((y % cell) < 3) or (carve_east and ((y%cell)<6)) or ((not carve_east) and ((x%cell)<6))
        z = (gy + 2*gx + (3 if in_corridor else 0)) % len(choices)
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 116:
        # BADPERSON WHAMMY
        
        # superformula params
        if count == 0:
            ffSpecificState = random.randint(3, 7)

        ffSpecificState2 = int(variant / 15) + 1

        m = variant % 15 if variant != 0 else ffSpecificState
        a = b = 1.0
        n1, n2, n3 = ffSpecificState*.1*ffSpecificState2, 1.7, 1.7
        dx, dy = (x - startx)/180.0, (y - starty)/180.0
        r = math.hypot(dx, dy)
        ang = math.atan2(dy, dx)
        t = (abs(math.cos(m*ang/4)/a)**n2 + abs(math.sin(m*ang/4)/b)**n3)**(-1/n1)
        z = int(abs(r - t) * 40)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 117:
        pitch = variant + 4 if variant>0 else 6
        kind = ((x//pitch) ^ (y//pitch)) & 1
        sub = (x % (3*pitch)) // pitch
        idx = (sub + (0 if kind else 1)) % 3
        z = idx % len(choices)
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 118:
        # ZIGZAG FEAST
        cell = variant + 8 if variant > 0 else 20
        gx, gy = x//cell, y//cell
        lx, ly = x%cell, y%cell

        A = [
            0b10101,
            0b00101,
            0b11100,
            0b00001,
            0b10100,
            0b01011,
            0b01110,
        ]

        sx = (lx * 5) // max(1, cell)
        sy = (ly * 7) // max(1, cell)
        bit = (A[sy] >> (4 - sx)) & 1 if 0<=sx<5 and 0<=sy<7 else 0
        z = (bit + gx + 2*gy) # % len(choices)
        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 119:
        # --- cell geometry ---
        cell = variant + 16 if variant > 0 else 22
        gx, gy = x // cell, y // cell          # cell coords
        lx, ly = x % cell,  y % cell           # local coords in cell

        # map local coords to 5x7 glyph coords
        sx = (lx * 5) // max(1, cell)
        sy = (ly * 7) // max(1, cell)

        # --- 5x7 bitmaps for T, D, L (MSB = leftmost pixel) ---
        FONT_5x7 = {
            "T": [
                0b11111,
                0b00100, 0b00100, 0b00100,
                0b00100, 0b00100, 0b00100,
            ],
            "D": [
                0b11110,
                0b10001, 0b10001, 0b10001,
                0b10001, 0b10001, 0b11110,
            ],
            "L": [
                0b10000,
                0b10000, 0b10000, 0b10000,
                0b10000, 0b10000, 0b11111,
            ],
        }

        # choose which glyph this cell shows
        glyph = "TDL"[(gx + gy) % 3]
        row_bits = FONT_5x7[glyph][sy] if (0 <= sx < 5 and 0 <= sy < 7) else 0
        bit = (row_bits >> (4 - sx)) & 1   # 1 if inside the glyph stroke

        # palette index: base from cell coords, flipped by glyph bit
        base = (3*gx + 5*gy) % len(choices)
        z = (base + (len(choices)//2 if bit else 0)) % len(choices)

        (colorsKept, newcolour) = get_kept_color(colorsKept, newcolour, choices, z)

    # the end of the tour
    return newcolour, choices, x, y, switcher

def _hash2(i, j, seed=0x9E3779B1):
    v = (i * 0x27d4eb2d) ^ (j * 0x85ebca6b) ^ seed
    v ^= (v >> 15); v *= 0x2c1b3c6d; v ^= (v >> 12); v *= 0x297a2d39; v ^= (v >> 15)
    return v & 0xffffffff

@njit
def isItTimeToDump(dumpEvery, iPoint):
    return dumpEvery > 0 and (iPoint > 0) and (iPoint % dumpEvery == 0 or iPoint % dumpEvery == 1)

def getTippingPoint(randomIt):
    if randomIt == 7:
        tippingPoint = 170
    elif randomIt == 10:
        tippingPoint = random.randint(4, 300)        
    elif randomIt in [18, 20, 23, 27, 33, 36, 40, 41, 46, 47, 51, 65]:
        tippingPoint = 5
    elif randomIt in [28, 32, 42, 43, 44, 45, 59, 60, 64]:
        tippingPoint = 7
    elif randomIt == 29:
        tippingPoint = 10
    elif randomIt in [13, 24, 25]:
        tippingPoint = 15        
    elif randomIt == 26:
        tippingPoint = 25                
    elif randomIt == 66:
        tippingPoint = random.randint(5, 25)
    elif randomIt in [75, 77, 78, 80]:
        tippingPoint = random.randint(15, 30)
    elif randomIt in [82]:
        tippingPoint = random.randint(5, 15)
    else:
        tippingPoint = random.randint(5, 25)

    return tippingPoint

def get_kept_color(colorsKept, newcolour, choices, mod_x):
    return get_kept_color_new(colorsKept, newcolour, choices, mod_x)

def get_kept_color_new(colorsKept, newcolour, choices, mod_x, override=None):
    if override is not None:
        return (colorsKept, override)
    
    if str(mod_x) not in colorsKept:
        if len(choices) == 0:
            newcolour = (random.randint(0,255),
                         random.randint(0,255),
                         random.randint(0,255))
        else:
            newcolour = random.choice(choices)

        colorsKept[str(mod_x)] = newcolour
    else:
        newcolour = colorsKept[str(mod_x)]

    return (colorsKept, newcolour)

def get_kept_color_avoid_sides(colorsKept, choices, mod_x, limit=0):
    newcolour = 0
    
    y1 = mod_x - 1
    y2 = mod_x + 1
    
    avoid1 = colorsKept[str(y1)] if str(y1) in colorsKept else 0
    avoid2 = colorsKept[str(y2)] if str(y2) in colorsKept else 1
    
    newcolour = get_new_color_only(colorsKept, choices, mod_x)
    
    if len(choices) > 0 and len(choices) <= 2:
        return newcolour
        
    iLimit = 0
    
    while (newcolour == avoid1 or newcolour == avoid2) and (iLimit < limit or limit <= 0):
        newcolour = get_new_color_only(colorsKept, choices, mod_x)
        iLimit += 1
            
    return newcolour

def get_new_color_only(colorsKept, choices, mod_x):
    newcolour = (0,0,0)
    
    if str(mod_x) not in colorsKept:
        if len(choices) == 0:
            newcolour = (random.randint(0,255),
                         random.randint(0,255),
                         random.randint(0,255))
        else:
            newcolour = random.choice(choices)
    else:
        newcolour = colorsKept[str(mod_x)]
        
    return newcolour    
            
def get_grid_vals(x, y, tippingPoint):
    mod_x = x - (x % tippingPoint)
    mod_y = y - (y % tippingPoint)

    return (mod_x, mod_y)    

def gradientFill(img, innerColor, outerColor, x1=0, y1=0, x2=0, y2=0):    
    pixdata = img.load()

    if x2 == 0:
        x2 = img.size[0]

    if y2 == 0:
        y2 = img.size[1]

    # find the center of the rectangle we've specified in the params
    xCenter = x1 + ((x2 - x1) // 2.0)
    yCenter = y1 + ((y2 - y1) // 2.0)
    halfWidth = (x2 - x1) // 2.0
    
    for y in range(y1, y2):
        for x in range(x1, x2):
            
            # Find the distance to the center
            distanceToCenter = math.sqrt((x - xCenter) ** 2 + (y - yCenter) ** 2)

            # Make it on a scale from 0 to 1
            distanceToCenter = float(distanceToCenter) // (math.sqrt(2) * halfWidth)

            # Calculate r, g, and b values
            r = outerColor[0] * distanceToCenter + innerColor[0] * (1 - distanceToCenter)
            g = outerColor[1] * distanceToCenter + innerColor[1] * (1 - distanceToCenter)
            b = outerColor[2] * distanceToCenter + innerColor[2] * (1 - distanceToCenter)

            pixdata[x, y] = (int(r), int(g), int(b))
            
    return img

def _color_diff(color1, color2):
    """
    Shamelessly stolen from PIL/Pillow.
    Uses 1-norm distance to calculate difference between two values.
    """
    if isinstance(color2, tuple):
        return sum(abs(color1[i] - color2[i]) for i in range(0, len(color2)))
    else:
        return abs(color1 - color2)

def _color_target_check(color1, color2, threshold=25):
    if _color_diff(color1, color2) <= threshold:
        return True
    return False

def targetCheck(pixdata, x, y, targ, compFunc=0):
    chk = False

    try:
        colorDiff = 15

        if compFunc == -1:
            return True

        # TODO: remove, used passed in only
        cf = getParam(2)

        if cf != "" and cf != 0:
            colorDiff = cf

        if callable(compFunc):
            chk = compFunc(pixdata[x,y], targ)
            return chk
        elif compFunc == 1:
            colorDiff = 15
        elif compFunc == 2:
            colorDiff = 2
        elif compFunc == 3:
            colorDiff = 25
        elif compFunc > 3:
            colorDiff = compFunc        

        if compFunc == 0:
            if targ == pixdata[x,y]:
                chk = True        
        elif compFunc >= 1:
            chk, diff, iTarg = checkPointTargDiff(pixdata[x,y], targ, colorDiff)

            #doTimeCheck(f"compFunc: {compFunc} colorDiff: {colorDiff} // pnt: {pnt} targ: {targ} // chk: {chk} diff: {diff} iTarg: {iTarg} ")
                            
        return chk
        
    except Exception as e:        
        logException(e)
        return False

def targetCheck0(pnt, targ, compFunc=0):
    chk = False

    try:
        colorDiff = 15

        # TODO: remove, used passed in only
        cf = getParam(2)

        if cf != "" and cf != 0:
            colorDiff = cf

        if callable(compFunc):
            chk = compFunc(pnt, targ)
            return chk
        elif compFunc == 1:
            colorDiff = 15
        elif compFunc == 2:
            colorDiff = 2
        elif compFunc == 3:
            colorDiff = 25
        elif compFunc > 3:
            colorDiff = compFunc        

        if compFunc == -1:
            chk = True
        elif compFunc == 0:
            if targ == pnt:
                chk = True
        elif compFunc >= 1:
            chk, diff, iTarg = checkPointTargDiff(pnt, targ, colorDiff)

            #doTimeCheck(f"compFunc: {compFunc} colorDiff: {colorDiff} // pnt: {pnt} targ: {targ} // chk: {chk} diff: {diff} iTarg: {iTarg} ")
                            
        return chk
        
    except Exception as e:        
        logException(e)
        
        rootLogger.error(str(datetime.datetime.now()))
        rootLogger.error("iTarg: " + str(iTarg))
        rootLogger.error("len(diff): " + str(len(diff)))
        rootLogger.error("diff: " + str(diff))
        rootLogger.error("len(targ): " + str(len(targ)))
        rootLogger.error("targ: " + str(targ))
        rootLogger.error("len(pnt): " + str(len(pnt)))
        rootLogger.error("pnt: " + str(pnt))
        rootLogger.error("---------------------")
        
        return False

@njit
def checkPointTargDiff(pnt, targ, colorDiff):
    """diff: will contain differences of rgba values """
    diff = [0] * len(targ)
            
    for iTarg in range(len(targ)-1):
        ci = 0
        if len(pnt) >= iTarg:
            ci = targ[iTarg] - pnt[iTarg]
            diff[iTarg] = ci

    chk = True
            
    for iTarg in range(len(diff)-1):            
        if abs(diff[iTarg]) > colorDiff:
            chk = False

    return chk, diff, iTarg

def getPaletteFromImage(sourceimg, distance=25, limit=5):
    return getPaletteFromImageFull(sourceimg, distance, limit)[0]

def getPaletteFromImageFull(sourceimg, distance=25, limit=5):
    img = sourceimg.copy()
    img = img.convert("RGB")
    pixdata = img.load()

    colors = dict()

    choices = []

    for x in range(0, img.size[0]):
        for y in range(0, img.size[1]):
            c = pixdata[x, y]

            if c not in colors:
                colors[c] = 1
            else:
                colors[c] += 1

    sc = sorted(list(colors.items()), key=itemgetter(1), reverse=True)

    for c in sc:
        (r, g, b) = c[0]
        thisc = (r, g, b)

        if r > distance or g > distance or b > distance:
            if not thisc in choices:
                choices.append(thisc)

        if len(choices) >= limit:
            break

    return (choices, sc)

def getPalette(choiceStatic=""):
    palette = getInsertWalk(palettesPath, choiceStatic=choiceStatic)

    choices = []

    addState(f"palette: {palette}")

    img = Image.open(palette)
    pixdata = img.load()

    y = 0

    # setting range is a hack because all the current palettes have big stripes
    
    for y in range(0, img.size[1]-100, 100):
        for x in range(0, img.size[0]-1, 50):
            z = pixdata[x,y]

            if len(z) > 3:
                z = z[:3]

            if z not in choices:
                choices.append(z)

    addState(f"choices: {choices}")
    rootLogger.debug(f"choices: {choices}")

    return choices

def getStamp(choiceStatic=""):
    doTimeCheck("getStamp starts")
    random.seed()
    stamp = getInsertWalk(stampPath, choiceStatic=choiceStatic)
    doTimeCheck("stamp gotten")

    img = Image.open(stamp)
    img = img.convert("RGBA")
    img = resizeToMinMax(img, maxW=75, maxH=75, minW=50, minH=50)

    return img

def getStampGenerated():
    img = ""

    try:
        width = 50
        height = 50
        
        img = Image.new("RGB", (width,height), "#0000ff")
        pixdata = img.load()

        cs = [getRandomColor() for i in range(random.randint(2, 10))]

        j = 0
        for x in range(0, img.size[0]):
            i = j
            
            for y in range(0, img.size[1]):
                c = cs[i]
                
                pixdata[x,y] = c
                i += 1
                
                if i > len(cs) - 1:
                    i = 0

            j += 1
            
            if j > len(cs) - 1:
                j = 0
                    
    except Exception as e:
        img = writeImageException(e)

    return img

def getShelfTopItems(pathfilter):
    d = shelve.open(shelfFileName)
    yy = [i for i in list(d.items()) if pathfilter in i[0]]
    yyy = sorted(yy, key=itemgetter(1), reverse=True)    
    
    d.close()

    yyylen = len(yyy)
    yyycut = int(yyylen // 4)
    output = [i[0] for i in yyy[:yyycut]]
    
    return output

# HARVEST CRAP
    
def getShelf(filename):
    d = shelve.open(shelfFileName)
    imgcount = 0
    
    if(filename in d):
        imgcount = d[filename]

    d.close()

    return imgcount

def setShelf(filename):
    d = shelve.open(shelfFileName)
    imgs = 0
    
    if(filename in d):
        imgs = d[filename]

    imgs += 1
    
    d[filename] = imgs
    
    d.close()
    
    return 

def getInt(i, default=0):
    if isinstance(i, int):
        return i
    
    x = int(i) if i.isdecimal() else default
    return x

def getPathById(i=0):
    global allPaths
    i = getInt(i)

    if i < len(allPaths):
        return allPaths[i]
    
    return allPaths[0]

def getInsertById(i=0, choiceStatic="", extensions=defaultInsertExtensions):
    doTimeCheck("getInsertById starts: " + str(i))
    return getInsertWalkPaths([getPathById(i)], choiceStatic, extensions)

def getInsertWalk(basepath, choiceStatic="", extensions=defaultInsertExtensions):
    return getInsertWalkPaths([basepath], choiceStatic, extensions)

def getInsertWalkPaths(paths, choiceStatic="", extensions=defaultInsertExtensions):
    images = []

    isPublic = False

    for basepath in paths:
        if "publicdomain" in basepath and "special" not in basepath:
            isPublic = True
        elif "special" in basepath:
            isPublic = False
        else:
            isPublic = False
            
        for root, dirs, files in os.walk(basepath):
            for leImg in files:
                if leImg[-4:].lower() in extensions:
                    images.append(os.path.join(root, leImg))

    chosen = ""
    
    random.seed()

    chosen = random.choice(images)
    
    if isPublic:
        # filter out the top x% used images
        # so different things come up more often
        
        topitems = getShelfTopItems("publicdomain")

        for ti in topitems:
            images.remove(ti)

        chosen = random.choice(images)

        while chosen in topitems:
            chosen = random.choice(images)

    if choiceStatic != "":
        for c in images:
            if c.endswith(choiceStatic):                
                chosen = c
                break

    # log that we're using this image
    setShelf(chosen)

    print("chosen: " + chosen)
    addState(f"chosen: {chosen}")
    
    return chosen

def getChoicesWalk(basepath, exts=defaultInsertExtensions):
    images = []

    for root, dirs, files in os.walk(basepath):
        for leImg in files:
            if leImg[-4:].lower() in exts:
                images.append(os.path.join(root, leImg))

    return images

def getInsert(choiceStatic="", pathOfInserts=""):
    if pathOfInserts == "":
        pathOfInserts = publicDomainImagePath

    files = os.listdir(pathOfInserts)
    possibles = []

    chosen = ""
    
    for f in files:
        # TODO: extensions - use defaultInsertExtensions
        if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".gif") or f.endswith(".tif"):
            possibles.append(f)

            if f[:-4].lower() == choiceStatic.lower():
                chosen = f

    if chosen == "":
        random.seed()
        chosen = random.choice(possibles)
       
    insertPath = pathOfInserts + chosen
    
    return insertPath        
 
def getFont(choiceStatic=""):
    pathFonts = fontPath
    
    global possibleFonts
       
    chosen = ""

    global fontBlacklist

    if len(possibleFonts) == 0:
        loadedFiles = []

        for root, dirs, files in os.walk(pathFonts):
            for leImg in files:
                if leImg[-4:].lower() in ('.ttf', '.otf'):               
                    qq = os.path.join(root, leImg)
                    loadedFiles.append(qq)

        for f in loadedFiles:
            if f.lower().endswith(".ttf") or f.lower().endswith(".otf"):
                blacklisted = False

                # check against the blacklist

                for b in fontBlacklist:
                    if b.lower() in f.lower():
                        blacklisted = True

                if not blacklisted:
                    possibleFonts.append(f)

    if choiceStatic != "":
        for f in possibleFonts:
            if f.lower() == choiceStatic.lower():
                chosen = f
            elif f.lower().find(choiceStatic.lower()) >= 0:
                chosen = f

    if chosen == "":
        chosen = random.choice(possibleFonts)
   
    return chosen

def draw_word_wrap(img, draw, text, xpos=0, ypos=0, max_width=130,
                   fill=(0,0,0), font=ImageFont.load_default()):
    '''Draw the given ``text`` to the x and y position of the image, using
    the minimum length word-wrapping algorithm to restrict the text to
    a pixel width of ``max_width.``
    '''
    #
    text_size_x, text_size_y = dropin_text_size(draw,text, font=font)
    remaining = max_width
    space_width, space_height = dropin_text_size(draw,' ', font=font)
    
    # use this list as a stack, push/popping each line
    output_text = []
    
    # split on whitespace...    
    for word in text.split(None):
        word_width, word_height = dropin_text_size(draw,word, font=font)
        if word_width + space_width > remaining:
            output_text.append(word)
            remaining = max_width - word_width
        else:
            if not output_text:
                output_text.append(word)
            else:
                output = output_text.pop()
                output += ' %s' % word
                output_text.append(output)
            remaining = remaining - (word_width + space_width)
            
    for text in output_text:
        draw.text((xpos, ypos), text, font=font, fill=fill)
        ypos += text_size_y
        
# graphics methods ------------------------------------------------------------

def shakeharderboy(lengthY, lengthX, pixdata):       
    walker = 0
    walkerLimit = 5

    ohSnapFactor = 20
    ohSnapper = 0

    lineMover = 50
    lineTuple = (0,0,0)
    lineColor = 255
    
    for y in range(lengthY):
        for x in range(lengthX):
            letuple = pixdata[x,y]
            r = letuple[0]
            g = letuple[1]
            b = letuple[2]
            a = letuple[3]
                       
            if(x - lineMover == y):
                lineColor = random.randint(200, 255)
            
                if(lineTuple[0] > 0):
                    lineTuple = (0,lineColor,0,0)
                elif(lineTuple[1] > 0):
                    lineTuple = (0,0,lineColor,0)
                else:
                    lineTuple = (lineColor,0,0,0)
                
                r = lineTuple[0]
                g = lineTuple[1]
                b = lineTuple[2]
            elif(x - lineMover > y):
                r = b
                b = b + g
                g = g + ohSnapper
                r = r * walker
            else:
                b = r // 2
                g = r - b
                r = r - (ohSnapper * ohSnapper)
                b = b * walker
            
            # safety stuff
            if(r < 0): r = r * -1
            if(g < 0): g = g * -1
            if(b < 0): b = b * -1
            
            if(r > 255): r = r - 255
            if(g > 255): g = g - 255
            if(b > 255): b = b - 255

            if(abs(250 - x) > random.randint(30,90)):
                pixdata[x,y] = (r,g,b,a)
            else:
                try:
                    pixdata[x,y] = pixdata[x+5,y+4]
                except:
                    pixdata[x,y] = (random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255))
                    
                    pass
                
            walker = walker + 1
            if(walker > walkerLimit):
                walker = 0
                
        ohSnapper = ohSnapper + 1
        if(ohSnapper > ohSnapFactor):
            ohSnapper = 0

    return pixdata

def keepfuckinthatdata(lengthY, lengthX, pixdata):       
    walker = 0
    walkerLimit = 5

    ohSnapFactor = 20
    ohSnapper = 0

    lineMover = 50
    lineTuple = (0,0,0)
    lineColor = 255
    
    for y in range(lengthY):
        for x in range(lengthX):
            letuple = pixdata[x,y]
            r = letuple[0]
            g = letuple[1]
            b = letuple[2]
            a = letuple[3]
                       
            if(x - lineMover == y):
                lineColor = random.randint(200, 255)
            
                if(lineTuple[0] > 0):
                    lineTuple = (0,lineColor,0,0)
                elif(lineTuple[1] > 0):
                    lineTuple = (0,0,lineColor,0)
                else:
                    lineTuple = (lineColor,0,0,0)
                
                r = lineTuple[0]
                g = lineTuple[1]
                b = lineTuple[2]
            elif(x - lineMover > y):
                r = b
                b = b + g
                g = g + ohSnapper
                r = r * walker
            else:
                b = r // 2
                g = r - b
                r = r - (ohSnapper * ohSnapper)
                b = b * walker
            
            # safety stuff
            if(r < 0): r = r * -1
            if(g < 0): g = g * -1
            if(b < 0): b = b * -1
            
            if(r > 255): r = r - 255
            if(g > 255): g = g - 255
            if(b > 255): b = b - 255

            if(abs(250 - x) > random.randint(30,90)):
                pixdata[x,y] = (r,g,b,a)
            else:
                try:
                    pixdata[x,y] = pixdata[x+5,y+4]
                except:
                    pixdata[x,y] = (random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255))
                    
                    pass
                
            walker = walker + 1
            if(walker > walkerLimit):
                walker = 0
                
        ohSnapper = ohSnapper + 1
        if(ohSnapper > ohSnapFactor):
            ohSnapper = 0

    return pixdata

def textStroke(draw, x, y, textString, fon, fillColor):
    draw.text((x+1,y+1), textString, font=fon, fill=fillColor)
    draw.text((x+1,y-1), textString, font=fon, fill=fillColor)
    draw.text((x-1,y+1), textString, font=fon, fill=fillColor)
    draw.text((x+1,y-1), textString, font=fon, fill=fillColor)
    
    return draw

def textStrokeExtra(draw, x, y, textString, fon, fillColor, reps):
    for i in range(0, reps):
        draw.text((x+i,y+i), textString, font=fon, fill=fillColor)
        draw.text((x+i,y-i), textString, font=fon, fill=fillColor)
        draw.text((x-i,y+i), textString, font=fon, fill=fillColor)
        draw.text((x-i,y-i), textString, font=fon, fill=fillColor)

    return draw

def textStrokeExtraMultiline(draw, x, y, textString, fon, fillColor, spacing, align, reps):
    for i in range(0, reps):
        draw.multiline_text((x+i, y+i), textString, font=fon, fill=fillColor, spacing=spacing, align=align)
        draw.multiline_text((x+i, y-i), textString, font=fon, fill=fillColor, spacing=spacing, align=align)
        draw.multiline_text((x-i, y+i), textString, font=fon, fill=fillColor, spacing=spacing, align=align)
        draw.multiline_text((x-i, y-i), textString, font=fon, fill=fillColor, spacing=spacing, align=align)

    return draw

def saveToWrapper_Insert(path):
    global wrapperData
    global currentUID
    uid = currentUID

    wrapperData["inserts_used"][uid].append(path)
    return

def saveToWrapper(key, path):
    global wrapperData
    global currentUID
    uid = currentUID

    try:        
        wrapperData[key][uid].append(path)
    except Exception as ex:
        rootLogger.debug(ex)        
        pass

    return

def saveForXanny(img):
    global wrapperData
    global currentUID
    global telemetry

    uid = currentUID    

    #wrapperData["xannies"][uid] = manager.list()

    wrapperData["xannies"][uid].append(img)
    
    #ColorPrint.logger_info("saveForXanny // telemetry: " + str(telemetry))

    telemetry['xanny_count'] += 1    

    return

def addState(statement, params={}, self=None):
    stm = TdlState(statement)
    saveToWrapper("function_states", str(stm))

    return

# TDL functions ---------------------------------------- @~-------

def flagship(fontSize=128):   
    try:        
        choices = getInputPalette()

        fImg = getOneSafeFunc()
        img = fImg()
       
        draw = ImageDraw.Draw(img)

        fontPath = getFont()
        word = getTDL(primer="tdldl")

        spacing = -40
        
        # shrink font until it fits
        text_size_x, text_size_y = img.size[0] + 100, img.size[1] + 100

        while text_size_x > img.size[0] - 10 or text_size_y > img.size[1] - 10:
            fontSize -= 1
            fon = ImageFont.truetype(fontPath, fontSize)
            bbox = draw.multiline_textbbox((0, 0), word, font=fon, align="center", spacing=spacing, stroke_width=3)
            text_size_x = bbox[2] - bbox[0]
            text_size_y = bbox[3] - bbox[1]

        fillColor = random.choice(choices)
        strokec = getInverse(fillColor)

        # compute top-left so the whole block is centered
        x = (img.size[0] - text_size_x) // 2 - bbox[0]
        y = (img.size[1] - text_size_y) // 2 - bbox[1]

        draw.multiline_text(
            (x, y), word, 
            font=fon, 
            fill=fillColor, 
            spacing=spacing, 
            align="center", 
            stroke_width=3, 
            stroke_fill=strokec
        )
                
    except Exception as e:
        img = writeImageException(e)  
        
    return img

# SQUINT ZEALOT

def dots():
    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        img = Image.new("RGBA", (width, height), "#000000")
        draw = ImageDraw.Draw(img)

        xStep = random.randint(4, 8)
        yStep = random.randint(4, 8)
        
        for x in range(0, width - 1, xStep):
            r,g,b = random.randint(0,255), random.randint(0,255), random.randint(0,255)

            dr = (random.randint(0,255) - r) // height
            dg = (random.randint(0,255) - g) // height
            db = (random.randint(0,255) - b) // height
            
            for y in range(0, height - 1, yStep):
                a = random.randint(0, 255)
                r,g,b = r+dr, g+dg, b+db
                draw.line((x,y,x,y+yStep), fill=(int(r),int(g),int(b),a), width=xStep)

    except Exception as e:
        img = writeImageException(e)    

    return img

def dotsDos():
    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        img = Image.new("RGBA", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)

        choices = []

        for x in range(0, width - 1, 3):
            z = getRandomColor(128)
            draw.line((x,0,width - x, height), fill=z, width=5)
            choices.append(z)

        for x in range(width - 1, 0, -3):
            z = getRandomColor(128)
            zy = (z[0],random.randint(100, 200),z[2],128)
            draw.line((x,height, width - x, 0), fill=zy, width=10)
            choices.append(zy)

        zP = getPaletteGenerated()    
        z = random.choice(zP)
        for y in range(height // 3, height - (height // 3), 1):
            draw.line((0, y, width, y), fill=z)
            choices.append(z)
            if y % 4 == 0:
                z = random.choice(zP)

        choices = list(set(choices))

        #alphaVal = random.randint(128, 255)

        fillR, fillG, fillB = random.randint(0,255), random.randint(0,255), random.randint(0,255)
            
        # for y in range(height // 3 - 1, height - (height // 3) + 1, random.randint(2,7)):
        #     fillR = fillG
        #     fillG = fillB
        #     fillB = random.randint(0, 255)
            
        #     draw.line((0, y, width, y), fill=(fillR, fillG, fillB, alphaVal))
        #     alphaVal -= 2

        startX = width // 2
        startY = height // 2
        circleRad = 50
        baseRad = 100
        
        iFill = [0, 1, 2]
        random.shuffle(iFill)

        for r in range(150, 0, -15):
            startX = (width // 2) 
            startY = (height // 2)
            circleRad = baseRad + r

            if random.randint(0,1) == 0:
                fillR = r
                fillG = 255 - r
            else:
                fillR = 255 - r
                fillG = r
                
            if fillR > fillG:
                fillB = random.randint(fillG, fillR) * 3
            else:
                fillB = random.randint(fillR, fillG) * 3

            fills = [fillR, fillG, fillB]

            z = (fills[iFill[0]], fills[iFill[1]], fills[iFill[2]], 128)

            draw.ellipse((startX - circleRad, startY - circleRad, startX + circleRad, startY + circleRad),
                        fill=z,
                        outline=(0,0,0,random.randint(128, 255)))        

        pixdata = img.load()
        targColr = pixdata[width // 2, height // 2]
        
        iAlg = getRandomFloodFill()

        floodfill(img, (width // 2, height // 2), targetcolour = targColr,
                newcolour = (0,0,0),
                choices=choices,
                randomIt = iAlg)

        z = getRandomColor()

        for pos in [(width // 5, height // 4),(width - width // 5, height // 4),(width // 5, height - height // 4),(width - width // 5, height - height // 4)]:
            targColr = pixdata[pos[0], pos[1]]

            floodfill(img, pos, targetcolour = targColr,
                    newcolour = z,
                    randomIt = 0)
             
    except Exception as e:
        img = writeImageException(e)

    return img

def boxabyss(mystrings=[], botStrings = []):
    try:
        if mystrings == []:
            mystrings = [getRandomWord()]

        if botStrings == []:
            botStrings = [getRandomWord(),getRandomWord()]

        thisFont = getFont()
        
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        img = Image.new("RGBA", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)
    
        r,g,b = random.randint(0,255), random.randint(0,255), random.randint(0,255)

        dr = (random.randint(0,255) - r)//height
        dg = (random.randint(0,255) - g)//height
        db = (random.randint(0,255) - b)//height

        debug = 1
        showLines = 1    
        color = 12
        yel = 25

        lines = 0
        
        for c in range(0, width - 1, 1):
            if random.randint(1, 4) == 2:
                if lines < 1 or True:

                    dr = (random.randint(0,255) - r) // height
                    dg = (random.randint(0,255) - g) // height
                    db = (random.randint(0,255) - b) // height
                    
                    r,g,b = r+dr, g+dg, b+db
                                    
                    lines = lines + 1

                    # TODO: fix                    
                    rootLogger.info('Width: ' + str(width))
                    
                    x0 = c if c < width//2 else width//2
                    x1 = width//2 if c < width // 2 else c

                    draw.rectangle((x0, height//2, x1, height), fill=(r,g,b,128))

                    if random.randint(0,5) == 3:
                        r = g
                        b ^= r

                    x0 = width - c if width - c < width//2 else width//2
                    x1 = width//2 if width - c < width//2 else width - c

                    draw.rectangle((x0, 0, x1, height//2), fill=(b,r,g,128))

        colorPrint.print_custom_palette(98, str(thisFont))
        fon = ImageFont.truetype(thisFont, 120)

        # draw wacky stuff

        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0

        for c in range(1, random.randint(20, 100)):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)

            x2 = random.randint(x1, width)
            y2 = random.randint(y1, height)

            dr = (random.randint(0,255) - r)
            dg = (random.randint(0,255) - g) 
            db = (random.randint(0,255) - b) 
                    
            r,g,b = r+dr, g+dg, b+db
            
            draw.rectangle(((x1, y1),(x2, y2)), outline=(g,r,b,200), fill=(r,g,b,128))
            
        xstep = 19
        ystep = 12

        # draw the "spiral"
        
        steps = range(0, 250, 15)
        step = 0

        fon = ImageFont.truetype(thisFont, 72)

        fillColor = getRandomColor(128)

        botS = 0
        
        for c in steps:
            botString = botStrings[botS]
            
            sizTup = fon.getsize(botString)
            fonSize = c // 2

            if fonSize < 15:
                fonSize = 5
                
            fon = ImageFont.truetype(thisFont, fonSize)        

            posX = 0.5 * c
            posY = c + (1.2 * c)

            if posX > width:
                posX = 0
                
            if posY > height:
                posY = 0
                
            pos = (posX, posY)
            
            draw.text(pos, botString, font=fon, fill=fillColor)
            step = step + c

            botS = botS ^ 1

        # draw the text that was passed in

        y = random.randint(0, img.size[1] // 2)
        x = random.randint(img.size[0] // 3, (img.size[0] // 3)*2)
        
        for mys in mystrings:
            fontSize = 144
            mysLength = 99999

            # get an appropriate font size by iterating down until it fits
            
            while mysLength > img.size[0] - x:
                fontSize -= 1
                fon = ImageFont.truetype(thisFont, fontSize)
                fsize = fon.getsize(mys)

                mysLength = fsize[0]

                if y + fsize[1] > img.size[1]:
                    y -= fsize[1]
            
            draw.text((x, y), mys, font=fon, fill=getRandomColor())
            y = y + ystep
            x = x + xstep

        # do some random edge enhancement
        
        for c in range(0, random.randint(2, 5)):
            img = img.filter(ImageFilter.EDGE_ENHANCE)

        # maybe draw some extra rectangles
        
        for c in range(0, random.randint(1, 4)):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)

            x2 = random.randint(x1, width)
            y2 = random.randint(y1, height)

            dr = (random.randint(0,255) - r)
            dg = (random.randint(0,255) - g) 
            db = (random.randint(0,255) - b) 
                    
            r,g,b = r+dr, g+dg, b+db
            
            draw.rectangle(((x1, y1),(x2, y2)), outline=(g,r,b,200), fill=(r,g,b,128))
    
    except Exception as e:
        img = writeImageException(e)

    return img

def patoot(text=[]):
    try:
        if text == []:
            text = [getRandomWord()]

        botString = getRandomWord()
        img = boxabyss(text, botString)
            
        for x in range(0, 4):
            output = boxabyss(text, botString)
            output = output.rotate(180)
            img = Image.blend(img, output, .5)

        img = img.rotate(180)

    except Exception as e:
        img = writeImageException(e)
      
    return img

def orangeblock(pics=[]):
    try:
        if len(pics) <= 1:
            insertPath = getParam(4)

            if insertPath == 0:
                pics = getChoicesWalk(allPaths[4])
            else:
                pics = getChoicesWalk(getPathById(insertPath))

            if len(pics) > 10:
                opts = []

                for i in range(10):
                    opts.append(random.choice(pics))

                pics = opts

            addState(f"pics: {pics}", None)

        width = 1024
        height = 768
        maxW = 400
        maxH = 400                

        img = Image.new("RGBA", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)

        addState(f"width: {width}, height: {height}", None)

        picsImgs = []
        
        for p in pics:
            colorPrint.print_custom_palette(155, f"opening: {p}")

            inputFile = Image.open(p)
            inputFile.load()
            inputFile = inputFile.convert("RGBA")

            saveToWrapper_Insert(p)

            if inputFile.size[0] > maxW or inputFile.size[1] > maxH:
                (w, h) = getSizeByMax(inputFile.size[0], inputFile.size[1], maxW, maxH)
                inputFile = inputFile.resize((int(w), int(h)), Image.LANCZOS)
                
            picsImgs.append(inputFile)
       
        x = 0
        y = 0

        for x in range(0, 100, 10):
            hexagram = random.randint(75,1000)
            addState(f"x: {x} / y-ing this many times: {hexagram}", None)

            for y in range(0, hexagram, 1):
                pasteFile = random.choice(picsImgs)

                # TODO: fix the paste cutoff when rotated

                rotChoice = random.randint(0, 5)
                if rotChoice == 5:
                    pasteFile = pasteFile.rotate(180)
                elif rotChoice == 4:
                    pasteFile = pasteFile.rotate(90)
                elif rotChoice == 3:
                    pasteFile = pasteFile.rotate(270)

                leMask = Image.new("RGBA", pasteFile.size, '#ffffff')

                if random.randint(0, 3) == 0:
                    pasteEdit = pasteFile.convert("RGB")
                    pasteFile = ImageOps.invert(pasteEdit)                
                
                img.paste(pasteFile, (random.randint(-50, width + y), random.randint(-50, height + y)), leMask)
                
    except Exception as e:
        img = writeImageException(e)    
        
    return img

def insertBlocks():
    pics = []
    for i in range(0, random.randint(3, 7)):
        pics.append(getInsertById(getParam(4)))

    return orangeblock(pics)

def ihavenoidea():
    img = ""

    try:    
        width = 1024
        height = 1024
        c = getRandomColor()
        
        img = Image.new("RGBA", (width,height), c)
        draw = ImageDraw.Draw(img)

        addState(f"width: {width}, height: {height}", None)

        global maxFloodFillArg

        iAlg = random.randint(1, maxFloodFillArg)

        addState(f"iAlg: {iAlg}", None)

        choices = getPaletteGenerated()

        addState(f"choices: {choices}", None)
        
        floodfill(img, (50, 30),
                  targetcolour = c,
                  newcolour=(255,255,0),
                  randomIt = iAlg,
                  choices = choices)

        leWordSource = '16398 79658 34394 99711 48642 18697 16378 48551 81467 54281 19973 80235 40911 37707 27196 25484 04295 08849 06465 34088 07131 71008 11311 53113 86384 11903 77470 19886 73348 66957 39217 98718 05677 33457 88323 51326 94656 23057 45304 17352 83386 40670 94204 50271 77740 96708 54737 26609 76665 30658 32641 63472 45618 99508 44920 72724 57863 84357 11023 15467 13958 67818 11866 13202 57041 56782 55060 45778 54777 31098 78679 50387 27281 41887 80272 59269 44197 54093 02613 22752 92862 67351 81525 42513 93136 73719 38901 44326 58665 66775 96672'
        leWord = ""
        
        for iiiii in range(0, len(leWordSource), 6):
            leWord += str(random.randint(10000, 99999)) + " "

        for r in range(1, 500, 15):
            for x in range(1, 15, 2):
                if r < 450:
                    img = img.rotate(89)
                    
                draw = ImageDraw.Draw(img)

                rC = 5 + r
                gC = 10

                if r >= 450:
                    gC = 0
                    rC = 75
                    
                bC = random.randint(0, 255)

                fon = ImageFont.truetype(fontPath + fontNameImpact, random.randint(10, 14))

                thisfill_c = random.randint(0, 5)
                
                if thisfill_c == 0:
                    myc = (rC, gC, bC)
                elif thisfill_c == 1:
                    myc = (rC, bC, gC)
                elif thisfill_c == 2:
                    myc = (gC, rC, bC)
                elif thisfill_c == 3:
                    myc = (gC, bC, rC)
                elif thisfill_c == 4:
                    myc = (bC, rC, gC)
                elif thisfill_c == 5:
                    myc = (bC, gC, rC)

                if r < 450:
                    draw.text((r + random.randint(0, r),r // (2 * r) + r), leWord, font=fon, fill=myc)

        pixdata = img.load()
        
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][0] == 0:
                    pixdata[x, y] = (255, 255, 255, 255)    

        blech = getRandomColor()

        newrgb = getRandomColor()

        iabc = random.randint(0, 2)
        
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if abs(pixdata[x, y][iabc] - blech[iabc]) < 6:
                    pixdata[x, y] = newrgb

        wordsize = random.randint(44, 84)

        fon = ImageFont.truetype(fontPath + fontNameImpact, wordsize)

        wurd1 = getRandomWord() + " " + getRandomWord()

        text_size_x, text_size_y = dropin_text_size(draw,wurd1, font=fon)

        wurd1_x = random.randint(0, width-1-text_size_x)
        wurd1_y = random.randint(0, height-1-text_size_y)
        
        xys = ([5,5], [width-5, 5], [5, height-5], [width-5,height-5])

        for xy in xys:
            targ = pixdata[xy[0], xy[1]]

            floodfill(img, (xy[0], xy[1]),
                      targetcolour = targ,
                      newcolour=(255,255,0),
                      randomIt = iAlg,
                      choices = choices)

        draw.text((wurd1_x,wurd1_y), wurd1, font=fon, fill=(0,0,0))
        
    except Exception as e:
        img = writeImageException(e)

    return img

def split_image_into_grid(rows, cols, width, height):   
    cell_width = width // cols
    cell_height = height // rows
    
    # colorPrint.print_info(f'cell_width: {cell_width} cell_height: {cell_height}')

    grid_coordinates = []

    for row in range(rows):
        for col in range(cols):
            x1 = col * cell_width
            x2 = x1 + cell_width
            
            y1 = row * cell_height            
            y2 = y1 + cell_height

            grid_coordinates.append((x1, y1, x2, y2))

            # colorPrint.print_info(f'row: {row} col: {col} // x1: {x1} x2: {x2} y1: {y1} y2: {y2}')
    
    return grid_coordinates

def fuckinthatdata(imgInputPath=""):
    img = ""

    if imgInputPath == "":
        imgInputPath = getInsertById(getParam(4))
    
    try:
        wts = Image.open(imgInputPath) 
        wts.load()
        wts = wts.convert("RGBA")

        width = getCurrentStandardWidth() // 4
        height = getCurrentStandardHeight() // 4

        wts = resizeToMinMax(wts, maxW=width, maxH=height, minW=640, minH=480)

        p1 = getParam(0)
        iterations = 9 # int(p1) if p1.isdecimal() else 9

        megaWidth = width * 3
        megaHeight = height * 3
        finalImage = Image.new("RGBA", (megaWidth, megaHeight), "#ffffff")

        pixdata = wts.load()
        height = wts.size[1]
        width = wts.size[0]

        img = Image.new("RGB", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)
       
        images = []        
        
        zgrid = split_image_into_grid(3,3, megaWidth, megaHeight)

        colorPrint.print_info(str(zgrid))

        for counter in range(0, iterations):
            pixdata = keepfuckinthatdata(height, width, pixdata)
            height = height - (height // iterations)
            width = width - (width // iterations)

            zg = zgrid[counter]

            finalImage.paste(wts, (zg[0], zg[1]), wts)

        #img.paste(wts, (0, 0), wts)

        img = finalImage

    except Exception as e:
        img = writeImageException(e)

    return img

def vaguetransfer(imgInputPath=""):
    img = ""

    if imgInputPath == "":
        imgInputPath = getInsertById(getParam(4))
    
    try:
        wts = Image.open(imgInputPath) 
        wts.load()
        wts = wts.convert("RGBA")

        wts = resizeToMinMax(wts, maxW=getCurrentStandardWidth(), maxH=getCurrentStandardHeight(), minW=640, minH=480)

        pixdata = wts.load()
        height = wts.size[1]
        width = wts.size[0]

        img = Image.new("RGB", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)
       
        iterations = 9
        
        for counter in range(0, iterations):
            pixdata = keepfuckinthatdata(height, width, pixdata)
            height = height - (height // iterations)
            width = width - (width // iterations)

        # this is the weird cum things
        cumCount = random.randint(3, 4)
        for counter in range(0, cumCount):
            startPlace = (random.randint(0, img.size[0]-1), random.randint((10 * counter),400))
            #startPlace = (random.randint(25,75)+(10*counter), random.randint((10 * counter),400))

            for x in range(0,40):
                for y in range(0,random.randint(15,35)):
                    blech = random.randint(0,255)

                    if startPlace[0] + x < img.size[0] and startPlace[1] + y < img.size[1]:
                        pixdata[startPlace[0] + x, startPlace[1] + y] = (blech,blech,0,blech)
                    
        img.paste(wts, (0, 0), wts)

    except Exception as e:
        img = writeImageException(e)

    return img

def shakeHarderBoyBase(imgpath=""):
    img = ""

    try:
        if imgpath == "":
            imgpath = getInsertById(getParam(4))

        width = 500
        height = 500
        img = Image.new("RGB", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)

        wts = Image.open(imgpath) 
        wts.load()

        wts = wts.convert("RGBA")

        pixdata = wts.load()
        
        height = wts.size[1]
        width = wts.size[0]

        iterations = 10
        
        for counter in range(0, iterations):
            pixdata = shakeharderboy(height, width, pixdata)
            height = height - (height // iterations)
            width = width - (width // iterations)
       
        img.paste(wts, (0, 0), wts)
        pixdata = img.load()

    except Exception as e:
        img = writeImageException(e)

    return img

def transferStation(inputImagePath=""):
    wts = ""
    
    try:            
        if inputImagePath == "":
            inputImagePath = getInsertById(getParam(4))

        wts = Image.open(inputImagePath)
        wts.load()

        wts = resizeToMinMax(wts, maxW=1280, maxH=1024, minW=640, minH=480)

        oldblechs = [2,3,7]
        
        for x in range(0, random.randint(1, 3)):
            wts = wts.convert("RGBA")
            blech = random.randint(2, 7)
            wts = vaguertransfer(wts, blechDivisor=blech)

    except Exception as e:
        wts = writeImageException(e)

    return wts

def vaguertransfer(wts, blechDivisor=2):
    pixdata = wts.load()
    
    height = wts.size[1]
    width = wts.size[0]

    img = Image.new("RGB", (width,height), "#ffffff")
    draw = ImageDraw.Draw(img)

    iterations = 0
    
    for counter in range(0, iterations):
        pixdata = shakeharderboy(height, width, pixdata)
        height = height - (height // iterations)
        width = width - (width // iterations)
   
    img.paste(wts, (0, 0), wts)

    pixdata = img.load()
    
    blech = pixdata[img.size[0] // blechDivisor, img.size[1] // blechDivisor]
    
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if abs(pixdata[x, y][0] - blech[0]) < 30:
                try:
                    zz = pixdata[y,x]
                    pixdata[x,y] = (zz[0]/2,zz[1]/2,zz[2]/2)
                except:
                    pixdata[x, y] = (random.randint(0,255), 255, 255, 128)
            elif abs(pixdata[x, y][1] - blech[1]) < 30:
                try:
                    zz = pixdata[y,x]
                    pixdata[x,y] = (zz[0]/2,zz[1]/2,zz[2]/2)
                except:
                    pixdata[x, y] = (255, random.randint(0,255), 255, 128)
            elif abs(pixdata[x, y][2] - blech[2]) < 30:
                try:
                    zz = pixdata[y,x]
                    pixdata[x,y] = (zz[0]/2,zz[1]/2,zz[2]/2)
                except:
                    pixdata[x, y] = (255, 255, random.randint(0,255), 128)
    
    botString = 'PROPELLANT CHILI BLISS'
    x = width - 400
    y = height - 50
    fon = ImageFont.truetype(fontPath + fontNameImpact, 35)
    fonStroke = ImageFont.truetype(fontPath + fontNameImpact, 38)
    textColor = (222,220,222,255)
    
    #textStroke(draw, x, y, botString, fonStroke, (0,0,0,128))
    #draw.text((x, y), botString, font=fon, fill=textColor)
    
    return img

def gritty():
    width = 1000
    height = 1000

    palette = getInputPalette()
       
    img = Image.new("RGB", (width,height), "#ffffff")
    draw = ImageDraw.Draw(img)
    pixdata = img.load()

    i = 0
    stripe = 0
    stripeRuined = 0
   
    iGritty = 4
    yGritty = random.randint(3, 7)

    for y in range(0, img.size[1], yGritty):
        for x in range(img.size[0]):
            currentColor = random.choice(palette)
            
            if stripeRuined == 0:
                if random.randint(1, 7) == iGritty:
                    currentColor = random.choice(palette)
                    stripeRuined = 1                

            for jjjj in range(0, yGritty):
                if y + jjjj < img.size[1]:
                    pixdata[x,y+jjjj] = currentColor

            i += 1

            if i % 3 == 0:
                stripe = stripe + 1
                stripeRuined = 0
    
    return img

def grittyer():
    """p1: weirdFactor (default=7)<br />
    p2: divisor (default=26.75)<br />
    p3: mod value (default=45)
    """

    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        img = Image.new("RGBA", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)
        
        pixdata = img.load()

        r = 0
        g = 0
        b = 0
        
        i = 0
        j = 0

        p1 = getParam(0)
        p2 = getParam(1)
        p3 = getParam(6)

        weirdFact = int(p1) if p1.isdecimal() else 7
        staticWeirdFact = int(p1) if p1.isdecimal() else 7
        staticDivisor = float(p2) if p2.isdecimal() or p2.isnumeric() else 26.75
        modValue = int(p3) if p3.isdecimal() else 45

        for x in range(0, width):
            if x % weirdFact == 0:
                for y in range(height):
                    pixdata[x, y] = (r, g, b, j)
                    try:
                        for wr in range(1, weirdFact+1):
                            pixdata[x+wr, y] = (r, g, b, j)                
                    except:
                        pass
                    
                    i += random.randint(1, 10)
                    i = i % 255
                    j = i

                    (r, g, b) = colorRandomInc(r, g, b)

                    weirdFact = int(staticWeirdFact + (y // staticDivisor))
    
        for x in range(0, width):
            if x % modValue == 0 or random.randint(0, 15) == 0:
                (r, g, b) = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
            
            for y in range(0, height):
                c = pixdata[x,y]
                if c[0] == 255 and c[1] == 255 and c[2] == 255:                
                    pixdata[x,y] = (r, g, b)

    except Exception as e:
        img = writeImageException(e)    
    
    return img

def bored(): # you wouldn't last an hour in the asylum where they raised me
    try:
        width = getCurrentStandardWidth() // 2
        height = getCurrentStandardHeight() // 2
        choices = getInputPalette()
        
        img = Image.new("RGB", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        rnd1 = width // 2

        cStroke = random.choice(choices)

        draw.polygon([(0,0), (rnd1,rnd1), (0, rnd1)], outline=cStroke)

        floodfill(img, (30, 50),
                targetcolour=(255,255,255),
                newcolour=(255,0,0),
                randomIt = 1,
                choices=choices)

        draw.polygon([(0,0),
                    (400,400),
                    (400,0)],
                    outline=cStroke,
                    fill=(255,255,255))

        floodfill(img, (350, 30),
                targetcolour = (255,255,255),
                newcolour=(255,255,0),
                randomIt = 2,
                choices=choices)

        draw.polygon([(0,200),
                    (150,500),
                    (200,400),
                    (50,150)],
                    outline = (255,255,0),
                    fill = (255, 255, 255))

        floodfill(img, (5, 200), targetcolour = (255,255,255),
                newcolour = cStroke,
                randomIt = 3,
                choices=choices)

        floodfill(img, (5, 400),
                targetcolour = (255,255,255),
                newcolour = (255,255,0),
                randomIt = 4,
                choices=choices)
        
    ##    for y in xrange(img.size[1]):
    ##        for x in xrange(img.size[0]):
    ##
    ##            if stripe >= random.randint(5, 22):
    ##                r = random.randint(0, 5)
    ##                g = random.randint(0, 255-r)
    ##                b = random.randint(0, 255-r-g)
    ##                a = 255
    ##                currentColor = (r, g, b, a)
    ##                stripe = 0
    ##                
    ##            pixdata[x,y] = currentColor
    ##            i += 1
    ##            stripe += 1

        imgInputPath = getInsertById(getParam(4))

        wts = Image.open(imgInputPath)
        wts.load()
        wts = wts.convert("RGBA")

        pixdata = wts.load()
            
        for y in range(wts.size[1]):
            for x in range(wts.size[0]):
                if x > 390 or x < 200:
                    pixdata[x,y] = (255,255,255,0)
                    
                if abs(pixdata[x,y][0] - pixdata[x,y][1]) < 20:
                    if x < 245 or x > 350 or y > 300:
                        pixdata[x,y] = (255,255,255,0)

        draw2 = ImageDraw.Draw(wts)
        
        height = wts.size[1]
        width = wts.size[0]

        img.paste(wts, (-125, 140), wts)
    
    except Exception as e:
        img = writeImageException(e)    
    
    return img

def catalinaimagemixer(squares=0):
    if squares == 0:
        squares = random.randint(5, 12)
    
    images = getChoicesWalk(getPathById(getParam(4)))
    
    success = False

    outputWidth = getCurrentStandardWidth()
    outputHeight = getCurrentStandardHeight()

    maxSquareWidth = outputWidth // 4
    maxSquareHeight = outputHeight // 4

    while not success:
        try:
            leImg = random.choice(images)            

            img = Image.open(leImg)
            img = img.resize((outputWidth, outputHeight))
            img = img.convert("RGBA")            

            xWine = random.randint(0, 4)

            if xWine == 2:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)

            if xWine == 3:
                img = img.rotate(180)

            pixdata = img.load()

            success = True

            saveToWrapper_Insert(leImg)
        except:
            pass

    height = img.size[1]
    width = img.size[0]

    for square in range(squares):
        placeAtX = random.randint(0,width-1)
        placeAtY = random.randint(0,height-1)

        aRandomX = random.randint(0,width-1)
        aRandomY = random.randint(0,height-1)

        squareWidth = random.randint(50, maxSquareWidth)
        squareHeight = random.randint(50, maxSquareHeight)

        success = False

        while not success:
            try:
                leImg = random.choice(images)
                mixin = Image.open(leImg)
                mixin = mixin.resize((width, height))                

                xWine = random.randint(0, 4)

                if xWine == 2:
                    mixin = mixin.transpose(Image.FLIP_LEFT_RIGHT)

                if xWine == 3:
                    mixin = mixin.rotate(180)

                mixdata = mixin.load()

                success = True
                saveToWrapper_Insert(leImg)
            except:
                pass
    
        iY = 0
        for y in range(placeAtY, placeAtY + squareHeight):    
            iX = 0
            for x in range(placeAtX, placeAtX + squareWidth):
                try:
                    pixdata[x,y] = mixdata[aRandomX + iX, aRandomY + iY]
                except:
                    pass

                iX += 1

            iY += 1        
    
    return img

def smellycatalina(startPos="",
                   fonSize=72,
                   lines=[],
                   fillStroke=(0,0,0,255),
                   fillText=(255,255,255,255),
                   squares=5,
                   fontPath=fontPath + fontNameImpact):
    img = ""

    if fillText == (255,255,255,255):
        fillText = getRandomColor()
    
    if len(lines) == 0:
        lines = [(getRandomWord()).upper(),(getRandomWord()).upper()]
    try:
        img = catalinaimagemixer(squares)

        if startPos == "":
            startPos = (random.randint(0, img.size[0]-1-fonSize), random.randint(0, img.size[1]-1-fonSize))
       
        fon = ImageFont.truetype(fontPath, fonSize)
        
        x = startPos[0]
        y = startPos[1]

        draw = ImageDraw.Draw(img)

        for theString in lines:    
            draw.text((x, y), theString, font=fon, fill=fillText, stroke_width=2, stroke_fill=fillStroke)
            y += fonSize
            
    except Exception as e:
        img = writeImageException(e)
        
    return img

def textalinaimagemixer(squares=35, text=[], fonSize=48):
    img = ""

    cat = getParam(0)
    cat = int(cat) if cat.isdecimal() else random.randint(0, 7)

    try:
        if cat == 1:
            startPos = (0,200)
            fonSize = 128
            lines = ['COME ON','GET NAKED']
            fillStroke = (0,0,0)
            fillText= (255,255,255)
        elif cat == 2:
            startPos = (0,100)
            fonSize = 144
            lines = ['BUTT','ASS']
            fillStroke = (255,233,22)
            fillText = (255,255,0)
        elif cat == 3:
            lines = ['THE MERE FACT THAT','YOU CALL IT THAT','TELLS ME YOU\'RE','NOT READY']
            startPos = (0,100)
            fonSize = 72
            fillStroke = (0,0,0)
            fillText = (222,255,227)
        elif cat == 5:
            startPos = (random.randint(0, 200), random.randint(0, 200))
            fonSize = 72
            lines = ['STARS','ENCLOSE','THE SKY']
            fillStroke = (0,0,0)
            fillText = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        elif cat == 6:
            startPos = (random.randint(0, 200), random.randint(0, 200))
            fonSize = 72
            lines = [getRandomWord(),getRandomWord(),getRandomWord()]
            fillStroke = (0,0,0)
            fillText = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        else:
            startPos = (random.randint(0, 200), random.randint(0, 200))
            #fonSize = 
            lines = text
            fillStroke = (0,0,0)
            fillText= getRandomColorRGB()
        
        img = smellycatalina(startPos, fonSize, lines, fillStroke, fillText, squares, fontPath=getFont())

        # if cat == 2 or cat == 4:
        #     pixdata = img.load()

        #     height = img.size[1]
        #     width = img.size[0]
            
        #     for y in range(0,height):
        #         for x in range(0,width):                            
        #                 floodfill(img, (width, height),
        #                         targetcolour = pixdata[x,y],
        #                         newcolour = (0,0,0),
        #                         randomIt = 4) 

    except Exception as e:
        img = writeImageException(e)
        
    return img

def roundPaste():
    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        img = Image.new("RGB", (width,height), "#ffffff")
        img = dots()

        images = getChoicesWalk(getPathById(getParam(4)))
    
        success = False

        outputWidth = getCurrentStandardWidth()
        outputHeight = getCurrentStandardHeight()

        maxSquareWidth = outputWidth // 4
        maxSquareHeight = outputHeight // 4

        zimg = ""
        
        while not success:
            try:
                leImg = random.choice(images)
                zimg = Image.open(leImg)
                zimg = zimg.resize((maxSquareWidth, maxSquareHeight))
                zimg = zimg.convert("RGBA")

                success = True

                saveToWrapper_Insert(leImg)
            except:
                pass

        mask = Image.new("L", (zimg.size[0], zimg.size[1]), 0)
        pixdata = mask.load()

        draw = ImageDraw.Draw(mask)
        draw.ellipse([(0,0),(mask.size[0],mask.size[1])], 255, 255, 1)

        img.paste(zimg, (maxSquareWidth,maxSquareHeight), mask)

    except Exception as e:
        img = writeImageException(e)
        
    return img

def vgaBox():
    width = 800
    height = 600
    img = Image.new("RGB", (width,height), "#ffffff")
    img = dots()

    draw = ImageDraw.Draw(img)
    
    x = 0
    y = 0

    pixdata = img.load()

    holder = 0
    
    i1 = random.randint(6, 15)
    i2 = random.randint(300, 425)

    for x in range(0, 70, i1):
        draw.polygon([(i1 + x, i1 + x),
                      (i2 + x, i1 + x),
                      (i2 + x, i2 + x),
                      (i1 + x, i2 + x)],
                     outline=(0,0,0),
                     fill=(255,255,255))
       
        floodfill(img, (i1 + 1 + x, i1 + 1 + x),
                 targetcolour = pixdata[i1 + 1 + x, i1 + 1 + x],
                 newcolour=(0,0,0),
                 randomIt = 5)

        holder += 1
        if holder > 2:
            holder = -1

    draw.polygon([(425, 425),
                  (500, 425),
                  (500, 500),
                  (425, 500)],
                 outline = (0,0,0),
                 fill=(255,255,255))

    floodfill(img, (430, 430),
              targetcolour = pixdata[430, 430],
              newcolour = (0,0,0),
              randomIt = 6)

    draw.polygon([(425, 10),
                  (700, 10),
                  (500, 400),
                  (425, 400)],
                 outline = (0,0,0),
                 fill = (255,255,255))

    floodfill(img, (430, 15),
              targetcolour = pixdata[430, 15],
              newcolour = (0,0,0),
              randomIt = 7)

    draw.polygon([(10, 550),
                  (790, 550),
                  (790, 590),
                  (10, 590)],
                 outline = (0,0,0),
                 fill = (255,255,255))

    floodfill(img, (15, 575),
              targetcolour = pixdata[15, 575],
              newcolour = (0,0,0),
              randomIt = 8)
    
    return img

def iWannaBeTheOne():
    """p1: baseFactor (default=5)
    """

    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()
        img = Image.new("RGB", (width,height), "#ffffff")

        draw = ImageDraw.Draw(img)
        
        x = 0
        y = 0

        pixdata = img.load()

        r, g, b = 0, 0, 0

        p1 = getParam(0)
        p2 = getParam(1)

        baseFactor = int(p1) if p1.isdecimal() else 5
        
        rfactor = baseFactor
        gfactor = baseFactor
        bfactor = baseFactor

        x = 0
        y = 0
        
        for x in range(width):
            for y in range(height):        
                #x = random.randint(0, width - 1)
                #y = random.randint(0, height - 1)
                
                i = random.randint(1, 450)
            
                if i == 1:
                    r += rfactor
                elif i == 2:
                    g += gfactor
                elif i == 3:
                    b += bfactor

                if r >= 255:
                    rfactor = -1 * baseFactor
                elif r <= 0:
                    rfactor = baseFactor
                    
                if g >= 255:
                    gfactor = -1 * baseFactor
                elif g <= 0:
                    gfactor = baseFactor
                    
                if b >= 255:
                    bfactor = -1 * baseFactor
                elif b <= 0:
                    bfactor = baseFactor
                    
                pixdata[x, y] = (r, g, b)

    except Exception as e:
        img = writeImageException(e)

    return img

def iWannaOneTheTwo():
    try:
        width = 1024
        height = 768
        img = Image.new("RGB", (width,height), "#ffffff")

        draw = ImageDraw.Draw(img)
        
        x = 0
        y = 0

        pixdata = img.load()

        baseFactor = random.randint(-20, 20)

        # weight the chances that 4 or greater (ie no factor inc)
        # are all equally likely as 1/2/3
        # so then if that happens, THEN pick a bigger number
        
        iFactor = random.randint(3, 6)

        if iFactor > 3:
            iFactor = random.randint(6, 100)

        if baseFactor >= 0:
            r, g, b = 0, 0, 0
        else:
            r, g, b = 255, 255, 255
        
        rfactor = baseFactor
        gfactor = baseFactor
        bfactor = baseFactor

        x = 0
        y = 0
        
        for x in range(width):
            i = random.randint(0, iFactor)
            
            for y in range(height):           
                if i == 1:
                    r += rfactor
                elif i == 2:
                    g += gfactor
                elif i == 3:
                    b += bfactor

                if r >= 255:
                    rfactor = -1 * baseFactor
                elif r <= 0:
                    rfactor = 1 * baseFactor
                    
                if g >= 255:
                    gfactor = -1 * baseFactor
                elif g <= 0:
                    gfactor = 1 * baseFactor
                    
                if b >= 255:
                    bfactor = -1 * baseFactor
                elif b <= 0:
                    bfactor = 1 * baseFactor

                c = (r, g, b)
                c = safetyCheck(c)
                
                pixdata[x, y] = c

    except Exception as e:
        img = writeImageException(e)

    return img
    
def nightInterference():
    try:
        width = 800
        height = 600

        img = Image.new("RGB", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)
        
        pixdata = img.load()

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = 50
        
        x = 0
        y = 0

        passes = 0
        flag = 0

        floodfill(img, (1,1),
                targetcolour = pixdata[x,y],
                newcolour = (0,0,0),
                randomIt = 3)

        for bleh in range(random.randint(5, 10)):
            for x in range(random.randint(0, width)):
                for y in range(random.randint(0, height)):
                    r = x % (255 - bleh)
                    g = y % (255 - bleh)
                    if flag >= 255:
                        flag = 0
                        passes += 1

                    b = (passes * 10) % 255
                    
                    pixdata[x, y] = (r, g, b)
                    flag += 1

        mixin = gritty()
        mixdata = mixin.load()

        for x in range(width):
            for y in range(height):
                try:
                    if random.randint(0, 10) == 5:
                        pixdata[x, y] = mixdata[x, y]
                except:
                    pass
    
    except Exception as e:
        img = writeImageException(e)

    return img

def dayInterference():
    try:
        width = 1024
        height = 768
        img = Image.new("RGB", (width,height), "#000000")

        draw = ImageDraw.Draw(img)
        
        x = 0
        y = 0

        pixdata = img.load()

        r, g, b = 0, 0, 0

        r = 0 #random.randint(0, 255)
        g = 0 #random.randint(0, 255)
        b = 0 #50
        
        x = 0
        y = 0

        passes = 0
        flag = 0

        floodfill(img, (1,1),
                targetcolour = pixdata[x,y],
                newcolour = (0,0,0),
                randomIt = 3)

        # put in some noise
        for x in range(width):
            for y in range(height):
                if random.randint(0, (height - y) // 4) == 1:
                    pixdata[x, y] = (0, 0, 0)
                    
        for bleh in range(random.randint(7, 11)):
            for x in range(random.randint(0, width)):
                for y in range(random.randint(0, height)):
                    r = x % (255 - bleh)
                    g = y % (255 - bleh)

                    if flag >= 255:
                        flag = 0
                        passes += 1

                    #b = (passes * 10) % 255
                    b = (passes * 50) % 255
                    
                    pixdata[x, y] = (r, g, b)
                    flag += 1

        mixin = gritty()
        mixdata = mixin.load()

        for x in range(width):
            for y in range(height):
                try:
                    if random.randint(0, 250) == 5:
                        pixdata[x, y] = mixdata[x, y]
                except:
                    pass

    except Exception as e:
        img = writeImageException(e)

    return img

def colorHatch(width=getCurrentStandardWidth(), height=0, bw=0, doFF=1, squareX=0, squareY=0):
    img = ""
    
    try:
        if height == 0:
            height = int(width * 0.75)

        if squareX == 0:
            squareX = random.randint(10, 150)

        if squareY == 0:
            squareY = random.randint(10, 150)
            
        img = Image.new("RGB", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)
        
        pixdata = img.load()

        r, g, b = 0, 0, 0

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        
        x = 0
        y = 0

        global randoFillList
        iAlg = random.choice(randoFillList)
        
        choices = getPaletteGenerated((r,g,b))

        if bw == 1:
            choices = [(0,0,0),(255,255,255)]
            
        i = 0

        modAmount = random.randint(3, 15)

        ys = []
        
        for x in range(0, img.size[0], squareX):
            for y in range(0, img.size[1], squareY):
                ys.append(y)

                if bw == 0:
                    grc = getRandomColor()
                else:
                    grc = random.choice(choices)
                
                draw.rectangle((x, y, x + squareX, y + squareY), grc)

                if x+1 < img.size[0] and y+1 < img.size[1] and doFF == 1:
                    floodfill(img, (x+1,y+1),
                              targetcolour = pixdata[x+1,y+1],
                              newcolour = (0,0,0),
                              randomIt = iAlg,
                              choices = choices,
                              sizeLimit=(squareX, squareY))

                    if bw == 0:
                        for i in range(0, len(choices)):
                            c = choices[i]
                            
                            k = random.randint(0, 2)
                            kk = random.choice([-1 * modAmount, modAmount])

                            c = replace_at_index(c, k, c[k]+kk)
                            c = safetyCheck(c)

                            choices[i] = c

        img = img.crop((0, 0, img.size[0], ys[-1]))
        l = img.load()
        img = img.convert("RGBA")
        
    except Exception as e:
        img = writeImageException(e)   
        
    return img

def whateverDude(caption=""):
    img2 = ""

    try:
        if caption == "":
            caption = getRandomWord() + " " + getRandomWord()
            
        imgPath = getInsert("", publicDomainImagePath)
        
        inputFile = Image.open(imgPath)

        img = resizeToMinMax(inputFile, maxW=1024, maxH=768, minW=640, minH=480)
        
        pixdata = inputFile.load()

        pallettes = (('082B2D','069498','73AC7F','C9FA9E','ffffff'),
                     ('ECD078','D95B43','C02942','542437','53777A'),
                     ('D9CEB2','948C75','D5DED9','7A6A53','99B2B7'),
                     ('951DF8','030105','CD1E1E','E48B19','E92581'),
                     ('4D454F','ffffff','FA1330','B3B5A7','2A1330'))   # red/black/white

        colors = []
        
        for i in range(0, 5):
            c = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
            chex = rgb_to_hex(c)
            if chex.startswith("#"):
                chex = chex[1:]
                
            colors.append(chex)

        #colors = random.choice(pallettes)
        
        inputFile = inputFile.convert("RGB")

        #enhancer = ImageEnhance.Contrast(inputFile)
        #enhancer.enhance(1.5)
            
        pixels = ImageOps.grayscale(inputFile).getdata()

        i1 = random.randint(0, 220)
        i2 = random.randint(i1+1, 240)
        i3 = random.randint(i2+1, 250)
        i4 = random.randint(i3+1, 255)

        bandarray = [i1, i2, i3, i4]

        img2 = Image.new(inputFile.mode, inputFile.size,)
        img2.putdata(colorfun(pixels, colors, bandarray))
        img2.putdata(pixels)

        if caption != "":
            # do some stuff here
            fonSize = 36
            fon = ImageFont.truetype(fontPath + fontNameImpact, fonSize)
            draw = ImageDraw.Draw(img2)

            i = 0
            for color in colors:
                pos = (img2.size[0] - 550 + i, img2.size[1] - 350 + i)
                inverse = hex_to_rgb("#"+color)

                if random.randint(0, 2) == 1:
                    inverse = (255-inverse[0],255-inverse[1],255-inverse[2])
                    
                draw.text(pos, caption, font=fon, fill=inverse)
                i += 2
                
    except Exception as e:
        img2 = writeImageException(e)  

    return img2

def floodSample(palette=""):
    """p3: variant"""

    try:
        width = 1800
        height = 1600
        
        choices = []

        if palette != "":
            choices = processPalette(palette)

        img = Image.new("RGB", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)
         
        fillTestTotal = 121
        rows, cols, gridStep = buildGrid(width, height, fillTestTotal)
        xTimeText = drawGrid(draw, rows, cols, gridStep)
                
        iAlg = 0

        fon = ImageFont.truetype(fontPath + fontNameImpact, 32)
        fonTime = ImageFont.truetype(fontPath + fontNameMono, 14)

        yTimeText = 0
        
        for y in range(0, rows):
            for x in range(0, cols):

                xFill = gridStep * x + (gridStep // 2)
                yFill = gridStep * y + (gridStep // 2)

                t0 = time.time()
                
                floodfill(img, (xFill, yFill),
                          targetcolour = (255, 255, 255),
                          newcolour = (160,128,100),
                          randomIt = iAlg,
                          maxStackDepth = 0 if iAlg == 21 else 0,
                          choices = choices)

                t1 = time.time()

                if iAlg < fillTestTotal:
                    xFillText = xFill - (gridStep // 2) + 5
                    yFillText = yFill - (gridStep // 2)
                    
                    time_taken = t1-t0
                    blah = "%2d: %.3f" %(iAlg, time_taken)

                    time_fill = (0,0,0,255)

                    if time_taken < .115:
                        time_fill = (0,128,0,255)
                    elif time_taken < .15:
                        time_fill = (128,128,0,255)
                    else:
                        time_fill = (128,0,0,255)

                    draw.text((xFillText, yFillText), str(iAlg),
                              font=fon, fill=(255,255,255,0), stroke_width=3, stroke_fill=time_fill)

                    draw.text((xTimeText, yTimeText), blah,
                              font=fonTime, fill=time_fill)

                    wbig, hbig = dropin_text_size(draw, blah, fonTime)

                    yTimeText += hbig + 3
                
                iAlg += 1

    except Exception as e:
        img = writeImageException(e)

    return img

def stampSample():
    img = ""

    try:
        width = 800
        height = 600
        
        img = Image.new("RGB", (width,height), "#ffffff")

        #stmp1 = getStampGenerated()
        stmp1 = getStamp()
        
        floodfill(img, (5, 5),
                          targetcolour = (255, 255, 255),
                          newcolour = (0,0,0),
                          randomIt = 0,
                          compFunc=-1,
                          stamp = stmp1)
        
    except Exception as e:
        img = writeImageException(e)

    return img

def paletteSample():
    """
    p1 = lum -> sort_by_lum(choices)
    """

    try:
        global palettelist

        rowCount = 0
        for p in palettelist:
            rowCount += 1
            pass
        
        recSize = 40
            
        height = rowCount * recSize * 2
        width = getCurrentStandardWidth()

        p1 = getParam(0)        

        fon = ImageFont.truetype(fontPath + fontNameMono, 18)
    
        img = Image.new("RGBA", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()      

        cOutline = (0,0,0,255)
        
        spacer = 5

        y = 0
        for i in palettelist:
            choices = getPaletteSpecific(i[0])

            if p1 == "lum":
                choices = sort_by_lum(choices)

            x = 25
            kz = ((width - x) / len(choices) - 3)
            
            kz = 5 if kz < 5 else kz

            boxWidth = int(kz if len(choices) > 10 else 50)

            label = f'{i[1]}'
            draw.text((x, y), label, font=fon, fill=cOutline)
            text_size_x, text_size_y = dropin_text_size(draw,label, font=fon)            

            y += spacer + text_size_y
            boxHeight = recSize - spacer - text_size_y

            for c in choices:
                # rootLogger.debug(f'i: {i} c: {c}')
                draw.rectangle(((x,y),(x+boxWidth,y+boxHeight)), fill=c, outline=cOutline)
                x += boxWidth

            y += recSize

        img = img.crop((0,0,img.size[0], y))
            
    except Exception as e:
        img = writeImageException(e)

    return img

def drawGrid(draw, rows, cols, gridStep, color="black"):
    xTimeText = 0
        
    for i in range(0, rows + 1):
        # horizontal gridlines
        draw.line((0, gridStep * i, gridStep * (cols), gridStep * i), color)

    for i in range(0, cols + 1):
        # vertical gridlines
        draw.line((i * gridStep, 0, i * gridStep, gridStep * (rows)), color)
        xTimeText = (i * gridStep) + 10

    return xTimeText

def buildGrid(width, height, fillTestTotal=90):
    squareCount = 0

    rows = 0
    cols = 0
        
    while squareCount < fillTestTotal:
        if rows < cols:
            rows += 1
        elif cols < rows:
            cols += 1
        else:
            if height > width:
                rows += 1
            else:
                cols += 1

        squareCount = rows * cols

    gridStep = (height // rows) - 1
        
    if height > width:
        gridStep = (width // cols) - 1

    return rows, cols, gridStep

def stampFull():
    img = ""

    try:
        width = 800
        height = 600
        
        img = Image.new("RGB", (width,height), "#ffffff")

        #stmp1 = getStampGenerated()
        stmp1 = getStamp()
        
        floodfill(img, (5, 5),
                          targetcolour = (255, 255, 255),
                          newcolour = (0,0,0),
                          randomIt = 0,
                          compFunc=-1,
                          stamp = stmp1)
        
    except Exception as e:
        img = writeImageException(e)

    return img

def jumpingDust():
    width = 1000
    height = 1000
    img = Image.new("RGB", (width,height), "#ffffff")

    draw = ImageDraw.Draw(img)
    
    x = 0
    y = 0

    pixdata = img.load()
     
    r, g, b = 0, 0, 0

    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = 200
    
    passes = 0
    flag = 0

    recSize = 50
    spacing = 10

    global maxFloodFillArg
    
    # level 1
   
    # draw some 'tangles and fill 'em
    for y in range(10, height-recSize, recSize + spacing):
        for x in range(10, width-recSize, recSize + spacing):
            draw.rectangle(((x,y),(x+recSize,y+recSize)), fill=(255,255,255,128), outline="black")

            thisX = x+1
            thisY = y+2

            fillAlg = random.randint(0, maxFloodFillArg)

            choices = getPaletteGenerated()
            
            floodfill(img, (thisX, thisY),
                      targetcolour = pixdata[thisX, thisY],
                      newcolour = (r,g,b),
                      randomIt = fillAlg,
                      choices=choices)

    # level 2
    
    for y in range((recSize//2)+spacing, height-recSize, (recSize*2)+(spacing*2)):
        for x in range((recSize//2)+spacing, width-recSize, (recSize*2)+(spacing*2)):
            x1 = x 
            y1 = y 
            
            draw.rectangle(((x1, y1), (x1+recSize+spacing, y1+recSize+spacing)),
                           fill=(255, 255, 255, 128), outline="black")

            fillAlg = random.randint(0, maxFloodFillArg)

            choices = getPaletteGenerated()

            floodfill(img, (x1+1, y1+1),
                      targetcolour = pixdata[x1+1, y1+1],
                      newcolour = (r,g,b),
                      randomIt = fillAlg,
                      choices = choices)

    # level 3
    
    for y in range(spacing+recSize+(spacing//2), height-recSize, (recSize*4)+(spacing*4)):
        for x in range(spacing+recSize+(spacing//2), width-recSize, (recSize*4)+(spacing*4)):
            x1 = x 
            y1 = y
            
            draw.rectangle(((x1, y1), (x1+(recSize*2)+(spacing*2), y1+(recSize*2)+(spacing*2))),
                                   fill=(255, 255, 255, 128), outline="black")

            fillAlg = random.randint(0, maxFloodFillArg)

            choices = getPaletteGenerated()
                        
            floodfill(img, (x1+1, y1+1),
                      targetcolour = pixdata[x1+1, y1+1],
                      newcolour = (r,g,b),
                      randomIt = fillAlg,
                      choices = choices)

    usedAlgs = []
    
    # level 4
    for y in range((2*recSize)+(2*spacing)+(spacing//2), height-recSize, (recSize*8)+(spacing*8)):
        for x in range((2*recSize)+(2*spacing)+(spacing//2), width-recSize, (recSize*8)+(spacing*8)):
            x1 = x
            y1 = y
            
            draw.rectangle(((x1, y1), (x1+(recSize*4)+(spacing*4), y1+(recSize*4)+(spacing*4))),
                                   fill=(255, 255, 255, 128), outline="black")

            fillAlg = random.randint(0, maxFloodFillArg)
            while fillAlg in usedAlgs:
                fillAlg = random.randint(0, maxFloodFillArg)

            usedAlgs.append(fillAlg)

            choices = getPaletteGenerated()
            
            floodfill(img, (x1+1, y1+1),
                      targetcolour = pixdata[x1+1, y1+1],
                      newcolour = (r,g,b),
                      randomIt = fillAlg,
                      choices = choices)

    fillAlg = random.randint(0, maxFloodFillArg)
    
    floodfill(img, (1, 1),
              targetcolour = pixdata[0,0],
              newcolour = (r,g,b),
              randomIt = fillAlg,
              choices = choices)
    
    return img

def dumpingJust():
    width = 1000
    height = 900
    img = Image.new("RGB", (width,height), "#ffffff")

    draw = ImageDraw.Draw(img)
    
    x = 0
    y = 0

    pixdata = img.load()

    global input_palette
        
    if len(input_palette) > 0:
        choices = input_palette
    else:
        choices = getPaletteGenerated()
     
    r, g, b = 0, 0, 0

    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = 200
    
    passes = 0
    flag = 0

    recSize = random.randint(50, 250)
    spacing = 10

    global maxFloodFillArg
    
    # level 1

    textSize = 36
    fon = ImageFont.truetype(fontPath + fontNameImpact, textSize)
    fillColor = (255,255,255,128)

    i = 0
    
    # draw some 'tangles and fill 'em
    for y in range(10, height-recSize, recSize + spacing):
        for x in range(10, width-recSize, recSize + spacing):
            draw.rectangle(((x,y),(x+recSize,y+recSize)), fill=(255,255,255,128), outline="black")

            thisX = x+1
            thisY = y+2

            fillAlg = i

            floodfill(img, (thisX, thisY),
                      targetcolour = pixdata[thisX, thisY],
                      newcolour = (r,g,b),
                      randomIt = fillAlg,
                      choices = choices)

            #text = str(fillAlg)

            #w, h = dropin_text_size(draw,text, fon)

            # recSize = h + 2q
            # q = (recSize - h) // 2
            # xText = x + ((recSize - w) // 2)
            # yText = y + ((recSize - h) // 2) - 4

            # textStroke(draw, xText, yText, text, fon, (0,0,0,128))
            # draw.text((xText, yText), text, font=fon, fill=fillColor)

            i += 1

            if i > maxFloodFillArg:
                i = 0

    fillAlg = random.randint(0, maxFloodFillArg)
    floodfill(img, (1, 1),
                      targetcolour = pixdata[0,0],
                      newcolour = (r,g,b),
                      randomIt = fillAlg, 
                      choices = choices)
    
    return img

def shapeMover(imgPath=""):
    """p1: mode (0=rectangle, 1=circle) (default=1)
    
    """
    global rootLogger

    if imgPath == "":
        imgPath = getInsert("", publicDomainImagePath)

    img = Image.open(imgPath)
    img.load()
    img = resizeToMinMax(img, maxW=1280, maxH=1024, minW=640, minH=480)
    inputFile = img.copy()

    squareCount = random.randint(10, 45)
    
    x = 0
    y = 0

    p1 = getParam(0)
    p1 = int(p1) if p1.isdecimal() else 1
    p1 = 1 if p1 > 1 else p1

    for i in range(squareCount):
        try:           
            x = random.randint(1, inputFile.size[0])
            y = random.randint(1, inputFile.size[1])

            w = random.randint(1, 350)

            if x + w > inputFile.size[0]:
                w = inputFile.size[0] - x
                
            h = random.randint(1, 350)

            if y + h > inputFile.size[1]:
                h = inputFile.size[1] - y            

            movedX = random.randint(1, inputFile.size[0])
            movedY = random.randint(1, inputFile.size[1])

            boxMoved = (movedX, movedY, movedX + w, movedY + h)

            region = inputFile.crop(boxMoved)

            # TODO: fix when the chosen region is at the edge so it doesn't turn black

            if p1 == 1:
                mask = Image.new("L", (region.size[0], region.size[1]), 0)
                maskdata = mask.load()
                draw = ImageDraw.Draw(mask)
                draw.ellipse([(0,0),(mask.size[0],mask.size[1])], 255, 255, 1)

            a = random.randint(1, inputFile.size[0])
            b = random.randint(1, inputFile.size[1])
            
            box = (a, b, a+w, b+h)
            
            if p1 == 1:
                img.paste(region, box, mask)
            else:
                img.page(region, box)

        except Exception as e:
            rootLogger.error(e)
            pass
   
    return img

def randomInversion(imgPath = ""):
    if imgPath == "":
        imgPath = getInsertById(getParam(4))

    global rootLogger

    img = Image.open(imgPath)
    img.load()

    img = resizeToMinMax(img, maxW=1280, maxH=1024, minW=640, minH=480)

    inputFile = img.copy()
    inputFile = inputFile.convert("RGB")
    inputFile = ImageOps.invert(inputFile)    

    z = random.randint(5, 50)
    
    for i in range(z):
        try:
            #box = (x, y, x + w, y + h)
            a = random.randint(1, inputFile.size[0])
            b = random.randint(1, inputFile.size[1])
            c = random.randint(1, inputFile.size[0])
            d = random.randint(1, inputFile.size[1])
            
            box = (a, b, c, d)
            
            region = inputFile.crop(box)
            img.paste(region, box)
        except Exception as e:
            rootLogger.error(e)
            pass

    img = img.convert("RGBA")
    img.load()
   
    return img

def repeatedInversion(imgPath=""):
    if imgPath == "":
        imgPath = getInsertById(getParam(4))

    img = Image.open(imgPath)
    img.load()

    img = resizeToMinMax(img, maxW=1024, maxH=768, minW=640, minH=480)
    
    draw = ImageDraw.Draw(img)
    
    x = 0
    y = 0

    orig = img.convert("RGB")
    orig = ImageOps.invert(orig)

    errors = 0

    w = orig.size[0]
    h = orig.size[1]
    
    for i in range(75):
        try:
            #box = (x, y, x + w, y + h)
            
            a = random.randint(1, w)
            b = random.randint(1, h)
            c = random.randint(a, w)
            d = random.randint(b, h)
            
            box = (a, b, c, d)
            
            region = orig.crop(box)
            img.paste(region, box)

            orig = ImageOps.invert(orig)    
        except:
            errors += 1
            pass
    
    return img

def remixer(imgPath="", rawImg=""):
    if imgPath == "":
        imgPath = getInsertById(getParam(4))
   
    # options
    desiredWidth = 1024.0
    desiredHeight = 768.0
    
    # pastebox width and height
    w = 111
    h = 111

    columnCount = 4
    rowCount = 5

    # chance paste will fail - 5, 1 is 20% (1 in 5)
    randomFactor = 4
    randomMatcher = 1
    
    useOriginalSize = True

    # end options

    if rawImg == "":
        inputFile = Image.open(imgPath)
        inputFile.load()
    else:
        inputFile = rawImg

    if useOriginalSize:
        desiredWidth = inputFile.size[0]
        desiredHeight = inputFile.size[1]

        w = desiredWidth // (columnCount)
        h = desiredHeight // (rowCount)

    if rawImg == "":
        img = Image.open(imgPath)
        img.load()
    else:
        img = rawImg

    # box = (left, upper, right, lower)
    # x, y, w, h = (70, 70, 30, 30)
    # box = (x, y, x + w, y + h)
    # region = img.crop(box)
    # img2.paste(region, box)

    midWidth = w * columnCount
    midHeight = h * rowCount

    startX = (inputFile.size[0] - midWidth) // 2
    startY = (inputFile.size[1] - midHeight) // 2

    lastPasteFailed = 0
    doPaste = True
    
    for row in range(rowCount):
        for col in range(columnCount):
            if random.randint(1, randomFactor) == randomMatcher:
            #if random.randint(1, 5) in [1, 2, 3, 4]:
                doPaste = False
            else:
                doPaste = True
                
            if doPaste or lastPasteFailed == 1:
                try:
                    #box = (x, y, x + w, y + h)

                    sourceX = random.randint(1, inputFile.size[0] - w)
                    sourceY = random.randint(1, inputFile.size[1] - h)
                    box = (sourceX, sourceY, sourceX + w, sourceY + h)
                    
                    region = inputFile.crop(box)

                    # move over w or h pixels per iteration
                    movedX = startX + (col * w)
                    movedY = startY + (row * h)
                    boxMoved = (movedX, movedY, movedX + w, movedY + h)            
                    
                    img.paste(region, boxMoved)
                    lastPasteFailed = 0
                except:
                    lastPasteFailed = 1
                    pass

    resizedFactor = 0
    resizedHeight = 0
    resizedWidth = 0

    originalWidth = img.size[0]
    originalHeight = img.size[1]
    
    if(img.size[0] > img.size[1]):
        # width greater than height
        resizedFactor = img.size[0] // desiredWidth
        resizedHeight = img.size[1] // resizedFactor

        resizedHeight = int(resizedHeight)
        desiredWidth = int(desiredWidth)
        
        img = img.resize((desiredWidth, resizedHeight))
    else:
        # height greater than width
        resizedFactor = img.size[1] // desiredHeight
        resizedWidth = img.size[0] // resizedFactor

        resizedWidth = int(resizedWidth)
        desiredHeight = int(desiredHeight)
        
        img = img.resize((resizedWidth, desiredHeight))

    debugText = False

    if debugText:
        draw = ImageDraw.Draw(img)
        debugTextSize = 12
        debugLineSize = debugTextSize + 5
        
        global fontPathSansSerif

        fon = ImageFont.truetype(fontPathSansSerif, debugTextSize)
        debugFillColor = (255, 0, 0, 128)
        textY = img.size[1] - debugLineSize
        
        outputMsg = 'resizedFactor: ' + str(resizedFactor)
        draw.text((5, textY), outputMsg, font=fon, fill=debugFillColor)
        textY -= debugLineSize

        outputMsg = 'resizedHeight: ' + str(resizedHeight)
        draw.text((5, textY), outputMsg, font=fon, fill=debugFillColor)
        textY -= debugLineSize

        outputMsg = 'resizedWidth: ' + str(resizedWidth)
        draw.text((5, textY), outputMsg, font=fon, fill=debugFillColor)
        textY -= debugLineSize

        outputMsg = 'originalWidth: ' + str(originalWidth)
        draw.text((5, textY), outputMsg, font=fon, fill=debugFillColor)
        textY -= debugLineSize

        outputMsg = 'originalHeight: ' + str(originalHeight)
        draw.text((5, textY), outputMsg, font=fon, fill=debugFillColor)
        textY -= debugLineSize

    img = resizeToMinMax(img, maxW=1024, maxH=768, minW=640, minH=480)
    
    return img

def colorfun(pixels, colors, ranges):
    new_pixels = []
    gtValue = -1
    
    for pixel in pixels:
        wasSet = False
        gtValue = -1

        for i in range(0, len(ranges) - 1):
            if pixel < ranges[i] and pixel > gtValue:
                color = get_rgb(colors, i)
                wasSet = True
                
            gtValue = ranges[i]

        if not wasSet:
            color = get_rgb(colors, len(colors) - 1)

        new_pixels.append(color)     

    return new_pixels

def get_rgb(colors, index, default=(255,255,255,0)):
    if type(colors[index]) is tuple:
        if len(colors) - 1 >= index:
            return colors[index]
        else:
            return default

    if isinstance(colors[index], str):
        if colors[index][0] == "#":
           return getrgb(colors[index]) 
        else:
            return getrgb('#' + colors[index])

    return default

def writeimage(img, frm="PNG"):
    [output, contentType, saveFormat] = writeImageToBytes(img, frm)

    filename = str(uuid.uuid4())

    return send_file(output, mimetype=contentType, as_attachment=False, download_name=filename+"."+saveFormat.lower())

def writeImageToBytes(img, frm="PNG"):
    saveFormat = ""
    contentType = ""
    output = BytesIO()

    if frm == "PNG":
        saveFormat = "PNG"
        contentType = "image/png"
        img.save(output, format=saveFormat)
    elif frm == "JPG":
        saveFormat = "JPEG"
        contentType = "image/jpeg"
        img.save(output, format=saveFormat)
    elif frm == "GIF":
        saveFormat = "GIF"
        contentType = "image/gif"
        img.save(output, format=saveFormat, save_all=True)    
    
    output.seek(0)

    return [output, contentType, saveFormat]

def writeToDisk(img, path, extension="PNG"):
    if extension == "GIF" or extension == ".gif":
        img.save(path, format="GIF", save_all=True)
    else:
        img.save(path, format=extension[-3:])

    rootLogger.info('Image saved: ' + path)
    
    return

def QRCoder(input_data="https://www.goatse.cx", fillColor="black", bgColor="white"):
    try:
        import qrcode
            
        qr = qrcode.QRCode(
            version=None,
            box_size=7,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            border=4)
            
        qr.add_data(input_data)

        qr.make(fit=True)
        img = qr.make_image(fill=fillColor, back_color=bgColor)

        img = img.convert("RGB")

        return img
    except ModuleNotFoundError as err:
        img = writeImageException(err)
    except Exception as e:
        img = writeImageException(e)

    return img

def generateQRCode():
    p1 = getParam(0)

    data = """BEGIN:VCARD
VERSION:3.0
N:I.P. Freely;
FN:I.P. Freely, Piss Christ;
TEL;TYPE=WORK;VOICE:(800) PEE-ON-ME
TEL;TYPE=WORK;FAX:(900) YUM-GOOD
EMAIL;TYPE=WORK,INTERNET:jesus@thepentagon.com                         
ADR;TYPE=POSTAL,WORK:;;Butt Incorporated;1 Tender-Ass Blvd;Sex Village;MO;80085;United States of America
END:VCARD"""

    if p1 != "":
        data = p1

    output = QRCoder(data)
    
    return output

def xannyImage(inputImgs):
    """there's too many images here. i need to xanny it"""

    doTimeCheck("xannying: " + str(len(inputImgs)) + " image(s)")
    width = 0
    height = 0
    yMargin = 10

    for i in inputImgs:
        height += i.size[1] + yMargin

        if i.size[0] > width:
            width = i.size[0]

    img = Image.new("RGBA", (width,height), "#ffffff")
    draw = ImageDraw.Draw(img)
    pixdata = img.load()

    y = 0
    x = 0

    rgbC = (0, 0, 0)

    for i in inputImgs:
        img.paste(i, (x, y))

        draw.line((x,y-(yMargin//2)+1,x+width,y-(yMargin//2)+1), fill=(rgbC), width=(yMargin//2)-2)

        y += i.size[1] + yMargin

    return img

def hueTranspose(filePath="", sideAmount=100):
    if filePath == "":
        filePath = getInsertById(getParam(4))

    wts = Image.open(filePath) 
    wts.load()
    wts = wts.convert("RGBA")

    wts = resizeToMinMax(wts, maxW=1024, maxH=768, minW=512, minH=384)
    
    pixdata = wts.load()

    height = wts.size[1]
    width = wts.size[0]    
    img = Image.new("RGB", (width,height), "#ffffff")
    
    moveFactor = 500
    
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            
            letuple = pixdata[x,y]
            r = letuple[0]
            g = letuple[1]
            b = letuple[2]
            a = letuple[3]

            randFactor = random.randint(4, 6)

            side = random.randint(sideAmount * -1, sideAmount)
            
            try:
                if randFactor == 1:
                    r = r + moveFactor
                if randFactor == 2:
                    g = g + moveFactor
                if randFactor == 3:
                    b = b + moveFactor
                if randFactor == 4:
                    g, b, r, a = pixdata[x+side,y]
                if randFactor == 5:
                    r, g, b = b, r, g
            except:
                r, g, b, a = r, g, b, a
                
            (r, g, b) = safetyCheck(r, g, b)
            
            pixdata[x, y] = (r, g, b, a)
                
    height = wts.size[1]
    width = wts.size[0]
    
    img.paste(wts, (0, 0), wts)
    return img

def atariripples():   
    width = getCurrentStandardWidth()
    height = getCurrentStandardHeight()
    img = Image.new("RGBA", (width,height), "#ffffff")
    draw = ImageDraw.Draw(img)
    
    pixdata = img.load()

    r = 0
    g = 0
    b = 0
    i = 0

    (r, g, b, i) = getRandomColor()
    
    j = i

    colorType = random.randint(0, 1)

    choices = getPaletteGenerated()

    xSize = random.randint(1, 15)
   
    x = 0
    while x < img.size[0]:
        direction = random.randint(0, 1)
        
        for y in range(img.size[1]):

            pixdata[x, y] = (r, g, b, j)
            
            try:
                for wr in range(1, xSize):
                    if x+wr < img.size[0]:
                        pixdata[x+wr, y] = (r, g, b, j)                
            except:
                pass

            if direction == 0:
                i += random.randint(1, 10)
            else:
                i -= random.randint(1, 10)

            i = abs(i % 255)
            j = i

            q = random.randint(0, 2)
            (r, g, b) = colorRandomInc(r, g, b, q)

        x += xSize
            
    return img

def halfbleed(imgInputPath=""):
    if imgInputPath == "":
        imgInputPath = getInsertById(getParam(4))

    wts = Image.open(imgInputPath)
    wts.load()
    wts = wts.convert("RGBA")

    pixdata = wts.load()
    height = wts.size[1]
    width = wts.size[0]

    img = Image.new("RGB", (width,height), "#ffffff")

##    for y in xrange(wts.size[1]):
##        for x in xrange(wts.size[0]):
##            if abs(pixdata[x, y][0] - blech[0]) < 30:
##                pixdata[x, y] = (255, 255, 255, 0)
##            elif abs(pixdata[x, y][1] - blech[1]) < 30:
##                pixdata[x, y] = (255, 255, 255, 0)
    
    iterations = 0
    
    for counter in range(0, iterations):
        pixdata = keepfuckinthatdata(height, width, pixdata)
        height = height - (height // iterations)
        width = width - (width // iterations)

    # these are the things
    for counter in range(0, random.randint(50, 80)):
        theThing = (5 * counter)
        thingVal = 111

        if theThing > thingVal:
            temp = theThing
            theThing = thingVal
            thingVal = temp
            
        startPlace = (random.randint(0,5)+(10*counter), random.randint(theThing,thingVal))

        eyeWidth = random.randint(20, 53)
        
        for x in range(0,eyeWidth):
            for y in range(0,random.randint(1,100)):
                blech2 = getRandomColor()

                try:
                    pixdata[startPlace[0] + x, startPlace[1] + y] = blech2
                except:
                    pass
    
    img.paste(wts, (0, 0), wts)

    img = resizeToMinMax(img, maxW=1024, maxH=768, minW=512, minH=384)
    
    return img

def linePainter(width=1024, height=768):
    img = Image.new("RGBA", (width,height), "#ffffff")
    pixdata = img.load()

    currentPoint = (random.randint(0, width), random.randint(0, height))

    bgColor = pixdata[0, 0]
    c = getRandomColor()

    pointCount = width * height
    i = 0
    j = 0
    
    try:
        while i < (pointCount // 2):
            x = 0
            y = 0
            
            while pixdata[currentPoint] != bgColor:
                whichWay = random.randint(0, 1)

                if whichWay == 0:
                    x = random.choice([-1, 1])
                else:
                    y = random.choice([-1, 1])

                newX = currentPoint[0] + x
                newY = currentPoint[1] + y

                if newX >= width:
                    newX = 0
                if newX < 0:
                    newX = width - 1
                    
                if newY >= height:
                    newY = 0
                if newY < 0:
                    newY = height - 1
                    
                currentPoint = (newX, newY)
            
            pixdata[currentPoint] = c # colorBlack
            i += 1
            j += 1

            if j >= (pointCount // 15):
                c = getRandomColor()
                j = 0
            
    except Exception as e:
        print(currentPoint)
        print(str(e))
        pass    
    
    return img

def imageWithText(imgPath = ""):
    if imgPath == "":
        imgPath = getInsertById(getParam(4))
        
    inputFile = Image.open(imgPath)
    inputFile.load()

    img = inputFile

    draw = ImageDraw.Draw(img)
    
    x = 0
    y = 0
    
    img = img.convert("RGBA")
    
    img = resizeToMinMax(img, maxW=1024, maxH=768, minW=800, minH=600)
    w = img.size[0]
    h = img.size[1]

    draw = ImageDraw.Draw(img)

    botString = getRandomWord() + " " + getRandomWord()

    currentFont = getFont()
    fontSize = random.randint(48, 96)
    fon = ImageFont.truetype(currentFont, fontSize)    
    text_size_x, text_size_y = dropin_text_size(draw,botString, font=fon)
    
    while text_size_x > w:
        fontSize -= 1        
        
        fon = ImageFont.truetype(currentFont, fontSize)
        text_size_x, text_size_y = dropin_text_size(draw,botString, font=fon)

    maxX = w - text_size_x
    minX = w // 3

    if minX >= maxX:
        minX = 0
    while minX >= maxX:
        maxX += 1

    maxY = h - text_size_y - 50
    minY = h // 2

    iY = 0
    if minY >= maxY:
        minY = 0
    while minY >= maxY:
        if iY == 0:
            minY = h // 2            
        else:
            minY -= iY
        
        iY -= 1
    
    if minY <= 0:
        minY = 0
        
    while minY >= maxY:
        maxY += 1

    x = random.randint(minX, maxX)
    y = random.randint(minY, maxY)    
    
    textStrokeExtra(draw, x, y, botString, fon, (0,0,0,255), 3)
    draw.text((x,y), botString, font=fon, fill=(255,255,255,128))

    return img

def colorRandomInc(r, g, b, q=-1):
    if q >= 0:
        x = q
    else:
        x = random.randint(0,2)

    if x == 0:
        if r >= 255:
            r = 0
        else:
            r = r + 1
    elif x == 1:
        if g >= 255:
            g = 0
        else:
            g = g + 1
    elif x == 2:
        if b >= 255:
            b = 0
        else:
            b = b + 1

    return (r, g, b)

def test():
    numbers_sizes = (i*10**exp for exp in range(2, 9) for i in range(1, 10))

    for n in numbers_sizes:
        print(n)        

def wordspiral(colorChoices=('000001','ff0000','00ff00','0000ff'),leWord=""):
    if leWord == "":
        leWord = getRandomWord()
    
    pallettes = (('000001','ff0000','00ff00','0000ff'),
                 ('082B2D','069498','73AC7F','C9FA9E','ffffff'),
                 ('ECD078','D95B43','C02942','542437','53777A'),
                 ('D9CEB2','948C75','D5DED9','7A6A53','99B2B7'),
                 ('951DF8','030105','CD1E1E','E48B19','E92581'),
                 ('4D454F','ffffff','FA1330','B3B5A7','2A1330'),
                 ('000000','D95B43','C02942','542437','2A1330'))

    colorChoices=pallettes[2]
    
    width = 1024
    height = 768
    img = Image.new("RGBA", (width,height), "#ffffff")
    draw = ImageDraw.Draw(img)

    #leWord = ''.join(str(random.randint(0,9)) for p in xrange(0,5))

    for r in range(1, 500, 35):
        for x in range(1, 50, 2):
            if r < 450 or 1==1:
                img = img.rotate(random.randint(30, 50))
                
            draw = ImageDraw.Draw(img)

##            rC = random.randint(0, 255)
##            gC = random.randint(0, 255)
##            bC = random.randint(0, 255)
##          fillColor = (rC, gC, bC)

            # try a random palette
            colorChoices=random.choice(pallettes)

            fillColor = '#'+random.choice(colorChoices)

            #fon = ImageFont.truetype(fontPath + "COOPBL.TTF", random.randint(36, 72))
            fon = ImageFont.truetype(fontPath + fontNameImpact, random.randint(36, 72))

            if random.randint(0, 1) == 1:
                draw.text((r + random.randint(0, r) - 4,r // (2 * r) + r), leWord, font=fon, fill="#000000")            

            draw.text((r + random.randint(0, r),r // (2 * r) + r), leWord, font=fon, fill=fillColor)
            
            #leWord = ''.join(str(random.randint(0,9)) for p in xrange(0,5))    

    return img

def iWannaBeTheTwo():
    try:
        img = iWannaBeTheOne()
        img2 = iWannaBeTheOne()
        
        imgPath = getInsert()
        imgPath2 = getInsert()
        
        inputFile = Image.open(imgPath)
        inputFile.load()

        inputFile2 = Image.open(imgPath2)
        inputFile2.load()

        w = img.size[0]
        h = img.size[1]

        wInsert = inputFile.size[0]
        hInsert = inputFile.size[1]

        wInsert2 = inputFile2.size[0]
        hInsert2 = inputFile2.size[1]
        
        if wInsert > w:
            x = 0
        else:
            x = (w - wInsert) // 2

        if hInsert > h:
            y = 0
        else:
            y = (h - hInsert) // 2
        
        #img.paste(inputFile, (x,y))

        inputFile = inputFile.resize((w, h), Image.LANCZOS)
        inputFile2 = inputFile2.resize((w, h), Image.LANCZOS)
        
        pixdata = img.load()
        mixdata = inputFile.load()
        mixdata2 = inputFile2.load()
        pixdata2 = img2.load()
        
        for ix in range(w):
            for iy in range(h):
                try:
                    if random.randint(0, 1) == 0: #iy % 2 == 0:
                        #pixdata[ix + x, iy + y] = mixdata[ix, iy]
                        #pixdata[ix, iy] = mixdata[ix, iy]
                        pixdata[ix, iy] = pixdata2[ix, iy]
                    #else:                    
                        #pixdata[ix, iy] = mixdata2[ix, iy]
                except:
                    pass

    except Exception as e:
        img = writeImageException(e)

    return img

def iWannaThreeTheBe():
    try:
        img = iWannaBeTheOne()
        img = img.resize((2048, 2048))
    
        fillColor = (255,255,255)

        draw = ImageDraw.Draw(img)

        txt = getRandomWord()
        
        for i in range(100):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)

            x = random.randint(-100, img.size[0])
            y = random.randint(-100, img.size[1])
            
            fillColor = (r, g, b)

            fon = ImageFont.truetype(getFont(), 128)
            
            draw.text((x, y), txt, font=fon, fill=fillColor)

            img = img.rotate(3)
            draw = ImageDraw.Draw(img)

        img = img.crop((200, 200, 1848, 1848))
        img = resizeToMinMax(img, maxW=1280, maxH=1024, minW=512, minH=384)

    except Exception as e:
        img = writeImageException(e)

    return img

def colorSwitchDetermine(z, color):
    colorOut = (0, 0, 0)
    
    if z == 0:
        colorOut = (color[0], color[1], color[2])
    elif z == 1:
        colorOut = (color[1], color[2], color[0])
    elif z == 2:
        colorOut = (color[2], color[0], color[1])
    elif z == 3:
        colorOut = (color[0], color[2], color[1])
    elif z == 4:
        colorOut = (color[1], color[0], color[2])
    elif z == 5:
        colorOut = (color[2], color[1], color[0])
        
    return colorOut

def colorSwitch(imgPath=""):
    if imgPath == "":
        imgPath = getInsertById(getParam(4))

    img = Image.open(imgPath)
    img.load()

    img = resizeToMinMax(img, maxW=800, maxH=600, minW=512, minH=384)

    origPic = img.copy()
    
    origW = img.size[0]
    origH = img.size[1]

    newW = origW * 2
    newH = origH * 3
    
    imgFull = Image.new("RGBA", (newW,newH), "#ffffff")

    version = []
                
    for z in range(0,6):
        version.append(z)

    random.shuffle(version)
                
    for z in range(0, 6):
        colorVersion = version[z]
                
        img = origPic.copy()
        img.load()    

        img = img.convert("RGBA")
           
        w = img.size[0]
        h = img.size[1]
        
        pixdata = img.load()

        for x in range(w):
            for y in range(h):
                pixdata[x, y] = colorSwitchDetermine(colorVersion, pixdata[x, y])

        if z == 0:
            pasteX = 0
            pasteY = 0
        elif z == 1:
            pasteX = w
            pasteY = 0
        elif z == 2:
            pasteX = 0
            pasteY = h
        elif z == 3:
            pasteX = w
            pasteY = h
        elif z == 4:
            pasteX = 0
            pasteY = h*2
        elif z == 5:
            pasteX = w
            pasteY = h*2
           
        imgFull.paste(img, (pasteX, pasteY, pasteX+w, pasteY+h), img)

    # resize the image down to <= the original size
    
    resizedW = newW
    resizedH = newH

    r = (newH * 1.0) // newW

    desiredW = (origW * 2.0)
    desiredH = (origH * 2.0)
    
    while resizedW > desiredW or resizedH > desiredH:
        resizedW -= 1.0
        resizedH = r * resizedW

    imgFull = imgFull.resize((int(resizedW), int(resizedH)), Image.LANCZOS)
    
    return imgFull

def starfield():
    imagelist = []
       
    w = 600
    h = 600

    # build the points
    
    points = []

    for i in range(75):
        (x, y) = (random.randint(0, w), random.randint(0, h))
        points.append((x,y))

    img = Image.new("RGBA", (w,h), "#000000")
    pixdata = img.load()

    pointCount = 0
    for p in points:
        (x, y) = (p[0], p[1])
        
        r = random.randint(50, 200)
        r2 = random.randint(r - 20, r + 20)

        alpha = random.randint(0, 255)
        
        if random.randint(0, 1) == 0:
            c = (r, r2, 0, alpha)
        else:
            c = (r2, r, 0, alpha)    

        ccc = random.randint(0, 2)

        if ccc == 0:
            c = (random.randint(180, 240), c[0], c[1], alpha)
        elif ccc == 1:
            c = (c[0], c[1], random.randint(180, 240), alpha)
        else:
            c = (c[0], random.randint(180, 240), c[1], alpha)
        
        try:
            pixdata[x, y] = c
        except:
            pass

        k = 1

        # vary the star size based on which loop this is
        jCount = 2

        if pointCount > 35:
            jCount = 3

        if pointCount > 45:
            jCount = 4
            
        diagOn = 0
        if random.randint(0, 3) == 3:
            diagOn = 1
            
        for j in range(jCount):
            c = (c[0], c[1], c[2]-30, alpha)            

            try:
                pixdata[x-k, y] = c
                pixdata[x+k, y] = c
                pixdata[x, y-k] = c
                pixdata[x, y+k] = c

                if diagOn == 1:
                    cAlpha = c[3] - 60
                    if cAlpha < 0:
                        cAlpha = 0
                        
                    pixdata[x-k, y-k] = (c[0], c[1], c[2], cAlpha)
                    pixdata[x+k, y+k] = (c[0], c[1], c[2], cAlpha)
                    pixdata[x-k, y+k] = (c[0], c[1], c[2], cAlpha)
                    pixdata[x+k, y-k] = (c[0], c[1], c[2], cAlpha)
            except:
                pass
            
            k += 1

        pointCount += 1        

    img = img.resize((int(w * 2), int(h * 2)), Image.NEAREST)
    
    return img

def replace_at_index(tup, ix, val):
    return tup[:ix] + (val,) + tup[ix+1:]
   
def subtlyWrong(imgpath=""):
    if imgpath == "":
        imgpath = getInsertById(getParam(4))

    img = Image.open(imgpath)

    img = resizeToMinMax(img, maxW=1280, maxH=1024, minW=640, minH=480)
    
    pixdata = img.load()
   
    a = random.randint(0, 2)
    b = random.randint(0, 1)
    z = random.randint(60, 140)

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if random.randint(0, 5) == 3:
                a = random.randint(0, 2)
                b = random.randint(0, 1)
                z = random.randint(60, 140)
    
            i = z if b == 0 else -1 * z

            c = pixdata[x,y]
            newval = c[a] + i

            if newval < 0:
                newval = 0
            elif newval > 255:
                newval = 255
            
            c = replace_at_index(c, a, newval)

            try:
                pixdata[x,y] = c
            except:
                pass
    
    return img

def subtlyWrongSquares(imgpath=""):
    if imgpath == "":
        imgpath = getInsert("", publicDomainImagePath)

    img = Image.open(imgpath)
    img = img.convert("RGBA")
    
    pixdata = img.load()

    yBoxes = random.randint(5, 15)
    xBoxes = random.randint(3, 10)
    
    cutoff1 = int(img.size[0] // xBoxes)
    cutoff2 = int(img.size[1] // yBoxes)

    yChanges = 0
    
    for y in range(img.size[1]):
        if y % cutoff2 == 0 and yChanges < yBoxes:
            statics = [()] * xBoxes
            
            for ichange in range(xBoxes):
                a = random.randint(0, 2)
                b = random.randint(0, 1)
                z = random.randint(60, 140)

                statics[ichange] = (a,b,z)

            yChanges += 1

        static = 0
        for x in range(img.size[0]):
            if x % cutoff1 == 0:                
                (a,b,z) = statics[static]
                static += 1
                
                if static > len(statics) - 1:
                    static = len(statics) - 1
                
            i = z if b == 0 else -1 * z            
            
            c = pixdata[x,y]
            newval = c[a] + i

            if newval < 0:
                newval = 0
            elif newval > 255:
                newval = 255
            
            c = replace_at_index(c, a, newval)

            try:
                pixdata[x,y] = c
            except:
                pass
    
    img = resizeToMinMax(img, maxW=1280, maxH=1024, minW=640, minH=480)

    return img

def drain(imgpath=""):
    try:
        if imgpath == "":
            imgpath = getInsert("", publicDomainImagePath)

        img = Image.open(imgpath)
        img = img.convert("RGBA")

        pixdata = img.load()
        
        for x in range(img.size[0]):
            for y in range(img.size[1]):
        
                c = pixdata[x,y]

                #for i in range(3):
                    #if c[i] < 70:
                        #c = replace_at_index(c, i, 0)
                    #   c = (c[i], c[i], c[i])

                i = 0 # random.randint(50, 80)
                j = random.randint(50, 80)
                if c[0] > j:
                    c = replace_at_index(c, 0, c[0] - j)
                    
                #c = (c[0] - i, c[1] - i, c[2] - i)

                for i in range(3):
                    if c[i] < 0:
                        c = replace_at_index(c, i, 0)
                        
                try:
                    pixdata[x,y] = c
                except:
                    pass
        
        img = resizeToMinMax(img, maxW=1280, maxH=1024, minW=640, minH=480)
    
    except Exception as e:
        img = writeImageException(e)

    return img

def gradientBars(imgpath=""):
    if imgpath == "":
        imgpath = getInsert("", publicDomainImagePath)

    img = Image.open(imgpath)
    img = img.convert("RGBA")

    img = resizeToMinMax(img, maxW=1280, maxH=1024, minW=640, minH=480)

    pixdata = img.load()

    lines = []
    while len(lines) < 5:
        iLine = random.randint(0, img.size[1]-1)
        if iLine not in lines:
            lines.append(iLine)

    iC = random.randint(0, 2)
    
    for y in range(img.size[1]):
        mod = 0
        for yy in range(random.randint(30, 70)):
            if y - yy in lines:
                mod = 255 - (4*yy)
                        
        if mod > 0:            
            jC = (0, 0, 0)
            jC = replace_at_index(jC, iC, mod)
            
            for x in range(img.size[0]):        
                c = pixdata[x,y]
                                       
                try:
                    pixdata[x,y] = jC
                except:
                    pass
        
    return img

def fakeGlitch(imgpath=""):
    if imgpath == "":
        imgpath = getInsert("", publicDomainImagePath)

    img = ""

    try:
        img = Image.open(imgpath)
        img = img.convert("RGBA")
        
        img = resizeToMinMax(img, maxW=1280, maxH=1024, minW=640, minH=480)
        
        pixdata = img.load()

        # introduce some noise
        
        yyy = 70

        if yyy > img.size[1]:
            yyy = yyy // 2

        lines = []
        while len(lines) < random.randint(20, yyy):
            iLine = random.randint(0, img.size[1]-1)
            if iLine not in lines:
                lines.append(iLine)
        
        for l in lines:
            for y in range(l, l+10):
                if y < img.size[1]:
                    for x in range(img.size[0]):
                        c = pixdata[x,y]

                        for i in range(0, 2):
                            cc = c[i] + random.randint(-20, 20)
                            c = replace_at_index(c, i, cc)
                            c = safetyCheck(c)
                            
                        pixdata[x,y] = c
                        
        lines = []

        while len(lines) < 7:
            iLine = random.randint(0, img.size[1]-1)
            
            if iLine not in lines:
                lines.append(iLine)

        # move some stuff sideways
        
        for l in lines:
            for y in range(l, l+10):
                i = random.randint(-10, 10)
                
                for x in range(0, img.size[0]):
                    xi = (x + i) % (img.size[0]-1)

                    if xi >= 0 and xi < img.size[0] and y >= 0 and y < img.size[1]:                    
                        c = pixdata[xi, y]

                        pixdata[x, y] = c

        lines = []

        while len(lines) < 7:
            iLine = random.randint(0, img.size[1]-1)
            
            if iLine not in lines:
                lines.append(iLine)

        # weird some bands

        allI = random.randint(0, 2)
        fFactor = random.randint(50, 150)
        
        for l in lines:
            ll = random.randint(0, 15)
            
            for y in range(l - ll, l + ll):
                for x in range(0, img.size[0]):
                    if x < img.size[0] and y < img.size[1] and x > 0 and y > 0:
                        c = pixdata[x, y]
                        c = replace_at_index(c, allI, c[allI] + fFactor)
                        c = safetyCheck(c)

                        pixdata[x, y] = c
                    
    except Exception as e:
        img = writeImageException(e)
        
    return img

def vhsText(imgpath=""):
    """p1: text<br />
    p2: font size<br />
    paramfont: partial font file name to match"""

    if imgpath == "":
        imgpath = getInsertById(getParam(4))

    img = Image.open(imgpath)
    img = resizeToMinMax(img, maxW=1280, maxH=1024, minW=640, minH=480)
    img = img.convert("RGB")
    
    pixdata = img.load()

    p1 = getParam(0)
    p2 = getParam(1)
    paramfont = getParam(3)

    textString = p1 if p1 != "" else getRandomWord() + " " + getRandomWord()
    textString = textString.upper()

    vcrSize = int(p2) if p2.isdecimal() else 72

    if paramfont != "":
        vcrPath = getFont(choiceStatic=paramfont)
    else:
        vcrPath = getFont()

    fon = ImageFont.truetype(vcrPath, vcrSize)

    draw = ImageDraw.Draw(img)    

    fsize = fon.getsize(textString)

    while fsize[0] > img.size[0] - 45:
        vcrSize -= 1
        fon = ImageFont.truetype(vcrPath, vcrSize)
        fsize = fon.getsize(textString)

    # center the text by finding the center, and subtracting half the text size
    x = int((img.size[0] // 2.0) - (fsize[0] // 2.0))
    
    maxY = img.size[1] - 75

    stepSize = random.randint(-50, -15)
    #stepSize = -30
    #stepSize = -22
    #stepSize = -17

    overdrive = random.randint(10, 30)
    
    for y in range(maxY - 60, (maxY // 2) + 40, stepSize):
        avgcolors = [0.0, 0.0, 0.0]

        for xc in range(img.size[0]):
            for i in range(3):
                avgcolors[i] += pixdata[xc,y][i]

        textC = (int(avgcolors[0] // img.size[0]), int(avgcolors[1] // img.size[0]), int(avgcolors[2] // img.size[0]))

        for i in range(3):
            textC = replace_at_index(textC, i, textC[i] + overdrive)
            
            if textC[i] > 255:
                textC = replace_at_index(textC, i, 255)
            elif textC[i] < 0:
                textC = replace_at_index(textC, i, 0)
                
        fillColor = (0, 0, 0, 255)
        textColor = textC 
        
        textStrokeExtra(draw, x, y, textString, fon, fillColor, 2)
        draw.text((x, y), textString, font=fon, fill=textColor)

    return img

def textGen():
    width = 1024
    height = 1024

    fontPathz = getFont()
    fontSize = 38
    img = Image.new("RGBA", (width,height), "#ffffff")
    fon = ImageFont.truetype(fontPathz, fontSize)

    jCount = 9
    textString = getRandomWord()

    colors = []
    for j in range(jCount):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        color = (r, g, b, 255)
        colors.append(color)
        
    for i in range(4):
        draw = ImageDraw.Draw(img)
        
        for j in range(jCount):            
            fillColor = (0, 0, 0, 255)
            textColor = colors[j]

            x = width // 2
            y = (height // 2) + (j * fontSize)
            
            textStroke(draw, x, y, textString, fon, fillColor)
            draw.text((x, y), textString, font=fon, fill=textColor)
            
        img = img.rotate(90)

    img = img.rotate(45)
    
    return img

def textGen2(textString=getRandomWord(), fontPath=getFont(), changeEvery=1, textColor=None):
    width = 1024
    height = 1024

    #fontPath = fontPath + "lamebrai.ttf" # getFont()
    fontSize = 128
    img = Image.new("RGBA", (width,height), "#ffffff")    

    if changeEvery == 0:
        fon = ImageFont.truetype(fontPath, fontSize)
        
    for i in range(75):
        if changeEvery == 1:
            fontPath=getFont()
            fon = ImageFont.truetype(fontPath, fontSize)
            
        draw = ImageDraw.Draw(img) 

        fillColor = (0, 0, 0, 255)

        if textColor != None:
            color = textColor
        else:            
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)

            color = (r, g, b, 255)

        x = random.randint((img.size[0]/2) * -1, img.size[0]-1)
        y = random.randint(-20, img.size[1]-1)
        
        textStroke(draw, x, y, textString, fon, fillColor)
        draw.text((x, y), textString, font=fon, fill=color)
   
    return img

def textGenScatter():
    global maxFloodFillArg
    
    targ = (0, 255, 0, 255)
    img = textGen2(getRandomWord(), getFont(), 1, targ)

    pixdata = img.load()
    
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            c = pixdata[x,y]
            if c == targ:
                #xi = random.randint(0, img.size[0]-1)
                #yi = random.randint(0, img.size[1]-1)

                r = random.randint(0, 255)
                g = random.randint(0, 50)
                b = random.randint(0, 75)

                color = (r, g, b, 255)
                
                #pixdata[x,y] = color

                rit = random.randint(13, 15)
                
                floodfill(img, (x, y), targetcolour = targ,
                              newcolour = (0,0,0),
                              randomIt = rit)
            
    return img
   
def colorizerize(imgpath=""):
    if imgpath == "":
        imgpath = getInsertById(getParam(4))

    img = Image.open(imgpath)
    img = img.convert("RGBA")
    
    pixdata = img.load()    
    draw = ImageDraw.Draw(img)

    width = img.size[0]
    height = img.size[1]
    section = width // 3

    # pick which third will be red, green, blue
    i1 = random.randint(0, 2)
    i2 = (i1 + 1) % 3
    i3 = (i1 + 2) % 3

    secSize = 30
    
    for y in range(0, img.size[1]):
        #section0 = section + random.randint(-y/2, y/2)
        #section1 = (section * 2) + random.randint(-y/2, y/2)

        section0 = section + random.randint(secSize * -1, secSize)
        section1 = 2 * section + random.randint(secSize * -1, secSize)
        
        for x in range(0, img.size[0]):
            if x < section0:
                i = i1
            elif x < section1:
                i = i2
            else:
                i = i3
                
            c = pixdata[x,y]
            xxxxx = c[i]+random.randint(10, 22)

            if xxxxx > 255:
                xxxxx = 255
                
            c = replace_at_index(c, i, xxxxx)
            pixdata[x,y] = c

    img = resizeToMinMax(img, maxW=1280, maxH=1024, minW=640, minH=480)
    
    return img

def randgradient():
    w = 800
    h = 800
    img = Image.new("RGB", (w,h), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    for j in range(3):
        r,g,b = random.randint(0,255), random.randint(0,255), random.randint(0,255)
        dr = (random.randint(0,255) * 1.0 - r) // w
        dg = (random.randint(0,255) * 1.0 - g) // w
        db = (random.randint(0,255) * 1.0 - b) // w
        
        for i in range(0, w, 1):
            if random.randint(1,50) == 1:
                r,g,b = r+dr, g+dg, b+db
                dw = (random.randint(1,10))
                lineWidth = random.randint(5, 6)
                draw.line((i,dw,i+dw,h-dw), fill=(int(r),int(g),int(b)), width=lineWidth)
                
                if(random.randint(1,5) == 3):
                    draw.line((i,dw,i+dw+dw,h-dw-dw), fill=(int(g),int(b),int(r)))

        for i in range(0, h, 1):
            if random.randint(1,50) == 1:
                r,g,b = r+dr, g+dg, b+db
                dh = (random.randint(1,10))
                lineWidth = random.randint(5, 6)
                draw.line((dh,i,w-dh,i+dh), fill=(int(r),int(g),int(b)), width=lineWidth)

                if(random.randint(1,5) == 3):
                    draw.line((dh,i,w-dh-dh,i+dh+dh), fill=(int(g), int(b), int(r)))

    pixdata = img.load()

    lastColor = (0,0,0)
    
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x,y] == (255,255,255):
                pixdata[x,y] = lastColor
                lastColor = (lastColor[0]+1,lastColor[1]+1,lastColor[2]+1)

                if lastColor[0] > 255:
                    lastColor = (0,lastColor[1],lastColor[2])

                if lastColor[1] > 255:
                    lastColor = (lastColor[0],0,lastColor[2])

                if lastColor[2] > 255:
                    lastColor = (lastColor[0],lastColor[1],0)
            else:
                lastColor = pixdata[x,y]
                
    text = "Hello nurse, how are you." # sentence.getString();
    size = 128

    #fill = (82, 124, 178)
    #fill = (255, 255, 255)
    fill = (10, 10, 10)

    font = ImageFont.truetype(fontPath + fontNameImpact, size)
    size = font.getsize(text) # Returns the width and height of the given text, as a 2-tuple.
    # draw.text((0, 0), text, font=font, fill=fill)

    #draw_word_wrap(img, draw, text, 5, 5, w - 5, fill, font)

    return img

palettesMaster = (('082B2D','069498','73AC7F','C9FA9E','ffffff'),
                 ('ECD078','D95B43','C02942','542437','53777A'),
                 ('D9CEB2','948C75','D5DED9','7A6A53','99B2B7'),
                 ('951DF8','030105','CD1E1E','E48B19','E92581'),
                 ('4D454F','ffffff','FA1330','B3B5A7','2A1330'),
                 ('fe80fe','01cdfe','fac0aa','fefe66','fefec4'))

def pieslice():
    width = 800
    height = 800
    
    img = Image.new("RGBA", (width,height), "#000000")
    draw = ImageDraw.Draw(img)
    pixdata = img.load()

    pieWidth = 800
    pieHeight = 800

    #boxes = [(0,0,400,400),
    #         (400,0,800,400),
    #         (0,400,400,800),
    #         (400,400,800,800)]

    boxes = [(0,0,800,800)]

    angles = []
    colors = []
    
    for y in range(0, len(boxes)):
        for x in range(0, random.randint(200,600), 5):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            
            startAngle = random.randint(0, 360)
            endAngle = random.randint(0, 360)

            color = (r,g,b)
            angle = (startAngle, endAngle, x)

            colors.append(color)
            angles.append(angle)

    i = 0
    y = 0
    for a in angles:       
        color = colors[i]
        startAngle = a[0]
        endAngle = a[1]
        x = a[2]
        
        boundingBox = (boxes[y][0]+x, boxes[y][1]+x, boxes[y][2]-x, boxes[y][3]-x)
        draw.pieslice(boundingBox, startAngle, endAngle, fill=color, outline=(0,0,0))

        if i % 2 == 0:
            floodRan = False

            for yy in range(boxes[y][1]+1, boxes[y][3]):
                if not floodRan:
                    for xx in range(boxes[y][0]+1, boxes[y][2]):
                        if not floodRan and pixdata[xx,yy][0:3] == (r,g,b):            
                            floodfill(img, (xx, yy), targetcolour = pixdata[xx,yy],
                              newcolour = (0,0,0),
                              randomIt = 12)

                            floodRan = True
                            break

        draw = ImageDraw.Draw(img)
        i += 1

    return img

def pieslice_anim():
    import subprocess
    
    width = 800
    height = 800
    
    pieWidth = 800
    pieHeight = 800

    #boxes = [(0,0,400,400),
    #         (400,0,800,400),
    #         (0,400,400,800),
    #         (400,400,800,800)]

    boxes = [(0,0,800,800)]

    angles = []
    colors = []

    palette = palettesMaster[5]
    
    for y in range(0, len(boxes)):    
        for x in range(0, random.randint(200,600), 15):
            #r = random.randint(0, 255)
            #g = random.randint(0, 255)
            #b = random.randint(0, 255)
            
            startAngle = random.randint(0, 360)
            endAngle = random.randint(startAngle + 20, startAngle+180)

            endAngle = endAngle % 360

            #color = (r,g,b)
            color = hex_to_rgb(random.choice(palette))
            angle = (startAngle, endAngle, x)

            colors.append(color)
            angles.append(angle)

    imagelist = []

    imgTotal = 32
    
    y = 0
    for imgCount in range(0, imgTotal):
        img = Image.new("RGBA", (width,height), "#000000")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        i = 0
        fuckFactor = -1
        
        for a in angles:
            fuckFactor = fuckFactor * -1
            color = colors[i]
            startAngle = a[0] + (imgCount*(360/imgTotal)*fuckFactor)
            endAngle = a[1] + (imgCount*(360/imgTotal)*fuckFactor)
            x = a[2]
            
            boundingBox = (boxes[y][0]+x, boxes[y][1]+x, boxes[y][2]-x, boxes[y][3]-x)
            draw.pieslice(boundingBox, startAngle, endAngle, fill=color, outline=(0,0,0))

            floodRan = False

##            for yy in range(boxes[y][1]+1, boxes[y][3]):
##                if not floodRan:
##                    for xx in range(boxes[y][0]+1, boxes[y][2]):
##                        if not floodRan and pixdata[xx,yy][0:3] == (r,g,b):            
##                            floodfill(img, (xx, yy), targetcolour = pixdata[xx,yy],
##                              newcolour = (0,0,0),
##                              randomIt = 12)
##
##                            floodRan = True
##                            break

            draw = ImageDraw.Draw(img)
            i += 1

        outputPath = "./pie_" + str(imgCount) + ".png"
        imagelist.append(outputPath)
        
        writeToDisk(img, outputPath)
        print("Wrote: " + outputPath)

    print(returnValue)
    
    return img

def glitchUp():   
    imgpath = getInsertById(getParam(4))
    
    img = Image.open(imgpath)
    img = img.convert("RGBA")

    pixdata = img.load()
    r, g, b, a = 0,0,0,0

    i = 1
    bumps = 1
    
    for y in range(0, img.size[1], 10):
        for x in range(0, img.size[0], 10):
            if (x > 425 and y > 220) or y > 275:
                if random.randint(1, bumps) < (bumps // 2.7) or bumps < 5 or (y > 350 and random.randint(0,1) == 1) or y > 414:
                    r = int(abs(math.sin(bumps)*220)) # random.randint(0, 255)
                    g = int(abs(math.cos(bumps)*100)) # random.randint(0, 255)
                    b = int(abs(math.tan(bumps)*170)) # random.randint(0, 255)
                    a = random.randint(y % 200, 255)

                    if y < 350:
                        b = random.randint(200, 255)
                        
                    if y > 400:
                        r = 255

                    if y > 450 and x > 100:
                        g = 0

                    if y > 525 and x > 200:
                        b = 0
                        
                    for jj in range(0, 20): # random.randint(10, 20)):
                        for ii in range(0, 20): # random.randint(10, 20)):
                            try:
                                pixdata[x+ii,y+jj] = (r,g,b,a)
                            except:
                                pass
                        
                    bumps += 1
                    
                i += 1

                if i > sys.maxsize:
                    i = 1

                if bumps > sys.maxsize:
                    bumps = 1

    img = resizeToMinMax(img, maxW=1280, maxH=1024, minW=640, minH=480)
    return img

# EMULSIFIED ZEROHOUR

def threecolor(imgPath=""):
    if imgPath == "":
        imgPath = getInsertById(getParam(4))

    img = Image.open(imgPath)
    img.load()    

    origW = img.size[0]
    origH = img.size[1]

    newW = origW * 3
    newH = origH
    
    imgFull = Image.new("RGBA", (newW,newH), "#ffffff")
    
    for z in range(0, 3):
        img = Image.open(imgPath)
        img.load()    

        img = img.convert("RGBA")
           
        w = img.size[0]
        h = img.size[1]
        
        pixdata = img.load()

        for x in range(w):
            for y in range(h):
                colorOut = (0,0,0)
                color = pixdata[x,y]

                colorOut = (0, 0, 0)
    
                if z == 0:
                    colorOut = (color[0]+100, color[1], color[2])
                elif z == 1:
                    colorOut = (color[2], color[0], color[1])
                elif z == 2:                    
                    colorOut = (color[1], color[2], color[0])
                elif z == 3:
                    colorOut = (color[0], color[2], color[1])
                elif z == 4:
                    colorOut = (color[1], color[0], color[2])
                elif z == 5:
                    colorOut = (color[2], color[1], color[0])

                (r, g, b) = colorOut
                if r > 255:
                    r = 255
                if g > 255:
                    g = 255
                if b > 255:
                    b = 255
                colorOut = (r, g, b)

                pixdata[x, y] = colorOut

        if z == 0:
            pasteX = 0
            pasteY = 0
        elif z == 1:
            pasteX = w
            pasteY = 0
        elif z == 2:
            pasteX = w * 2
            pasteY = 0        
           
        imgFull.paste(img, (pasteX, pasteY, pasteX+w, pasteY+h), img)

    imgFull = resizeToMinMax(imgFull, maxW=1280, maxH=1024, minW=640, minH=480)
    
    return imgFull

def hardLandscape():
    height = 800
    width = 800

    img = Image.new("RGBA", (width, height), "#FFFFFF")    

    palette = getPalette()
    
    demarcs = [160, 250, 350, 430]
    lastDem = 0
    
    draw = ImageDraw.Draw(img)
    pixdata = img.load()

    fillPtMsgs = []
    
    i = 0
    for dem in demarcs:
        ptLast = (width, dem)
        
        pts = [(0, dem)]
        
        peaks = random.randint(3, 17)

        for x in range(0, width, width // peaks):
            y = random.randint(pts[-1][1] - 30, pts[-1][1] + 30)

            # don't cross the streams
            if y < lastDem:
                y = lastDem + 1
                
            pts.append((x, y))

        pts.append((width, y))
        
        for pt in range(0, len(pts) - 1):        
            draw.line((pts[pt][0], pts[pt][1], pts[pt+1][0], pts[pt+1][1]), fill=palette[i])        

        sortedpts = sorted(pts, key=lambda tup: tup[1])

        targetPt = sortedpts[0]
        
        #try:
        targ = pixdata[targetPt[0], targetPt[1]-1]

        msg = str(targetPt) + ": " + str(targ)
        fillPtMsgs.append(msg)

        floodfill(img, (targetPt[0]+5, targetPt[1]-1), targetcolour = targ,
                  newcolour = palette[i],
                  randomIt = 0)
        #except:
        #    pass

        lastDem = dem
        i += 1

    targ = pixdata[width/2, height-1]
    
    floodfill(img, (width // 2, height-1), targetcolour = targ,
                  newcolour = palette[i],
                  randomIt = 0)

##    global fontPathSansSerif
##    fon = ImageFont.truetype(fontPathSansSerif, 12)
##    debugFillColor = (255, 0, 0, 128)    
##
##    textY = 0
##    for msg in fillPtMsgs:
##        draw.text((5, textY), msg, font=fon, fill=debugFillColor)
##        textY += 12

    whiteFound = False
    
    for x in range(0, width - 1):
        for y in range(0, height - 1):
            if pixdata[x,y][0:3] == (255,255,255):
                whiteFound = True
                break

    if whiteFound:
        img = hardLandscape()
        
    return img

def hardLandscape2():
    height = getCurrentStandardHeight()
    width = getCurrentStandardWidth()

    try:
        img = Image.new("RGBA", (width, height), "#FFFFFF")    

        colorDiff = 10
        
        demarcs = [50, 100, 200, 300, 400, 500, 600, 700, 750]
        lastDem = 0

        maxCPart = 255 - (len(demarcs) * colorDiff)
        c = (random.randint(0, maxCPart), random.randint(0, maxCPart), random.randint(0, maxCPart))

        colors = []
                            
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        fillPtMsgs = []

        lastMax = 0
        
        i = 0
        for dem in demarcs:
            thisDiff = random.randint(colorDiff - 3, colorDiff + 3)
            
            c = (c[0] + thisDiff, c[1] + thisDiff, c[2] + thisDiff)
            c = safetyCheck_LeaveAtMax(c)
            
            ptLast = (width, dem)
            
            pts = [(0, dem)]
            
            peaks = random.randint(3, 17)

            for x in range(0, width, width // peaks):
                y = random.randint(pts[-1][1] - 30, pts[-1][1] + 30)

                # don't cross the streams
                if y < lastDem:
                    y = lastDem + 1

                if y < lastMax:
                    y = lastMax + 2
                    
                pts.append((x, y))

            pts.append((width, y))

            colors.append((lastMax, c))
            
            for pt in range(0, len(pts) - 1):
                thisy = pts[pt][1]

                if thisy > lastMax:
                    lastMax = thisy
                    
                draw.line((pts[pt][0], pts[pt][1], pts[pt+1][0], pts[pt+1][1]), fill=c)

            sortedpts = sorted(pts, key=lambda tup: tup[1])

            targetPt = sortedpts[0]
            
            targ = pixdata[targetPt[0], targetPt[1]-1]

            msg = str(targetPt) + ": " + str(targ)
            fillPtMsgs.append(msg)

            floodfill(img, (targetPt[0]+5, targetPt[1]-1), targetcolour = targ,
                      newcolour = c,
                      randomIt = 0)

            lastDem = dem
            i += 1

        targ = pixdata[width/2, height-1]
        
        floodfill(img, (width // 2, height-1), targetcolour = targ,
                      newcolour = c,
                      randomIt = 0)
        
        for x in range(0, width - 1):
            for y in range(0, height - 1):
                if pixdata[x,y][0:3] == (255,255,255):
                    
                    for ctup in colors:
                        if y > ctup[0]:
                            c = ctup[1]

                    targ = pixdata[x,y]
                    
                    floodfill(img, (x, y), targetcolour = targ,
                              newcolour = c,
                              randomIt = 0)

                    break
            
    except Exception as e:
        img = writeImageException(e)
        
    return img

def hardLandscape3():
    height = 800
    width = 800

    try:
        img = Image.new("RGBA", (width, height), "#FFFFFF")    

        global maxFloodFillArg
        
        demarcs = [100, 300, 500, 700]
        lastDem = 0

        colors = getPaletteGenerated()

        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        fillPtMsgs = []
        lastMax = 0
        
        i = 0
        for dem in demarcs:           
            c = random.choice(colors)
            
            ptLast = (width, dem)
            
            pts = [(0, dem)]
            
            peaks = random.randint(3, 17)

            for y in range(0, width, width // peaks):
                x = random.randint(pts[-1][1] - 30, pts[-1][1] + 30)

                # don't cross the streams
                if x < lastDem:
                    x = lastDem + 1

                if x < lastMax:
                    x = lastMax + 2
                    
                pts.append((y, x))

            pts.append((width, x))
           
            for pt in range(0, len(pts) - 1):
                thisy = pts[pt][1]

                if thisy > lastMax:
                    lastMax = thisy
                    
                draw.line((pts[pt][1], pts[pt][0], pts[pt+1][1], pts[pt+1][0]), fill=c)

            sortedpts = sorted(pts, key=lambda tup: tup[1])

            targetPt = sortedpts[0]            
            targ = pixdata[targetPt[0], targetPt[1]-1]

            msg = str(targetPt) + ": " + str(targ)
            fillPtMsgs.append(msg)

            floodfill(img, (targetPt[0]+5, targetPt[1]-1), targetcolour = targ,
                      newcolour = c,
                      randomIt = random.randint(1, maxFloodFillArg),
                      choices = colors)

            lastDem = dem
            i += 1

        targ = pixdata[width/2, height-1]
        
        floodfill(img, (width // 2, height-1), targetcolour = targ,
                      newcolour = c,
                      randomIt = 0)

        # fix any white ones
        for x in range(0, width - 1):
            for y in range(0, height - 1):
                if pixdata[x,y][0:3] == (255,255,255):
                    targ = pixdata[x,y]

                    c = random.choice(colors)
                    
                    floodfill(img, (x, y), targetcolour = targ,
                              newcolour = c,
                              randomIt = random.randint(1, maxFloodFillArg),
                              choices = colors)

                    break
                
    except Exception as e:
        img = writeImageException(e)
        
    return img

def lotsOfLetters():
    width = getCurrentStandardWidth()
    height = getCurrentStandardHeight()

    (r,g,b) = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
    
    try:
        img = Image.new("RGBA", (width, height), getRandomColor())        
        draw = ImageDraw.Draw(img)

        grid = 50

        used = []
        
        for i in range(500):
            fon = ImageFont.truetype(getFont(), grid - 5)
            x = random.randint(-5, int(width // grid * 1.0)) * grid
            y = random.randint(-5, int(height // grid * 1.0)) * grid

            if random.randint(0, 10) == 0:
                (r,g,b) = (g,b,r)

            if (x, y) not in used:
                txt = random.choice(string.ascii_letters)

                cInv = (255 - r, 255 - g, 255 - b)
                
                textStrokeExtra(draw, x, y, txt, fon, cInv, 2)
                draw.text((x, y), txt, font=fon, fill=(r,g,b))

                i = random.randint(-2, 2)

                textStrokeExtra(draw, x+i, y+i, txt, fon, (r,g,b), 2)
                draw.text((x+i, y+i), txt, font=fon, fill=cInv)

                used.append((x, y))

        pixdata = img.load()
               
    except Exception as e:
        img = Image.new("RGBA", (width, height), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        x = 5
        y = 0

        fon = ImageFont.truetype(fontPath + fontNameMono, 12)
        
        draw.text((x, y), str(e), font=fon, fill=(0,0,0,128))
        
    return img

def pixelDiff(imgPath=""):
    try:
        if imgPath == "":
            imgPath = getInsertById(getParam(4))

        img = Image.open(imgPath)
        img = img.convert("RGB")

        pixdata = img.load()    

        lastC = (0,0,0)
        markColor = (0,128,0)
        
        for y in range(img.size[1]):
            # get average color
            avgcolors = [0, 0, 0]

            for xc in range(img.size[0]):
                for i in range(3):
                    avgcolors[i] += pixdata[xc,y][i]

            avgcolor = (avgcolors[0] // img.size[0], avgcolors[1] // img.size[0], avgcolors[2] // img.size[0])

            for i in range(3):
                avgcolor = replace_at_index(avgcolor, i, avgcolor[i] + 15)
                
                if avgcolor[i] > 255:
                    avgcolor = replace_at_index(avgcolor, i, 255)
                elif avgcolor[i] < 0:
                    avgcolor = replace_at_index(avgcolor, i, 0)
                    
            for x in range(img.size[0]):
                thisC = pixdata[x,y]

                diff = [-1,-1,-1]
                
                for a in range(len(lastC)):
                    #diff[a] = abs(lastC[a] - thisC[a])
                    diff[a] = abs(avgcolor[a] - thisC[a])

            # markColor = lastC
                
                colorDiff = 105
                
                if diff[0] > colorDiff or diff[1] > colorDiff or diff[2] > colorDiff:
                    randX = random.randint(0,0)
                    randY = random.randint(0,0)

                    mcG = random.randint(-50, 50)
                    
                    try:
                        pixdata[x+randX,y+randY] = (markColor[0],markColor[1]+mcG,markColor[2])
                    except:
                        pass
                else:
                    lastC = thisC

        (resizedW, resizedH) = getSizeByMax(img.size[0], img.size[1], 800, 600)
        
        img = img.resize((int(resizedW), int(resizedH)), Image.LANCZOS)

    except Exception as e:
        img = writeImageException(e)

    return img

def textGrid(word="ALONE"):
    if word == "":
        word = getRandomWord()
        
    width = 1000
    height = 1000  
           
    try:        
        palette = getPalette()

        c = random.choice(palette)
        
        img = Image.new("RGBA", (width, height), c)
        draw = ImageDraw.Draw(img)

        used = []
        used.append(c)
        
        for j in range(3):
            maxX = 0
            x = 0
            
            while maxX < img.size[0]:
                x = maxX + 10
                y = 0
                maxY = 0
                
                while maxY < img.size[1]:
                    y = maxY + 10
                    
                    fon = ImageFont.truetype(getFont(), random.randint(20, 50))

                    text_size_x, text_size_y = dropin_text_size(draw, word, font=fon)

                    if text_size_x + x > maxX:
                        maxX = x + text_size_x + 5

                    if text_size_y + y > maxY:
                        maxY = y + text_size_y + 5
                        
                    #print x, y, maxX, maxY

                    if len(used) >= len(palette):
                        used = []
                        
                    fillColor = random.choice(palette)

                    while fillColor in used:
                        fillColor = random.choice(palette)
                    
                    if y + text_size_y < img.size[1] and x + text_size_x < img.size[0]:                        
                        draw.text((x, y), word, font=fon, fill=fillColor)
                        
    except Exception as e:
        img = writeImageException(e)  
        
    return img

def fourdots():
    width = 1200
    height = 1000

    try:
        img = Image.new("RGBA", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        global palettesMaster
        palette = random.choice(palettesMaster)

        yStep = 50
        xStep = 17
        
        for y in range(0, img.size[1], yStep):
            for x in range(0, img.size[0], xStep):
                c = hex_to_rgb(random.choice(palette))

                for i in range(xStep):
                    for j in range(yStep):
                        if x+i < width and y+j < height:
                            pixdata[x+i,y+j] = c
    except Exception as e:
        img = writeImageException(e)
        
    return img

def fourdotsAnim():
    try:
        frames = []

        palette = getPaletteGenerated()

        width = 1024
        height = 1024
    
        yStep = random.randint(30, 75)
        xStep = yStep

        for i in range(0, 10):
            img = Image.new("RGBA", (width,height), "#ffffff")
            pixdata = img.load()            
            
            for y in range(0, img.size[1], yStep):
                for x in range(0, img.size[0], xStep):
                    c = random.choice(palette)

                    for i in range(xStep):
                        for j in range(yStep):
                            if x+i < width and y+j < height:
                                pixdata[x+i,y+j] = c
        
            # Saving/opening is needed for better compression and quality
            fobj = BytesIO()
            img.save(fobj, 'GIF')
            frame = Image.open(fobj)
            frames.append(frame)

        animated_gif = BytesIO()
        frames[0].save(animated_gif,
                    format='GIF',
                    save_all=True,
                    append_images=frames[1:],
                    duration=1,
                    loop=0)
        
        animated_gif.seek(0)
        img = Image.open(animated_gif)
    
    except Exception as e:
        img = writeImageException(e)
        
    return img

def xdots():
    width = 1200
    height = 1000

    try:
        img = Image.new("RGBA", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        i = random.randint(3, 10)

        palette = getPaletteGenerated(paletteLength=i)

        yStep = random.randint(10, 70)
        xStep = random.randint(10, 70)

        pts = []
        
        for y in range(0, img.size[1], yStep):
            for x in range(0, img.size[0], xStep):
                pts.append((x, y))

        random.shuffle(pts)
        
        for pt in pts:
            x = pt[0]
            y = pt[1]
           
            c = random.choice(palette)

            for i in range(xStep):
                for j in range(yStep):
                    if x+i < width and y+j < height:
                        pixdata[x+i,y+j] = c
                        
    except Exception as e:
        img = writeImageException(e)
        
    return img

def fourdotsRemixed():
    img = fourdots()
    img = remixer("", img)
    
    return img

def fourdots_18():
    width = 1200
    height = 1000       

    try:
        img = Image.new("RGBA", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        global palettesMaster
        palette = random.choice(palettesMaster)

        yStep = 11
        xStep = 11
        
        for y in range(0, img.size[1], yStep):
            for x in range(0, img.size[0], xStep):
                c = hex_to_rgb(random.choice(palette))

                for i in range(xStep):
                    for j in range(yStep):
                        if x+i < width and y+j < height:
                            pixdata[x+i,y+j] = c

        #imgOrig = img
        
        for i in range(5000):
            x = random.randint(0, img.size[0]-1)
            y = random.randint(0, img.size[1]-1)
            
            targ = pixdata[x,y]
            
            floodfill(img, (x, y), targetcolour = targ,
                  newcolour = (0,0,0),
                  randomIt = random.randint(18, 19),
                  sizeLimit=(11,11))

#        img = ImageOps.contrast(img, cutoff=0, ignore=None)            
    except Exception as e:
        img = writeImageException(e)

    return img

def eightdots():
    width = 1200
    height = 1000       

    try:
        img = Image.new("RGBA", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        global palettesMaster
        palette = random.choice(palettesMaster)

        starting = [(0,0,25,25,""),
                    (12,12,50,25,""),
                    (37,37,100,25,"")]        
        
        for start in starting:
            yStep = start[2]
            xStep = start[2]
            xSize = start[3]
            ySize = start[3]
            override = start[4]
            
            for y in range(start[1], img.size[1], yStep):
                for x in range(start[0], img.size[0], xStep):
                    if override == "":
                        c = hex_to_rgb(random.choice(palette))
                    else:
                        c = hex_to_rgb(override)

                    for i in range(xSize):
                        for j in range(ySize):
                            if x+i < width and y+j < height:
                                pixdata[x+i,y+j] = c
            
        for y in range(0, img.size[1], 50):
            for x in range(0, img.size[0], 50):
                targ = pixdata[x,y]

                floodalg = 3
                if x % 100 == 0 and y % 100 == 0:
                    floodalg = random.randint(1, 18)
                    
                floodfill(img, (x, y), targetcolour = targ,
                  newcolour = (0,0,0),
                  randomIt = floodalg,
                  sizeLimit=(100,100))
                
    except Exception as e:
        img = writeImageException(e)

    return img

def bigSquareGrid(choices=[], yStep=0, xStep=0):
    width = getCurrentStandardWidth()
    height = getCurrentStandardHeight()

    try:
        if yStep == 0:
            yStep = random.randint(18, 111)

        if xStep == 0:
            xStep = yStep

        width = width - (width % xStep)
        height = height - (height % yStep)

        img = Image.new("RGBA", (width, height), "#ffffff")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()
        
        if choices == []:
            choices = getInputPalette()
        
        for y in range(0, img.size[1], yStep):
            for x in range(0, img.size[0], xStep):
                c = random.choice(choices)

                for i in range(xStep):
                    for j in range(yStep):
                        if x+i < width and y+j < height:
                            pixdata[x+i,y+j] = c

    except Exception as e:
        img = writeImageException(e)
        
    return img    

def coco2remixed():
    img = bigSquareGrid()
    img = remixer("", img)

    return img

def bigGridFilled():
    global randoFillList
    iAlg = random.choice(randoFillList)
    
    try:
        choices = getInputPalette()
        yStep = random.randint(18, 111)
        img = bigSquareGrid(choices, yStep=yStep)

        pixdata = img.load()

        zzz = yStep // 3

        for i in range(zzz):
            x = random.randint(0, img.size[0]-1)
            y = random.randint(0, img.size[1]-1)

            targ = pixdata[x,y]
            
            floodfill(img, (x, y), targetcolour = targ,
                      newcolour = (0,0,0),
                      randomIt = iAlg,
                      choices = choices,
                      sizeLimit=(x,y),
                      compFunc=0)
            
    except Exception as e:
        img = writeImageException(e)
        
    return img

def insert_18(imgpath=""):
    startTime = time.time()

    if imgpath == "":
        imgpath = getInsertById(getParam(4))
    
    img = Image.open(imgpath)
    img = img.convert("RGBA")
    
    img = resizeToMinMax(img, maxW=1280, maxH=1024, minW=640, minH=480)

    pixdata = img.load()

    changePerc = 0.18
    paletteLength = 18
    blendAmount = .18
    
    i = 0
    totalCount = 0
    maxCount = int((img.size[0] * img.size[1]) * changePerc)

    now = time.time()
    duration = now - startTime

    choices = getPaletteGenerated(paletteLength=paletteLength)

    origImg = img.copy()
    
    try:
        while totalCount < maxCount and duration < 27:
            x = random.randint(0, img.size[0]-1)
            y = random.randint(0, img.size[1]-1)
            
            targ = pixdata[x,y]

            if targ[0:3] != (0,0,0) or True:
                img2 = img.copy()
                
                thisCount = floodfill(img2, (x, y), targetcolour = targ,
                      newcolour = (0,0,0),
                      randomIt = random.choice([19, 21, 13, 11, 17, 25, 40, 41]),
                                      choices = choices,
                                      compFunc=1)

                if thisCount >= 30:
                    img = img2

                    totalCount += thisCount

            i += 1

            now = time.time()
            duration = now - startTime

        img = Image.blend(origImg, img, blendAmount)        
        
    except Exception as e:        
        img = writeImageException(e)
        
    return img

def insertFoured(imgpath=""):
    if imgpath == "":
        imgpath = getInsert("", publicDomainImagePath)
        
    img = Image.open(imgpath)

    try:
        mirror1 = img.transpose(Image.FLIP_LEFT_RIGHT)
        rot1 = img.rotate(180)
        mirror2 = mirror1.rotate(180)
        
        blendAmount = .50
        
        img = Image.blend(img, rot1, blendAmount)
        mirror = Image.blend(mirror1, mirror2, blendAmount)
        
        img = Image.blend(img, mirror, blendAmount)
    except Exception as e:        
        img = writeImageException(e)       

    return img

def insertStreaks(imgpath="", maxIterations=250, pointCount=25):
    if imgpath == "":
        imgpath = getInsert("", publicDomainImagePath)

    img = Image.open(imgpath)
    img = img.convert("RGBA")

    img = resizeToMinMax(img, maxW=1024, maxH=768, minW=640, minH=480)
    
    try:
        pixdata = img.load()

        choices = getPaletteGenerated()
        
        xs = []
        ys = []
        
        for i in range(pointCount):
            x = random.randint(0, img.size[0]-1)
            xs.append((x, "x"))

            y = random.randint(0, img.size[1]-1)
            xs.append((y, "y"))

        for point in xs:
            x = 0
            y = 0
            j = 0
            k = 0
            
            if point[1] == "x":
                x = point[0]
                j = img.size[1]
                k = 0
            else:
                y = point[0]
                j = img.size[0]
                k = 1
                
            r,g,b,a = random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(0,255)

            lastC = (0,0,0,0)

            thisxCount = 0

            for i in range(j):
                if k == 0:
                    y = i
                else:
                    x = i
                    
                (rC, gC, bC, aC) = pixdata[x,y]
                (rT, gT, bT, aT) = (rC-lastC[0],gC-lastC[1],bC-lastC[2],aC-lastC[3])

                diffrange = random.randint(10, 25)
                
                if i == 0 or (abs(rT) < diffrange and abs(gT) < diffrange and abs(bT) < diffrange and abs(aT) < diffrange):
                    if random.randint(0, thisxCount) <= (int(thisxCount // 2.0)):
                        # don't always do it - do it less as we go down the image
                        lastC = pixdata[x,y]
                        pixdata[x,y] = (r,g,b,a)
                        thisxCount += 1

        floodedCount = 0
        pixCount = img.size[0] * img.size[1]

        iteration = 0        
        
        while floodedCount < int(pixCount // 5.0) and iteration < maxIterations:
            (x,y) = (random.randint(0, img.size[0]-1), random.randint(0, img.size[1]-1))

            targ = pixdata[x,y]

            global randoFillList
            iAlg = random.choice(randoFillList)
            
            floodedCount += floodfill(img, (x, y), targetcolour = targ,
                                      newcolour = (0,0,0),
                                      randomIt = iAlg,
                                      choices = choices,
                                      compFunc = 2)

            iteration += 1
            
    except Exception as e:        
        img = writeImageException(e)        

    return img

def insertStreaksAdapt():
    try:
        img = insertStreaks()

        cCount = random.randint(4, 15)
        
        img = img.convert("P", palette=Image.ADAPTIVE, colors=cCount)
        
    except Exception as e:
        img = writeImageException(e)

    return img

def insertStreaksCoco():
    try:
        img = insertStreaks()
        img = img.convert("RGB")
        
        coco = bigSquareGrid()
        coco = coco.convert("P", palette=Image.ADAPTIVE)
        
        img = img.quantize(palette=coco)
        
    except Exception as e:
        img = writeImageException(e)

    return img

# PIGEONHOLE PUMP

def randoFillStyle(choices=[], imgpath=""):   
    try:
        if imgpath == "":
            imgpath = getInsertById(getParam(4))
       
        img = Image.open(imgpath)
        img = img.convert("RGBA")

        img = resizeToMinMax(img, maxW=1024, maxH=768, minW=640, minH=480)

        maxIterations = 500
        
        pixdata = img.load()
                
        floodedCount = 0
        pixCount = img.size[0] * img.size[1]

        iteration = 0

        # build a choice list from taking the color of a random point and iterating over 0 to 255               

        if choices == []:
            for j in range(0, 3):
                (x,y) = (random.randint(0, img.size[0]-1), random.randint(0, img.size[1]-1))
                c = pixdata[x,y]

                di = random.randint(0, 2)        

                iCount = 15
                cDiff = 255 // (iCount * 1.0)
                iThis = 0
                
                for i in range(0, iCount):
                    iThis = int(i * cDiff)

                    if iThis < 0:
                        iThis = 0
                    elif iThis > 255:
                        iThis = 255
                        
                    ci = replace_at_index(c, di, iThis)

                    if ci not in choices:
                        choices.append(ci)

        # now do random floodfills

        global fontPathSansSerif

        fon = ImageFont.truetype(fontPathSansSerif, 18)
        debugFillColor = (255, 255, 255, 255)

        draw = ImageDraw.Draw(img)
        #draw.text((375, 360), "X marks the spot", font=fon, fill=debugFillColor)

        global randoFillList
        
        while floodedCount < int(pixCount // 4.0) and iteration < maxIterations:
            (x,y) = (random.randint(0, img.size[0]-1), random.randint(0, img.size[1]-1))

            iAlg = 0

            while iAlg == 0:
                iAlg = random.choice(randoFillList)

            temp = img.copy()
            pixdata = temp.load()
            targ = pixdata[x,y]
            
            tempFC = floodfill(temp, (x, y), targetcolour = targ,
                               newcolour = (0,0,0),
                               randomIt = iAlg,
                               compFunc=1,
                               choices=choices)
        
            if tempFC > 10:                
                # only allow the flood if it did some bigger changes
                
                img = temp                
                
                floodedCount += tempFC

            iteration += 1
            
    except Exception as e:
        img = writeImageException(e)
        draw = ImageDraw.Draw(img)
        
        fon = ImageFont.truetype(fontPathSansSerif, 18)
        debugFillColor = (0, 0, 0, 255)
        textY = 100
        
        draw.text((5, textY), "imgpath: " + imgpath, font=fon, fill=debugFillColor)
    
    return img

def randoFillStyle_Prism():
    img = ""

    try:
        choices = []
        
        hexchoices = ["#ff3b3b","#ff8848","#feff5d","#aaff59","#84ffd7"]

        for c in hexchoices:
            choices.append(hex_to_rgb(c))
            
        img = randoFillStyle(choices=choices)

    except Exception as e:
        img = writeImageException(e)

    return img

def randoFill_Insert():
    img = ""

    try:        
        palette = getPalette()
        imgpath = getInsert("", publicDomainImagePath)

        print(imgpath)

        img = randoFillStyle(choices=palette, imgpath=imgpath)

    except Exception as e:
        img = writeImageException(e)

    return img

def randoFill_Public():
    img = ""

    try:        
        palette = getPaletteGenerated()

        imgpath = getInsertById(getParam(4))
        
        img = randoFillStyle(choices=palette, imgpath=imgpath)

    except Exception as e:
        img = writeImageException(e)

    return img

def radioFill(imgpath="", img=""):
    """p1: maxStackDepth<br />
    p2: flood count max (default: -1 => pixel count / 4)"""

    p1 = getParam(0)
    p2 = getParam(1)

    p1 = int(p1) if p1.isdecimal() else 0
    p2 = int(p2) if p2.isdecimal() else -1
    
    floodLimit = p2    

    return radioFill_process(imgpath=imgpath, choices=[], img=img, maxStackDepth=p1, floodLimit=floodLimit, sizeLimit=(250,250))[0]

def getNextPoint(points, pointsChosen):    
    complete = False

    for point in points:
        if point not in pointsChosen:
            return (point, complete)

    complete = True
    return ((-1,-1), complete)

def radioFill_process(imgpath="", choices=[], img="", stamp=None, stampTrans=None, compFunc=1, points=None, minFloodChange=40, disobey=0, maxStackDepth=0, floodLimit=-8, sizeLimit=(0,0)):
    doTimeCheck("radioFill_process starts")

    origImg = ""
    global fontPathSansSerif
    
    try:
        if imgpath == "" and img == "":
            imgpath = getInsertById(getParam(4))
            img = Image.open(imgpath)
        elif imgpath != "" and img == "":
            img = Image.open(imgpath)
            
        img = img.convert("RGBA")

        img = resizeToMinMax(img, maxW=1280, maxH=1024, minW=800, minH=600)

        origImg = img.copy()
        
        maxIterations = 200
        
        pixdata = img.load()
                
        floodedCount = 0
        pixCount = img.size[0] * img.size[1]

        if floodLimit < 0:
            floodLimit = abs(int(pixCount // (floodLimit * 1.0)))

        iteration = 0

        iCount = 15

        if choices == [] and stamp is None:
            rrint = random.randint(0, 2)
            
            if rrint == 0:
                # build a choice list from taking the color of a random point and iterating over 0 to 255
                jCount = 3
                
                for j in range(0, jCount):
                    (x,y) = (random.randint(0, img.size[0]-1), random.randint(0, img.size[1]-1))
                    c = pixdata[x,y]

                    di = random.randint(0, 2)        
                    
                    cDiff = 255 // (iCount * 1.0)
                    iThis = 0
                    
                    for i in range(0, iCount):
                        iThis = int(i * cDiff)

                        if iThis < 0:
                            iThis = 0
                        elif iThis > 255:
                            iThis = 255
                            
                        ci = replace_at_index(c, di, iThis)

                        if ci not in choices:
                            choices.append(ci)
            elif rrint == 1:
                # just take the color of some random points
                jCount = 15
                jAttempts = 250
                jAttempt = 0
                
                while len(choices) < jCount and jAttempt < jAttempts:
                    (x,y) = (random.randint(0, img.size[0]-1), random.randint(0, img.size[1]-1))
                    c = pixdata[x,y]

                    if c not in choices:
                        choices.append(c)

                    jAttempt += 1
            else:
                # iterate with hsv
                jCount = 10
                kCount = 5
                cAttempts = 250
                cAttempt = 0
                
                picked = []
                
                while len(picked) < jCount and cAttempt < cAttempts:
                    theseChoices = []
                    (x,y) = (random.randint(0, img.size[0]-1), random.randint(0, img.size[1]-1))
                    c = pixdata[x,y]

                    cAttempt += 1
                    
                    if c not in picked:
                        picked.append(c)
                        hsvc = colorsys.rgb_to_hsv(c[0] // 255.0, c[1] // 255.0, c[2] // 255.0)

                        # need the amount to subtract to get jCount items

                        amountToSub = 0.1
                        
                        while hsvc[2] > 0 and len(choices) < (kCount // 2):
                            hsvc = replace_at_index(hsvc, 2, hsvc[2]-amountToSub)

                            if hsvc[1] < 0.4:
                                # bump up the saturation
                                hsvc = replace_at_index(hsvc, 1, hsvc[1]+0.2)
                                
                            c = myhsv_to_rgb(hsvc)
                            
                            if c not in theseChoices:
                                theseChoices.append(c)

                        while hsvc[2] < 1 and len(choices) < (kCount):
                            hsvc = replace_at_index(hsvc, 2, hsvc[2]+amountToSub)

                            if hsvc[1] < 0.4:
                                # bump up the saturation
                                hsvc = replace_at_index(hsvc, 1, hsvc[1]+0.2)
                                
                            c = myhsv_to_rgb(hsvc)
                            
                            if c not in theseChoices:
                                theseChoices.append(c)

                        for c in theseChoices:
                            if c not in choices:
                                if c[0] > 25 and c[1] > 25 and c[2] > 25:
                                    # sick of black
                                    choices.append(c)
                    
        doTimeCheck("now do random floodfills")
        doTimeCheck("maxStackDepth: " + str(maxStackDepth))
        doTimeCheck(f"choices: {choices}")
        
        # now do random floodfills

        fon = ImageFont.truetype(fontPathSansSerif, 18)
        debugFillColor = (255, 255, 255, 255)

        draw = ImageDraw.Draw(img)
        
        pointsChosen = []

        addState(f'floodedCount: {floodedCount}, floodLimit: {floodLimit}, iteration: {iteration}, maxIterations: {maxIterations}')

        while (floodedCount < floodLimit and iteration < maxIterations) or (points is not None and len(pointsChosen) < len(points)):
            # doTimeCheck("while loop start")
            addState(f'floodedCount: {floodedCount}, floodLimit: {floodLimit}, iteration: {iteration}, maxIterations: {maxIterations}')

            if points is None:
                (x,y) = (random.randint(0, img.size[0]-1), random.randint(0, img.size[1]-1))
            else:
                ((x,y),isComplete) = getNextPoint(points, pointsChosen)

                if isComplete:
                    break

            pointsChosen.append((x,y))

            # rootLogger.debug("pointsChosen: " + str(pointsChosen))
            global randoFillList
            
            p1 = getParam(0)
            iAlg = int(p1) if p1.isdecimal() else 0

            if iAlg != 0:
                while iAlg == 0:
                    iAlg = random.choice(randoFillList)

            temp = img.copy()
            pixdata = temp.load()
            targ = pixdata[x,y]
            
            #choices = getPaletteGenerated()

            tempFC = floodfill(temp, (x, y), targetcolour = targ,
                               newcolour = (0,0,0),
                               randomIt = iAlg,
                               compFunc=compFunc,
                               choices=choices,
                               stamp=stamp,
                               stampTrans=stampTrans,
                               disobey=disobey,
                               maxStackDepth=maxStackDepth,
                               sizeLimit=sizeLimit)
        
            saveForXanny(temp)

            doTimeCheck(f"tempFC: {tempFC} compFunc: {compFunc}")

            if tempFC > minFloodChange or points is not None:                
                # only allow the flood if it did some bigger changes
                
                img = temp                
                
                floodedCount += tempFC

                doTimeCheck("allowed - floodedCount is now: " + str(floodedCount) + " (of a requested: " + str(floodLimit) + "/" + str(pixCount) + ")")

            iteration += 1
            
    except Exception as e:
        img = writeImageException(e)
        draw = ImageDraw.Draw(img)
        
        fon = ImageFont.truetype(fontPathSansSerif, 18)
        debugFillColor = (0, 0, 0, 255)
        textY = 100
        
        draw.text((5, textY), "imgpath: " + imgpath, font=fon, fill=debugFillColor)
    
    return [img, origImg]

def radioFillMixed():
    img = mix2_public()
    img = radioFill(img=img)

    return img

def radioFillWords():
    img = mix2_public()
    img = radioFill(img=img)
    fontPath = getFont()
    imgw = wordGrid2("", 30, fontPath)

    img = ImageChops.screen(img, imgw)

    return img

def radioFill_blend(imgpath=""):
    """p1: iAlg<br />    
    """
    try:
        global input_palette

        if len(input_palette) > 0:
            choices = input_palette
        else:
            choices = []

        if imgpath != "" and len(choices) <= 0:
            choices = getPaletteFromImage(img)

        imgs = radioFill_process(imgpath=imgpath,
                                 choices=choices,
                                 floodLimit=-4)
        
        img = imgs[0]
        origImg = imgs[1]

        blendAmount = random.uniform(0.4, 0.7)
        
        img = Image.blend(origImg, img, blendAmount)

    except Exception as e:
        img = writeImageException(e)
        
    return img

def radioFill_stamp(imgpath="", img="", stamp="", blendOverride=0, compFunc=50, minFloodChange=40, disobey=0, maxStackDepth=0, floodLimit=-8, sizeLimit=(0,0)):
    doTimeCheck("radioFill_stamp starts")

    try:
        global input_palette

        if imgpath == "" and img == "":
            imgpath = getInsertById(getParam(4))        
            img = Image.open(imgpath)        

        if stamp == "":
            stamp = getStamp() # fullFillStamp()
        
        stampTrans = None
        
        if imgpath != "":
            img = Image.open(imgpath)
            choices = [] # getPaletteFromImage(img)
            doTimeCheck("radioFill_stamp - cond 1")
            imgs = radioFill_process(imgpath=imgpath,
                                     choices=choices,
                                     stamp=stamp,
                                     stampTrans=stampTrans,
                                     img=img,
                                     compFunc=compFunc,
                                     disobey=disobey,
                                     maxStackDepth=maxStackDepth,
                                     floodLimit=floodLimit,
                                     sizeLimit=sizeLimit)
        else:
            if len(input_palette) > 0:
                doTimeCheck("radioFill_stamp - cond 2")
                imgs = radioFill_process(imgpath=imgpath, 
                                         choices=input_palette, 
                                         stamp=stamp, 
                                         stampTrans=stampTrans, 
                                         img=img, 
                                         compFunc=compFunc, 
                                         minFloodChange=minFloodChange, 
                                         disobey=disobey, 
                                         maxStackDepth=maxStackDepth,
                                         floodLimit=floodLimit,
                                         sizeLimit=sizeLimit)
            else:
                doTimeCheck("radioFill_stamp - cond 3")
                imgs = radioFill_process(imgpath=imgpath, 
                                         stamp=stamp, 
                                         stampTrans=stampTrans, 
                                         img=img, 
                                         compFunc=compFunc, 
                                         minFloodChange=minFloodChange, 
                                         disobey=disobey, 
                                         maxStackDepth=maxStackDepth,
                                         floodLimit=floodLimit,
                                         sizeLimit=sizeLimit)
        
        img = imgs[0]
        origImg = imgs[1]

        blendAmount = random.uniform(0.4, 0.7)

        addState(f'blendAmount: {blendAmount}')

        if blendOverride != 0:
            blendAmount = blendOverride
        
        origImg = origImg.convert("RGBA")
        img = img.convert("RGBA")
        img = Image.blend(origImg, img, blendAmount)

    except Exception as e:
        img = writeImageException(e)
        
    doTimeCheck("radioFill_stamp complete")

    return img

def radioFill_stamp_fromFunc():
    try:
        global input_palette

        imgpath = getInsertById(getParam(4))
        img = Image.open(imgpath)

        imgOrig = img.copy()

        stampFuncs = getSafeFuncs()
      
        stampf = random.choice(stampFuncs)        
        stamp = stampf()
        stamp = resizeToMinMax(stamp, maxW=200, maxH=100, minW=100, minH=50)

        for i in range(3):
            img = radioFill_stamp(imgpath="", img=img, stamp=stamp)
       
    except Exception as e:
        img = writeImageException(e)
        
    return img

def radioFill_stamp_newgrid():
    try:
        global input_palette

        imgpath = getInsertById(getParam(4))
        img = Image.open(imgpath)

        imgOrig = img.copy()        
              
        stamp = newgrid()
        stamp = resizeToMinMax(stamp, maxW=200, maxH=100, minW=100, minH=50)

        for i in range(3):
            img = radioFill_stamp(imgpath="", img=img, stamp=stamp)
       
    except Exception as e:
        img = writeImageException(e)
        
    return img

def radioFill_stamp_fullFill():
    try:
        stamp = fullFill()
        img = radioFill_stamp(imgpath="", img="", stamp=stamp, blendOverride=0.5)

    except Exception as e:
        img = writeImageException(e)
        
    return img

def radioFill_stamp_fullFill_specific():
    p1 = getParam(0)
    p2 = getParam(1)
    
    p1 = int(p1) if p1.isdecimal() else 31       
    p2 = int(p2) if p2.isdecimal() else 50 
      
    try:
        stamp = fullFill(w=p2, h=p2, iAlg=p1)
        img = radioFill_stamp(imgpath="", img="", stamp=stamp, blendOverride=0.5)

    except Exception as e:
        img = writeImageException(e)
        
    return img

def radioFill_stamp_fullFillLatest():
    try:
        stamp = fullFillLatest()
        img = radioFill_stamp(imgpath="", img="", stamp=stamp, blendOverride=0.5)

    except Exception as e:
        img = writeImageException(e)
        
    return img

def radioFill_stamp_wordfilled():
    try:
        stamp = wordfilled(width=400, height=100)
        img = radioFill_stamp(imgpath="", img="", stamp=stamp, blendOverride=0.3)

    except Exception as e:
        img = writeImageException(e)
        
    return img

def radioFill_stamp_wordfilled_mult():
    try:
        stamp = wordfilled_mult(width=400, height=100)
        img = radioFill_stamp(imgpath="", img="", stamp=stamp, blendOverride=0.3)

    except Exception as e:
        img = writeImageException(e)
        
    return img

def radioFill_recurse(imgpath="", img=None, passes=7, maxDuration = 10):
    try:
        global input_palette

        if img is None:
            if imgpath == "":
                imgpath = getInsertById(getParam(4))
            img = Image.open(imgpath)

        startTime = time.time()        

        for i in range(passes):
            now = time.time()
            duration = now - startTime

            if duration > maxDuration:
                break;

            stamp = img.copy()
            stamp = resizeToMinMax(stamp, maxW=200, maxH=100, minW=100, minH=50)

            img = radioFill_stamp(imgpath="", img=img, stamp=stamp)
        
    except Exception as e:
        img = writeImageException(e)
        
    return img

def radioFill_recurse_canny():
    try:
        global input_palette

        img = opencv_canny_inv()

        stampW = random.randint(30, 75)
        stampH = random.randint(30, 75)

        stamp = fullFill(w=stampW, h=stampH)

        if len(input_palette) > 0:
            imgs = fillFromOuter_Process(choices=input_palette, stamp=stamp, img=img, maxIterations=25)
        else:
            iAlg = random.choice(randoFillList)
            rndln = random.randint(5, 50)
            imgs = fillFromOuter_Process(getPaletteGenerated(paletteLength=rndln), alg=iAlg, stamp=stamp, img=img, maxIterations=25)
        
        img = imgs[0]        

        for i in range(5):
            stamp = img.copy()
            stamp = resizeToMinMax(stamp, maxW=200, maxH=100, minW=100, minH=50)

            img = radioFill_stamp(imgpath="", img=img, stamp=stamp)
        
    except Exception as e:
        img = writeImageException(e)
        
    return img    

def radioFill_recurse2():
    try:
        global input_palette

        imgpath = getInsertById(getParam(4))
        img = Image.open(imgpath)

        iicount = random.randint(3, 7)
        
        for i in range(iicount):
            stamp = img.copy()

            if random.randint(0, 1) == 0:
                stamp = stamp.convert("RGB")
                stamp = ImageOps.invert(stamp)
                stamp = stamp.convert("RGBA")
        
            stamp = resizeToMinMax(stamp, maxW=200, maxH=100, minW=100, minH=50)

            img = radioFill_stamp(imgpath="", img=img, stamp=stamp)
        
    except Exception as e:
        img = writeImageException(e)
        
    return img

def radioFill_recurse_anim():
    try:
        frames = []

        global input_palette

        imgpath = getInsertById(getParam(4))
        img = Image.open(imgpath)

        iicount = random.randint(8, 15)
        
        for i in range(iicount):
            stamp = img.copy()

            if random.randint(0, 1) == 0:
                stamp = stamp.convert("RGB")
                stamp = ImageOps.invert(stamp)
                stamp = stamp.convert("RGBA")
        
            stamp = resizeToMinMax(stamp, maxW=200, maxH=100, minW=100, minH=50)

            img = radioFill_stamp(imgpath="", img=img, stamp=stamp)

            # Saving/opening is needed for better compression and quality
            fobj = BytesIO()
            img.save(fobj, 'GIF')
            frame = Image.open(fobj)
            frames.append(frame)

        animated_gif = BytesIO()
        frames[0].save(animated_gif,
                    format='GIF',
                    save_all=True,
                    append_images=frames[1:],
                    delay=0.1,
                    loop=0)
        
        animated_gif.seek(0)
        img = Image.open(animated_gif)
    
    except Exception as e:
        img = writeImageException(e)
        
    return img
    
def radioFill_recurse_special():
    try:
        global input_palette

        imgpath = getInsertById(1)
        stamppath = imgpath
        stamppath2 = imgpath
        
        img = Image.open(imgpath)

        stamps = []
        
        stamp = Image.open(stamppath)
        stamps.append(stamp)

        stamp = Image.open(stamppath2)
        stamps.append(stamp)        
        
        iicount = random.randint(2, 4)
        
        for i in range(iicount):
            stamp = random.choice(stamps)

            if random.randint(0, 1) == 0:
                stamp = stamp.convert("RGB")
                stamp = ImageOps.invert(stamp)
                stamp = stamp.convert("RGBA")
        
            stamp = resizeToMinMax(stamp, maxW=200, maxH=100, minW=100, minH=50)

            img = radioFill_stamp(imgpath="", img=img, stamp=stamp)
        
    except Exception as e:
        img = writeImageException(e)
        
    return img

def radioFill_recurse_func():
    try:
        global input_palette

        img = ""

        safeFuncs = getSafeFuncs()
        
        if img == "":            
            c = random.choice(safeFuncs)
            img = c()

        for i in range(5):
            stamp = img.copy()
            stamp = resizeToMinMax(stamp, maxW=200, maxH=100, minW=100, minH=50)

            img = radioFill_stamp(imgpath="", img=img, stamp=stamp)
        
    except Exception as e:
        img = writeImageException(e)
        
    return img

def radioFill_recurse_swap(imgpath="", imgpath2=""):
    if imgpath == "":
        imgpath = getInsertById(getParam(4))

    if imgpath2 == "":
        imgpath2 = getInsertById(getParam(4))

    global input_palette
   
    img = Image.open(imgpath)
    img2 = Image.open(imgpath2)

    return radioFill_recurse_swap_images(img, img2)

def radioFill_recurse_swap_images(img, img2):
    try:
        global input_palette
        
        img_orig1 = img.copy()
        img_orig2 = img2.copy()

        xxxx = random.randint(0, 1)
        
        if xxxx == 0:
            for i in range(3):
                stamp = img.copy()
                stamp = resizeToMinMax(stamp, maxW=200, maxH=100, minW=100, minH=50)
                img = radioFill_stamp(imgpath="", img=img, stamp=stamp)
            
            stamp = resizeToMinMax(img, maxW=200, maxH=100, minW=100, minH=50)
            img = radioFill_stamp(imgpath="", img=img_orig2, stamp=stamp)
        else:
            for i in range(3):
                stamp2 = img2.copy()
                stamp2 = resizeToMinMax(stamp2, maxW=200, maxH=100, minW=100, minH=50)            
                img2 = radioFill_stamp(imgpath="", img=img2, stamp=stamp2)
            
            stamp = resizeToMinMax(img2, maxW=200, maxH=100, minW=100, minH=50)
            img = radioFill_stamp(imgpath="", img=img_orig1, stamp=stamp)
            
    except Exception as e:
        img = writeImageException(e)
        
    return img

def radioFill_recurse_swap_AB():
    x = 0
    xStop = 2

    imgA = Image.open(getInsertById(getParam(4)))
    imgB = Image.open(getInsertById(getParam(4)))
    
    try:
        while x < xStop:            
            imgACopy = imgA.copy()
            imgBCopy = imgB.copy()       

            if x % 2 == 0:
                stamp = imgACopy
                img = imgBCopy
            else:
                stamp = imgBCopy
                img = imgACopy

            stamp = resizeToMinMax(stamp, maxW=200, maxH=100, minW=100, minH=50)
            img = radioFill_stamp(imgpath="", img=img, stamp=stamp)
            
            if x % 2 == 0:
                imgA = imgA
                imgB = img
            else:
                imgA = img
                imgB = imgB

            random.seed()
            
            x += 1
        
    except Exception as e:
        print(e)
        img = writeImageException(e)

    return img

def radioFill_compFunc(imgpath="", img=None, passes=5, maxDuration = 10):
    try:
        global input_palette

        if img is None:
            if imgpath == "":
                imgpath = getInsertById(getParam(4))
            img = Image.open(imgpath)

        startTime = time.time()

        def thisTargCheck(pnt, targ):
            return _color_target_check(pnt, targ, 25)

        minFloodChange = 0

        for i in range(passes):
            now = time.time()
            duration = now - startTime

            if duration > maxDuration:
                break;

            stamp = img.copy()
            stamp = resizeToMinMax(stamp, maxW=200, maxH=100, minW=100, minH=50)

            img = radioFill_stamp(imgpath="", img=img, stamp=stamp, compFunc=thisTargCheck, minFloodChange=minFloodChange, blendOverride=0.3)
        
    except Exception as e:
        img = writeImageException(e)
        
    return img

def parboil(imgpath=""):
    if imgpath == "":
        imgpath = getInsertById(getParam(4))

    try:
        img = Image.open(imgpath)
        img = img.convert("RGBA")
        
        img = resizeToMax(img, maxW=1024, maxH=768)
        
        pixdata = img.load()    
        draw = ImageDraw.Draw(img)

        colors = []
   
        baseC = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        for i in range(-25, 25, 5):
            (r,g,b,a) = (baseC[0]+i, baseC[1]+i, baseC[2]+i, baseC[3]+i)
            if r < 0: r = 0
            if r > 255: r = 255
            if g < 0: g = 0
            if g > 255: g = 255
            if b < 0: b = 0
            if b > 255: b = 255
            if a < 0: a = 0
            if a > 255: a = 255
            
            colors.append((r,g,b,a))

        for y in range(0, img.size[1]):
            for x in range(0, img.size[0]):
                targ = pixdata[x,y]
                (r,g,b,a) = (targ[0],targ[1],targ[2],targ[3])
                
                if (r > 180 and g > 180 and b > 180) or (r < 10 and g < 20 and b < 20):
                    newC = random.choice(colors)            
                    pixdata[x,y] = newC                    
            
    except Exception as e:
        img = writeImageException(e)
        
    return img

def realspiral():
    width = 1024
    height = 1024

    try:
        img = Image.new("RGBA", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        direction = 1
        x = 0
        y = 0

        white = (255,255,255,255)
        baseC = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        subseq = 0
        
        while direction > 0 and subseq < 8:
            # print direction, x, y, subseq
            
            if direction == 1:
                if x < img.size[0]:
                    if pixdata[x,y] == white:
                        pixdata[x,y] = baseC
                        x += 1
                        subseq = 0
                    else:
                        direction = 2
                        #baseC = getRandomColor(alpha=255)
                        if y > 0:
                            x -= 1                            
                        y += 1
                        subseq += 1
                else:
                    x -= 1
                    direction = 2                    
                    #baseC = getRandomColor(alpha=255)
                    y += 1
                    subseq += 1
            elif direction == 2:
                if y < img.size[1]:
                    if pixdata[x,y] == white:
                        pixdata[x,y] = baseC
                        y += 1
                        subseq = 0
                    else:
                        direction = 3
                        #baseC = getRandomColor(alpha=255)
                        if x < img.size[0]:
                            y -= 1
                        x -= 1
                        subseq += 1
                else:
                    y -= 1
                    direction = 3
                    #baseC = getRandomColor(alpha=255)
                    x -= 1
                    subseq += 1
            elif direction == 3:
                if x >= 0:
                    if pixdata[x,y] == white:
                        pixdata[x,y] = baseC
                        x -= 1
                        subseq = 0
                    else:
                        direction = 4
                        #baseC = getRandomColor(alpha=255)
                        if y < img.size[1]:
                            x += 1
                        y -= 1
                        subseq += 1
                else:
                    x += 1
                    direction = 4
                    #baseC = getRandomColor(alpha=255)
                    y -= 1
                    subseq += 1
            elif direction == 4:
                if y >= 0:
                    if pixdata[x,y] == white:
                        pixdata[x,y] = baseC
                        y -= 1
                        subseq = 0
                    else:
                        direction = 1
                        baseC = getRandomColor()
                        x += 1
                        y += 1
                        subseq += 1
                else:                    
                    direction = 1
                    baseC = getRandomColor()                    
                    y += 1
                    x += 1
                    subseq += 1
   
    except Exception as e:
        img = writeImageException(e)

    return img

def DEADNIGHTSKY():
    width = 1024
    height = 1024

    img = ""
    
    try:
        img = Image.new("RGBA", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        myy = random.randint(10, height - 10)

        draw.line((0, myy, img.size[0], myy), "black")

        global randoFillList
        iAlg = random.choice(randoFillList)

        x1 = random.randint(0, width-1)
        y1 = random.randint(0, height-1)

        x2 = random.randint(x1, width-1)
        y2 = random.randint(y1, height-1)

        draw.rectangle((x1, y1, x2, y2), "white", "black")        

        floodfill(img, (50, myy - 5),
                          targetcolour = (255, 255, 255, 255),
                          newcolour = (128,128,128),
                          randomIt = iAlg,
                          maxStackDepth = 0)

        floodfill(img, (50, myy + 5),
                          targetcolour = (255, 255, 255, 255),
                          newcolour = (0,0,0, 255),
                          randomIt = 23,
                          maxStackDepth = 0)

        fonz = ImageFont.truetype(fontPath + fontNameMono, 12)   
        
        
    except Exception as e:
        img = writeImageException(e)

    return img

def grid_18():
    width = getCurrentStandardWidth()
    height = getCurrentStandardHeight()

    img = ""
    
    try:
        i = random.randint(50, 75)
        c = (i, i, i)
        
        img = Image.new("RGBA", (width,height), c)
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        for y in range(0, img.size[1]-1, 25):
            draw.line((0, y, img.size[0], y), "black")

        for x in range(0, img.size[0]-1, 25):
            draw.line((x, 0, x, img.size[1]), "black")

        y = img.size[1]-1
        x = img.size[0]-1
        
        draw.line((0, y, img.size[0], y), "black")
        draw.line((x, 0, x, img.size[1]), "black")

        for y in range(5, img.size[1]-1, 25):
            for x in range(5, img.size[0]-1, 25):
                iAlg = random.randint(18, 19)
                
                floodfill(img, (x, y),
                          targetcolour = pixdata[x,y],
                          newcolour = (0,0,0,255),
                          randomIt = iAlg,
                          maxStackDepth = 0)
    except Exception as e:
        img = writeImageException(e)

    return img

def grid_other(choices=[], lineColor="black"):
    width = getCurrentStandardWidth()
    height = getCurrentStandardHeight()

    img = ""
    
    try:
        if lineColor == "staticChoice":
            lineColor = random.choice(choices)
            
        squareSize = random.randint(25, 125)
        i = random.randint(50, 75)
        c = (i, i, i)
        
        img = Image.new("RGBA", (width,height), c)
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        global randoFillList
        iAlg = random.choice(randoFillList)

        for y in range(0, img.size[1]-1, squareSize):
            if lineColor == "choice":
                lineC = random.choice(choices)
            else:
                lineC = lineColor
                
            draw.line((0, y, img.size[0], y), lineC)

        for x in range(0, img.size[0]-1, squareSize):
            if lineColor == "choice":
                lineC = random.choice(choices)
            else:
                lineC = lineColor
            
            draw.line((x, 0, x, img.size[1]), lineC)

        y = img.size[1]-1
        x = img.size[0]-1
        
        draw.line((0, y, img.size[0], y), "black")
        draw.line((x, 0, x, img.size[1]), "black")

        for y in range(5, img.size[1]-1, squareSize):
            for x in range(5, img.size[0]-1, squareSize):                
                
                floodfill(img, (x, y),
                          targetcolour = pixdata[x,y],
                          newcolour = (0,0,0,255),
                          randomIt = iAlg,
                          maxStackDepth = 0,
                          choices = choices)
    except Exception as e:
        img = writeImageException(e)

    return img

def grid_rando_unique(choices=[], lineColor="black"):
    """p1: square size<br />
    p2: iAlg"""
    width = 1024
    height = 1024

    img = ""
    
    try:
        global input_palette
        
        if len(input_palette) > 0:
            choices = input_palette
        else:
            choices = getPaletteGenerated()

        if lineColor == "staticChoice":
            lineColor = random.choice(choices)

        p1 = getParam(0)
        p2 = getParam(1)

        try:
            squareSize = int(p1)    
        except ValueError:
            squareSize = random.randint(25, 125)

        try:
            p2 = int(p2)
        except ValueError:
            p2 = 0
        
        i = random.randint(50, 75)
        c = (i, i, i)
        
        img = Image.new("RGBA", (width,height), c)
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        global randoFillList        

        for y in range(0, img.size[1]-1, squareSize):
            if lineColor == "choice":
                lineC = random.choice(choices)
            else:
                lineC = lineColor
                
            draw.line((0, y, img.size[0], y), lineC)

        for x in range(0, img.size[0]-1, squareSize):
            if lineColor == "choice":
                lineC = random.choice(choices)
            else:
                lineC = lineColor
            
            draw.line((x, 0, x, img.size[1]), lineC)

        y = img.size[1]-1
        x = img.size[0]-1
        
        draw.line((0, y, img.size[0], y), "black")
        draw.line((x, 0, x, img.size[1]), "black")

        for y in range(5, img.size[1]-1, squareSize):
            for x in range(5, img.size[0]-1, squareSize):
                if p2 != 0:
                    iAlg = p2
                else:            
                    iAlg = random.choice(randoFillList)

                floodfill(img, (x, y),
                          targetcolour = pixdata[x,y],
                          newcolour = (0,0,0,255),
                          randomIt = iAlg,
                          maxStackDepth = 0,
                          choices = choices)
    except Exception as e:
        img = writeImageException(e)

    return img

def grid_palette():
    img = ""
    
    try:
        global input_palette
        
        if len(input_palette) > 0:
            choices = input_palette
        else:
            choices = getPaletteGenerated()

        img = grid_other(choices, lineColor="staticChoice")
        
    except Exception as e:
        img = writeImageException(e)

    return img

def grid_new(choices=[], lineColor="black"):
    width = 1024
    height = 1024

    img = ""

    iAlg = 68
    
    try:
        if lineColor == "staticChoice":
            lineColor = random.choice(choices)
            
        squareSize = random.randint(25, 225)
        i = random.randint(50, 75)
        c = (i, i, i)
        
        img = Image.new("RGBA", (width,height), c)
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        for y in range(0, img.size[1]-1, squareSize):
            if lineColor == "choice":
                lineC = random.choice(choices)
            else:
                lineC = lineColor
                
            draw.line((0, y, img.size[0], y), lineC)

        for x in range(0, img.size[0]-1, squareSize):
            if lineColor == "choice":
                lineC = random.choice(choices)
            else:
                lineC = lineColor
            
            draw.line((x, 0, x, img.size[1]), lineC)

        y = img.size[1]-1
        x = img.size[0]-1
        
        draw.line((0, y, img.size[0], y), "black")
        draw.line((x, 0, x, img.size[1]), "black")

        for y in range(5, img.size[1]-1, squareSize):
            for x in range(5, img.size[0]-1, squareSize):                

                choices = getPalette()
                
                floodfill(img, (x, y),
                          targetcolour = pixdata[x,y],
                          newcolour = (0,0,0,255),
                          randomIt = iAlg,
                          maxStackDepth = 0,
                          choices = choices)
    except Exception as e:
        img = writeImageException(e)

    return img

def nightgrid():
    width = getCurrentStandardWidth()
    height = getCurrentStandardHeight()

    img = ""
    
    try:
        i = random.randint(50, 75)
        d = (i, i, i)
                
        img = Image.new("RGBA", (width,height), d)
        draw = ImageDraw.Draw(img)

        gridSize = random.randint(6, 10)
        
        for y in range(0, img.size[1]-1, gridSize):
            for x in range(0, img.size[0]-1, gridSize):
                
                di = random.randint(0, 2)
                d = replace_at_index(d, di, d[di] + random.randint(-1, 1))                
                
                d = safetyCheck(d)

                draw.rectangle(((x,y),(x+gridSize,y+gridSize)), fill=d, outline=None)
                
        for y in range(0, img.size[1]-1, gridSize):
            draw.line((0, y, img.size[0], y), "black")

        for x in range(0, img.size[0]-1, gridSize):
            draw.line((x, 0, x, img.size[1]), "black")

        y = img.size[1]-1
        x = img.size[0]-1
        
        draw.line((0, y, img.size[0], y), "black")
        draw.line((x, 0, x, img.size[1]), "black")

    except Exception as e:
        img = writeImageException(e)

    return img

def nightgridStars():
    img = nightgrid()

    try:
        
        w = img.size[0]
        h = img.size[1]
        
        points = []

        for i in range(75):
            (x, y) = (random.randint(0, w), random.randint(0, h))
            points.append((x,y))
            
        pixdata = img.load()

        pointCount = 0
        for p in points:
            (x, y) = (p[0], p[1])
            
            r = random.randint(50, 200)
            r2 = random.randint(r - 20, r + 20)

            alpha = random.randint(0, 255)
            
            if random.randint(0, 1) == 0:
                c = (r, r2, 0, alpha)
            else:
                c = (r2, r, 0, alpha)    

            ccc = random.randint(0, 2)

            if ccc == 0:
                c = (random.randint(180, 240), c[0], c[1], alpha)
            elif ccc == 1:
                c = (c[0], c[1], random.randint(180, 240), alpha)
            else:
                c = (c[0], random.randint(180, 240), c[1], alpha)
            
            try:
                pixdata[x, y] = c
            except:
                pass

            k = 1

            # vary the star size based on which loop this is
            jCount = 2

            if pointCount > 35:
                jCount = 3

            if pointCount > 45:
                jCount = 4
                
            diagOn = 0
            if random.randint(0, 3) == 3:
                diagOn = 1
                
            for j in range(jCount):
                c = (c[0], c[1], c[2]-30, alpha)            

                try:
                    pixdata[x-k, y] = c
                    pixdata[x+k, y] = c
                    pixdata[x, y-k] = c
                    pixdata[x, y+k] = c

                    if diagOn == 1:
                        cAlpha = c[3] - 60
                        if cAlpha < 0:
                            cAlpha = 0
                            
                        pixdata[x-k, y-k] = (c[0], c[1], c[2], cAlpha)
                        pixdata[x+k, y+k] = (c[0], c[1], c[2], cAlpha)
                        pixdata[x-k, y+k] = (c[0], c[1], c[2], cAlpha)
                        pixdata[x+k, y-k] = (c[0], c[1], c[2], cAlpha)
                except:
                    pass
                
                k += 1

            pointCount += 1

    except Exception as e:
        img = writeImageException(e)
        
    return img

def vhsTextGrid():
    try:
        width = 1024
        height = 768
        
        img = Image.new("RGBA", (width, height), getRandomColor())
        draw = ImageDraw.Draw(img)
         
        #fon = ImageFont.truetype(fontPath + "VCR_OSD_MONO_1.001.ttf", 72)
        #fon = ImageFont.truetype(fontPath + "dephunked-brk.regular.ttf", 44)
        fon = ImageFont.truetype(getFont(), 44)

        c = (0,0,0)

        outputs = []

        for i in range(3):
            outputs.append(getRandomWord())

        choices = getPalette()
        
        text = []  

        maxX = 0
        maxY = 0
        
        for o in outputs:
            fsize = fon.getsize(o)

            if fsize[0] > maxX:
                maxX = fsize[0]

            if fsize[1] > maxY:
                maxY = fsize[1]
            
        zs = []

        zsi = 1

        while zsi < 8:
            zsi += random.randint(1, 2)
            zs.append(zsi)
            
        for i in range(0, len(zs)):
            z = zs[i]

            j = 0
            for y in range(0, img.size[1]-1, maxY + 12):
                for x in range(0, img.size[0]-1, maxX + 12):
                    #c = (i*35, i*35, i*35)
                    c = random.choice(choices)

                    if len(text) <= j:
                        text.append(random.choice(outputs))

                    outputMsg = text[j]

                    if x + maxX + z < img.size[0] and y + maxY + i < img.size[1]:
                        draw.text((x+z, y+i), outputMsg, font=fon, fill=c)

                    j += 1

        draw = ImageDraw.Draw(img)
    except Exception as e:
        img = writeImageException(e)
        
    return img

def picGrid(walkPath="", doAdapt=False):
    """p1: row/col count (default=5)<br />
    p2: square size (px) (default=250)"""

    picCount = 5
    gridSize = 250
    
    p1 = getParam(0)
    p2 = getParam(1)
    
    try:
        picCount = int(p1)    
    except ValueError:
        picCount = 5

    try:
        gridSize = int(p2)
    except ValueError:
        gridSize = 250
    
    try:
        width = gridSize * picCount
        height = gridSize * picCount
        
        img = Image.new("RGBA", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        # draw a grid

        inserts = []
        
        if p1 == "cover":
            inserts = [
                "/mnt/u/My Webs/tooinside/universemdwiki/_private/AAAAAA/beansnoface.png",
                "/mnt/u/My Webs/tooinside/universemdwiki/_private/AAAAAA/equinoxcake4.png",
                "/mnt/u/My Webs/tooinside/universemdwiki/_private/AAAAAA/cosmicegg.png",
                "/mnt/u/My Webs/tooinside/universemdwiki/_private/AAAAAA/a man named tajimat.png",
                "/mnt/u/My Webs/tooinside/universemdwiki/_private/AAAAAA/blackholedemon.png",
                "/mnt/u/My Webs/tooinside/universemdwiki/_private/AAAAAA/knife warning.png",
                "/mnt/u/My Webs/tooinside/universemdwiki/_private/AAAAAA/omegavirus.png",
                "/mnt/u/My Webs/tooinside/universemdwiki/_private/AAAAAA/blackholepeople.png",
                "/mnt/u/My Webs/tooinside/universemdwiki/_private/AAAAAA/abyss.png",
                "/mnt/u/My Webs/tooinside/universemdwiki/_private/AAAAAA/tumbleweeds.png",
                "/mnt/u/My Webs/tooinside/universemdwiki/_private/AAAAAA/artflowtajimat.png",
                "/mnt/t/Pictures/iPhone_Sync/iPhone4/IMG_0307.JPG",
                "/mnt/t/Pictures/art/created/contextfree/zambs.png",
                "/mnt/t/Pictures/art/created/contextfree/hardlandscape2.png",
                "/mnt/t/Pictures/art/edits/nihilisttree.png",
                "/mnt/t/Pictures/From Lumia920White/Camera roll/WP_20130212_004.jpg",
                "/mnt/t/Pictures/From Lumia920White/Camera roll/WP_20130413_014.jpg",
                "/mnt/t/Pictures/From Lumia920White/Camera roll/WP_20130526_001.jpg",
                "/mnt/t/Pictures/From Lumia920White/Camera roll/WP_20130807_004.jpg",
                "/mnt/t/Pictures/From Lumia920White/Camera roll/WP_20131008_001.jpg",
                "/mnt/t/Pictures/From Lumia920White/Camera roll/WP_20131111_002.jpg",
                "/mnt/t/Pictures/From_iPhone6/IMG_0169.JPG",
                "/mnt/t/Pictures/From_iPhone6/IMG_0510.JPG",
                "/mnt/t/Pictures/camsnaps/saved/4-p0032.jpg",
                "/mnt/t/Pictures/idiot pics/5356378556_9f39f0c092_z.jpg",
                "/mnt/t/Pictures/idiot pics/tear.png",
                "/mnt/t/Pictures/canoncam/resized/111_1146.jpg"
            ]

        if walkPath != "" and inserts == []:
            inserts = getChoicesWalk(walkPath)
            
        for y in range(0, img.size[1]-1, gridSize):
            draw.line((0, y, img.size[0], y), "black")

        for x in range(0, img.size[0]-1, gridSize):
            draw.line((x, 0, x, img.size[1]), "black")

        y = img.size[1]-1
        x = img.size[0]-1
        
        draw.line((0, y, img.size[0], y), "black")
        draw.line((x, 0, x, img.size[1]), "black")

        imgs = []
        
        # now put pics in each square
        for y in range(1, img.size[1]-1, gridSize):
            for x in range(1, img.size[0]-1, gridSize):
                worked = False

                pic = ""
                
                while not worked and (len(inserts) > 0 or walkPath == "") and (len(imgs) < len(inserts) or walkPath == ""):
                    try:
                        if walkPath == "" and inserts == []:
                            imgpath = getInsertById(getParam(4))
                        else:
                            imgpath = random.choice(inserts)
                        
                        if imgpath not in imgs:
                            pic = Image.open(imgpath)
                            pic = pic.convert("RGBA")
                            imgs.append(imgpath)

                        if imgpath in inserts:
                            inserts.remove(imgpath)
                            
                        worked = True
                    except Exception as e:
                        worked = False
                        
                        if imgpath in inserts:
                            inserts.remove(imgpath)

                        print(e)
                        pass

                if pic != "":
                    pic = pic.resize((gridSize-1, gridSize-1), Image.LANCZOS)

                    if doAdapt:
                        cCount = random.randint(10, 40)
                        pic = pic.convert("P", palette=Image.ADAPTIVE, colors=cCount)

                    img.paste(pic, (x, y))

        #img = img.convert("P", palette=Image.WEB)

    except Exception as e:
        img = writeImageException(e)
        draw = ImageDraw.Draw(img)
        fonError = ImageFont.truetype(fontPath + fontNameMono, 12)
        
        draw.text((5, 160), imgpath, font=fonError, fill=(255, 0, 0, 255))
        
    return img

def adaptSpiral():
    try:
        img = realspiral()

        cCount = random.randint(4, 25)
        
        img = img.convert("P", palette=Image.ADAPTIVE, colors=cCount)
        img = img.convert("RGBA")
        
    except Exception as e:
        img = writeImageException(e)

    return img

def hollywoodSign():
    img = Image.open("hollywoodsign.jpg")
    
    try:        
        img = img.convert("RGBA")
        draw = ImageDraw.Draw(img)

        fonbg = ImageFont.truetype(fontPath + "Hollywood Capital Hills (Final).ttf", 52)
        fon = ImageFont.truetype(fontPath + "Hollywood Capital.ttf", 52)

        x = 310
        y = 190

        words = [getRandomWord() + " " + getRandomWord()]

        for w in words:
            draw.text((x, y), w, font=fonbg, fill=(70, 70, 70, 255))
            draw.text((x-3, y-5), w, font=fon, fill=(255, 255, 255, 255))
            y += 34
        
    except Exception as e:
        img = writeImageException(e)

    return img

def vaporwave1(choices=[]):
    img = ""

    try:       
        img = Image.new("RGBA", (1280, 1024), "#FFFFFF")
        
        pixdata = img.load()

        x = 1
        y = 1
        targ = pixdata[x,y]

        hexchoices = ["#00f9ff","#c36fbf","#6cffa2","#fff400","#ff00ce"]

        if choices == []:
            for c in hexchoices:
                choices.append(hex_to_rgb(c))

        addons = []
        
        for c in choices:
            xx = (c[0], c[1], c[2])
            
            for jj in range(5):
                i = random.randint(0, 2)

                xx = replace_at_index(xx, i, xx[i] + (random.randint(-5, 5)))
                xx = safetyCheck(xx)
            
            addons.append(xx)

        for a in addons:
            choices.append(a)

        global randoFillList
        
        randomIt = random.choice(randoFillList)
        
        floodfill(img, (x, y), targetcolour = targ,
                  newcolour = (0,0,0),
                  randomIt = randomIt,
                  choices = choices)
            
    except Exception as e:
        img = writeImageException(e)

    return img

def vaporwave2(choices=[], lines=[]):
    img = ""
    
    try:        
        if choices == []:
            choices = getPaletteGenerated()

        if lines == []:
            lines = [ getRandomWord() for i in range(random.randint(4, 8)) ]

        img = vaporwave1(choices)
        draw = ImageDraw.Draw(img)

        textSize = 120

        fon = ImageFont.truetype(getFont(), textSize)

        x = 50
        y = 10

        for line in lines:
            textStrokeExtra(draw, x, y, line, fon, (0,0,0,255), 2)
            c = random.choice(choices)
            draw.text((x, y), line, font=fon, fill=c)

            y += textSize + 5
            
    except Exception as e:
        img = writeImageException(e)

    return img

def vaporwave2By4():
    img = ""
    
    try:
        choices = []
        choices = getPaletteGenerated()

        lines = [getRandomWord(),getRandomWord(),getRandomWord(),getRandomWord()]
        
        img1 = vaporwave2(choices, lines)
        w = img1.size[0]
        h = img1.size[1]
        
        img1 = img1.resize((w//2,h//2))

        lines = [getRandomWord(),getRandomWord(),getRandomWord(),getRandomWord()]
        img2 = vaporwave2(choices, lines)
        img2 = img2.resize((w//2,h//2))

        lines = [getRandomWord(),getRandomWord(),getRandomWord(),getRandomWord()]
        img3 = vaporwave2(choices, lines)
        img3 = img3.resize((w//2,h//2))

        lines = [getRandomWord(),getRandomWord(),getRandomWord(),getRandomWord()]
        img4 = vaporwave2(choices, lines)
        img4 = img4.resize((w//2,h//2))        
        
        img = Image.new("RGBA", (w,h), "#000000")

        img.paste(img1, (0, 0))
        img.paste(img2, (w//2, 0))
        img.paste(img3, (0, h//2))
        img.paste(img4, (w//2, h//2))

    except Exception as e:
        img = writeImageException(e)

    return img

def wordsquares():
    imgout = ""

    try:
        textSize = 48
        wordCount = 15
        spacing = 15

        w = 1024
        h = (wordCount + 1) * (textSize) + 25

        maxX = 0

        choices = getPalette()

        bgColor = random.choice(choices)
        fill = random.choice(choices)

        while bgColor == fill:
            fill = random.choice(choices)
            
        if fill[0] < bgColor[0] or fill[1] < bgColor[1] or fill[2] < bgColor[2]:
            # swap the two
            tempfill = fill
            fill = bgColor
            bgColor = tempfill
            
        img = Image.new("RGBA", (w,h), bgColor)
       
        draw = ImageDraw.Draw(img)

        lineColor = ""

        while lineColor == "" or lineColor == bgColor:
            lineColor = random.choice(choices)

        lastYPos = 0

        # vert line on the left
        draw.line((5, 0, 5, h), fill=lineColor)

        font = ImageFont.truetype(fontPath + fontNameWordGrid, textSize)
        #fontPath = getFont()
        #font = ImageFont.truetype(fontPath, textSize)

        for i in range(0, wordCount * 5, 5):
            text = getRandomWord()

            size = font.getsize(text)

            xpos = spacing
            ypos = lastYPos + spacing + size[1]

            if lastYPos == 0:
                ypos = spacing                

            if ypos > h:
                ypos = h

            draw.text((xpos, ypos), text, font=font, fill=fill)

            lineYPos = ypos + size[1] + 5

            if xpos + size[0] > maxX:
                maxX = xpos + size[0]
                    
            # horizontal line under text
            draw.line((0, lineYPos, w, lineYPos), fill=lineColor)

            lastYPos = ypos                
        
        # right side first vert line
        fadeOut = lineColor
        diFactor = 14
        for i in range(0, 75, 5):
                finalMaxX = maxX + spacing + i
                fadeOut = (fadeOut[0] - diFactor, fadeOut[1] - diFactor, fadeOut[2] - diFactor)
                draw.line((finalMaxX, 0, finalMaxX, h), fill=fadeOut)

        if finalMaxX > w:
            finalMaxX = w
            
        img = img.crop((0, 0, finalMaxX, h))
        img = img.convert("RGBA")

    except Exception as e:
        img = writeImageException(e)
        
    return img

def vaporSquares():
    img = ""
    
    try:
        img = wordsquares()
        img = img.convert("RGB")
        
        pixdata = img.load()
        
        choices = []
        hexchoices = ["#00f9ff","#c36fbf","#6cffa2","#fff400","#ff00ce"]

        for c in hexchoices:
            choices.append(hex_to_rgb(c))

        coco = bigSquareGrid(choices)
        coco = coco.convert("P", palette=Image.ADAPTIVE)
        
        img = img.quantize(method=2, palette=coco)
        
    except Exception as e:
        img = writeImageException(e)
        
    return img

def wordGrid():       
    width = 1200
    height = 1000  

    p1 = getParam(0)
           
    try:
        img = Image.new("RGBA", (width, height), "#000000")
        draw = ImageDraw.Draw(img)
               
        maxX = 0
        x = 0
        fontSize = 42
        xTra = 10

        choices = getInputPalette(generate=False)
        
        while maxX < img.size[0]:            
            x = maxX + 25

            for y in range(5, img.size[1]-1 - (fontSize+xTra), fontSize+xTra):
                iAlg = random.randint(0, 15)
                word = getGridWord(iAlg, 0, p1)
               
                fon = ImageFont.truetype(fontPath + fontNameWordReg, fontSize)

                text_size_x = draw.textlength(word, font=fon)

                if text_size_x + x > maxX:
                    maxX = x + text_size_x + 5

                fillColor = random.choice(choices)

                while fillColor[:3] == (0,0,0):
                    fillColor = random.choice(choices)

                if x + text_size_x < img.size[0]:                        
                    draw.text((x, y), word, font=fon, fill=fillColor)
                        
    except Exception as e:
        img = writeImageException(e)  
        
    return img

def getGridWord(iAlg, wordAlg, c="", attempts=250):
    output = ""

    global rootLogger

    rootLogger.debug("getGridWord iAlg: " + str(iAlg) + " wordAlg: " + str(wordAlg) + " " + str(c))

    iAttempt = 0

    while (output == "" or (len(output) > 0 and len(c) > 0 and output[0].lower() != c[0].lower())) and iAttempt < attempts:
        if iAlg == 0:
            if wordAlg == 0:
                output = getRandomWordSpecial("adjective",c)
            else:
                output = getRandomWordSpecial("noun",c)
        elif iAlg == 1:
            if wordAlg == 0:
                output = getRandomWordSpecial("adjective",c)
            else:
                output = getRandomWordSpecial("verb",c)
        elif iAlg == 2:
            if wordAlg == 0:
                output = getRandomWordSpecial("verb",c)
            else:
                output = getRandomWordSpecial("noun",c)
        elif iAlg == 3:
            if wordAlg == 0:
                output = getRandomWordSpecial("adjective",c)
            else:
                output = getRandomWordSpecial("noun",c)
        elif iAlg == 4:
            if wordAlg == 0:
                output = getRandomWordSpecial("positive",c)
            else:
                output = getRandomWordSpecial("jargon",c)
        elif iAlg == 5:
            if wordAlg == 0:
                output = getRandomWordSpecial("negative",c)
            else:
                output = getRandomWordSpecial("jargon",c)
        elif iAlg == 6:
            if wordAlg == 0:
                output = getRandomWord_Moby(choice=c)
            else:
                output = getRandomWord_Moby(choice=c)
        elif iAlg == 7:
            if wordAlg == 0:
                output = getRandomWord_Moby(choice=c)
            else:
                output = getRandomWord_Moby("h", c)
        elif iAlg == 8:
            if wordAlg == 0:
                output = getRandomWord_Moby("V", c)
            else:
                output = getRandomWord_Moby("!", c)
        else:
            if wordAlg == 0:
                output = getRandomWord(c)
            else:
                output = getRandomWord(c)
        
        # colorPrint.print_custom_rgb(f"iAttempt: {iAttempt} / attempts: {attempts} // output: {output}", 255,255,0)

        iAttempt += 1

    return output

def wordGrid2(wordline="", fontSize=48, fontPath=""):
    """p1: first word must match first char of p1<br />
    p2: second word must match first char of p2<br />
    paramfont: partial match of font filename"""

    global rootLogger
    global fontPathSansSerif

    paramfont = getParam(3)

    if paramfont != "":
        fontPath = getFont(choiceStatic=paramfont)
    if fontPath == "":
        fontPath = getFont()
        
    width = 1280
    height = 1024
    
    p1 = getParam(0)
    p2 = getParam(1)    
    
    try:
        bgColor = hex_to_rgb("#000000")

        global input_palette

        if input_palette != "" and input_palette != []:
            choices = input_palette
        else:         
            choices = getPaletteGenerated(bgColor=bgColor, minContrast=2.75)        

        img = Image.new("RGBA", (width, height), bgColor)
        draw = ImageDraw.Draw(img)
               
        maxX = 0
        x = 0

        xTra = 20
        
        lastChoice = 0

        while maxX < img.size[0]:
            x = maxX + 35

            for y in range(10, img.size[1]-1 - (fontSize+xTra), fontSize+xTra):
                if wordline == "":
                    word = getDecree(p1, p2).upper()
                else:
                    word = wordline
                                
                fon = ImageFont.truetype(fontPath, fontSize)

                text_size_x, _ = dropin_text_size(draw,word, font=fon)

                if text_size_x + x > maxX:
                    maxX = x + text_size_x + 5

                fillColor = random.choice(choices)

                iChoice = 0

                while (fillColor[:3] == (0,0,0) or lastChoice == fillColor) and iChoice < 5:
                    fillColor = random.choice(choices)
                    iChoice += 1

                # ccr = calcContrastRatio(bgColor, fillColor)

                strokec = getInverse(fillColor)
                strokec = (strokec[0], strokec[1], strokec[2], 64)

                if x + text_size_x < img.size[0]:                    
                    draw.text((x, y), f"{word}", font=fon, fill=fillColor, stroke_width=1, stroke_fill=strokec)

                lastChoice = fillColor
        
        fontName = fontPath.split("/")[-1]
        fonSans = ImageFont.truetype(fontPathSansSerif, 20)
        text_size_x, text_size_y = dropin_text_size(draw,fontName, font=fonSans)
        draw.text((img.size[0] - text_size_x - 5, img.size[1] - text_size_y - 6), fontName, font=fonSans, fill=(255,255,255))

    except Exception as e:
        rootLogger.error(e)
        img = writeImageException(e)  
        
    return img

def getDecree(p1, p2, attempts=50):
    w1 = ""
    w2 = ""
    w1_1 = p1
    w2_1 = p2
                    
    pos = random.choice(["C", "i", "o"])

    conjuc = getRandomWord_Moby(pos)

    iAttempts = 0
    while w1 == "" or w2 == "" or (len(w1_1) > 0 and len(w1) > 0 and w1_1[0].lower() != w1[0].lower()) or (len(w2_1) > 0 and len(w2) > 0 and w2_1[0].lower() != w2[0].lower()):
        iAlg = random.randint(0, 15)
        w1 = getGridWord(iAlg, 0, w1_1, attempts)
        w2 = getGridWord(iAlg, 1, w2_1, attempts)

        colorPrint.print_custom_rgb(f"Decree: iAlg: {iAlg} w1, w2: {w1} {w2}", 88, 84, 255)

        iAttempts += 1

        if iAttempts > attempts:
            break
                       
    word = (w1 + " " + w2)

    if random.randint(0, 1) == 1 and conjuc != "":
        word = (w1 + " " + conjuc + " " + w2)

    return word

def textHash(wordline="", fontSize=36, fontPath=""):
    global rootLogger
    global fontPathSansSerif

    paramfont = getParam(3)

    if paramfont != "":
        fontPath = getFont(choiceStatic=paramfont)
    if fontPath == "":
        fontPath = getFont()
        
    width = getCurrentStandardWidth()
    height = getCurrentStandardHeight()
    
    p1 = getParam(0)
    p2 = getParam(1)
    
    outputs = []

    try:
        global input_palette

        if input_palette != "" and input_palette != []:
            choices = input_palette
        else:         
            choices = getPaletteGenerated()
        
        things = [time.time(), "ABC", "123", 255, 128, 0]

        for y in things:
            v2 = hashlib.sha256(str(y).encode('utf-8')).hexdigest()
            line = [y, hash(y), v2]
            
            outputs.append(line)
        
        #fontName = fontPath.split("/")[-1]
        #fonSans = ImageFont.truetype(fontPathSansSerif, 16)
        #text_size_x, text_size_y = dropin_text_size(draw,fontName, font=fonSans)
        #draw.text((img.size[0] - text_size_x - 5, img.size[1] - text_size_y - 5), fontName, font=fonSans, fill=(255,255,255))

    except Exception as e:
        rootLogger.error(e)
        img = writeImageException(e)  
        
    outputText = "<div class='output-text single-file' id='output-text'>"
    outputText += f'<table class="palette">'
    outputText += f'<tr><th>Value</th><th>hash()</th><th>SHA256</th></tr>'

    for o in outputs:
        xx = ''.join(f'<td>{h}</td>' for h in o)
        outputText += f'<tr>{xx}</tr>'

    outputText += "</table></div>"

    return outputText

def colorSample():
    """p1: comma-separated list of hex codes without #<br />
    p2: length of palette to generate if p1 not supplied (default=5)"""

    palette = []

    p1 = getParam(0)
    p2 = getParam(1)

    p2 = int(p2) if p2 != "" and p2.isdecimal() else 5

    if p1 != "" and "," in p1:
        hexc = [z.strip() for z in p1.split(',')]
    
        for c in hexc:
            palette.append(hex_to_rgb("#"+c))
    else:
        palette = getPaletteGenerated(paletteLength=p2)

    rootLogger.debug(f'p1: {p1}, p2: {p2}, palette: {palette}')

    rowCount = 10
    recSize = 100
        
    height = recSize * rowCount + 1
    cutoff = len(palette) // rowCount
    
    if cutoff < 5:
        cutoff = 5
        
    width = (recSize * (cutoff + 1)) + 1

    try:
        img = Image.new("RGBA", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        y = 0
        j = 0
        
        for i in range(0, len(palette)):         
            c = palette[i]
            x = recSize * j

            rootLogger.debug(f'square {i}: {c} @ {x},{y}:{x+recSize},{y+recSize}')
            
            draw.rectangle(((x,y),(x+recSize,y+recSize)), fill=c, outline=palette[0])

            if j == cutoff:
                y += recSize
                j = 0                
            else:
                j += 1
        
        y += recSize + 1

        img = img.crop((0, 0, width, y))

    except Exception as e:
        img = writeImageException(e)

    return img

def wordGridTxT(wordline="", fontSize=36, fontPath=""):
    """p1: first word must match first char of p1<br />
    p2: second word must match first char of p2<br />
    paramfont: partial match of font filename"""

    global rootLogger
    global fontPathSansSerif

    paramfont = getParam(3)

    if paramfont != "":
        fontPath = getFont(choiceStatic=paramfont)
    if fontPath == "":
        fontPath = getFont()
        
    width = getCurrentStandardWidth()
    height = getCurrentStandardHeight()
    
    p1 = getParam(0)
    p2 = getParam(1)    
    
    outputs = []

    try:
        global input_palette

        if input_palette != "" and input_palette != []:
            choices = input_palette
        else:         
            choices = getPaletteGenerated()
                  
        for y in range(0, 48):
            if wordline == "":
                word = getDecree(p1, p2, attempts=50).upper()                  
            else:
                word = wordline               
            
            outputs.append(word)
        
        #fontName = fontPath.split("/")[-1]
        #fonSans = ImageFont.truetype(fontPathSansSerif, 16)
        #text_size_x, text_size_y = dropin_text_size(draw,fontName, font=fonSans)
        #draw.text((img.size[0] - text_size_x - 5, img.size[1] - text_size_y - 5), fontName, font=fonSans, fill=(255,255,255))

    except Exception as e:
        rootLogger.error(e)
        img = writeImageException(e)  
        
    outputText = "<div class='output-text' id='output-text'>"
    outputText += f'<ul>'

    for o in outputs:
        outputText += f'<li>{o}</li>'

    outputText += "</ul></div>"

    return outputText

def generate_stats(name, stats={
        'STR': 5,
        'DEX': 5,
        'CON': 5,
        'INT': 5,
        'WIS': 5,
        'CHR': 5
    }):

    X = 3

    seed = int(hashlib.sha256(name.encode('utf-8')).hexdigest(), 16)
    random.seed(seed)

    # List of stat keys for cyclic assignment
    stat_keys = list(stats.keys())

    # Iterate over each character in the name
    for i, char in enumerate(name):
        # Convert character to a numerical value
        char_value = ord(char)

        # Assign character value to stats in a cyclic manner
        stat_key = stat_keys[i % len(stat_keys)]
        stats[stat_key] += char_value % X  # Add remainder of division by X to keep stat increase reasonable

    for s in stats.keys():
        val = stats[s]

        stats[s] = val if val < 20 else 20

    return (stats, seed)

def wordGridStats(wordline="", fontSize=14, fontPath=""):
    global rootLogger
    global fontPathSansSerif

    paramfont = getParam(3)

    if paramfont != "":
        fontPath = getFont(choiceStatic=paramfont)
    if fontPath == "":
        fontPath = getFont()
        
    width = getCurrentStandardWidth()
    height = getCurrentStandardHeight()
    
    p1 = getParam(0)
    p2 = getParam(1)    
    
    outputs = []

    try:
        choices = getInputPalette()

        if wordline == "":
            word = getDecree(p1, p2, attempts=50).upper()                  
        else:
            word = wordline

        for y in range(-1, 7):
            if y >= 0:
                wordHere = word + " " + str(y)
            else:
                wordHere = word

            statsz = generate_stats(wordHere, {'Fire':0, 'Water':0, 'Wind': 0, 'Earth': 0, 'Spirit': 0})    
            stats = statsz[0]
            
            outputs.append(wordHere)
            outputs.append(statsz[1])
            outputs.append(str(stats))
            outputs.append("")      

    except Exception as e:
        rootLogger.error(e)
        img = writeImageException(e)  
        
    outputText = "<div class='output-text single-file' id='output-text'>"
    outputText += f'<ul>'

    for o in outputs:
        outputText += f'<li>{o}</li>'

    outputText += "</ul></div>"

    return outputText

def english_gematria(word):
    return sum((ord(char.upper()) - ord('A') + 1) * 6 for char in word if char.isalpha())

def wordGridGematria(wordline="", fontSize=36, fontPath=""):
    """p1: first word must match first char of p1<br />
    p2: second word must match first char of p2<br />
    paramfont: partial match of font filename"""

    filterFunc = lambda word: english_gematria(word)
    #filterFunc = lambda word: get_random_unicode(1)

    return wordGridGeneral(wordline, fontSize, fontPath, filterFunc)

def getWordFunc(p1):
    iAlg = random.randint(0, 15)
    word = getGridWord(iAlg, 0, p1, 25)
    return word
    
def wordGridGeneral(wordline="", fontSize=36, fontPath="", filterFunc=lambda w: w, word_count=48, extra_html="", actual_words=None, lemmas=None):
    """p1: first word must match first char of p1<br />
    p2: second word must match first char of p2<br />
    paramfont: partial match of font filename"""

    global rootLogger
    global fontPathSansSerif

    paramfont = getParam(3)

    if paramfont != "":
        fontPath = getFont(choiceStatic=paramfont)
    if fontPath == "":
        fontPath = getFont()
        
    width = getCurrentStandardWidth()
    height = getCurrentStandardHeight()
    
    p1 = getParam(0)
    p2 = getParam(1)
    
    outputs = []

    try:
        choices = getInputPalette(generate=False)

        if actual_words is not None:
            for y in actual_words:
                outputs.append(y)
        else:
            for y in range(0, word_count):
                if wordline == "":
                    iAlg = random.randint(0, 15)
                    word = getGridWord(iAlg, 0, p1, 25)
                else:
                    word = wordline               
                
                eg = filterFunc(word)

                if "—" in eg:
                    if eg[-1] == "—":
                        outputs.append(eg[:-1])
                    else:
                        outputs.append(eg)
                else:
                    outputs.append(f'{word}: {eg}')
        
    except Exception as e:
        rootLogger.error(e)
        img = writeImageException(e)  

    outputText = ""

    if lemmas is not None:
        outputText = "<div class='lemmas' id='lemmas'>"
        outputText += "lemmas:<br />"

        for lem in lemmas:
            outputText += f"{lem}<br />"
            
        outputText += "</div>"
        
    outputText += extra_html + "<div class='output-text' id='output-text'>"
    outputText += f'<ul>'

    for o in outputs:
        outputText += f'<li>{o}</li>'

    outputText += "</ul></div>"

    return outputText

def wordGrid_image():
    wordline=""
    fontSize=34

    global rootLogger
    global fontPathSansSerif
    
    paramfont = getParam(3)

    fontPathZ = ""
    if paramfont != "":
        fontPathZ = getFont(choiceStatic=paramfont)
    if fontPathZ == "":
        fontPathZ = getFont()
           
    try:
        inputPath = getInsertById(getParam(4))
        inputImg = Image.open(inputPath)
        
        inputImg = inputImg.convert("RGBA")
        img = resizeToMinMax(inputImg, 1280, 900, 1024, 600)

        p1 = getParam(0)
        p2 = getParam(1)
        
        choices = getPaletteGenerated()

        draw = ImageDraw.Draw(img)
               
        maxX = 0
        x = 0

        xTra = 20
        
        while maxX < img.size[0]:
            x = maxX + 35

            for y in range(10, img.size[1]-1 - (fontSize+xTra), fontSize+xTra):
                if wordline == "":
                    w1 = ""
                    w2 = ""
                    w1_1 = p1
                    w2_1 = p2
                    
                    pos = random.choice(["C", "i", "o"])

                    conjuc = getRandomWord_Moby(pos)

                    while w1 == "" or w2 == "" or (len(w1_1) > 0 and len(w1) > 0 and w1_1[0].lower() != w1[0].lower()) or (len(w2_1) > 0 and len(w2) > 0 and w2_1[0].lower() != w2[0].lower()):
                        iAlg = random.randint(0, 15)
                        w1 = getGridWord(iAlg, 0, w1_1)
                        w2 = getGridWord(iAlg, 1, w2_1)
                       
                    word = (w1 + " " + w2).upper()

                    if random.randint(0, 1) == 1 and conjuc != "":
                        word = (w1 + " " + conjuc + " " + w2).upper()
                        
                else:
                    word = wordline
                                
                fon = ImageFont.truetype(fontPathZ, fontSize)

                text_size_x, _ = dropin_text_size(draw,word, font=fon)

                if text_size_x + x > maxX:
                    maxX = x + text_size_x + 5

                if x + text_size_x + 10 < img.size[0]: 
                    draw.text((x, y), word, font=fon, fill=getRandomColor(), stroke_width=3, stroke_fill=(0,0,0))
        
        fontName = fontPathZ.split("/")[-1]
        fonSans = ImageFont.truetype(fontPathSansSerif, 16)
        text_size_x, text_size_y = dropin_text_size(draw,fontName, font=fonSans)
        draw.text((img.size[0] - text_size_x - 5, img.size[1] - text_size_y - 5), fontName, font=fonSans, fill=(255,255,255))

    except Exception as e:
        rootLogger.error(e)
        img = writeImageException(e)  
        
    return img

def wordGrid_Moby(wordline="", fontSize=42, fontPath=""):
    """
    <pre>moby pos (p1,p2)<br />
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
    </pre>
    """

    global rootLogger
    global fontPathSansSerif

    if fontPath == "":
        fontPath = getFont()
        
    width = getCurrentStandardWidth()
    height = getCurrentStandardHeight()
    
    p1 = getParam(0)
    p2 = getParam(1)

    rootLogger.debug("p1: " + p1)
    rootLogger.debug("p2: " + p2)
    
    try:        
        img = Image.new("RGBA", (width, height), "#000000")
        draw = ImageDraw.Draw(img)
               
        maxX = 0
        x = 0
        xTra = 20
        
        throwaway = getRandomWord_Moby()

        keylist = list(wordsMoby.keys())

        colorPrint.print_custom_palette(24, f'keylist: {str(keylist)}')

        keylist.remove("e")

        xRounds = 0

        while maxX < img.size[0] and xRounds <= 1:
            x = maxX + 35

            for y in range(10, img.size[1]-1 - (fontSize+xTra), fontSize+xTra):
                skipPosAppend = 0

                if wordline == "":
                    w1 = ""
                    w2 = ""
                   
                    while w1 == "" or w2 == "":
                        if p1 == "" or p1 not in keylist:
                            pos1 = random.choice(keylist)                            
                        else:
                            pos1 = p1
                            skipPosAppend += 1

                        if p2 == "" or p2 not in keylist:
                            pos2 = random.choice(keylist)
                        else:
                            pos2 = p2
                            skipPosAppend += 1

                        w1 = getRandomWord_Moby(pos1)
                        w2 = getRandomWord_Moby(pos2)
                       
                    if skipPosAppend < 2:
                        word = pos1 + "," + pos2 + ": " + (w1 + " " + w2).upper()
                    else:
                        word = (w1 + " " + w2).upper()
                else:
                    word = wordline
                                
                fon = ImageFont.truetype(fontPath, fontSize)

                text_size_x, _ = dropin_text_size(draw,word, font=fon)

                if text_size_x + x > maxX:
                    maxX = x + text_size_x + 5

                if x + text_size_x < img.size[0]: 
                    draw.text((x, y), word, font=fon, fill=getRandomColor())
        
            xRounds += 1

        rightCornerDisplay = f'({p1},{p2}) {fontPath.split("/")[-1]}'

        fonSans = ImageFont.truetype(fontPathSansSerif, 16)
        text_size_x, text_size_y = dropin_text_size(draw,rightCornerDisplay, font=fonSans)
        draw.text((img.size[0] - text_size_x - 5, img.size[1] - text_size_y - 5), rightCornerDisplay, font=fonSans, fill=(255,255,255))

    except Exception as e:
        rootLogger.error(e)
        img = writeImageException(e)  
        
    return img

def wordGrid_single(wordline="", fontSize=128):
    width = 640
    height = 300
    
    try:        
        c = (random.randint(50, 255),random.randint(50, 255),random.randint(50, 255))
        i = random.randint(0,2)
        c = replace_at_index(c, i, 0)

        choices = []

        for j in range(0,255,25):
            ci = replace_at_index(c, i, j)

            choices.append(ci)            

        img = Image.new("RGBA", (width, height), getRandomColor())
        draw = ImageDraw.Draw(img)
               
        maxX = 0
        x = 0

        xTra = 10

        fontPath = getFont()        
        spacing = 25
        
        x = spacing
        y = spacing

        if wordline == "":
            word = (getRandomWord() + "\n" + getRandomWord() + "\n" + getRandomWord()).upper()
        else:
            word = wordline

        text_size_x = img.size[0] + 100

        while text_size_x > img.size[0] - x - 10 or text_size_y > img.size[1] - y - 10:
            fontSize -= 1
            
            fon = ImageFont.truetype(fontPath, fontSize)

            text_size_x, text_size_y = draw.multiline_textsize(word, font=fon, spacing=spacing)

        fillColor = random.choice(choices)

        while fillColor[:3] == (0,0,0):
            fillColor = random.choice(choices)

        half_x = int(img.size[0] // 2)
        half_text_x = int(text_size_x // 2)

        x = half_x - half_text_x

        if x < 0:
            x = 0
        
        strokec = getInverse(fillColor)
        textStrokeExtraMultiline(draw, x, y, word, fon, strokec, spacing, "center", 3)
        draw.multiline_text((x, y), word, font=fon, fill=fillColor, spacing=spacing, align="center")

        #img = img.crop((0, 0, text_size_x + (x * 2), text_size_y + (y * 2)))
        #img.load()
                
    except Exception as e:
        img = writeImageException(e)  
        
    return img

def wordGrid_static(wordline=""):    
    if wordline == "":
        wordline = (getRandomWord() + " " + getRandomWord()).upper()
        
    return wordGrid2(wordline, 30)

def wordGrid_Special(wordline="", fontSize=36, fontPath=""):
    """p1: partial filename to match<br />
    p2: static info. types: 1=The {} Man, blank=default"""
    
    global rootLogger
    global fontPathSansSerif       

    if fontPath == "":
        fontPath = getFont()

    width = getCurrentStandardWidth()
    height = getCurrentStandardHeight()
    
    p1 = getParam(0)
    p2 = getParam(1)
   
    try:
        filepath, wurdos = loadSpecialWordlist(p1)

        filename = filepath.split('/')[-1]

        choices = getPaletteGenerated()

        img = Image.new("RGBA", (width, height), "#000000")
        draw = ImageDraw.Draw(img)
               
        maxX = 0
        x = 0

        xTra = 20
        
        thesewyrdos = []

        while maxX < img.size[0]:
            x = maxX + 35

            for y in range(10, img.size[1]-1 - (fontSize+xTra), fontSize+xTra):
                rngWords = random.randint(2, 4)

                if wordline == "" and p2 != "1":
                    rsrsrs = [random.choice(wurdos) for c in range(rngWords)]
                    word = (' '.join(rsrsrs)).upper()
                elif p2 == "1":
                    middletxt = (random.choice(wurdos)).strip()                    
                    word = ("The " + middletxt + " Man").title()

                    while word in thesewyrdos:
                        middletxt = (random.choice(wurdos)).strip()                    
                        word = ("The " + middletxt + " Man").title()
                        
                    thesewyrdos.append(word)
                else:
                    word = wordline
                                
                fon = ImageFont.truetype(fontPath, fontSize)

                text_size_x, _ = dropin_text_size(draw,word, font=fon)

                if text_size_x + x > maxX:
                    maxX = x + text_size_x + 5

                if x + text_size_x < img.size[0]: 
                    draw.text((x, y), word, font=fon, fill=getRandomColor())
        
        fontName = fontPath.split("/")[-1]
        fonSans = ImageFont.truetype(fontPathSansSerif, 16)
        text_size_x, text_size_y = dropin_text_size(draw,fontName, font=fonSans)
        draw.text((img.size[0] - text_size_x - 5, img.size[1] - text_size_y - 5), fontName, font=fonSans, fill=(255,255,255))

        draw.text((5, img.size[1] - text_size_y - 5), filename, font=fonSans, fill=(255,255,255))

    except Exception as e:
        rootLogger.error(e)
        img = writeImageException(e)  
        
    return img

def loadSpecialWordlist(p1):
    filepaths = getChoicesWalk(wordListsPath, ('.txt'))
    filepath = random.choice(filepaths)

    if p1 != "":
        pz = [c for c in filepaths if p1.lower() in c.lower()]
        if len(pz) > 0:
            filepath = pz[0]

    wurdos = []
    wurdos = loadWordsFrom(filepath)

    return filepath, wurdos

def slightlyDiffSquares():
    img = ""
    
    try:
        imgpath = getInsertById(getParam(4))
        img = Image.open(imgpath).convert("RGBA")

        img = resizeToMinMax(img, 1280, 1024, 800, 600)
            
        pixdata = img.load()

        xxxCount = random.randint(1, 7)
        
        for xxx in range(xxxCount):
            sqCnt = random.randint(8, 12)
            
            xi = int(img.size[0] // sqCnt)
            yi = int(img.size[1] // sqCnt)

            lbX = 0
            lbY = 0

            while lbX < img.size[0] or lbY < img.size[1]:
                j = random.randint(0, int(130.0 // xxxCount))
                
                for x in range(lbX, lbX + xi):
                    for y in range(lbY, lbY + yi):
                        if x < img.size[0] and y < img.size[1]:
                            c = pixdata[x,y]

                            for i in range(0, 4):
                                ci = c[i]
                                ci += j
                                
                                if ci < 0:
                                    ci = 0
                                    
                                if ci > 255:
                                    ci = 255
                                    
                                c = replace_at_index(c, i, ci)                    
                            
                            pixdata[x,y] = c

                if lbX < img.size[0]:
                    lbX += xi
                else:
                    lbY += yi
                    lbX = 0
        
    except Exception as e:
        img = writeImageException(e)  
        
    return img

def adaptivePublic():
    img = ""
    try:
        imgpath = getInsertById(getParam(4))

        img = Image.open(imgpath)
        img = img.convert("RGB")
        img = resizeToMinMax(img, maxW=1280, maxH=1024, minW=640, minH=480)

        palette = getInputPalette()
        gen = generatePalette(palette)
        gen = gen.convert("P", palette=Image.ADAPTIVE)
        
        img.load()
        img = img.quantize(method=2, palette=gen) 
        img = img.convert("RGBA")
        
    except Exception as e:
        img = writeImageException(e)
        
    return img

def randomTriangles():
    img = ""

    try:
        img = Image.new("RGBA", (1024, 768), "#000000")
        draw = ImageDraw.Draw(img)

        pixdata = img.load()

        global maxFloodFillArg

        choices = getInputPalette()
        
        floodfill(img, (1, 1), targetcolour = pixdata[1,1],
                      newcolour = (0,0,0),
                      randomIt = random.randint(1, maxFloodFillArg),
                      choices = choices)

        for i in range(50):
            pts = []

            leastX = img.size[0]
            leastY = img.size[1]
            
            for j in range(3):
                x = random.randint(-50, img.size[0]+50)
                y = random.randint(-50, img.size[1]+50)

                pts.append((x,y))

                if x < leastX:
                    leastX = x
                    leastY = y

            c = random.choice(choices)
            cFill = random.choice(choices)

            draw.polygon(pts, fill=cFill, outline=c)

            #floodfill(img, (leastX+1, leastY+1), targetcolour = pixdata[leastX+1, leastY+1],
            #          newcolour = (0,0,0),
            #          randomIt = random.choice([20, 25, 33, 34]))
            
    except Exception as e:
        img = writeImageException(e)

    return img

def triangleSys(choices=[]):
    img = ""

    try:
        global input_palette
        
        choices = getInputPalette(generate=False)

        img = Image.new("RGBA", (getCurrentStandardWidth(), getCurrentStandardHeight()), "#000000")
        draw = ImageDraw.Draw(img)

        sqCnt = random.choice([2, 4, 5, 8, 10, 20, 30, 40])
        
        xi = int(img.size[0] // sqCnt)
        yi = int(img.size[1] // sqCnt)

        lbX = 0
        lbY = 0

        lastC = (0,0,0)
        
        while lbX < img.size[0] or lbY < img.size[1]:
            for k in range(0, 2):
                pts = []
                if k == 0:
                    pts.append((lbX, lbY))
                    pts.append((lbX + xi, lbY))
                    pts.append((lbX, lbY + yi))
                else:
                    pts.append((lbX + xi, lbY))
                    pts.append((lbX + xi, lbY + yi))
                    pts.append((lbX, lbY + yi))                    
            
                c = random.choice(choices)
                cFill = random.choice(choices)

                while cFill[:3] == lastC[:3]:
                    cFill = random.choice(choices)

                lastC = cFill
                    
                draw.polygon(pts, fill=cFill, outline=c)

            if lbX < img.size[0]:
                lbX += xi
            else:
                lbY += yi
                lbX = 0
            
    except Exception as e:
        img = writeImageException(e)

    return img

def triangleGrid():
    img = ""

    try:
        img = Image.new("RGBA", (getCurrentStandardWidth(), getCurrentStandardHeight()), "#ffffff")
        draw = ImageDraw.Draw(img)

        pixdata = img.load()
        
        sqCnt = random.choice([2, 5, 10, 20, 30])
        
        xi = int(img.size[0] // sqCnt)
        yi = int(img.size[1] // sqCnt)
        zXi = int(xi * sqCnt) + 1
        zYi = int(yi * sqCnt) + 1

        lbX = 0
        lbY = 0

        choices = getInputPalette(generate=False)

        while lbX < img.size[0] or lbY < img.size[1]:
            for k in range(0, 2):
                pts = []
                fillPt = (0, 0)
                
                if k == 0:
                    pts.append((lbX, lbY))
                    pts.append((lbX + xi, lbY))
                    pts.append((lbX, lbY + yi))

                    fillPt = (lbX+1, lbY+1)
                else:
                    pts.append((lbX + xi, lbY))
                    pts.append((lbX + xi, lbY + yi))
                    pts.append((lbX, lbY + yi))

                    fillPt = (lbX+xi-1, lbY-1)
                    
                draw.polygon(pts, fill=(255,255,255), outline=(0,0,0))

                global maxFloodFillArg                
                iAlg = random.randint(1, maxFloodFillArg)

                try:
                    floodfill(img, fillPt,
                              targetcolour = pixdata[fillPt[0], fillPt[1]],
                              newcolour = choices[0],
                              randomIt = iAlg,
                              maxStackDepth = 0, 
                              choices=choices,
                              sizeLimit=(lbX+xi+1,lbY+yi+1))
                except:
                    pass            

            if lbX < img.size[0]:
                lbX += xi
            else:
                lbY += yi
                lbX = 0

        img = img.crop((0, 0, zXi, zYi))

    except Exception as e:
        img = writeImageException(e)

    return img

def squareGrid():
    """p1: iAlg<br />
    """

    img = ""

    try:
        img = Image.new("RGBA", (getCurrentStandardWidth(), getCurrentStandardHeight()), "#ffffff")
        draw = ImageDraw.Draw(img)

        pixdata = img.load()

        global randoFillList
        
        p1 = getParam(0)
        iAlg = int(p1) if p1.isdecimal() else random.choice(randoFillList)
        
        sqCnt = random.randint(5, 15)
        
        xi = int(img.size[0] // sqCnt)
        yi = int(img.size[1] // sqCnt)

        lbX = 0
        lbY = 0

        choices = getInputPalette(generate=False)
        cStroke = random.choice(choices)

        while lbX < img.size[0] or lbY < img.size[1]:
            pts = []
            pts.append((lbX, lbY))
            pts.append((lbX + xi, lbY))
            pts.append((lbX + xi, lbY + yi))
            pts.append((lbX, lbY + yi))   

            fillPt = (lbX+1, lbY+1)
                
            draw.polygon(pts, fill=(255,255,255), outline=cStroke)

            try:
                floodfill(img, fillPt,
                            targetcolour = pixdata[fillPt[0], fillPt[1]],
                            newcolour = (0,0,0,255),
                            randomIt = iAlg,
                            maxStackDepth = 0, 
                            choices=choices)
            except:
                pass

            if lbX < img.size[0]:
                lbX += xi
            else:
                lbY += yi
                lbX = 0

    except Exception as e:
        img = writeImageException(e)

    return img

# NECTARINE HEADLINE

# Calculate the mandelbrot sequence for the point c with start value z
def iterate_mandelbrot(iterate_max, c, z = 0):
    for n in range(iterate_max + 1):
        z = z*z +c
        if abs(z) > 2:
            return n
        
    return None

def fractal1():
    img = fractal(1)
    return img

def fractal2():
    img = fractal(2)
    return img

def fractal3():
    img = fractal(3)
    return img

def fractal4():
    img = fractal(4)
    return img

def fractalText0():
    try:
        img = fractal(1)
        d = ImageDraw.Draw(img)
        fontSize = 72
        fontPath = getFont()
        fon = ImageFont.truetype(fontPath, fontSize)
        
        pixdata = img.load()

        c = pixdata[int(img.size[0]/2), img.size[1]-1]        

        txt = Image.new('L', (500, 200))
        dtxt = ImageDraw.Draw(txt)

        word = getRandomWord()
        dtxt.text((0, 0), word, font=fon, fill=255)

        word = getRandomWord()
        dtxt.text((0, fontSize), word, font=fon, fill=255)
        
        w = txt.rotate(random.randint(-45, 45), expand=1)

        paste_point = (random.randint(0, img.size[0]),20)

        img.paste( ImageOps.colorize(w, (0,0,0), c), paste_point,  w)  
        
    except Exception as e:
        img = writeImageException(e)
        
    return img

def fractal(fractalSet=1):
    img = ""    
    
    try:
        dimensions = (getCurrentStandardWidth(), getCurrentStandardHeight())  

        if fractalSet == 1:
            # Mandelbrot set
            y_center = random.uniform(-0.4, 0.09)
            center = (1, y_center)
            scale = random.uniform(.0003, .0005) # 0.0004
            colors_max = 500
            iterate_max = 100
        elif fractalSet == 2:
            # Julia set
            center = (0.3, 0.85)
            scale = random.uniform(.0003, .00375)
            
            colors_max = 250
            iterate_max = 75
        elif fractalSet == 3:
            # Julia set
            center = (random.uniform(0, 0.3), random.uniform(0, 1))
            scale = random.uniform(.0003, .005)
            
            colors_max = 250
            iterate_max = 75
        elif fractalSet == 4:
            # Julia set, heavily modified
            centerX = random.uniform(0.28, 0.31)
            center = (centerX, 0.85)
            scale = random.uniform(.0003, .00375)
            
            colors_max = 100
            iterate_max = 40

        img = Image.new("RGBA", dimensions)
        d = ImageDraw.Draw(img)

        # Calculate a tolerable palette
        palette = [0] * colors_max

        random.seed()
        ru = random.uniform(0, 0.8)
        rv = random.uniform(0, 1)
        
        for i in range(colors_max):
            f = 1 - abs((float(i)/colors_max-1)**15)

            if fractalSet == 1:                
                r, g, b = colorsys.hsv_to_rgb(ru+f/3, rv, f)            
            elif fractalSet == 2:                
                r, g, b = colorsys.hsv_to_rgb(ru+f/3, 1 - f/3, f * rv)
            elif fractalSet == 3:
                r, g, b = random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)
            elif fractalSet == 4:
                r, g, b = colorsys.hsv_to_rgb(ru+f/3, 1 - f/3, f * rv)

            palette[i] = (int(r*255), int(g*255), int(b*255))

            rv = random.uniform(0, 1)

        ac = random.uniform(0.1, 0.4)
        bc = random.uniform(ac+.3, ac+.6)

        addState(f"ac: {ac} bc: {bc}", None)

        for y in range(dimensions[1]):
            for x in range(dimensions[0]):
                c = complex(x * scale - center[0], y * scale - center[1])

                if fractalSet == 1:
                    # Use this for Mandelbrot set
                    n = iterate_mandelbrot(iterate_max, c) 
                elif fractalSet == 2:
                    # Use this for Julia set
                    n = iterate_mandelbrot(iterate_max, complex(0.3, 0.6), c)
                elif fractalSet == 3:
                    # Use this for Julia set
                    n = iterate_mandelbrot(iterate_max, complex(ac, bc), c)
                elif fractalSet == 4:
                    # Use this for Julia set
                    n = iterate_mandelbrot(iterate_max, complex(0.3, 0.6), c)

                v = 1 if n is None else n/100.0

                p = int(v * (colors_max-1))

                if p >= len(palette):
                    p = -1
                    
                d.point((x, y), fill = palette[p])

        del d
        
    except Exception as e:
        img = writeImageException(e)

    return img

def hsvTesting():
    img = ""

    try:
        fon = ImageFont.truetype(fontPath + fontNameMono, 12)

        w = random.randint(640, 1280)
        h = random.randint(480, 1024)
        
        img = Image.new("RGB", (w, h), "#ffffff")
        d = ImageDraw.Draw(img)

        pixdata = img.load()
        
        x = 0
        y = 0

        h, s, v = 0.0, 0.0, 0.0
        hdir, sdir, vdir = 0.05, 0.05, 0.05

        version = random.randint(0, 1)

        step = random.randint(1, 25)
        
        while x < img.size[0] or y < img.size[1]:
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
        
            c = (int(r*255), int(g*255), int(b*255))
            
            #d.text((x, y), str(r), font=fon, fill=(0, 0, 0))

            d.rectangle((x, y, x + step, y + step), fill = c)

            if version == 0:
                y += step

                if y > img.size[1]:
                    if x > img.size[0]:
                        break
                    
                    x += step
                    y = 0
            else:
                x += step

                if x > img.size[0]:
                    if y > img.size[1]:
                        break
                    
                    y += step
                    x = 0
                    
            i = random.randint(0, 2)
            
            if i == 0:
                v += vdir
            elif i == 1:
                s += sdir
            else:
                h += hdir

            if h > 1 or h < 0:
                if h < 0:
                    h = 0
                if h > 1:
                    h = 1
                    
                hdir *= -1

            if s > 1 or s < 0:
                if s > 1:
                    s = 1
                if s < 0:
                    s = 0
                    
                sdir *= -1

            if v > 1 or v < 0:
                if v > 1:
                    v = 1
                if v < 0:
                    v = 0
                    
                vdir *= -1
            
    except Exception as e:
        img = writeImageException(e)

    return img

def longWordListBase(sort=False):
    img = ""

    try:
        width = 700
        height = 10000
        
        img = Image.new("RGBA", (width, height), "#000000")

        #innerColor = (0, 0, 255)
        #outerColor = (0, 0, 0)
        #img = gradientFill(img, innerColor, outerColor)
        
        draw = ImageDraw.Draw(img)
        
        fontSize = 42

        x = 20
        y = 10

        wordCount = 100

        mywords = []
        
        for i in range(wordCount):
            mywords.append(getRandomWord())

        if sort:
            mywords.sort(key=str.lower)
            
        altePath = fontPath + "AlteHaasGroteskBold.ttf"

        fontPath = getFont()
        fon = ImageFont.truetype(fontPath, fontSize)

        h = 0
        s = 1
        v = 1

        i = 0
        while y < img.size[1] and h < 1 and i < len(mywords):            
            word = mywords[i]

            r, g, b = colorsys.hsv_to_rgb(h, s, v)        
            c = (int(r*255), int(g*255), int(b*255))
            
            draw.text((x, y), word, font=fon, fill=c)

            y += fontSize + 5

            h += 0.01
            i += 1

        img = img.crop((0, 0, img.size[0], y + 25))
        l = img.load()
        img = img.convert("RGBA")
            
    except Exception as e:
        img = writeImageException(e)

    return img

def longWordList():
    img = longWordListBase(sort=False)
    return img

def longWordList_Sorted():
    img = longWordListBase(sort=True)
    return img

def listFonts(sort=False):
    img = ""

    try:
        width = 1200
        height = 100000
        
        img = Image.new("RGBA", (width, height), "#FFFFFF")
        
        draw = ImageDraw.Draw(img)
        
        fontSize = 25

        y = 10
        
        getFont()

        basePath = fontPath

        global possibleFonts
        global fontBlacklist
        global fontPathSansSerif
                        
        fon = ImageFont.truetype(fontPathSansSerif, fontSize)

        sampleString = "AaBbCcDdEeFfGgHhIiJj  "
        
        for f in possibleFonts:
            x = 20
            try:
                loadedFont = ImageFont.truetype(f, fontSize)
            except:
                continue
            
            fontFile = f.rfind("/")

            c = (0, 0, 0)
            word = " - " + loadedFont.getname()[0] + " (" + f[fontFile+1:] + ")"

            try:
                sampleSize = loadedFont.getsize(sampleString)

                draw.text((x, y), sampleString, font=loadedFont, fill=c)
                x += sampleSize[0] + 2
            except:
                x = 20            

            blacklisted = False
            for b in fontBlacklist:
                if b in f:
                    blacklisted = True

            if blacklisted:
                word += " (BLACKLISTED)"
                
            draw.text((x, y), word, font=fon, fill=c)

            y += fontSize + 5
            
        img = img.crop((0, 0, img.size[0], y + 20))
        l = img.load()
        img = img.convert("RGBA")
            
    except Exception as e:
        img = writeImageException(e)

    return img

def muchoLetters():
    img = ""
    
    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()
        
        img = Image.new("RGBA", (width, height), "#FFFFFF")        
        draw = ImageDraw.Draw(img)

        fontPath = getFont()
        
        pixdata = img.load()

        letter_count = random.randint(500, 1000)
        choices = getInputPalette(paletteLength=letter_count)

        c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        global maxFloodFillArg
        floodfill(img, (0, 0), targetcolour = pixdata[0, 0],
                          newcolour = c,
                          randomIt = random.randint(0, maxFloodFillArg),
                          choices = choices)

        for i in range(letter_count):
            fontSize = random.randint(10, 128)
            strokeSize = random.randint(2, 5)
            
            x = random.randint(-50, img.size[0])
            y = random.randint(-50, img.size[1])

            fon = ImageFont.truetype(fontPath, fontSize)
            
            word = random.choice(string.ascii_letters)
            #c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            #cStroke = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            c = random.choice(choices)
            cStroke = getInverse(c)
            
            textStrokeExtra(draw, x, y, word, fon, cStroke, strokeSize)
            draw.text((x, y), word, font=fon, fill=c)            
            
    except Exception as e:
        img = writeImageException(e)

    return img

def typewriterStuff():
    try:
        width = 800
        height = 800
        fontSize = 48
        
        img = Image.new("RGBA", (width, height), "#DEDEDE")        
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        basePath = fontPath
        fontPath = basePath + "veteran typewriter.ttf"

        fon = ImageFont.truetype(fontPath, fontSize)

        x = 20
        y = 15

        cStroke = (0, 0, 0)

        h = 0
        s = 0
        vStart = 150
        v = vStart

        iCount = 15

        choices = []

        for i in range(iCount):
            cup = random.randint(200, 255)
            cupc = (cup, cup, cup)
            choices.append(cupc)

        floodfill(img, (0, 0), targetcolour = pixdata[0, 0],
                  newcolour = (0,0,0),
                  randomIt = 1,
                  choices = choices)
        
        for i in range(iCount):
            word = getRandomWord() + " " + getRandomWord()

            r, g, b = colorsys.hsv_to_rgb(h, s, v)        
            c = (int(r), int(g), int(b))
            
            textStrokeExtra(draw, x, y, word, fon, cStroke, 2)
            draw.text((x, y), word, font=fon, fill=c)

            y += fontSize + 2
            v += int((255.0 - vStart) // iCount)            
            
        img = img.filter(ImageFilter.GaussianBlur(1))
        
    except Exception as e:
        img = writeImageException(e)

    return img

def gradientSquares():
    img = ""

    try:
        choices = getPaletteGenerated() 

        img = Image.new("RGBA", (1200, 1024), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()        

        jSize = 50

        sizes = []
        i = random.randint(3, 7) * jSize
        
        sizes.append(i)

        j = i
        
        while j > jSize:
            j -= jSize

            if j >= jSize:
                sizes.append(j)
        
        for squareSize in sizes:
            for x in range(0, img.size[0], squareSize):
                for y in range(0, img.size[1], squareSize):
                    if sizes[0] == squareSize or random.randint(1, 5) < 3:
                        innerColor = random.choice(choices)
                        outerColor = random.choice(choices)

                        while innerColor == outerColor:
                            outerColor = random.choice(choices)
                    
                        x2 = x + squareSize
                        y2 = y + squareSize

                        if x2 > img.size[0]:
                            x2 = img.size[0]

                        if y2 > img.size[1]:
                            y2 = img.size[1]
                            
                        img = gradientFill(img, innerColor=innerColor, outerColor=outerColor, x1=x, y1=y, x2=x2, y2=y2)

    except Exception as e:
        img = writeImageException(e)   

    return img

def processPalette(palette):
    arr_palette = []
    
    if palette != "":
        try:
            intpal = int(palette)
            arr_palette = getPaletteSpecific(intpal)
        except ValueError:
            arr_palette = getPaletteGenerated()

    return arr_palette

def getInputPalette(paletteLength=7, generate=True):
    global input_palette

    if input_palette != "" and input_palette != []:
        choices = input_palette
    else:         
        if generate:
            choices = getPaletteGenerated(paletteLength=paletteLength)
        else:
            choices = getPalette() # from directory

    return choices

def getPaletteSpecific(palette):
    global rootLogger

    if isinstance(palette, str) and str != "":
        try:
            palette = int(palette)
        except:
            palette = 0

    choices = []

    random.seed()

    colorPrint.print_custom_palette(191, f"palette: {palette}")
    
    if palette == 1 or palette == 101:
        # V_A_P_O_R_W_A_V_E______________________ONE
        hexchoices = ["#00f9ff","#c36fbf","#6cffa2","#fff400","#ff00ce"]

        for c in hexchoices:
            c1 = hex_to_rgb(c)
            choices.append(c1)

            if palette == 101:
                c2 = getColorComplement(c1)
                choices.append(c2)
    elif palette == 2 or palette == 102:
        # primary
        global primaryColors
        choices = primaryColors.copy()

        if palette == 102:
            choices = addOppositeColors(choices)
    elif palette == 3 or palette == 103:
        # wacky
        global wackyColors
        choices = wackyColors.copy()

        if palette == 103:
            choices = [(128,128,0),(0,128,0),(128,0,128),(0,128,128),(0,0,128),(128,0,0)]
    elif palette == 4 or palette == 104:
        # coco
        global cocoColors

        for c in cocoColors:
            c1 = hex_to_rgb(c)
            choices.append(c1)

            if palette == 104:
                c2 = getColorComplement(c1)
                choices.append(c2)            
    elif palette == 5 or palette == 105:
        # atari
        global atariColors

        for c in atariColors:
            c1 = hex_to_rgb(c)
            choices.append(c1)

        if palette == 105:
            for c1 in choices.copy():
                c2 = getColorComplement(c1)
                choices.append(c2)
    elif palette == 6 or palette == 106:
        hexc = ["#e3fb68","#c1ee73","#52a3ba","#344d78","#27292b"]

        for c in hexc:
            choices.append(hex_to_rgb(c))

        if palette == 106:
            cy = []
            for c in choices:
                cx = getInverse(c)
                cy.append(cx)

            for c in cy:
                choices.append(c)
    elif palette == 7:
        hexc = ["#ff0000","#310000","#ef0000","#ff9999","#faf999"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 8:
        hexc = ["#000000","#FF0000","#fcc10f","#68068c","#0e30c7"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 9 or palette == 109:
        hexc = ["#000000","#FF0000","#FFFFFF","#FFFF00"]

        for c in hexc:
            c1 = hex_to_rgb(c)
            choices.append(c1)

            if palette == 109:
                c2 = getColorComplement(c1)
                choices.append(c2)
    elif palette == 10:
        hexc = ["#010101","#031b75","#108c00","#17bbd3","#720c0a","#6c1c9e","#b25116","#b8b0a8","#4a4842","#0b63c4","#9bce00","#73f5d5","#e89e00","#ff7bdb","#fef255","#fffffe"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 11:
        hexc = ["#000000","#ff55ff","#55ffff","#ffffff"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 12:
        hexc = ["#000000","#55ff55","#ff5555","#ffff55"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 13:
        choices.append((0,0,0))

        for ipfreely in range(4, 255, 4):
            choices.append((ipfreely, 0, 0))
    elif palette == 14:
        hexc = ["#000000","#1D2B53","#7E2553","#008751","#AB5236","#5F574F","#C2C3C7","#FFF1E8","#FF004D","#FFA300","#FFEC27","#00E436","#29ADFF","#83769C","#FF77A8","#FFCCAA"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 15:
        hexc = ["#332c50","#46878f","#94e344","#e2f3e4"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 16:
        hexc = ["#ffffff","#fb6b1d","#e83b3b","#831c5d","#c32454","#f04f78","#f68181","#fca790","#1ebc73","#91db69","#fbff86","#cd683d","#9e4539","#7a3045","#6b3e75","#905ea9","#a884f3","#FF0000"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 17:
        hexc = ["#ff0546","#9c173b","#660f31","#450327","#270022","#17001d","#09010d","#0ce6f2","#0098db","#1e579c"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 18:
        hexc = ["#ff7b23","#474eff","#010afb","#ffaf47","#f48b01","#fd9206","#0a0a0a","#ffffff"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 19:
        hexc = ["#CCF1FF", "#E0D7FF", "#FFCCE1", "#D7EEFF", "#FAFFC7", "#E0BBE4", "#957DAD", "#D291BC", "#FEC8D8", "#FFDFD3"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 20:
        hexc = ["#FF0000", "#FF6600", "#FFFF00", "#00FF00", "#0000FF", "#000066", "#990099"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 21:
        h = random.random()

        for s in [.2, .4, .6, .8, 1]:
            v = random.random()
            r, g, b = colorsys.hsv_to_rgb(h, s, s)
            c = (int(r*255), int(g*255), int(b*255))

            choices.append(c)
    elif palette == 22:
        for s in [.2, .4, .6, .8, 1]:
            h = random.random()
            v = random.random()
            r, g, b = colorsys.hsv_to_rgb(h, s, 1)
            c = (int(r*255), int(g*255), int(b*255))

            choices.append(c)
    elif palette == 23:
        hexc = ["#000000","#ff55ff","#55ffff","#ffffff", "#55ff55","#ff5555","#ffff55"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 24:
        hexc = ["#000000","#55ff55","#88ff88","#ff5555","#ff8888","#ffff55","#ffff88"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 25:
        hexc = ["#85daeb","#5fc9e7","#5fa1e7","#5f6ee7","#4c60aa","#444774","#32313b","#463c5e","#5d4776","#855395","#ab58a8","#ca60ae","#f3a787","#f5daa7","#8dd894","#5dc190","#4ab9a3","#4593a5","#5efdf7","#ff5dcc","#fdfe89","#ffffff"]

        for c in hexc:
            choices.append(hex_to_rgb(c))    
    elif palette == 26:
        hexc = ["#FF0000", "#00FF00", "#FFFF00", "#0000FF"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 27:
        hexc = ["#000000","#fcfcfc","#f8f8f8","#bcbcbc","#7c7c7c","#a4e4fc","#3cbcfc","#0078f8","#0000fc","#b8b8f8","#6888fc","#0058f8","#0000bc","#d8b8f8","#9878f8","#6844fc","#4428bc","#f8b8f8","#f878f8","#d800cc","#940084","#f8a4c0","#f85898","#e40058","#a80020","#f0d0b0","f87858","#f83800","#a81000","#fce0a8","#fca044","#e45c10","#881400","#f8d878","#f8b800","#ac7c00","#503000","#d8f878","#b8f818","#00b800","#007800","#b8f8b8","#58d854","#00a800","#006800","#b8f8d8","#58f898","#00a844","#005800","#00fcfc","#00e8d8","#008888","#000458","#f8d8f8","#787878"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 28:
        choices.append((0,0,0))

        for ipfreely in range(4, 255, 4):
            choices.append((0, ipfreely, 0))
    elif palette == 29:
        choices.append((0,0,0))

        for ipfreely in range(4, 255, 4):
            choices.append((0, 0, ipfreely))
    elif palette == 30:
        choices.append((0,0,0))

        for ipfreely in range(4, 255, 32):
            c = (ipfreely//3,ipfreely//3,ipfreely//3)
            z = random.randint(0,2)            
            c = replace_at_index(c, z, ipfreely)

            z = random.randint(0,2)            
            c = replace_at_index(c, z, ipfreely)

            if c not in choices:
                choices.append(c)
    elif palette == 31:
        hexc = ["#FF6C11","#FF3864","#2DE236","#261447","#0D0221","#023788","#650D89","#920075","#F6019D","#D40078","#241743","#2E2157","#FD3777","#F706CF","#FD1D53","#F9C80E","#FF4365","#540D6E","#791E94","#541388"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 32:
        hexc = ["#ffd319", "#ff901f", "#ff2975", "#f222ff", "#8c1eff"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 33:
        hexc = ["#4b3832","#854442","#fff4e6","#3c2f2f","#be9b7b"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 34:
        hexc = ["#338833","#1da27c","#30105a","#fbe82d","#510e0e","#632812","#0c4540"]
        
        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 35:
        hexc = ["#9A52FF","#FF5500","#980000","#FFE100","#63FFFC"]
        
        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 36:
        hexc = ["#3498DB", "#2E3E70", "#1A1D23", "#3495B7", "#5C6BC0"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 37:
        hexc = ["#99dd99","#dd99dd", "#9999dd", "#dd9999","#dddd99","#99dddd"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 38:
        hexc = ["#99ff99","#ff99ff", "#9999ff", "#ff9999","#ffff99","#99ffff"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 39:
        hexc = ["#ddff99","#f55df5", "#65faff", "#ffdd99","#f0f09d","#ddffff"]

        for c in hexc:
            choices.append(hex_to_rgb(c))  
    elif palette == 40:
        hexc = ["#ff1b1b","#bc99dd","#0000ff","#00d21f","#ffffff","#ffff00"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 41:
        hexc = ["#dd9999","#ffdd99","#ff9999","#1C1919","#d49292"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 42:
        hexc = ["#00446f", "#6e2774", "#205061", "#6e6963", "#22aa22"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 43:
        hexc = ["#001f26","#003f4d","#33bdbd","#99e5e5", "#ce4993","#ff0000","#FFD700"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 44:
        hexc = ["#001f26","#b91010", "#003f4d", "#887788", "#9E16C4", "#3E3210"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 45:
        hexc = ["#b91010", "#c8ff00", "#366E36", "#042A02", "#FF7300"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 46:
        hexc = [ "#9E16C4", "#3300aa", "#f9d79f", "#ff4395", "#0099ff"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 47:
        hexc = ["#FFD700", "#c8b400", "#006400", "#3CB371"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 48:
        hexc = ["#ff00c1","#9600ff","#4900ff","#00b8ff","#00fff9"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 49:
        hexc = ["#fbbbad","#ee8695","#4a7a96","#333f58","#292831"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 50:
        hexc = ["#eeaf61","#fb9062","#ee5d6c","#ce4993","#6a0d83"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 51:
        hexc = ["#000000","#1a0a00","#331400","#662800","#994d00","#cc7700","#ff9900","#ffbb33","#ffcc66"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 52:
        hexc = ["#000000","#1e004f","#3b00a6","#6f00cc","#b000a6","#e6005c","#ff3300","#ff6600","#ffcc00","#ffff66","#ffffff"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 53:
        hexc = ["#0b1a0f","#1f3d1a","#335c26","#4d7f33","#6ba64d","#99c27a","#c2d9aa","#8c6239","#5c3b1e","#332011"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 54:
        hexc = ["#001f26","#003f4d","#005c66","#007a80","#009999","#33bdbd","#66d1d1","#99e5e5","#cceeee","#e6ffff"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 55:
        hexc = ["#ffffff","#000000","#e41a1c","#377eb8","#4daf4a","#984ea3","#ff7f00","#ffff33"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 56:  # Corporate '90s
        hexc = [
            "#0f2a4e",  # navy binder
            "#1e4e79",  # powerpoint blue
            "#0f6a6a",  # office teal
            "#2f6b3c",  # forest green
            "#7a1e3a",  # boardroom maroon
            "#c49a00",  # mustard accent
            "#8e7a66",  # taupe cubicle
            "#e7d8c9",  # beige paper
            "#b0b7c3",  # slate toolbar
            "#707c8a",  # mouse gray
            "#3b2f2a",  # walnut veneer
            "#ffffff",  # white
            "#000000"   # black
        ]
        for c in hexc:
            choices.append(hex_to_rgb(c))

    elif palette == 57:  # Cyberpunk Alley
        hexc = [
            "#0a0c10",  # wet asphalt
            "#200028",  # back-alley violet
            "#002b36",  # oily teal-black
            "#004d59",  # neon shadow teal
            "#2a7fff",  # electric blue signage
            "#00f7ff",  # cyan tube
            "#7cff00",  # acid green leak
            "#ffb000",  # sodium amber
            "#ff6a00",  # rust orange neon
            "#ff264a",  # signage red
            "#ff2bd6",  # hot magenta
            "#f2f2f2"   # glare/overexposed
        ]
        for c in hexc:
            choices.append(hex_to_rgb(c))

    elif palette == 58:  # Solarized Variant (classic set)
        hexc = [
            "#002b36",  # base03
            "#073642",  # base02
            "#586e75",  # base01
            "#657b83",  # base00
            "#839496",  # base0
            "#93a1a1",  # base1
            "#eee8d5",  # base2
            "#fdf6e3",  # base3
            "#b58900",  # yellow
            "#cb4b16",  # orange
            "#dc322f",  # red
            "#d33682",  # magenta
            "#6c71c4",  # violet
            "#268bd2",  # blue
            "#2aa198",  # cyan
            "#859900"   # green
        ]
        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 59:
        hexc = [
            "#29abe2",  # bright teal / turquoise
            "#93278f",  # bold purple stroke
            "#f2f2f2",  # paper cup white
            "#0d3b66",  # dark navy accent
            "#ff66cc",  # neon pink highlight (optional exaggeration for vaporwave feel)
        ]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 60:
        hexc = [
            "#3b9c9c",  # teal base
            "#264653",  # dark navy lines
            "#6a4c93",  # purple accents
            "#e63946",  # red dots
        ]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 61:
        hexc = [
            "#000000",  # black base
            "#ff00ff",  # neon pink
            "#00ffff",  # neon cyan
            "#39ff14",  # neon green
            "#ffea00",  # neon yellow
            "#8000ff",  # neon purple
        ]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 62:
        hexc = [
            "#ff66cc",  # hot pink
            "#00ccff",  # bright turquoise
            "#9933ff",  # electric purple
            "#66ff66",  # neon green
            "#ffff66",  # pastel yellow highlight
            "#ffffff",  # white accents
        ]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 63:
        hexc = [    "#000000",    "#0000d8",    "#0000ff",    "#d80000",    "#ff0000",    "#d800d8",    "#ff00ff",    "#00d800",    "#00ff00",    "#00d8d8",    "#00ffff",    "#d8d800",    "#ffff00",    "#d8d8d8",    "#ffffff"]
        
        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 64:
        hexc = ["#000000","#626262","#898989","#adadad","#ffffff","#9f4e44","#cb7e75","#6d5412","#a1683c","#c9d487","#9ae29b","#5cab5e","#6abfc6","#887ecb","#50459b","#a057a3"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 65:  # Desert Sun
        hexc = [
            "#e6c27a",  # warm sand
            "#d98e04",  # ochre
            "#c1440e",  # rust red
            "#732c02",  # deep clay
            "#87a6c1"   # washed-out sky blue
        ]
        for c in hexc:
            choices.append(hex_to_rgb(c))

    elif palette == 66:  # Tropical Fruit
        hexc = [
            "#ffe135",  # banana yellow
            "#ff6f61",  # guava pink
            "#ff9f1c",  # papaya orange
            "#2ec4b6",  # teal/palm leaf
            "#6ee16e"   # lime green
        ]
        for c in hexc:
            choices.append(hex_to_rgb(c))

    elif palette == 67:  # Glitchwave
        hexc = [
            "#ff00ff",  # harsh magenta
            "#00ffff",  # neon cyan
            "#00ff00",  # toxic green
            "#000000",  # deep black
            "#aaaaaa"   # static gray
        ]
        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 68:
        choices.append((0,0,255))

        for ipfreely in range(4, 255, 4):
            choices.append((ipfreely, ipfreely, 255))
    elif palette == 69:
        choices.append((0,255,255))

        for ipfreely in range(4, 255, 4):
            choices.append((ipfreely, 255, 255))
    elif palette == 70:
        for ipfreely in range(4, 255, 4):
            choices.append((0, ipfreely, ipfreely))

        choices.append((0,255,255))
    elif palette == 71:
        hexc = [
            "#000000",  # black background
            "#001a00",  # very dark green
            "#003300",  # dark green
            "#006600",  # medium-dark green
            "#00994d",  # green with slight phosphor glow
            "#00cc77",  # brighter green
            "#00ff00",  # classic bright green
            "#33ff99",  # green glow highlight
            "#66ffcc"   # pale green/teal highlight
        ]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 72:  # Blue CRT
        hexc = ["#000000","#001a0a","#00331a","#004d33","#00664d","#008066","#339999","#66b2b2","#99cccc"]
        for c in hexc:
            choices.append(hex_to_rgb(c))

    elif palette == 73:  # Rust and Patina
        hexc = ["#2f1b0c","#5e2d15","#8c3f1d","#b85a28","#d98c4d","#35524a","#4f7c72","#6fa69a","#9cc9b8"]
        for c in hexc:
            choices.append(hex_to_rgb(c))

    elif palette == 74:  # Memphis Design
        hexc = ["#ff6f61","#6b5b95","#88b04b","#f7cac9","#92a8d1","#ffde59","#ffb347","#ff77ff","#40e0d0"]
        for c in hexc:
            choices.append(hex_to_rgb(c))

    elif palette == 75:  # Corporate 2000s
        hexc = ["#003366","#336699","#6699cc","#99ccff","#cce6ff","#e6e6e6","#cccccc","#999999","#333333"]
        for c in hexc:
            choices.append(hex_to_rgb(c))

    elif palette == 76:  # Neon Tubes
        hexc = ["#ff00ff","#00ffff","#39ff14","#ff3131","#ffff33","#ff6ec7","#00ffcc","#ff9a00","#ff0055"]
        for c in hexc:
            choices.append(hex_to_rgb(c))

    elif palette == 77:  # Plastic Toys
        hexc = ["#ff0000","#0000ff","#ffff00","#00ff00","#ff7f00","#ff00ff","#00ffff","#ff3399","#9933ff"]
        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 78: 
        hexc = ["#ED0A3F","#FF8833","#FBE870","#01A368","#0066FF","#8359A3","#AF593E","#000000"]
        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 79:
        hexc = ["#FFFFFF","#FDD5B1","#FFCBA4","#FA9D5A","#E97451","#9E5B40","#CA3435","#000000"]
        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 80:
        hexc = [
            "#263A79","#ED0A3F","#FF8833","#FBE870","#01A368","#0066FF","#8359A3","#AF593E","#000000",
            "#FF3F34","#FFAE42","#C5E17A","#0095B7","#6456B7","#BB3385","#FFA6C9","#FFFFFF","#FD0E35",
            "#C62D42","#CA3435","#B94E48","#FE6F5E","#FF7034","#FFB97B","#FCD667","#F1E788","#B5B35C",
            "#ECEBBD","#7BA05B","#9DE093","#5FA777","#93DFB8","#00CCCC","#6CDAE7","#76D7EA","#009DC4",
            "#02A4D3","#93CCEA","#A9B2C3","#C3CDE6","#4F69C6","#8071B4","#C9A0DC","#E29CD2","#843179",
            "#F653A6","#FF3399","#FBAED2","#F7468A","#FC80A5","#F091A9","#FF91A4","#FEBAAD","#E97451",
            "#9E5B40","#D27D46","#DEA681","#FA9D5A","#FFCBA4","#FDD5B1","#E6BE8A","#C9C0BB","#8B8680",
            "#D9D6CF"
        ]

        for c in hexc:
            choices.append(hex_to_rgb(c))
            
    elif palette == 81:  # Pastel Goth
        hexc = ["#b28ccf","#a0c4ff","#ffafcc","#cdb4db","#000000","#444444","#777777"]
        for c in hexc:
            choices.append(hex_to_rgb(c))

    elif palette == 82:  # Modern SaaS (Corporate Pastel)
        hexc = ["#e0f7fa","#80deea","#4dd0e1","#00acc1","#7e57c2","#f8bbd0","#263238"]
        for c in hexc:
            choices.append(hex_to_rgb(c))

    elif palette == 83:  # Aurora Borealis
        hexc = ["#0b3d91","#0d1b2a","#1b4332","#00ffb3","#5efc8d","#8a2be2","#000000"]
        for c in hexc:
            choices.append(hex_to_rgb(c))

    elif palette == 84:  # Renaissance Fresco
        hexc = ["#a37c40","#c9a66b","#6d8b99","#bfb9a3","#ede3d0","#8c5a3c","#4a403a"]
        for c in hexc:
            choices.append(hex_to_rgb(c))

    elif palette == 85:  # Japanese Woodblock
        hexc = ["#0f4c81","#b22222","#f5deb3","#2e8b57","#000000","#c0c0c0","#ffffff"]
        for c in hexc:
            choices.append(hex_to_rgb(c))

    elif palette == 86:  # Pop Art (CMYK style)
        hexc = ["#00bfff","#ff00ff","#ffff00","#000000","#ffffff","#ff4500","#32cd32"]
        for c in hexc:
            choices.append(hex_to_rgb(c))

    elif palette == 87:  # MOS6502 Woodgrain
        hexc = ["#2c1b0f","#8b5a2b","#cdaa7d","#f4a460","#ffd700","#000000","#556b2f"]
        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 88:  # Toxic Earth
        hexc = ['#361313', '#a9593d', '#ff5c5c', '#d3ea54', '#c7ff5c']
        for c in hexc:
            choices.append(hex_to_rgb(c))

    elif palette == 89:  # Alice in Wonderland
        hexc = ['#f4ed46', '#b4f2ff', '#5ce1f4', '#ffffff', '#ffeaca']
        for c in hexc:
            choices.append(hex_to_rgb(c))

    elif palette == 90:  # Bird Cry
        hexc = ['#7abac7', '#89cedd', '#9afffc', '#fcceff', '#eeb0ff']
        for c in hexc:
            choices.append(hex_to_rgb(c))

    elif palette == 91:  # Cotton Candy Rainbow
        hexc = ['#fbc0c0', '#ffdaa1', '#f9ffc9', '#baffe5', '#a9cdff']
        for c in hexc:
            choices.append(hex_to_rgb(c))

    elif palette == 92:  # Ice Cream
        hexc = ['#6b3e26', '#ffc5d9', '#c2f2d0', '#fdf5c9', '#ffcb85']
        for c in hexc:
            choices.append(hex_to_rgb(c))

    elif palette == 93:  # Loud Amplifiers
        hexc = ['#ff0000', '#ffa700', '#fff400', '#009fff', '#0011ff']
        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 94:
        hexc = ['#52c7ad', '#47dfd3', '#b46464', '#695b5b', '#f0caa4']
        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 95:
        hexc = ['#2175d9', '#00308f', '#e30074', '#b8d000', '#ff9900']
        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 100:
        hexc = ["#e88325","#ff9029","#ff9c3f","#062800","#066f00"]
        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 98:
        choices = getPalette()        
    elif palette == 99:
        global input_palette
        input_palette = []
        choices = getPaletteGenerated(rgb = (0,0,0), paletteLength = random.randint(3, 8))
    elif palette == 96:
        # _color_target_check(pnt, targ, 25)

        c1 = getRandomColorRGB()
        c2 = getRandomColorRGB()

        c3 = getColorComplement(c1)
        c4 = getColorComplement(c2)

        choices = [c1, c2, c3, c4]
    elif palette == 97:
        # _color_target_check(pnt, targ, 25)

        c1 = getRandomColorRGB()
        c2 = getRandomColorRGB()
        c3 = getRandomColorRGB()

        c4 = getColorComplement(c1)
        c5 = getColorComplement(c2)
        c6 = getColorComplement(c3)

        choices = [c1, c2, c3, c4, c5, c6]
    elif palette == 126:
        hexc = ["#FF0000", "#00FF00", "#FFFF00", "#0000FF", "#ac4313", "#ff00ff", "#00ffff"]

        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 226:
        hexc = ["#FF0000", "#00FF00", "#FFFF00", "#0000FF", "#ac4313", "#ff00ff", "#00ffff"]

        for c in hexc:
            z = hex_to_rgb(c)
            choices.append(z)
            zc = getColorComplement(z)
            choices.append(zc)
    elif palette == 300:
        hexc = ["#003049","#d62828","#f77f00","#fcbf49","#eae2b7"]
        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette == 301:
        hexc = ["#6f1d1b","#bb9457","#432818","#99582a","#ffe6a7"]
        for c in hexc:
            choices.append(hex_to_rgb(c))
    elif palette > 100 and palette < 5000:
        pParent = palette - 100
        choices = getPaletteSpecific(pParent)

        c2 = []

        for c in choices:
            zc = getColorComplement(c)
            c2.append(zc)

        for c in c2:
            choices.append(c)
    else:
        input_palette = []
        return getPaletteGenerated()

    seen = {}
    choices = [seen.setdefault(x, x) for x in choices if x not in seen]

    return choices

def addOppositeColors(choices):
    colorPrint.print_warn('addOppositeColors: ' + str(choices))

    d = []

    for c in choices:
        colorPrint.print_warn('c: ' + str(c))
        c2 = getColorComplement(c)
        d.append(c2)

    for doice in d:
        choices.append(doice)

    return choices

def getPaletteGenerated(rgb=(0,0,0), paletteLength=5, bgColor=None, minContrast=3):
    if rgb == (0,0,0):
        rgb = (0,0,0)

    if paletteLength==5:
        paletteLength=5

    global input_palette
    palette = []

    if len(input_palette) == 0 or input_palette == "":
        # generate a palette
        if rgb == (0,0,0):
            c = getRandomColor()
        else:
            c = rgb

        hsv = colorsys.rgb_to_hsv(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)

        while len(palette) < paletteLength:
            for hsvX in [0, 2]:
                if hsvX == 2:
                    ru = random.uniform(0.3, 0.8)
                else:
                    ru = random.uniform(0.1, 0.2)
                    
                replacement = hsv[hsvX] + (ru * random.choice([-1,1]))

                if replacement > 1:
                    replacement = 1

                if replacement < 0:
                    replacement = 0
                    
                hsv = replace_at_index(hsv, hsvX, replacement)
            
            p = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])

            p = (int(p[0] * 255.0), int(p[1] * 255.0), int(p[2] * 255.0))

            skipThisOne = False

            if bgColor != None and minContrast > 0:
                ccr = calcContrastRatio(bgColor, p)

                if ccr < minContrast:
                    skipThisOne = True

            if p not in palette and not skipThisOne:
                palette.append(p)
    else:
        # use the one that was specified elsewhere
        palette = input_palette
        
    palette = sort_by_lum(palette)

    return palette

def generatePalette(palette=[], w=900, h=600):
    img = ""
    
    try:
        img = Image.new("RGBA", (w, h), "#FFFFFF")
        draw = ImageDraw.Draw(img)

        if len(palette) == 0:
            palette = getPaletteGenerated()
        
        pstep = int(w // (len(palette) * 1.0))

        x = 0
        for p in palette:
            draw.rectangle((x, 0, x + pstep, img.size[1]), fill=p)

            x += pstep + 1        
        
    except Exception as e:
        img = writeImageException(e)   

    return img

def paletteSquares():
    img = ""

    try:
        choices = getPalette() 

        img = Image.new("RGBA", (800, 600), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()        

        sizes = [50]

        iDirection = random.choice([0, 1, 2])
        
        for squareSize in sizes:
            for x in range(0, img.size[0], squareSize):
                for y in range(0, img.size[1], squareSize):
                    if sizes[0] == squareSize or random.randint(1, 5) < 3:
                        palette = getPaletteGenerated()

                        yw = int(squareSize // (len(palette) * 1.0))
                        
                        x2 = x + squareSize
                        y2 = y + squareSize

                        if x2 > img.size[0]:
                            x2 = img.size[0]

                        if y2 > img.size[1]:
                            y2 = img.size[1]

                        ystep = y
                        xstep = x
                        
                        for p in palette:
                            thisChoice = random.randint(0, 1)
                            
                            if iDirection in (0, 2):
                                draw.rectangle((x, ystep, x2, ystep + yw), p)
                                
                            if iDirection == 1 or (iDirection == 2 and thisChoice == 1):
                                draw.rectangle((xstep, y, xstep + yw, y2), p)
                                    
                            ystep += yw + 1
                            xstep += yw + 1
                            
    except Exception as e:
        img = writeImageException(e)   

    return img



    secSize = 30
    
    for y in range(0, img.size[1]):
        #section0 = section + random.randint(-y/2, y/2)
        #section1 = (section * 2) + random.randint(-y/2, y/2)

        section0 = section + random.randint(secSize * -1, secSize)
        section1 = 2 * section + random.randint(secSize * -1, secSize)
        
        for x in range(0, img.size[0]):
            if x < section0:
                i = i1
            elif x < section1:
                i = i2
            else:
                i = i3
                
            c = pixdata[x,y]
            xxxxx = c[i]+random.randint(10, 22)

            if xxxxx > 255:
                xxxxx = 255
                
            c = replace_at_index(c, i, xxxxx)
            pixdata[x,y] = c

    img = img.resize((int(width * .7), int(height * .7)), Image.LANCZOS)
    
    return img

def pieslice():
    width = 800
    height = 800
    
    img = Image.new("RGBA", (width,height), "#000000")
    draw = ImageDraw.Draw(img)
    pixdata = img.load()

    pieWidth = 800
    pieHeight = 800

    #boxes = [(0,0,400,400),
    #         (400,0,800,400),
    #         (0,400,400,800),
    #         (400,400,800,800)]

    boxes = [(0,0,800,800)]

    angles = []
    colors = []
    
    for y in range(0, len(boxes)):
        for x in range(0, random.randint(200,600), 5):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            
            startAngle = random.randint(0, 360)
            endAngle = random.randint(0, 360)

            color = (r,g,b)
            angle = (startAngle, endAngle, x)

            colors.append(color)
            angles.append(angle)

    i = 0
    y = 0
    for a in angles:       
        color = colors[i]
        startAngle = a[0]
        endAngle = a[1]
        x = a[2]
        
        boundingBox = (boxes[y][0]+x, boxes[y][1]+x, boxes[y][2]-x, boxes[y][3]-x)
        draw.pieslice(boundingBox, startAngle, endAngle, fill=color, outline=(0,0,0))

        if i % 2 == 0:
            floodRan = False

            for yy in range(boxes[y][1]+1, boxes[y][3]):
                if not floodRan:
                    for xx in range(boxes[y][0]+1, boxes[y][2]):
                        if not floodRan and pixdata[xx,yy][0:3] == (r,g,b):            
                            floodfill(img, (xx, yy), targetcolour = pixdata[xx,yy],
                              newcolour = (0,0,0),
                              randomIt = 12)

                            floodRan = True
                            break

        draw = ImageDraw.Draw(img)
        i += 1

    return img

def insertFoured(imgpath=""):
    if imgpath == "":
        imgpath = getInsert("", publicDomainImagePath)
        
    img = Image.open(imgpath)

    try:
        mirror1 = img.transpose(Image.FLIP_LEFT_RIGHT)
        rot1 = img.rotate(180)
        mirror2 = mirror1.rotate(180)
        
        blendAmount = .50
        
        img = Image.blend(img, rot1, blendAmount)
        mirror = Image.blend(mirror1, mirror2, blendAmount)
        
        img = Image.blend(img, mirror, blendAmount)
    except Exception as e:        
        img = writeImageException(e)       

    return img

def insertStreaksPublic():
    try:
        ins = getInsertById(getParam(4))
        img = insertStreaks(ins, maxIterations=100, pointCount=10)
    except Exception as e:
        img = writeImageException(e)
        
    return img

def grid_18():
    width = 1024
    height = 1024

    img = ""
    
    try:
        i = random.randint(50, 75)
        c = (i, i, i)
        
        img = Image.new("RGBA", (width,height), c)
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        for y in range(0, img.size[1]-1, 25):
            draw.line((0, y, img.size[0], y), "black")

        for x in range(0, img.size[0]-1, 25):
            draw.line((x, 0, x, img.size[1]), "black")

        y = img.size[1]-1
        x = img.size[0]-1
        
        draw.line((0, y, img.size[0], y), "black")
        draw.line((x, 0, x, img.size[1]), "black")

        for y in range(5, img.size[1]-1, 25):
            for x in range(5, img.size[0]-1, 25):
                iAlg = random.randint(18, 19)
                
                floodfill(img, (x, y),
                          targetcolour = pixdata[x,y],
                          newcolour = (0,0,0,255),
                          randomIt = iAlg,
                          maxStackDepth = 0)
    except Exception as e:
        img = writeImageException(e)

    return img

def nightgridStars():
    img = nightgrid()

    try:
        
        w = img.size[0]
        h = img.size[1]
        
        points = []

        for i in range(75):
            (x, y) = (random.randint(0, w), random.randint(0, h))
            points.append((x,y))
            
        pixdata = img.load()

        pointCount = 0
        for p in points:
            (x, y) = (p[0], p[1])
            
            r = random.randint(50, 200)
            r2 = random.randint(r - 20, r + 20)

            alpha = random.randint(0, 255)
            
            if random.randint(0, 1) == 0:
                c = (r, r2, 0, alpha)
            else:
                c = (r2, r, 0, alpha)    

            ccc = random.randint(0, 2)

            if ccc == 0:
                c = (random.randint(180, 240), c[0], c[1], alpha)
            elif ccc == 1:
                c = (c[0], c[1], random.randint(180, 240), alpha)
            else:
                c = (c[0], random.randint(180, 240), c[1], alpha)
            
            try:
                pixdata[x, y] = c
            except:
                pass

            k = 1

            # vary the star size based on which loop this is
            jCount = 2

            if pointCount > 35:
                jCount = 3

            if pointCount > 45:
                jCount = 4
                
            diagOn = 0
            if random.randint(0, 3) == 3:
                diagOn = 1
                
            for j in range(jCount):
                c = (c[0], c[1], c[2]-30, alpha)            

                try:
                    pixdata[x-k, y] = c
                    pixdata[x+k, y] = c
                    pixdata[x, y-k] = c
                    pixdata[x, y+k] = c

                    if diagOn == 1:
                        cAlpha = c[3] - 60
                        if cAlpha < 0:
                            cAlpha = 0
                            
                        pixdata[x-k, y-k] = (c[0], c[1], c[2], cAlpha)
                        pixdata[x+k, y+k] = (c[0], c[1], c[2], cAlpha)
                        pixdata[x-k, y+k] = (c[0], c[1], c[2], cAlpha)
                        pixdata[x+k, y-k] = (c[0], c[1], c[2], cAlpha)
                except:
                    pass
                
                k += 1

            pointCount += 1

    except Exception as e:
        img = writeImageException(e)
        
    return img

def adaptiveInsert():
    img = ""
    
    try:
        imgpath = getInsert("", publicDomainImagePath)
        img = Image.open(imgpath)
        img = img.convert("RGBA")

        cCount = random.randint(4, 15)
        
        img = img.convert("P", palette=Image.ADAPTIVE, colors=cCount)
        
    except Exception as e:
        img = writeImageException(e)

    return img

def fractalText():
    try:
        img = fractal(4)
        d = ImageDraw.Draw(img)
        fontSize = 72
        thisFont = getFont()
        fon = ImageFont.truetype(thisFont, fontSize)
        
        pixdata = img.load()

        c = pixdata[int(img.size[0]/2), img.size[1]-1]        
        c = (255 - c[0], 255 - c[1], 255 - c[2])
        cStroke = pixdata[int(img.size[0]/3), img.size[1]-1]
        
        txt = Image.new('L', (700, 200))
        dtxt = ImageDraw.Draw(txt)

        x = 0
        y = 20
        word = getRandomWord()
        textStrokeExtra(dtxt, x, y, word, fon, fillColor=255, reps=3)
        dtxt.text((x, y), word, font=fon, fill=128)

        word = getRandomWord()
        textStrokeExtra(dtxt, x, y + fontSize, word, fon, fillColor=255, reps=3)
        dtxt.text((x, y + fontSize), word, font=fon, fill=128)
        
        w = txt.rotate(random.randint(-45, 45), expand=1)

        img.paste( ImageOps.colorize(w, (0,0,0), c), (275, 225),  w)
        
    except Exception as e:
        img = writeImageException(e)
        
    return img

def longWordListBase(sort=False):
    img = ""

    try:
        width = 700
        height = 10000
        
        img = Image.new("RGBA", (width, height), "#000000")

        draw = ImageDraw.Draw(img)
        
        fontSize = 42

        x = 20
        y = 10

        wordCount = 100

        mywords = []
        
        for i in range(wordCount):
            mywords.append(getRandomWord())

        if sort:
            mywords.sort(key=str.lower)

        fontPath = getFont()    
        altePath = fontPath + "AlteHaasGroteskBold.ttf"
        
        fon = ImageFont.truetype(fontPath, fontSize)

        h = 0
        s = 1
        v = 1

        i = 0
        while y < img.size[1] and h < 1 and i < len(mywords):            
            word = mywords[i]

            r, g, b = colorsys.hsv_to_rgb(h, s, v)        
            c = (int(r*255), int(g*255), int(b*255))
            
            draw.text((x, y), word, font=fon, fill=c)

            y += fontSize + 5

            h += 0.01
            i += 1

        img = img.crop((0, 0, img.size[0], y + 25))
        l = img.load()
        img = img.convert("RGBA")
            
    except Exception as e:
        img = writeImageException(e)

    return img

def longWordList():
    img = longWordListBase(sort=False)
    return img

def longWordList_Sorted():
    img = longWordListBase(sort=True)
    return img

def Favs30():
    img = ""
    
    try:
        lineCount = 30
        fontSize = 20
        headSize = 22
        
        width = 550
        height = lineCount * (fontSize + 4) + 10 + 30
        
        img = Image.new("RGBA", (width, height), "#FFFFFF")

        draw = ImageDraw.Draw(img)

        x = 10
        y = 50        

        altePath = fontPath + fontNameWordReg
        headingPath = fontPath + fontNameArcade

        fon = ImageFont.truetype(altePath, fontSize)
        fonHeading = ImageFont.truetype(headingPath, headSize)

        txtHeading = "1 LIKE = 1 OF THESE"

        headingSize = fonHeading.getsize(txtHeading)
        
        headX = int(img.size[0] // 2.0) - int(headingSize[0] // 2.0)
        headY = 10
        
        c = (255, 150, 150)
        textStrokeExtra(draw, headX, headY, txtHeading, fonHeading, (60, 60, 60), 2)
        draw.text((headX, headY), txtHeading, font=fonHeading, fill=c)       

        c = (0, 0, 0)
        
        for i in range(1, lineCount + 1, 1):
            words = []

            for j in range(4):
                if j == 0:
                    firstLetter = "n"
                elif j == 1:
                    firstLetter = "a"
                elif j == 2:
                    firstLetter = "t"
                elif j == 3:
                    firstLetter = "e"
                    
                w = getRandomWord(firstLetter)
                words.append(w)

            if i < 10:
                word = "  " + str(i) + ". "
            else:
                word = str(i) + ". "

            word += "".join([w[0].upper() + w[1:] + " " for w in words])
            
            draw.text((x, y), word, font=fon, fill=c)

            y += fontSize

    except Exception as e:
        img = writeImageException(e)

    return img

def typewriterStuff():
    try:
        width = 800
        height = 800
        fontSize = 48
        
        img = Image.new("RGBA", (width, height), "#DEDEDE")        
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        global fontPath
        basePath = fontPath
        fontPathT = basePath + "veteran typewriter.ttf"

        try:
            fon = ImageFont.truetype(fontPathT, fontSize)
        except:
            fontPathT = getFont()
            fon = ImageFont.truetype(fontPathT, fontSize)

        x = 20
        y = 15

        cStroke = (0, 0, 0)

        h = 0
        s = 0
        vStart = 150
        v = vStart

        iCount = 15

        choices = []

        for i in range(iCount):
            cup = random.randint(200, 255)
            cupc = (cup, cup, cup)
            choices.append(cupc)

        floodfill(img, (0, 0), targetcolour = pixdata[0, 0],
                  newcolour = (0,0,0),
                  randomIt = 1,
                  choices = choices)
        
        for i in range(iCount):
            word = getRandomWord() + " " + getRandomWord()

            r, g, b = colorsys.hsv_to_rgb(h, s, v)        
            c = (int(r), int(g), int(b))
            
            textStrokeExtra(draw, x, y, word, fon, cStroke, 2)
            draw.text((x, y), word, font=fon, fill=c)

            y += fontSize + 2
            v += int((255.0 - vStart) // iCount)            
            
        img = img.filter(ImageFilter.GaussianBlur(1))
        
    except Exception as e:
        img = writeImageException(e)

    return img

def paletteSquareLetters():
    img = ""

    import string

    try:
        img = Image.new("RGBA", (800, 600), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()        

        sizes = [50]

        fontPath = getFont()
        fontSize = 42
        fon = ImageFont.truetype(fontPath, fontSize)

        for squareSize in sizes:
            for x in range(0, img.size[0], squareSize):
                for y in range(0, img.size[1], squareSize):
                    if sizes[0] == squareSize or random.randint(1, 5) < 3:
                        palette = getPaletteGenerated()

                        yw = int(squareSize // (len(palette) * 1.0))
                        
                        x2 = x + squareSize
                        y2 = y + squareSize

                        if x2 > img.size[0]:
                            x2 = img.size[0]

                        if y2 > img.size[1]:
                            y2 = img.size[1]

                        ystep = y
                        for p in palette:                            
                            draw.rectangle((x, ystep, x2, ystep + yw), p)

                            ystep += yw + 1

                        c = random.choice(palette)
                        cStroke = c

                        while cStroke == c:
                            cStroke = random.choice(palette)                        

                        # invert the text color so it looks better against the bg
                        c = (255 - c[0], 255 - c[1], 255 - c[2])
                        
                        word = random.choice(string.ascii_letters).upper()

                        wsize = fon.getsize(word)
                        
                        # the center of the letter needs to be over the center
                        # the center is at x + (squareSize // 2)
                        # so put it at x + (squareSize // 2.0) - (wsize // 2.0)

                        wordPosX = int(x + (squareSize // 2.0) - (wsize[0] // 2.0))
                        # y is down too far. not sure why. manually adjusting
                        wordPosY = int(y + (squareSize // 2.0) - (wsize[1] // 2.0)) - 5
                        
                        textStrokeExtra(draw, wordPosX, wordPosY, word, fon, cStroke, 2)
                        draw.text((wordPosX, wordPosY), word, font=fon, fill=c)
                            
    except Exception as e:
        img = writeImageException(e)   

    return img

def mix2():
    img = ""

    outputWidth = 1280
    outputHeight = 1024

    try:
        img = Image.new("RGBA", (outputWidth, outputHeight), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        inserts = []

        for i in range(2):
            z = getInsertById(getParam(4))
            insert = Image.open(z)
            insert = resizeToMinMax(insert, maxW=outputWidth, maxH=outputHeight, minW=outputWidth//2, minH=outputHeight//2)
            
            img0 = Image.new("RGBA", (outputWidth, outputHeight), "#FFFFFF")
            img0.paste(insert, (0, 0))            
            
            inserts.append(img0)            

        img.paste(inserts[0], (0, 0))

        #img = ImageChops.add(img, inserts[1])
        img = ImageChops.darker(img, inserts[1])
        #img = ImageChops.multiply(img, inserts[1])
        
    except Exception as e:
        img = writeImageException(e)   

    return img

def mix2_public():
    img = ""
    
    try:
        w = 1280
        h = 1024
        bottomX = 800
        bottomY = 600
        
        img = Image.new("RGBA", (w, h), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        inserts = []        
        
        for i in range(2):
            insert = Image.open(getInsertById(getParam(4)))
            insert = resizeToMax(insert, maxW=w, maxH=h)
            
            img0 = Image.new("RGBA", (w, h), "#FFFFFF")
            img0.paste(insert, (0, 0))            

            if insert.size[1] < bottomY:
                bottomY = insert.size[1]
            if insert.size[0] < bottomX:
                bottomX = insert.size[0]
                
            inserts.append(img0)            

        img.paste(inserts[0], (0, 0))

        #img = ImageChops.add(img, inserts[1])
        img = ImageChops.darker(img, inserts[1])
        #img = ImageChops.multiply(img, inserts[1])

        img = img.crop((0, 0, bottomX, bottomY))
        l = img.load()
        img = img.convert("RGBA")
        
    except Exception as e:
        img = writeImageException(e)   

    return img

def mixpub_add():
    return mixpub_chop("add_modulo")

def mixpub_diff():
    return mixpub_chop("difference")

def mixpub_screen():
    return mixpub_chop("screen")

def mixpub_blend():
    """we're blending mixpubs ova heah<br />
    """

    i = getInt(getParam(4))

    return mix2_imageops("blend", i)

def mixpub_chop(imageop="add_modulo"):
    return mix2_imageops(imageop)

def mix2_imageops(imageop="add_modulo", source=0):
    img = ""

    w = getCurrentStandardWidth()
    h = getCurrentStandardHeight()
    
    try:
        img = Image.new("RGBA", (w, h), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        imgpaths = []
        inserts = []

        for i in range(2):
            xxv = getInsertById(source)

            while xxv in imgpaths:
                xxv = getInsertById(source)

            imgpaths.append(xxv)

            insert = Image.open(xxv)
            insert = resizeToMinMax(insert, maxW=w, maxH=h, minW=640, minH=480)
            insert = insert.convert("RGBA")

            if insert.size[0] < w:
                w = insert.size[0]

            if insert.size[1] < h:
                h = insert.size[1]
                
            img0 = Image.new("RGBA", (w, h), "#FFFFFF")
            img0.paste(insert, (0, 0))            
            
            inserts.append(img0)            

        img.paste(inserts[0], (0, 0))

        if imageop == "add_modulo":
            img = ImageChops.add_modulo(img, inserts[1])
        elif imageop == "subtract":
            img = ImageChops.subtract(img, inserts[1])            
        elif imageop == "subtract_modulo":
            img = ImageChops.subtract_modulo(img, inserts[1])
        elif imageop == "screen":
            img = ImageChops.screen(img, inserts[1])
        elif imageop == "difference":
            img = ImageChops.difference(img, inserts[1])
        elif imageop == "blend":
            blendAmount = random.uniform(.35, .75)

            if img.size != inserts[1].size:
                if inserts[1].size[0] > img.size[0] or inserts[1].size[1] > img.size[1]:
                    img = img.resize(inserts[1].size, Image.LANCZOS)
                else:
                    inserts[1] = inserts[1].resize(img.size, Image.LANCZOS)
            
            img = ImageChops.blend(img, inserts[1], blendAmount)
            
        img = img.crop((0, 0, w, h))
        l = img.load()
        img = img.convert("RGBA")
        
    except Exception as e:
        img = writeImageException(e)   

    return img

def mix2_other():
    img = ""
    
    try:
        goodImage = False

        while not goodImage:
            w = 1024
            h = 768
            
            img = Image.new("RGBA", (w, h), "#FFFFFF")
            draw = ImageDraw.Draw(img)
            pixdata = img.load()

            inserts = []

            bottomX = w
            bottomY = h

            safeFuncs = getSafeFuncs()

            iii = 2
            
            for i in range(iii):
                if i == 0 or i == 2:
                    insert = Image.open(getInsertById(getParam(4)))
                else:
                    zzbzzozzbzz = random.choice(safeFuncs)
                    insert = zzbzzozzbzz()
                    
                insert = resizeToMinMax(insert, maxW=w, maxH=h, minW=bottomX, minH=bottomY)
                
                img0 = Image.new("RGBA", (w, h), "#FFFFFF")
                img0.paste(insert, (0, 0))            

                if insert.size[1] < bottomY:
                    bottomY = insert.size[1]
                if insert.size[0] < bottomX:
                    bottomX = insert.size[0]
                    
                inserts.append(img0)            

            img.paste(inserts[0], (0, 0))

            imageops = ["add_modulo", "subtract", "subtract_modulo", "screen", "blend"]

            nextpic = 1

            while nextpic < len(inserts):
                thispic = inserts[nextpic]
                imageop = random.choice(imageops)
                
                if imageop == "add_modulo":
                    img = ImageChops.add_modulo(img, thispic)
                elif imageop == "subtract":
                    img = ImageChops.subtract(img, thispic)
                elif imageop == "subtract_modulo":
                    img = ImageChops.subtract_modulo(img, thispic)
                elif imageop == "screen":
                    img = ImageChops.screen(img, thispic)
                elif imageop == "difference":
                    img = ImageChops.difference(img, thispic)
                elif imageop == "blend":
                    blendAmount = random.uniform(0.2, 0.6)
                    img = ImageChops.blend(img, thispic, blendAmount)

                nextpic += 1
                
            img = img.crop((0, 0, bottomX, bottomY))
            l = img.load()
            img = img.convert("RGBA")
            img = img.convert("RGB")

            colors = img.getcolors(256)

            if colors is None:
                goodImage = True
            else:
                if len(colors) > 5:
                    goodImage = True
                else:
                    print('bad settings: ' + imageop + ' resulted in ' + str(len(colors)) + ' color(s)')
        
    except Exception as e:
        img = writeImageException(e)   

    return img

def ladiesSpend():
    img = ""
    try:
        img = Image.new("RGBA", (550, 500), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()
        
        fontSize = 32
        fontPathz = fontPath + "arial.ttf"
        fon = ImageFont.truetype(fontPathz, fontSize)
        
        fonBold = ImageFont.truetype(fontPath + "arialbd.ttf", 42)
        
        c = (0, 0, 0)

        smallAmount = 15
        largeAmount = random.randint(400, 900)
        
        totalAmount = random.randint(3, smallAmount)

        amount1 = random.randint(1, totalAmount-1)
        amount2 = totalAmount - amount1

        y = 20
        
        word = "Ladies you have $" + str(totalAmount)
        ws = fonBold.getsize(word)
        xmid = img.size[0] // 2

        x = xmid - (ws[0] // 2)        
        draw.text((x, y), word, font=fonBold, fill=c)
        y += 42 + 6

        word = "to build your ideal man"
        ws = fonBold.getsize(word)

        x = xmid - (ws[0] // 2)
        draw.text((x, y), word, font=fonBold, fill=c)
        y += 42 + 6
        
        y += 42 + 6

        amounts = []

        amounts.append(amount1)
        amounts.append(amount2)

        totLarge = 0

        while totLarge < largeAmount - smallAmount and len(amounts) < 6:
            amountLeft = largeAmount - totLarge
            
            thisAmt = random.randint(smallAmount, amountLeft)

            amounts.append(thisAmt)

            totLarge += thisAmt

        random.shuffle(amounts)
        
        x = 100
        for amount in amounts:
            if amount < totalAmount:
                term = getRandomWordSpecial("negative") 
            else:
                term = getRandomWordSpecial("positive")

            if random.randint(0, 1) == 0:
                term += " " + getRandomWord()

            word = "$" + str(amount) + ": " + term
            
            draw.text((x, y), word, font=fon, fill=c)

            y += fontSize + 6
        
    except Exception as e:
        img = writeImageException(e)   

    return img

def rose():
    img = ""
    try:
        # r = cos k theta
        # k = n // d
        
        w = 800
        h = 800

        debugText = False
        interval = 0.001
        strokeWidth = random.randint(2, 12)
        colorSwitch = random.randint(10, 250)
        
        choices = getPaletteGenerated()
        fillChoices = getPaletteGenerated()        
        
        global maxFloodFillArg        
        
        img = Image.new('RGBA', (w, h), "#ffffff")
        pixdata = img.load()

        x = w // 2
        y = h // 2        

        floodfill(img, (x,y), targetcolour = pixdata[x,y],
                              newcolour = (0,0,0),
                              randomIt = random.randint(1, maxFloodFillArg),
                              choices=fillChoices)
        
        random.seed()
        
        n = random.randint(1, 7)
        d = n

        while d == n:
            d = random.randint(1, 8)
            
        k = (n * 1.0) / (d * 1.0)

        if debugText:            
            draw = ImageDraw.Draw(img)
            debugTextSize = 12
            #debugLineSize = debugTextSize + 5
            
            global fontPathSansSerif
            fon = ImageFont.truetype(fontPathSansSerif, debugTextSize)
            debugc = (255, 255, 255, 255)
            debugtxt = "n: " + str(n) + " d: " + str(d)
            
            draw.text((5, img.size[1]-15), debugtxt, font=fon, fill=debugc)
        
        xCenter = int(img.size[0] // 2.0) 
        yCenter = int(img.size[1] // 2.0)
        
        c = random.choice(choices)
        
        iCount = 0
        
        a = 0.0
        while a < d * (2 * math.pi):
            # calculate and move to the center of the image

            r = (img.size[0] // 2.0) * math.cos(k * a)
            ix = int(r * math.cos(a)) + xCenter
            iy = int(r * math.sin(a)) + yCenter
            
            if iCount % colorSwitch == 0:
                c = random.choice(choices)
                    
            for x in range(ix-strokeWidth, ix+strokeWidth):
                for y in range(iy-strokeWidth, iy+strokeWidth):
                    if x >= 0 and y >= 0 and x < img.size[0] and y < img.size[1]:
                        pixdata[x, y] = c
                                    
            a += interval		
            iCount += 1

        pts = []
        
        if n == 8 and d == 2:
            pts = [(400, 50),
                   (400, 750),
                   (300, 300),
                   (600, 600),
                   (50, 400),
                   (750, 400),
                   (600, 250),
                   (250, 600)]        

        global randoFillList
        
        for pt in pts:
            x = pt[0]
            y = pt[1]
            
            floodfill(img, (x, y), targetcolour = pixdata[x,y],
                              newcolour = (0,0,0),
                              randomIt = random.choice(randoFillList),
                              choices=choices)
        
    except Exception as e:
        img = writeImageException(e)   

    return img

def astrologyTable():
    img = ""

    try:
        w = 601
        h = 679
               
        img = Image.new('RGB', (w, h), "#FFFFFF")

        draw = ImageDraw.Draw(img)

        fontSize = 16
        
        fon = ImageFont.truetype(fontPath + "cour.ttf", fontSize)
        c = (0, 0, 0)        

        x = 125
        y = 15

        bodys = ["Planet", "Sun", "Moon", "Mercury", "Venus", "Mars",
                 "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Chiron",
                 "Ceres", "Pallas", "Juno", "Vesta", "Node", "Lilith"]
        
        for b in bodys:
            txt = b + ":"
            txtSize = fon.getsize(txt)
            
            draw.text((x - txtSize[0], y), txt, font=fon, fill=c)

            y += fontSize + 2

        pts = [("Position", 150, fontSize),
               ("Aspects", 250, fontSize),
               ("Total", 350, fontSize),
               ("Percent", 475, fontSize)]
        
        for pt in pts:
            txt = pt[0]
            x = pt[1]
            y = pt[2]
            
            draw.text((x, y), txt, font=fon, fill=c)

        # get a total number
        total = random.uniform(500, 1000)
        total_position = random.uniform(0, total)
        total_aspects = total - total_position
        tots = []
        percs = []
        
        # calculate some values for position
        pos = (np.random.dirichlet(np.ones(len(bodys)-1), size=1))[0]
        pos = total_position * pos

        # draw em
        y = 15 + fontSize + 2

        for val in pos:
            tots.append((val, 0))
            
            x = 150
            txt = str(round(val, 2))
            draw.text((x, y), txt, font=fon, fill=c)

            y += fontSize + 2

        # write total
        txt = str(round(total_position, 2))
        draw.text((x, y), txt, font=fon, fill=c)

        # calc vals for aspects
        asp = (np.random.dirichlet(np.ones(len(bodys)-1), size=1))[0]
        asp = total_aspects * asp

        # draw asp
        y = 15 + fontSize + 2

        i = 0
        
        for val in asp:
            x = 250
            tots[i] = (tots[i][0], val)
            
            txt = str(round(val, 2))
            draw.text((x, y), txt, font=fon, fill=c)

            y += fontSize + 2

            i += 1

        # write total asp
        txt = str(round(total_aspects, 2))
        draw.text((x, y), txt, font=fon, fill=c)

        # draw the totals
        x = 350
        y = 15 + fontSize + 2
        
        for val in tots:
            thistot = val[0] + val[1]
            perc = thistot // total
            percs.append(perc)
            
            txt = str(round(thistot, 2))
            draw.text((x, y), txt, font=fon, fill=c)

            y += fontSize + 2

        # write total total
        txt = str(round(total_aspects + total_position, 2))
        draw.text((x, y), txt, font=fon, fill=c)

        # draw percentages
        x = 475
        y = 15 + fontSize + 2

        totPerc = 0
        
        for val in percs:
            thisPerc = val * 100
            txt = str(round(thisPerc, 2)) + "%"
            draw.text((x, y), txt, font=fon, fill=c)

            y += fontSize + 2

            totPerc += thisPerc

        # draw this even though it's pointless
        txt = str(totPerc) + "%"
        draw.text((x, y), txt, font=fon, fill=c)
        
    except Exception as e:
        img = writeImageException(e)   

    return img

def neobored():
    img = ""
    try:
        width = 900
        height = 900
               
        img = Image.new("RGB", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)

        pixdata = img.load()   

        global maxFloodFillArg
        
        for i in range(width-1, 0, -100):
            choices = getPaletteGenerated()
            
            draw.polygon([(0,0),
                          (i, i),
                          (i, 0)],
                         outline=(0,0,0),
                         fill=(255,255,255))

            draw.polygon([(0,0),
                          (i, i),
                          (0, i)],
                         outline=(0,0,0),
                         fill=(255,255,255))

            iAlg = random.randint(1, maxFloodFillArg)
            
            floodfill(img, (i - 50, 30),
                      targetcolour = (255,255,255),
                      newcolour=(255,255,0),
                      randomIt = iAlg,
                      choices = choices)

            random.shuffle(choices)
            
            floodfill(img, (30, i - 50),
                      targetcolour = (255,255,255),
                      newcolour=(255,255,0),
                      randomIt = iAlg,
                      choices = choices)

        #floodfill(img, (5, 400),
        #          targetcolour = (255,255,255),
        #          newcolour = (255,255,0),
        #          randomIt = 4)        
        
    except Exception as e:
        img = writeImageException(e)
        
    return img

def triangleNonSys(choices=[]):
    img = ""

    try:
        choices = getPalette()

        img = Image.new("RGBA", (800, 800), "#000000")
        draw = ImageDraw.Draw(img)

        sqCnt = 30
        
        xi = int(img.size[0] // sqCnt)
        yi = int(img.size[1] // sqCnt)

        lbX = 0
        lbY = 0

        lastC = (0,0,0)

        pts = []
        
        while lbX < img.size[0] or lbY < img.size[1]:
            for k in range(0, 2):
                j = random.randint(0, 100)
                
                if k == 0:
                    pts.append((lbX, lbY))
                    pts.append((lbX + xi, lbY))
                    pts.append((lbX, lbY + yi))
                else:
                    pts.append((lbX + xi, lbY))
                    pts.append((lbX + xi, lbY + yi))
                    pts.append((lbX, lbY + yi))

            if lbX < img.size[0]:
                lbX += xi
            else:
                lbY += yi
                lbX = 0

        random.shuffle(pts)
        
        i = 0
        while i < len(pts):
            pt1 = pts[i]
            pt2 = pts[i+1]
            pt3 = pts[i+2]
            
            c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))            
            cFill = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            
            if choices != []:
                c = random.choice(choices)
                cFill = random.choice(choices)

                while cFill[:3] == lastC[:3]:
                    cFill = random.choice(choices)

                lastC = cFill
                
            draw.polygon([pt1, pt2, pt3], fill=cFill, outline=c)

            i += 3
            
    except Exception as e:
        img = writeImageException(e)

    return img

def ellipseGuy():
    img = ""

    try:
        choices = getPalette()

        bg = getRandomColorRGB()
        
        img = Image.new("RGB", (800, 800), rgb_to_hex(bg))
        draw = ImageDraw.Draw(img)

        j = random.randint(10, 250)

        ir_step = random.randint(-10, -2)
        
        for i in range(0, j):
            c = random.choice(choices)
            cFill = random.choice(choices)

            while c == cFill:
                cFill = random.choice(choices)

            x = random.randint(0, img.size[0])
            y = random.randint(0, img.size[1])

            r = random.randint(1, 100)            
            
            for ir in range(r,0,ir_step):
                draw.ellipse((x-ir, y-ir, x+ir, y+ir), fill=cFill, outline=c)
                ctemp = c
                c = cFill
                cFill = ctemp
        
    except Exception as e:
        img = writeImageException(e)

    return img

def ellipseGroup():
    img = ""
    
    try:
        img = ellipseGuy()

        iCount = random.randint(2, 10)
        
        i = 1

        maxop = 4
        
        op2 = random.randint(0, 4)
        
        while i < iCount:
            img2 = ellipseGuy()
            op = random.randint(0, maxop)

            if op == 0:
                img = ImageChops.darker(img, img2)
            elif op == 1:
                img = ImageChops.add(img, img2)
            elif op == 2:
                img = ImageChops.multiply(img, img2)
            elif op == 3:
                img = ImageChops.difference(img, img2)
            elif op == 4:
                img = ImageChops.screen(img, img2)
                
            if op2 == 0:
                img = ImageChops.invert(img)

            
                
            i += 1            

        colors = img.getcolors()

        if colors is not None and len(colors) <= 1:
            print("only one color")
            img = ellipseGroup()
    
    except Exception as e:
        img = writeImageException(e)

    return img

def fillFromOuter():
    imgs = fillFromOuter_Process()

    return imgs[0]

def fillFromOuter_Process(choices=[], stamp=None, imgpath="", img="", alg=0, maxIterations = 200):
    global fontPathSansSerif

    try:
        if imgpath == "":
            imgpath = getInsertById(getParam(4))

        if img == "":
            img = Image.open(imgpath)

        img = img.convert("RGBA")

        img = resizeToMinMax(img, maxW=1024, maxH=768, minW=640, minH=480)

        origImg = img.copy()
        
        pixdata = img.load()
                
        floodedCount = 0
        pixCount = img.size[0] * img.size[1]

        iteration = 0

        # build a choice list from taking the color of a random point and iterating over 0 to 255               
       
        if choices == []:
            for j in range(0, 3):
                (x,y) = (random.randint(0, img.size[0]-1), random.randint(0, img.size[1]-1))
                c = pixdata[x,y]

                di = random.randint(0, 2)        

                iCount = 15
                cDiff = 255 / (iCount * 1.0)
                iThis = 0
                
                for i in range(0, iCount):
                    iThis = int(i * cDiff)

                    if iThis < 0:
                        iThis = 0
                    elif iThis > 255:
                        iThis = 255
                        
                    ci = replace_at_index(c, di, iThis)

                    if ci not in choices:
                        choices.append(ci)

        # now do random floodfills

        fon = ImageFont.truetype(fontPathSansSerif, 18)
        debugFillColor = (255, 255, 255, 255)

        draw = ImageDraw.Draw(img)        

        global randoFillList
        
        lastX = img.size[0]-1
        while iteration < maxIterations and lastX >= 0:
            (x,y) = (lastX, random.randint(0, img.size[1]-1))

            iAlg = 0

            if alg != 0:
                iAlg = alg
            else:
                while iAlg == 0:
                    iAlg = random.choice(randoFillList)

            temp = img.copy()
            pixdata = temp.load()
            targ = pixdata[x,y]

            #choices = getPaletteGenerated()

            tempFC = floodfill(temp, (x, y), targetcolour = targ,
                               newcolour = (0,0,0),
                               randomIt = iAlg,
                               compFunc=1,
                               choices=choices,
                               stamp=stamp)
        
            if tempFC > 100:                
                # only allow the flood if it did some bigger changes
                
                img = temp                
                
                floodedCount += tempFC

            iteration += 1
            lastX -= random.randint(1, 5)
            
    except Exception as e:
        img = writeImageException(e)
        draw = ImageDraw.Draw(img)
        
        fon = ImageFont.truetype(fontPathSansSerif, 18)
        debugFillColor = (0, 0, 0, 255)
        textY = 100
        
        draw.text((5, textY), "imgpath: " + imgpath, font=fon, fill=debugFillColor)
    
    return [img, origImg]

def fillFromOuter_blend():
    try:
        global input_palette

        iAlg = random.choice(randoFillList)

        if len(input_palette) > 0:
            imgs = fillFromOuter_Process(choices=input_palette, alg=iAlg)
        else:
            rndln = random.randint(5, 50)
            imgs = fillFromOuter_Process(getPaletteGenerated(paletteLength=rndln), alg=iAlg)
        
        img = imgs[0]
        origImg = imgs[1]

        blendAmount = random.uniform(0.1, 0.4)
        
        img = Image.blend(origImg, img, blendAmount)

    except Exception as e:
        img = writeImageException(e)
        
    return img

def fillFromOuter_stamp():
    try:
        global input_palette

        #stamp = vaporwave1()
        # stamp = None
        stamp = fullFill(w=50, h=50)

        if len(input_palette) > 0:
            imgs = fillFromOuter_Process(choices=input_palette, stamp=stamp)
        else:
            rndln = random.randint(5, 50)
            imgs = fillFromOuter_Process(getPaletteGenerated(paletteLength=rndln), stamp=stamp)
        
        img = imgs[0]
        origImg = imgs[1]

        blendAmount = random.uniform(0.28, 0.5)
        
        img = Image.blend(origImg, img, blendAmount)

    except Exception as e:
        img = writeImageException(e)
        
    return img

def fillFromOuter_canny():
    try:
        global input_palette

        stampW = random.randint(30, 75)
        stampH = random.randint(30, 75)

        stamp = fullFill(w=stampW, h=stampH)

        if random.randint(0, 1) == 0:
            img = opencv_canny()
        else:
            img = opencv_canny_inv()

        if len(input_palette) > 0:
            imgs = fillFromOuter_Process(choices=input_palette, stamp=stamp, img=img)
        else:
            rndln = random.randint(5, 50)
            imgs = fillFromOuter_Process(getPaletteGenerated(paletteLength=rndln), stamp=stamp, img=img)
        
        img = imgs[0]
        origImg = imgs[1]

        blendAmount = random.uniform(0.28, 0.5)
        
        img = Image.blend(origImg, img, blendAmount)

    except Exception as e:
        img = writeImageException(e)
        
    return img

def labelSquares(imgpath=""):        
    img = ""

    try:
        imgpxth = pathLabelSquares
        img2 = Image.open(imgpxth)
        img2 = img2.convert("RGBA")        
        
        img = Image.new("RGBA", img2.size, "#ffffff")
        #img.paste(img2, (0, 0), img2)

        pixdata = img.load()
        draw = ImageDraw.Draw(img)

        squares = []

        sqW = 300
        sqH = 299
        
        # first square starts at 150, 150
        # first square ends at 450, 150
        # first square starts at 150, 450
        # first square ends at 450, 450

        # row 2 1 starts at 150, 488
        # row 2 1 ends at 450, 488
        
        # square width: 
        # square height: 
       
        for y in [150,
                  151+337,
                  151+(337*2),
                  151+(337*3),
                  151+(337*4),
                  151+(337*5),
                  151+(337*6),
                  152+(337*7),
                  153+(337*8)]:
            for x in range(150, img.size[0], 325):

                if x+sqW < img.size[0] and y+sqH < img.size[1]:
                    sq = []
                    sq.append((x, y))
                    sq.append((x+sqW, y))
                    sq.append((x, y+sqH))
                    sq.append((x+sqW, y+sqH))
                    
                    squares.append(sq)

        option = 3

        choices = []

        if option == 0:
            # option 0
            choices = [
                ["INFINITE", "BOOBY", False],
                ["NONSENSE", "LOSES", False],
                ["SERENE", "PLANTATION", False],
                ["BLOODCURDLING", "EXTRACT", False],
                ["CRACK", "TOILETRY", False],
                ["FLYABLE", "BOLOGNA", False]
                ]
  
        for sq in squares:
            # top corner - 0
            tl = sq[0]
            tr = sq[1]
            bl = sq[2]
            br = sq[3]
            
            found = False
            
            for c in choices:
                if c[2] == False and found == False:
                    word1 = c[0]
                    word2 = c[1]
                    c[2] = True
                    found = True

            if not found:
                if option == 1:
                    word1 = getRandomWordSpecial("verb").upper()
                    word2 = getRandomWord().upper()
                elif option == 2:
                    word1 = get_random_unicode(1)
                    word2 = ""
                elif option == 3:
                    # inn/tavern/pub
                    pathchoice = random.randint(0, 6)
                    
                    if pathchoice >= 0 and pathchoice <= 1:
                        word1 = "THE " + getRandomWordSpecial("noun").upper()
                        word2 = "AND " + getRandomWordSpecial("noun").upper()
                    elif pathchoice == 6:
                        word1 = "THE" 
                        word2 = getRandomWordSpecial("noun").upper()
                    elif pathchoice >= 2 and pathchoice <= 3:
                        word1 = "THE " + getRandomWordSpecial("verb").upper()
                        word2 = getRandomWordSpecial("noun").upper()
                    else:
                        word1 = "THE " + getRandomWordSpecial("adjective").upper()
                        word2 = getRandomWordSpecial("noun").upper()
                else:
                    word1 = getRandomWord().upper()
                    word2 = getRandomWord().upper()
                    
            fonsize = 72

            if option == 2:
                fonsize = 128
                
            myf = getFont()
            fonEncoding = ""

            if option == 2:
                myf = fontPath + "NotoSans_Regular.ttf"
                fonEncoding = ""

            if fonEncoding == "":
                fon = ImageFont.truetype(myf, fonsize)
            else:
                fon = ImageFont.truetype(myf, fonsize, encoding=fonEncoding)
                
            wp1 = fon.getsize(word1)
            wp2 = fon.getsize(word2)
            
            while wp1[0] + 10 > sqW or wp2[0] + 10 > sqW:
                fonsize -= 1
                
                if fonEncoding == "":
                    fon = ImageFont.truetype(myf, fonsize)
                else:
                    fon = ImageFont.truetype(myf, fonsize, encoding=fonEncoding)
                
                wp1 = fon.getsize(word1)
                wp2 = fon.getsize(word2)

            midX = int(tl[0] + (sqW // 2.0))
            midY = int(tl[1] + (sqH // 2.0))

            wx1 = int(wp1[0] // 2.0)
            wy1 = int(wp1[1] // 2.0)
            wx2 = int(wp2[0] // 2.0)
            wy2 = int(wp2[1] // 2.0)

            halffont = int(fonsize // 3.0)
            
            fc = (0,0,0)

            if word2 != "":
                draw.text((midX-wx1, midY-wp1[1] - halffont), word1, font=fon, fill=fc) 
                draw.text((midX-wx2, midY + halffont), word2, font=fon, fill=fc)
            else:
                draw.text((midX-wx1, midY-wp1[1]), word1, font=fon, fill=fc) 
            
            #draw.polygon([sq[0], sq[1], sq[3], sq[2]], outline=(128,0,0))
        
    except Exception as e:
        img = writeImageException(e)

    return img

def darkbits():
    img = ""
    
    try:
        width = random.randint(400, 1100)
        height = random.randint(200, 1000)

        fon = ImageFont.truetype(fontPath + fontNameImpact, 32)
        
        img = Image.new("RGBA", (width,height), "#000000")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        choices = getPaletteGenerated(paletteLength=7)

        global randoFillList
        iAlg = random.choice(randoFillList)
        
        floodfill(img, (5, 5),
                          targetcolour = pixdata[5,5],
                          newcolour = (160,128,100),
                          randomIt = iAlg,
                          maxStackDepth = 0 if iAlg == 21 else 0,
                  choices = choices)
        
        xi = 25

        c = getRandomColor()
        
        for x in range(0, img.size[0], xi):
            for y in range(0, img.size[1]):
                i = random.randint(x, x + xi)               

                if i >= img.size[0]:
                    i = img.size[0] - 1
                    
                pixdata[i, y] = c

    except Exception as e:
        img = writeImageException(e)

    return img

def altWorld():
    """p1: replacement method (<br />
    0=random color,<br />
    1=choices,<br />
    2=saturation crank,<br />
    3=after fourcolor)
    """

    try:
        imgpath = getInsertById(getParam(4))        
        
        img = Image.open(imgpath)
        img = img.convert("RGBA")

        img = resizeToMinMax(img, maxW=1024, maxH=768, minW=640, minH=480)
       
        pixdata = img.load()

        # replace every pixel with a different color
        # and keep that color to use for the same color elsewhere in the image
        # has intentional "bug" that it only replaces the first instance of the color
        # because actually doing every pixel looks incomprehensible
        
        p1 = getParam(0)
        p1 = int(p1) if p1.isdecimal() and int(p1) >= 0 and int(p1) <= 3 else random.randint(0, 2)

        method = p1
      
        choices = getInputPalette()

        fixBug = 0
        
        if method in [2,3]:
            fixBug = 1

        if method == 3:
            img = fourColorWithPalette(img, choices)
            pixdata = img.load()

        addState(f"fixBug: {fixBug}, method: {method}")
        
        colorsKept = {}

        for y in range(0, img.size[1]):
            for x in range(0, img.size[0]):
                c = pixdata[x, y]
                crep = c
                
                if str(c) not in colorsKept:
                    if method == 0:
                        crep = getRandomColor()
                    elif method == 1:
                        crep = random.choice(choices)
                    elif method == 2:
                        # crank up the saturation
                        crep = c
                        hsvc = colorsys.rgb_to_hsv(c[0] // 255.0, c[1] // 255.0, c[2] // 255.0)
                        hsvc = replace_at_index(hsvc, 1, 1)
                        crep = myhsv_to_rgb(hsvc)
                    elif method == 3:
                        crep = random.choice(choices)
                        
                    colorsKept[str(c)] = crep
                    pixdata[x, y] = crep
                else:
                    if fixBug == 1:
                        crep = colorsKept[str(c)]
                        pixdata[x, y] = crep
                   
    except Exception as e:
        img = writeImageException(e)

    return img

def ctrlWorld():
    try:
        imgpath = getInsertById(getParam(4))        
        
        img = Image.open(imgpath)
        img = img.convert("RGBA")

        img = resizeToMinMax(img, maxW=1024, maxH=768, minW=640, minH=480)
       
        pixdata = img.load()

        colorsKept = {}

        # replace every pixel with a different color
        # and keep that color to use for the same color elsewhere in the image
             
        choices = getPaletteGenerated()      

        dividingLine = random.uniform(0.01, 0.99)        

        p1 = getParam(0)
        p1 = int(p1) if p1.isdecimal() else 0
        
        l_mod = random.uniform(0, 1)  

        for y in range(0, img.size[1]):
            for x in range(0, img.size[0]):
                c = pixdata[x, y]
                crep = c
                
                if str(c) not in colorsKept:
                    # crank up the saturation
                    crep = c

                    h, l, s = colorsys.rgb_to_hls(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)

                    if h > dividingLine:
                        hue = random.uniform(dividingLine, 1)
                    else:
                        hue = random.uniform(0, dividingLine)                                      

                    r, g, b = colorsys.hls_to_rgb(hue, l, l_mod)
                    zc = (int(r*255.0), int(g*255.0), int(b*255.0))

                    colorsKept[str(c)] = zc

                crep = colorsKept[str(c)]
                pixdata[x, y] = crep
                   
    except Exception as e:
        img = writeImageException(e)

    return img

def shiftWorld():
    """p1: maxStackDepth"""

    img = ""
    
    try:
        w = 1280
        h = 1024
        
        img = Image.new("RGBA", (w, h), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        p1 = getParam(0)
        p1 = int(p1) if p1.isdecimal() else 4

        inserts = []

        bottomX = w
        bottomY = h
        
        for i in range(3):
            insert = Image.open(getInsertById(getParam(4)))
            insert = resizeToMinMax(insert, maxW=w, maxH=h, minW=bottomX, minH=bottomY)
            insert = imageop_hueshift(insert)

            saveForXanny(insert)
            
            img0 = Image.new("RGBA", (w, h), "#FFFFFF")
            img0.paste(insert, (0, 0))            

            if insert.size[1] < bottomY:
                bottomY = insert.size[1]
            if insert.size[0] < bottomX:
                bottomX = insert.size[0]
                
            inserts.append(img0)            

        img.paste(inserts[0], (0, 0))
        
        img = ImageChops.darker(img, inserts[1])
        img = ImageChops.add(img, inserts[2])

        img = img.crop((0, 0, bottomX, bottomY))
        l = img.load()
        img = img.convert("RGBA")

        saveForXanny(img)

        stamp = wordfilled(width=500, height=150)
        img = radioFill_stamp(imgpath="", img=img, stamp=stamp, blendOverride=0.5, maxStackDepth=p1)

        saveForXanny(stamp)
        saveForXanny(img)
        
        saveConfiguration()

    except Exception as e:
        img = writeImageException(e)

    return img

def metaWorld():
    """p1: maxStackDepth
    p2: flood count max (default: -1 => pixel count / 4)"""

    startTimeCheck()
    doTimeCheck("metaWorld starts")

    stampFuncs = [triangleSys,
                      atariripples,
                      rose,
                      gritty,
                      grittyer,
                      randgradient,
                      wordGrid_single,
                      paletteSquares,
                      generatePalette,
                      ellipseGuy,
                      colorHatch,
                      hsvTesting]
    
    doTimeCheck("stampFuncs gotten")

    stampf = random.choice(stampFuncs)        
    
    doTimeCheck("stampf gotten")

    stamp = stampf()
    
    doTimeCheck("stampf ran")

    stamp = resizeToMinMax(stamp, maxW=200, maxH=100, minW=100, minH=50)

    doTimeCheck("stamp resized")

    saveForXanny(stamp)

    img = metaWorldBase(stamp)

    saveForXanny(img)

    doTimeCheck("metaWorldBase done")

    return img

def metaWorldStamp():
    """p1: maxStackDepth<br />
    p2: flood count max (default: -1 => pixel count / 4)"""

    disobey = 1

    startTimeCheck()
    doTimeCheck("metaWorldStamp starts")

    stamp = getStamp()
    stamp = resizeToMinMax(stamp, maxW=200, maxH=100, minW=100, minH=50)

    return metaWorldBase(stamp, disobey, sizeLimit=(200,200))

def metaWorldBase(stamp, disobey=0, sizeLimit=(0,0)):
    doTimeCheck("metaWorldBase starts")

    img = ""
    
    try:
        w = 1280
        h = 1024

        saveForXanny(stamp)
        
        img = Image.new("RGBA", (w, h), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        inserts = []

        bottomX = w
        bottomY = h
        
        p1 = getParam(0)
        p2 = getParam(1)
    
        p1 = int(p1) if p1.isdecimal() else 0
        p2 = int(p2) if p2.isdecimal() else -1

        compFunc = 50

        floodLimit = p2

        doTimeCheck("p1: " + str(p1))
        doTimeCheck("\ti = 0")

        for i in range(3):
            doTimeCheck("\ti = " + str(i))

            insert = Image.open(getInsertById(getParam(4)))
            insert = resizeToMinMax(insert, maxW=w, maxH=h, minW=bottomX, minH=bottomY)

            saveForXanny(insert)

            insert = radioFill_stamp(imgpath="", img=insert, stamp=stamp, blendOverride=0.5, compFunc=compFunc, disobey=disobey, maxStackDepth=p1, floodLimit=floodLimit, sizeLimit=sizeLimit)

            saveForXanny(insert)

            if random.randint(0, 1) == 0:
                insert = imageop_hueshift(insert)
            else:
                insert = imageop_invert(insert)
            
            img0 = Image.new("RGBA", (w, h), "#FFFFFF")
            img0.paste(insert, (0, 0))            

            if insert.size[1] < bottomY:
                bottomY = insert.size[1]
            if insert.size[0] < bottomX:
                bottomX = insert.size[0]
                
            inserts.append(img0)            

        img.paste(inserts[0], (0, 0))

        img = ImageChops.darker(img, inserts[2])
        img = ImageChops.add(img, inserts[1])

        img = img.crop((0, 0, bottomX, bottomY))
        l = img.load()
        img = img.convert("RGBA")
        
    except Exception as e:
        img = writeImageException(e)

    saveForXanny(img)

    return img

def hyperWorld():
    img = ""

    w = 1024
    h = 768
    
    try:
        img = Image.new("RGBA", (w, h), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        insert = Image.open(getInsertById(getParam(4)))
        insert = resizeToMinMax(insert, maxW=w, maxH=h, minW=640, minH=480)
        insert = insert.convert("RGBA")

        if insert.size[0] < w:
            w = insert.size[0]

        if insert.size[1] < h:
            h = insert.size[1]
            
        img.paste(insert, (0, 0))            

        img2 = Image.new("RGBA", (insert.size[0], insert.size[1]), "#FFFFFF")
        stamp = wordfilled(width=w // 4, height=h // 4)
        
        img2 = radioFill_stamp(imgpath="", img=img2, stamp=stamp, blendOverride=1)

        blendAmount = random.uniform(.2, .4)

        if img.size != img2.size:
            if img2.size[0] > img.size[0] or img2.size[1] > img.size[1]:
                img = img.resize(img2.size, Image.LANCZOS)
            else:
                img2 = img2.resize(img.size, Image.LANCZOS)
        
        #img = ImageChops.blend(img, img2, blendAmount)
        #img = ImageChops.difference(img, img2)
        img3 = ImageChops.darker(img, img2)
        img = ImageChops.blend(img, img3, blendAmount)
            
        img = img.crop((0, 0, insert.size[0], insert.size[1]))
        l = img.load()
        img = img.convert("RGBA")
        
    except Exception as e:
        img = writeImageException(e)
    
    return img

def greekWorld_toconvert():
    # TODO: convert to imageop

    img = ""

    w = 1024
    h = 768
    
    try:
        img = Image.open(getInsertById(getParam(4)))
        img = resizeToMinMax(img, maxW=w, maxH=h, minW=640, minH=480)
        img = img.convert("RGBA")

        w = img.size[0]
        h = img.size[1]
            
        img2 = Image.new("RGBA", (w, h), "#FFFFFF")
        #stamp = wordfilled(width=w // 4, height=h // 4)        
        stamp = getStamp()
        img2 = radioFill_stamp(imgpath="", img=img2, stamp=stamp, blendOverride=1)

        blendAmount = random.uniform(.2, .4)

        if img.size != img2.size:
            if img2.size[0] > img.size[0] or img2.size[1] > img.size[1]:
                img = img.resize(img2.size, Image.LANCZOS)
            else:
                img2 = img2.resize(img.size, Image.LANCZOS)
                
        img3 = ImageChops.darker(img, img2)
        img = ImageChops.blend(img, img3, blendAmount)  
        
        l = img.load()
        img = img.convert("RGBA")
        
    except Exception as e:
        img = writeImageException(e)
    
    return img

def greekWorld():
    startTimeCheck()
    doTimeCheck("greekWorld starts")

    global wrapperData
    global currentUID

    uid = currentUID

    #ColorPrint.logger_info("wrapperData as greekWorld starts: " + writeWrapperToLog(wrapperData))

    img = ""

    w = 1280
    h = 1024
    
    try:
        img = Image.open(getInsertById(getParam(4)))
        img = resizeToMinMax(img, maxW=w, maxH=h, minW=640, minH=480)
        img = img.convert("RGBA")

        saveForXanny(img)

        w = img.size[0]
        h = img.size[1]

        pixCount = w * h

        (img, mask, mask_cv) = opencv_removeBG_op(img)

        img = img.convert("RGBA")

        saveForXanny(img)
        saveForXanny(mask)

        points = []

        pixdata = mask.load()

        for x in range(0, mask.size[0]):
            for y in range(0, mask.size[1]):
                c = pixdata[x, y]

                if c == 0:
                    points.append((x,y))                

        random.shuffle(points)

        colors = getPaletteFromImage(img)

        stamp = getStamp() 
        stamp = stamp.convert("RGB")
        pixels = ImageOps.grayscale(stamp).getdata()

        if len(colors) <= 0:
            colors = getPalette()

        ranges = getGoodRanges(pixels, len(colors))

        stamp = Image.new(stamp.mode, stamp.size,)
        stamp.putdata(colorfun(pixels, colors, ranges))

        stamp.load()

        mask_old = mask.copy()

        mask = mask.convert("RGBA")        

        pixdata = mask.load()

        pointCount = 0
        greekFactor = .17 # .4

        for point in points:
            #doTimeCheck("pointCount: " + str(pointCount) + " pixCount: " + str(pixCount))
            x = point[0]
            y = point[1]

            pointCount += floodfill(mask, (x, y), targetcolour = pixdata[x,y],
                                newcolour = (0,0,0),
                                randomIt = 0,
                                compFunc=0,
                                choices=[],
                                stamp=stamp,
                                stampTrans=None)

            #doTimeCheck("pointCount: " + str(pointCount) + " pixCount: " + str(pixCount))

            if pointCount >= (pixCount * greekFactor):
                break
   
        zonk = img.copy()
        img = ImageChops.composite(img, mask, mask_old)

        saveForXanny(zonk)
        saveForXanny(mask)

        doTimeCheck("img comp done // goodbye greekWorld")
        
        return img
    
    except Exception as e:
        img = writeImageException(e)
    
    return img

def localWorld(distance=5):
    """p1: distance (default=5)"""
    img = ""

    w = getCurrentStandardWidth()
    h = getCurrentStandardHeight()
    
    try:
        p1 = getParam(0)
        p2 = getParam(1)
    
        p1 = int(p1) if p1.isdecimal() else 0
        p2 = int(p2) if p2.isdecimal() else -1

        if p1 != 0:
            distance = p1
    
        img = Image.open(getInsertById(getParam(4)))
        img = resizeToMinMax(img, maxW=w, maxH=h, minW=640, minH=480)
        img = img.convert("RGBA")

        w = img.size[0]
        h = img.size[1]

        colors = getPaletteFromImage(img, distance=distance, limit=5)

        im_pil = img.copy().convert("RGB")
        im_pil = ImageChops.invert(im_pil)

        colors2 = getPaletteFromImage(im_pil, distance=distance, limit=25)

        [colors.append(c) for c in colors2]

        random.shuffle(colors)
        
        pixels = ImageOps.grayscale(img).getdata()
        ranges = getGoodRanges(pixels, len(colors))

        psys = Image.new(img.mode, img.size,)
        psys.putdata(colorfun(pixels, colors, ranges))

        img = psys
    
    except Exception as e:
        img = writeImageException(e)
    
    return img

def compuWorld(distance=5):
    """p1: distance (default=5)"""

    import cv2

    startTimeCheck()
    doTimeCheck("compuWorld starts")

    global wrapperData
    global currentUID

    uid = currentUID

    #ColorPrint.logger_info("wrapperData as greekWorld starts: " + writeWrapperToLog(wrapperData))

    img = ""

    w = getCurrentStandardWidth()
    h = getCurrentStandardHeight()
    
    try:
        img = Image.open(getInsertById(getParam(4)))
        img = resizeToMinMax(img, maxW=w, maxH=h, minW=640, minH=480)
        img = img.convert("RGBA")

        saveForXanny(img)

        choices = getInputPalette(5)

        w = img.size[0]
        h = img.size[1]

        pixCount = w * h

        (img, mask, mask_cv) = opencv_removeBG_op(img, limitsLower=[200, 200, 200], limitsUpper=[255,255,255], kernelEllipse=(20,20))
        # def opencv_removeBG_op(img="", limitsLower=[200, 200, 200], limitsUpper=[255,255,255], kernelEllipse=(20,20)):

        img = img.convert("RGBA")

        saveForXanny(img)
        saveForXanny(mask)        

        ogc = opencv_get_contours(img, random.choice(choices))
        result = cv2.cvtColor(ogc, cv2.COLOR_BGR2RGB)

        img2 = Image.fromarray(result)
        img2 = img2.convert("RGBA")
        
        img = ImageChops.blend(img, img2, .5)

        points = []

        pixdata = mask.load()

        for x in range(0, mask.size[0]):
            for y in range(0, mask.size[1]):
                c = pixdata[x, y]

                if c == 0:
                    points.append((x,y))                

        random.shuffle(points)

        pointCount = 0
        greekFactor = .1

        mask_old = mask.copy()
        mask = mask.convert("RGBA")
        pixdata = mask.load()
        iAlg = random.randint(1, maxFloodFillArg)

        for point in points:
            #doTimeCheck("pointCount: " + str(pointCount) + " pixCount: " + str(pixCount))
            x = point[0]
            y = point[1]

            pointCount += floodfill(mask, (x, y), targetcolour = pixdata[x,y],
                                newcolour = (0,0,0),
                                randomIt = iAlg,
                                compFunc = 0,
                                sizeLimit=(40, 40),
                                choices=choices)

            #doTimeCheck("pointCount: " + str(pointCount) + " pixCount: " + str(pixCount))

            if pointCount >= (pixCount * greekFactor):
                break
   
        zonk = img.copy()
        saveForXanny(zonk)

        img = ImageChops.composite(img, mask, mask_old)
        
        saveForXanny(mask)

        doTimeCheck("img comp done // goodbye compuWorld")
        
        return img
    
    except Exception as e:
        img = writeImageException(e)
    
    return img

def effect_mandelbrot():
    img = ""
    
    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        #z = (-1.5, -1, .5, 1)
        z = (-.5, -.5, .8, 1)

        img = Image.effect_mandelbrot((width, height), z, 100)
    except Exception as e:
        img = writeImageException(e)

    return img

def radial_gradient():
    img = ""
    
    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        #img = Image.new("RGBA", (width, height), "#ffffff")

        img = Image.radial_gradient("P")

        pixdata = img.load()

        global maxFloodFillArg
        
        iAlg = random.randint(1, maxFloodFillArg)

        c = pixdata[5, 5]
        pl = random.randint(10, 25)
        
        choices = getInputPalette()        
         
    except Exception as e:
        img = writeImageException(e)

    return img

def fullFill(w=getCurrentStandardWidth(),h=getCurrentStandardHeight(),iAlg=0):
    """
    p1 = iAlg (default 0)<br />
    p2 = palette length when generated
    """

    img = ""
    
    try:
        w = 640
        h = 480
        img = Image.new("RGBA", (w, h), "#ffffff")
        pixdata = img.load()

        global maxFloodFillArg
        
        if iAlg == 0:
            iAlg = random.randint(1, maxFloodFillArg)

        c = pixdata[w//2,h//2]

        parmies = getIntParams(iAlg, random.randint(10, 25))
        pl1 = parmies[1]

        iAlg = parmies[0]
        
        choices = getInputPalette(paletteLength=pl1)
        
        floodfill(img, (w//2,h//2),
                          targetcolour = c,
                          newcolour = (160,128,100),
                          randomIt = iAlg,
                          maxStackDepth = 0 if iAlg == 21 else 0,
                          compFunc=-1,
                  choices = choices)
         
    except Exception as e:
        img = writeImageException(e)

    return img

def fullFillSpecific(iAlg=84):
    """p1: iAlg (default=84)<br />
    p3: variant
    """

    p1 = getParam(0)
    p2 = getParam(1)
    
    if p1 == "":
        p1 = iAlg
    else:
        p1 = int(p1) if p1.isdecimal() else iAlg
    
    return fullFill(iAlg=p1)

def fullFillLatest():
    global maxFloodFillArg

    return fullFill(iAlg=maxFloodFillArg)

def fullfillBlend2():
    """
    p1 = iAlg (default 0)<br />
    p2 = palette length when generated
    """

    try:
        img = fullFill()
        img2 = fullFill()

        blendAmount = random.uniform(0.4, 0.7)
        
        img = Image.blend(img, img2, blendAmount)

    except Exception as e:
        img = writeImageException(e)

    return img

def fullFillStamp():
    img = ""

    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()
        
        img = Image.new("RGB", (width,height), "#ffffff")

        stmp1 = getStamp()
        
        floodfill(img, (5, 5),
                          targetcolour = (255, 255, 255),
                          newcolour = (0,0,0),
                          randomIt = 0,
                          compFunc=-1,
                          stamp = stmp1)
        
    except Exception as e:
        img = writeImageException(e)

    return img

def fullFillVariants(iAlg=0):
    """p1: iAlg (default=random)<br />
    p3: variant
    """

    img = ""

    try:
        p1 = getParam(0)
        p2 = getParam(1)
        
        if p1 != "":
            iAlg = int(p1) if p1.isdecimal() else iAlg
        
        global maxFloodFillArg
        
        if iAlg == 0:
            iAlg = random.randint(1, maxFloodFillArg)   

        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()
        
        img = Image.new("RGB", (width,height), "#ffffff")        
        draw = ImageDraw.Draw(img)
        pixdata = img.load()
         
        fillTestTotal = 48
        rows, cols, gridStep = buildGrid(width, height, fillTestTotal)
        xTimeText = drawGrid(draw, rows, cols, gridStep, "gray")        

        pl = random.randint(5, 10)        
        choices = getInputPalette(pl)
        
        addState(f"rows: {rows}, cols: {cols}, p1: {p1}, iAlg: {iAlg}, choices: {choices}", None)

        fon = ImageFont.truetype(fontPath + fontNameImpact, 16)

        i = 0
        for y in range(0, rows):
            for x in range(0, cols):
                xFill = gridStep * x + (gridStep // 2)
                yFill = gridStep * y + (gridStep // 2)

                t0 = time.time()
               
                c = pixdata[xFill, yFill]

                fillCount = floodfill(img, (xFill, yFill),
                          targetcolour = c,
                          newcolour = (160,128,100),
                          randomIt = iAlg,
                          maxStackDepth = 0 if iAlg == 21 else 0,
                          choices = choices,
                          variantOverride = i)
                
                t1 = time.time()

                addState(f"fillCount: {fillCount}, time taken: {str(round(t1 - t0, 2))}s", None)
                
                xFillText = xFill - (gridStep // 2) + 3
                yFillText = yFill - (gridStep // 2)
                
                textStrokeExtra(draw, xFillText, yFillText, str(i), fon, (0,0,0,255), 2)

                draw.text((xFillText, yFillText), str(i), font=fon, fill=(255,255,255,0))

                i += 1
   
        img = img.crop((0, 0, xTimeText, height))

    except Exception as e:
        img = writeImageException(e)

    return img

def screenshotFill():
    img = ""
    
    try:        
        choices = []

        stamppath = getInsertById(getParam(4))
        stamp = Image.open(stamppath)
        stamp = resizeToMinMax(stamp, maxW=200, maxH=100, minW=100, minH=50)
        
        stampTrans = None
        
        imgpath = getInsertById(getParam(4))
        img = Image.open(imgpath)        
        img = img.convert("RGBA")
        img = resizeToMinMax(img, maxW=1024, maxH=768, minW=800, minH=600)
                       
        pixdata = img.load()
                
        floodedCount = 0

        if choices == []:
            # just take the color of some random points
            jCount = 15
            jAttempts = 250
            jAttempt = 0
            
            while len(choices) < jCount and jAttempt < jAttempts:
                (x,y) = (random.randint(0, img.size[0]-1), random.randint(0, img.size[1]-1))
                c = pixdata[x,y]

                if c not in choices:
                    choices.append(c)

                jAttempt += 1
                
        draw = ImageDraw.Draw(img)                

        iAlg = 0
        global randoFillList
        
        while iAlg == 0:
            iAlg = random.choice(randoFillList)

        toflood = getPaletteFromImage(img)

        goes = 200000
        go = 0
        
        for y in range(0, img.size[1]):
            for x in range(0, img.size[0]):
                if go < goes:
                    c = pixdata[x, y]
                    ct = (c[0],c[1],c[2])

                    if ct in toflood:                    
                        floodedCount += floodfill(img, (x, y), targetcolour = c,
                                              newcolour = (0,0,0),
                                              randomIt = iAlg,
                                              compFunc=3,
                                              choices=choices,
                                                  stamp=stamp,
                                                  stampTrans=stampTrans)

                        go += 1

    except Exception as e:
        img = writeImageException(e)

    return img

def surrealColors():
    img = ""
    try:
        w = 750
        h = 800
        
        img = Image.new("RGBA", (w, h), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        y = 30
        x = 40

        sqX = 80
        sqY = 50

        xText = x + sqX + 20

        fontPath = getFont()
        fon = ImageFont.truetype(fontPath, 22) # + "YuGothic-Bold.ttf", 22)
        
        for i in range(10):
            c = getRandomColorRGB()

            iAlg = random.randint(0, 8)
            w1 = ""
            w2 = ""
            
            if iAlg == 0:
                w1 = getRandomWordSpecial("adjective")
                w2 = getRandomWordSpecial("noun")
            elif iAlg == 1:
                w1 = getRandomWordSpecial("adjective")
                w2 = getRandomWordSpecial("verb")
            elif iAlg == 2:
                w1 = getRandomWordSpecial("verb")
                w2 = getRandomWordSpecial("noun")
            elif iAlg == 3:
                w1 = getRandomWordSpecial("adjective")
                w2 = getRandomWordSpecial("noun")
            elif iAlg == 4:
                w1 = getRandomWordSpecial("positive")
                w2 = getRandomWordSpecial("jargon")
            elif iAlg == 5:
                w1 = getRandomWordSpecial("negative")
                w2 = getRandomWordSpecial("jargon")
            elif iAlg == 6:
                w1 = getRandomWord_Moby()
                w2 = getRandomWord_Moby()
            elif iAlg == 7:
                w1 = getRandomWord_Moby()
                w2 = getRandomWord_Moby("h")
            elif iAlg == 8:
                w1 = getRandomWord_Moby("V")
                w2 = getRandomWord_Moby("!")
                
            w1 = w1.title()

            if w2 != "":
                w2 = w2.title()

            if w2 != "":
                colorName = w1 + " " + w2
            else:
                colorName = w1
            
            while colorName == "":
                colorName = getRandomWordSpecial("noun")

            draw.rectangle(((x, y),(x+sqX, y+sqY)), fill=c)

            txt = colorName + " "
            txt += rgb_to_hex(c) + " (" + str(c[0]) + ", " + str(c[1]) + ", " + str(c[2]) + ")"            
            
            draw.text((xText, y + 9), txt, font=fon, fill=(0, 0, 0))

            y += 70

    except Exception as e:
        img = writeImageException(e)

    return img

def surrealPatterns():
    img = ""
    try:
        w = 800
        h = 800
        
        img = Image.new("RGBA", (w, h), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        y = 30
        x = 40

        sqX = 80
        sqY = 50

        xText = x + sqX + 20

        fontPath = getFont()
        fon = ImageFont.truetype(fontPath, 22) # + "YuGothic-Bold.ttf", 22)

        fillAlgs = []
        
        for i in range(10):
            c = getRandomColorRGB()

            iAlg = random.randint(0, 8)
            w1 = ""
            w2 = ""
            
            if iAlg == 0:
                w1 = getRandomWordSpecial("adjective")
                w2 = getRandomWordSpecial("noun")
            elif iAlg == 1:
                w1 = getRandomWordSpecial("adjective")
                w2 = getRandomWordSpecial("verb")
            elif iAlg == 2:
                w1 = getRandomWordSpecial("verb")
                w2 = getRandomWordSpecial("noun")
            elif iAlg == 3:
                w1 = getRandomWordSpecial("adjective")
                w2 = getRandomWordSpecial("noun")
            elif iAlg == 4:
                w1 = getRandomWordSpecial("positive")
                w2 = getRandomWordSpecial("jargon")
            elif iAlg == 5:
                w1 = getRandomWordSpecial("negative")
                w2 = getRandomWordSpecial("jargon")
            elif iAlg == 6:
                w1 = getRandomWord_Moby()
                w2 = getRandomWord_Moby()
            elif iAlg == 7:
                w1 = getRandomWord_Moby()
                w2 = getRandomWord_Moby("h")
            elif iAlg == 8:
                w1 = getRandomWord_Moby("V")
                w2 = getRandomWord_Moby("!")
                
            w1 = w1.title()

            if w2 != "":
                w2 = w2.title()

            if w2 != "":
                colorName = w1 + " " + w2
            else:
                colorName = w1

            while colorName == "":
                colorName = getRandomWordSpecial("noun")
            
            draw.rectangle(((x, y),(x+sqX, y+sqY)), fill=c)

            global maxFloodFillArg
            fillAlg = random.randint(1, maxFloodFillArg)

            while fillAlg in fillAlgs:
                fillAlg = random.randint(1, maxFloodFillArg)    

            fillAlgs.append(fillAlg)

            choices = getPaletteGenerated()

            floodfill(img, (x+1, y+1),
                      targetcolour = pixdata[x+1,y+1],
                      newcolour = (0,0,0),
                          randomIt = fillAlg,
                          maxStackDepth = 0,
                      choices = choices)            

            txt = colorName + " "
            #txt += "(" + str(c[0]) + ", " + str(c[1]) + ", " + str(c[2]) + ")"            
            
            draw.text((xText, y + 9), txt, font=fon, fill=(0, 0, 0))

            y += 70

    except Exception as e:
        img = writeImageException(e)

    return img

def colorItUp(img, version=2, palnum=0):
    if img.mode != "RGB":
        img = img.convert("RGB")

    if version == 1:
        palette = [random.randint(0, 255) for i in range(12)]

        p_img = Image.new('P', (16, 16))
        p_img.putpalette(palette * 64)

        conv = img.quantize(palette=p_img, dither=0)

        return conv
    else:
        try:
            intpalette = int(palnum)
            colors = getPaletteSpecific(palnum)
        except:
            colors = random.choice(fourColorPalettes)

        colorsTemp = []

        if isinstance(colors[0], str):
            for izc in colors:                    
                if izc[0] == "#":
                    zcdca = getrgb(izc) 
                else:
                    zcdca = getrgb('#' + izc)

                colorsTemp.append(zcdca)

            colors = colorsTemp
        
        global rootLogger

        for ic in colors:
            rootLogger.warning("color: " + str(ic))

        palette = [0 for i in range(len(colors) * 3)]

        p_img = Image.new('P', (len(colors) - 1, 16))

        for c in range(0, len(colors)):
            z = c * 3

            palette[z] = colors[c][0]
            palette[z+1] = colors[c][1]
            palette[z+2] = colors[c][2]

        zp = palette * (255 // len(colors) + 1)

        rootLogger.debug("zp length: " + str(len(zp)))

        if len(zp) > (255 * 3):
            zp = zp[:255 * 3]

        p_img.putpalette(zp)

        conv = img.quantize(palette=p_img, dither=0)

        return conv        

def gingerNo():
    try:
        global input_palette

        imgpath = getInsertById(getParam(4))
        img = Image.open(imgpath)
       
        return garlic(img)
        
    except Exception as e:
        img = writeImageException(e)
        
    return img

def garlic(img, hp=0):
    if img.mode in ["P", "L"]:
        img = colorItUp(img, version=1, palnum=0)

    img = img.convert("RGB")

    img = resizeToMinMax(img, maxW=1280, maxH=1024, minW=800, minH=600)

    pixdata = img.load()        

    img = img.convert("HSV")
    
    pixdata = img.load()

    if hp == 0:
        hp = random.randint(35, 220)

    global rootLogger
    rootLogger.debug("hp: " + str(hp))

    for y in range(img.size[1] - 1):
        for x in range(img.size[0] - 1):
            c = pixdata[x,y]
            z = c[0] + hp

            if z > 255: 
                z = z % 255

            pixdata[x,y] = (z,c[1],c[2])

    img = img.convert("RGBA")

    return img 

def vhsDouble():
    try:
        global input_palette

        imgpath = getInsertById(getParam(4))
        img = Image.open(imgpath)

        stampFuncs = [triangleSys,
                     atariripples,
                     rose,
                     gritty,
                     grittyer,
                     randgradient,
                     wordfilled,
                     paletteSquares,
                     generatePalette,
                     ellipseGuy,
                     colorHatch]
      
        stampf = random.choice(stampFuncs)        
        stamp = stampf()
        img = resizeToMinMax(stamp, maxW=200, maxH=100, minW=100, minH=50)

        for i in range(3):
           img = radioFill_stamp(imgpath="", img=img, stamp=stamp)
                
    except Exception as e:
        img = writeImageException(e)
        
    return img

def wordfilled(wordline="", fontSize=128, width=800, height=250, iAlg=None, spacing=15, stroke_w=3):
    try:
        global randoFillList
        if iAlg is None:
            iAlg = random.choice(randoFillList)

        img = Image.new("RGBA", (width, height), (0, 0, 0, 255))
        draw = ImageDraw.Draw(img)

        choices = getInputPalette() or [(255,255,255,255)]

        # background flood
        floodfill(
            img, (50, 50),
            targetcolour=img.getpixel((50, 50)),
            newcolour=(0, 0, 0, 255),
            randomIt=iAlg,
            maxStackDepth=0,
            choices=choices
        )

        word = (wordline or getRandomWord()).upper()
        font_path = getFont()
        font = ImageFont.truetype(font_path, fontSize)

        # helper that MEASURES with stroke accounted for
        def measure(text, fnt):
            x0, y0, x1, y1 = draw.multiline_textbbox(
                (0, 0), text, font=fnt, spacing=spacing,
                align="center", stroke_width=stroke_w
            )
            return (x1 - x0, y1 - y0)

        # shrink-to-fit (width/height minus a small padding)
        pad = 10
        tw, th = measure(word, font)
        while (tw > width - 2*pad) or (th > height - 2*pad):
            fontSize -= 2
            if fontSize < 8:
                break
            font = ImageFont.truetype(font_path, fontSize)
            tw, th = measure(word, font)

        # pick colors (avoid black) and set stroke as inverse
        def pick_nonblack():
            for _ in range(32):
                c = random.choice(choices)
                if c[:3] != (0,0,0):
                    return c
            return (255,255,255,255)

        fill_color   = pick_nonblack()
        stroke_color = getInverse(fill_color)

        # CENTER draw: anchor 'mm' = middle/middle
        cx, cy = width // 2, height // 2
        draw.multiline_text(
            (cx, cy), word, font=font, spacing=spacing, align="center",
            fill=fill_color, stroke_width=stroke_w, stroke_fill=stroke_color,
            anchor="mm"
        )

        # recompute bbox at the same anchor to crop tightly
        vpad = 6
        bb = draw.multiline_textbbox((cx,cy), word, font=font,
                                        spacing=spacing, align="center",
                                        stroke_width=stroke_w, anchor="mm")
        x0,y0,x1,y1 = bb
        y0 = max(0, y0 - vpad)
        y1 = min(height, y1 + vpad)
        img = img.crop((0, y0, width, y1))

    except Exception as e:
        img = writeImageException(e)
        
    return img

def wordfilled_any():    
    iAlg = random.randint(1, maxFloodFillArg)

    return wordfilled(iAlg=iAlg)

def wordfilled_mult(width=800, height=300):
    wf = []

    totalHeight = 0

    ySize = random.randint(4, 10)
    
    for i in range(0, ySize):
        random.seed()
        iAlg = random.randint(1, maxFloodFillArg)
        
        wl = getAHex()
        wi = wordfilled(iAlg=iAlg, wordline=wl)
        wf.append(wi)

        if wi.size[0] > width:
            width = wi.size[0]

        totalHeight += wi.size[1]  

    img = Image.new("RGBA", (width, totalHeight), "#000000")
    draw = ImageDraw.Draw(img)
    pixdata = img.load()

    x = 0
    y = 0
    
    for wts in wf:        
        img.paste(wts, (x, y))

        y += wts.size[1]

    return img

def newgrid(width=getCurrentStandardWidth(),height=getCurrentStandardHeight()):
    try:
        img = Image.new("RGBA", (width, height), "#000000")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        boxes = []

        addState(f"width: {width}, height: {height}", None)

        cols = random.randint(20, 300)
        rows = random.randint(20, 300)
        
        colWidth = width // cols
        rowHeight = height // rows

        boxes = np.zeros((cols, rows))    

        choices = getPaletteGenerated()

        zz = 0
        
        for z in np.nditer(boxes, op_flags=['readwrite']):
            zz += random.randint(1, 4)
            
            z[...] = zz

        for z in np.nditer(boxes, op_flags=['readwrite']):
            th = z[...]

            if th % 2 == 0:
                z[...] = th * -1
        
        colorPrint.print_custom_palette(190, str(boxes))

        y = 0
        iRow = 0
        for row in boxes:
            x = 0
            iCol = 0

            for col in row:
                # z = int(col)
                
                # zR = abs(z % 255)
                # zB = abs(z % 128)
                # zG = abs(z % 77)

                # if z < 0:
                #     c = (zR, zG, zB)
                # else:
                #     c = (zG, zR, zB)

                c = colorsys.hsv_to_rgb(iCol * 10.0, iRow * 0.01, 1.0)
                p = (int(c[0] * 255.0), int(c[1] * 255.0), int(c[2] * 255.0))

                #colorPrint.print_custom_palette(190, f'row: {row} col: {col} iCol: {iCol} iRow: {iRow}')

                # c = random.choice(choices)
                    
                draw.rectangle(((x, y),(x+colWidth, y+rowHeight)), fill=p)

                x += colWidth
                iCol += 1

            y += rowHeight
            iRow += 1

        img = img.crop((0, 0, x, y-rowHeight))
    except Exception as e:
        img = writeImageException(e)

    return img

def fullGradient(width=1024, height=768):
    try:
        # choose which channel will vary (0=R, 1=G, 2=B)
        varying = random.randint(0, 2)
        fixedA  = random.randint(0, 255)
        fixedB  = random.randint(0, 255)

        # gradient direction: 1 = top→bottom (0→255), 0 = bottom→top (255→0)
        down = bool(random.getrandbits(1))

        img  = Image.new("RGBA", (width, height), "#FFFFFF")
        draw = ImageDraw.Draw(img)

        # float step; use height-1 so first row is 0 and last row is 255
        denom = max(1, height - 1)
        step  = 255.0 / denom
        step  = step if down else -step

        # start value at top edge
        j = 0.0 if down else 255.0

        for y in range(height):
            jj = int(round(min(255, max(0, j))))  # clamp + round

            # build RGB where two channels are fixed and one varies
            if varying == 0:      # R varies
                c = (jj, fixedA, fixedB)
            elif varying == 1:    # G varies
                c = (fixedA, jj, fixedB)
            else:                 # B varies
                c = (fixedA, fixedB, jj)

            draw.line((0, y, width, y), fill=c, width=1)
            j += step

        return img

    except Exception as e:
        return writeImageException(e)

def simplePublic():
    img = ""

    w = getCurrentStandardWidth()
    h = getCurrentStandardHeight()
    
    try:
        img = Image.new("RGBA", (w, h), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()
    
        leImg = getInsertById(getParam(4))
        img = Image.open(leImg)

        saveToWrapper_Insert(leImg)
        
        #image_exif = img.getexif()
        #orientation = image_exif.get(ExifTags.Base.Orientation.value)

        #rootLogger.debug(orientation)

        #doTimeCheck("simplePublic tags", 2)

        #doTimeCheck(str(list(ExifTags.TAGS.keys())), 2)
        #doTimeCheck(str(list(ExifTags.TAGS.values())), 2)

        img = ImageOps.exif_transpose(img)

        img = resizeToMinMax(img, maxW=w, maxH=h, minW=640, minH=480)
        img = img.convert("RGBA")

        #ColorPrint.color_test()

    except Exception as e:
        img = writeImageException(e)

    return img

def diagonal4Way(width=getCurrentStandardWidth(), height=getCurrentStandardHeight()):
    try:
        img = ""
        
        img = Image.new("RGBA", (width, height), "#ffffff")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        (gridLineWidth, p2) = getIntParams(5)

        draw.line((0,0,width,height), fill=(0,0,0), width=gridLineWidth)
        draw.line((0,height,width,0), fill=(0,0,0), width=gridLineWidth)

        global maxFloodFillArg
        global randoFillList

        choices = getPaletteGenerated()

        pnt = [(width // 2, height // 4),
               (width - 1, height // 2),
               (width // 2, height - 1),
               (100, height // 2)]
        
        for p in pnt:
            iAlg = random.choice(randoFillList)

            x = pixdata[p[0],p[1]]

            floodfill(img, p, targetcolour = x,
                    newcolour = (0,0,0),
                    choices=choices,
                    randomIt = iAlg)

    except Exception as e:
        img = writeImageException(e)

    return img

def sigilGrid(width=None, height=None,
    cols=10, rows=10,
    margin=24, gutter=10,
    stroke=3,
    seed=None,
    palette=None,        # list of RGBA or hex strings; None -> default
    bg="#0b0e12",        # background color
    invert=False,        # swap ink/background sense
    jitter=0.10          # 0..0.4 small random offsets
):
    """Generate a grid of procedural 'sigils' (abstract glyphs) as an RGBA image."""

    try:
        if width is None:  width  = getCurrentStandardWidth()
        if height is None: height = getCurrentStandardHeight()

        rng = random.Random(seed)

        # Palette: ink + accents
        if not palette:
            palette = getPalette()

        # Canvas
        img = Image.new("RGBA", (width, height), bg if not invert else palette[0])
        draw = ImageDraw.Draw(img)

        # Cell geometry
        inner_w = max(1, width  - 2*margin)
        inner_h = max(1, height - 2*margin)
        cw = (inner_w - (cols-1)*gutter) / cols
        ch = (inner_h - (rows-1)*gutter) / rows

        def jitter_xy(cx, cy, scale=1.0):
            j = jitter * min(cw, ch) * scale
            return (cx + rng.uniform(-j, j), cy + rng.uniform(-j, j))

        def pick(n=1):
            if n == 1:
                return rng.choice(palette)
            return [rng.choice(palette) for _ in range(n)]

        def poly(draw, center, r, sides, rot=0, **kw):
            cx, cy = center
            pts = []
            for i in range(sides):
                ang = rot + (i / sides) * math.tau
                x = cx + r * math.cos(ang)
                y = cy + r * math.sin(ang)
                pts.append((x, y))
            draw.polygon(pts, **kw)

        def ring(draw, center, r, w, **kw):
            # Pillow doesn't have stroke-only ellipse fill with width for ellipse()
            # so we draw two concentric ellipses to fake a ring.
            cx, cy = center
            bbox_o = (cx-r, cy-r, cx+r, cy+r)
            bbox_i = (cx-r+w, cy-r+w, cx+r-w, cy+r-w)
            draw.ellipse(bbox_o, **kw)
            draw.ellipse(bbox_i, fill=img.getpixel((0,0)))  # erase center with bg

        def line(draw, a, b, w, fill):
            draw.line([a, b], fill=fill, width=w, joint="curve")

        def arc(draw, center, r, a0, a1, w, fill):
            cx, cy = center
            bbox = (cx-r, cy-r, cx+r, cy+r)
            draw.arc(bbox, a0, a1, fill=fill, width=w)

        def draw_sigil(draw, cell_x, cell_y, cell_w, cell_h, hseed):
            rng2 = random.Random(hseed)
            cx = cell_x + cell_w/2
            cy = cell_y + cell_h/2
            r  = 0.38 * min(cell_w, cell_h)
            ink, acc = pick(2)

            if invert:
                ink, acc = img.getpixel((0,0)), ink  # swap to draw 'carved' look

            # base: one of {ring, polygon, none}
            base_mode = rng2.randrange(3)
            if base_mode == 0:
                ring(draw, (cx, cy), r, max(2, stroke), fill=ink)
            elif base_mode == 1:
                sides = rng2.choice([3,4,5,6,8])
                poly(draw, (cx, cy), r, sides, rot=rng2.random()*math.tau, outline=ink, fill=None)
                # thicken outline
                arc(draw, (cx, cy), r, 0, 360, max(2, stroke-1), ink)

            # motif A: diagonal bar
            if rng2.random() < 0.7:
                a = jitter_xy(cx - r*0.9, cy - r*0.2, 0.6)
                b = jitter_xy(cx + r*0.9, cy + r*0.2, 0.6)
                line(draw, a, b, stroke, acc)

            # motif B: opposing arcs
            if rng2.random() < 0.4:
                zz = random.randint(30, 80) / 100

                arc(draw, (cx, cy), r*zz, rng2.uniform(-40,20), rng2.uniform(160,220), stroke, ink)
                arc(draw, (cx, cy), r*0.42, rng2.uniform(140,200), rng2.uniform(320,380), stroke, ink)

            # motif C: inner marks (cross, chevrons, dots)
            mode_c = rng2.randrange(3)
            if mode_c == 0:
                # cross
                line(draw, (cx-r*0.55, cy), (cx+r*0.55, cy), stroke, ink)
                line(draw, (cx, cy-r*0.55), (cx, cy+r*0.55), stroke, ink)
            elif mode_c == 1:
                # chevrons
                for k in (-0.35, 0, 0.35):
                    y = cy + k*r
                    line(draw, (cx-r*0.4, y), (cx, y-r*0.12), stroke, acc)
                    line(draw, (cx, y-r*0.12), (cx+r*0.4, y), stroke, acc)
            else:
                # dots
                ang1 = random.randint(90, 140)
                ang2 = random.randint(150, 350)

                for ang in (0, ang1, ang2):
                    th = math.radians(ang) + rng2.uniform(-0.2,0.2)
                    dx = math.cos(th)*r*0.62
                    dy = math.sin(th)*r*0.62
                    rr = max(2, int(stroke*0.9))
                    draw.ellipse((cx+dx-rr, cy+dy-rr, cx+dx+rr, cy+dy+rr), fill=acc)

            # motif D: corner ticks
            if rng2.random() < 0.6:
                tick = max(1, stroke-1)
                
                for ux, uy in [(-1,-1),(1,-1),(1,1),(-1,1)]:
                    px = cx + ux*r*0.86; py = cy + uy*r*0.86
                    line(draw, (px, py), (px-ux*r*0.2, py), tick, acc)

        # Draw grid
        y0 = margin
        for r_ in range(rows):
            x0 = margin
            for c_ in range(cols):
                draw_sigil(draw, x0, y0, cw, ch, (r_<<16) ^ (c_<<8) ^ rng.randint(0, 1<<30))
                x0 += cw + gutter
            y0 += ch + gutter

        # subtle vignette (nice finish)
        # darken edges a bit for mood
        vignette = Image.new("L", (width, height), 0)
        vg = ImageDraw.Draw(vignette)
        vg.ellipse((-width*0.2, -height*0.2, width*1.2, height*1.2), fill=255)
        vignette = vignette.filter(ImageFilter.GaussianBlur( max(4, int(min(width, height)*0.02)) ))        

        # composite: multiply-ish
        mask = vignette.point(lambda v: int(v*0.65))
        overlay = Image.new("RGBA", (width, height), "#000000")
        img = Image.composite(overlay, img, mask)

        return img

    except Exception as e:
        img = writeImageException(e)

    return img

def diagonalXWay(width=getCurrentStandardWidth(), height=getCurrentStandardHeight()):
    """
    Draw N radial lines (3..14 by default) from the center to the image bounds,
    then seed a flood fill in each wedge between adjacent lines.
    """
    try:
        img = Image.new("RGBA", (width, height), "#ffffff")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        # Use your param helper: first value = line width; second nudges ray count
        line_w, p2 = getIntParams(1)   # keep same call shape as diagonal4Way
        cx, cy = width // 2, height // 2
        radius = int(0.48 * min(width, height))  # safe radius toward edges

        # Choose how many rays. Skew by p2 so different presets feel different.
        n_min, n_max = 3, 14
        n_rays = max(n_min, min(n_max, 6 + (p2 % 7) + random.randint(-2, 4)))

        # Random rotation so patterns vary each time
        theta0 = random.random() * 2 * math.pi

        # Compute all end points on the rectangle boundary by ray/box intersection
        def ray_to_edge(cx, cy, dx, dy, w, h):
            # parametric t where (cx + t*dx, cy + t*dy) hits each canvas edge
            ts = []
            if dx != 0:
                ts += [(0 - cx) / dx, (w - 1 - cx) / dx]
            if dy != 0:
                ts += [(0 - cy) / dy, (h - 1 - cy) / dy]
            ts = [t for t in ts if t > 0]
            if not ts:
                return (cx, cy)
            t = min(ts)
            return (int(round(cx + t * dx)), int(round(cy + t * dy)))

        endpoints = []
        angles = []
        for i in range(n_rays):
            ang = theta0 + (2 * math.pi * i / n_rays)
            dx, dy = math.cos(ang), math.sin(ang)
            ex, ey = ray_to_edge(cx, cy, dx, dy, width, height)
            endpoints.append((ex, ey))
            angles.append(ang)

        # Draw the rays
        for (ex, ey) in endpoints:
            draw.line((cx, cy, ex, ey), fill=(0, 0, 0), width=line_w)

        # Prepare palette + algorithms
        global randoFillList
        choices = getPaletteGenerated()

        # Seed a flood fill in each wedge (mid-angle between adjacent rays)
        margin = max(6, line_w * 2)
        r = max(margin, radius - random.randint(10, 40))
        for i in range(n_rays):
            a0 = angles[i]
            a1 = angles[(i + 1) % n_rays]
            # unwrap angles so mid-angle is meaningful
            while a1 < a0:
                a1 += 2 * math.pi
            amid = (a0 + a1) * 0.5

            px = int(cx + r * math.cos(amid))
            py = int(cy + r * math.sin(amid))

            # Clamp just in case
            px = max(0, min(width - 1, px))
            py = max(0, min(height - 1, py))

            iAlg = random.choice(randoFillList)
            target = pixdata[px, py]

            floodfill(
                img,
                (px, py),
                targetcolour=target,
                newcolour=(0, 0, 0),
                choices=choices,
                randomIt=iAlg
            )

        return img

    except Exception as e:
        return writeImageException(e)

def _rand_color(choices=None):
    """
    Pick a random color.
    If `choices` is provided, it should be a list of RGB tuples (like from Pillow).
    """
    if choices and len(choices) > 0:
        return random.choice(choices)
    else:
        # fallback to full random if no palette passed
        return tuple(np.random.randint(0, 256, size=3).tolist())
    
def _make_stops(n=2, choices=[]):
    """Create 2–4 (pos, color) stops with pos in [0,1], including 0 and 1."""
    k = random.randint(n, min(4, n+2))
    pos = sorted(np.random.rand(k-2).tolist() + [0.0, 1.0])
    cols = [_rand_color(choices) for _ in range(k)]
    return list(zip(pos, cols))

def _sample_gradient(t, stops):
    """Piecewise-linear color interpolation over stops; vectorized for NumPy."""
    t = np.clip(t, 0.0, 1.0)
    out = np.zeros(t.shape + (3,), dtype=np.float32)

    for (p0, c0), (p1, c1) in zip(stops[:-1], stops[1:]):
        mask = (t >= p0) & (t <= p1)
        denom = (p1 - p0) if (p1 - p0) != 0 else 1.0
        u = ((t - p0) / denom)[mask][..., None]
        c0 = np.asarray(c0, dtype=np.float32)
        c1 = np.asarray(c1, dtype=np.float32)
        out[mask] = c0 + (c1 - c0) * u

    return out

def _tile_gradient(w, h, kind="linear", choices=[]):
    """Render one gradient tile."""
    x = np.linspace(0, 1, w, dtype=np.float32)
    y = np.linspace(0, 1, h, dtype=np.float32)
    X, Y = np.meshgrid(x, y)
    stops = _make_stops(n=random.choice([2,3,3,4]),choices=choices)

    if kind == "linear":
        theta = random.uniform(0, 2*math.pi)
        t = np.cos(theta)*X + np.sin(theta)*Y
        t = (t - t.min()) / (t.max() - t.min() + 1e-8)

    elif kind == "radial":
        cx, cy = random.uniform(0.3,0.7), random.uniform(0.3,0.7)
        r = np.sqrt((X - cx)**2 + (Y - cy)**2)
        t = r / r.max()

    elif kind == "conic":
        ang = np.arctan2(Y - 0.5, X - 0.5)   # -pi..pi
        t = (ang + math.pi) / (2*math.pi)    # 0..1

    elif kind == "banded":
        theta = random.uniform(0, 2*math.pi)
        base = np.cos(theta)*X + np.sin(theta)*Y
        base = (base - base.min()) / (base.max() - base.min() + 1e-8)
        freq = random.choice([6,8,10,12,14])
        t = 0.5*(1 + np.sin(2*math.pi*freq*base))

    elif kind == "split":
        # Two opposing ramps meeting along a random line → “knife” look
        theta = random.uniform(0, 2*math.pi)
        d = np.cos(theta)*(X-0.5) + np.sin(theta)*(Y-0.5)
        t = np.where(
            d >= 0,
            (d - d.min())/(d.max()-d.min() + 1e-8),
            (d - d.max())/(d.min()-d.max() + 1e-8))
        t = np.clip(t*0.5 + 0.5, 0, 1)

    else:
        t = X

    rgb = _sample_gradient(t, stops).astype(np.uint8)
    return Image.fromarray(rgb, mode="RGB")

def gradient_mosaic(width=768, height=768, min_cell=128, max_cell=128, seed=None):
    """
    Makes a quilt of variable-size tiles filled with random gradients.
    """
    if seed is not None:
        random.seed(seed); np.random.seed(seed)

    img = Image.new("RGB", (width, height))
    y = 0

    choices = getInputPalette()

    while y < height:
        cell_h = min(random.randint(min_cell, max_cell), height - y)
        x = 0
        while x < width:
            cell_w = min(random.randint(min_cell, max_cell), width - x)
            kind = random.choices(
                ["linear","radial","conic","banded","split"],
                weights=[3,2,2,2,2], k=1
            )[0]
            tile = _tile_gradient(cell_w, cell_h, kind=kind, choices=choices)

            # Optional: subtle diagonal punch on ~20% of tiles
            if random.random() < 0.2:
                arr = np.asarray(tile, dtype=np.int16)
                diag = np.linspace(0.9, 1.05, min(cell_w, cell_h), dtype=np.float32)
                if cell_w <= cell_h:
                    ramp = np.pad(diag, (0, cell_h - cell_w), constant_values=diag[-1])[:,None]
                else:
                    ramp = np.pad(diag, (0, cell_w - cell_h), constant_values=diag[-1])[None,:]
                ramp = ramp[:cell_h,:cell_w]
                arr = np.clip(arr * ramp[...,None], 0, 255).astype(np.uint8)
                tile = Image.fromarray(arr, "RGB")

            img.paste(tile, (x, y))
            x += cell_w
        y += cell_h
    return img
   
def numpytest():
    #mod_x = lambda x, y, z, count, choicelen: (y-x ^ int(y-(x*.05)))

    def mymod_x(x, y, z, count, choicelen):
        if count % 2 == 0:
            return int(abs(math.hypot(x, y))) ^ x                        
        else:
            return x ^ y

    def mymod_y(x, y, z, count, choicelen):
        q = count // 75
        return q % choicelen

    choices = getPaletteGenerated(paletteLength=10)

    (rgb, colorsKept) = generateNumpy(mymod_y, 1280, 1024, choices)
    img = Image.fromarray(rgb)
    
    return img

def numpyVerySimple():
    def mod_x(w, h, x, y, z, iCount, choicelen, tippingPoint):
        y2 = y - (y % 30)
        x2 = x - (x % 30)
        q = y2 * x2

        return q % choicelen

    return numpyFill(mod_x)

def numpySimple():
    def mod_x(w, h, x, y, z, iCount, choicelen, tippingPoint):
        q = (x % 255,y % 255,(x | y) % 255)        

        return q

    return numpyFill(mod_x)

def numpyFloodfill(iAlg=1):
    # --- magic happens: tdlIdFloodfill

    tippingPoint = getTippingPoint(iAlg)

    def mod_x_1(width, height, x, y, z, count, choices, tippingPoint):
        q = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        return q[0]

    def mod_x_2(width, height, x, y, z, count, choices, tippingPoint):
        # the tipping point
        #if choices == []:
        #    newcolour = primaryColors[count]
        #else:
            #newcolour = choices[count % choices]
            
        # i += 1

        # if i % tippingPoint == 0:
        #     switcher += 1

        # if choices == []:    
        #     if switcher > len(primaryColors) - 1:
        #         switcher = 0
        # else:
        #     if switcher > len(choices) - 1:
        #         switcher = 0

        return x
    
    def mod_x_47(width, height, x, y, z, count, choices, tippingPoint):
        # SATURN'S BIRTHDAY
        mod_x = int(abs(math.log1p(x) + math.log1p(y)) * 250)
        return mod_x

    def mod_x_78(width, height, x, y, z, count, choices, tippingPoint):
        # BIG SQUARES NO TOE        

        mod_y = y - (y % tippingPoint)
        mod_x = x - (x % tippingPoint)

        z = (mod_y << 4) + mod_x
        return z

    def mod_x_5001(width, height, x, y, z, count, choices, tippingPoint):
        # SATURN'S ANNIVERSARY

        xHonk = x // 2

        (p1, p2) = getIntParams()
        
        mod_x = int(abs(math.log1p(x) + math.log1p(y)) * p1)
        mod_y = int(abs(math.log1p(xHonk) - math.log1p(y)) * p2)

        return (mod_x | (mod_y << 2))

    def mod_x_5002(width, height, x, y, z, count, choices, tippingPoint):
        # SUNDAY NIGHT LAST RESORT

        xHonk = x // tippingPoint
        yHonk = y // tippingPoint

        (p1, p2) = getIntParams()

        return (xHonk * yHonk)

    def mod_y_5002(width, height, x, y, z, count, c, q):
        h, l, s = colorsys.rgb_to_hls(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)

        l_mod = y / height

        if l_mod > 1:
            l_mod = 1.0

        r, g, b = colorsys.hls_to_rgb(h, l_mod, s)
        zc = (r*255.0,g*255.0,b*255.0)

        return zc

    # TODO: make an operation that's a demo that outputs a grid with various options using math

    # TODO: change getKeptColorNew to use few choices but have a second modifier that modifies that color by sat/lightness so we can blend

    random.seed()
    choices = getPaletteGenerated(paletteLength=10)

    mod_x_touse = mod_x_1
    mod_y_touse = mod_x_1

    if iAlg == 47:
        mod_x_touse = mod_x_47
        mod_y_touse = mod_x_47
    elif iAlg == 5001:
        mod_x_touse = mod_x_5001
        mod_y_touse = mod_x_5001
    
    return numpyFill(mod_x_touse, mod_y=mod_y_touse, choices=choices, tippingPoint=tippingPoint)
   
def numpyFillStandardModY(width, height, x, y, z, count, c, q):
    return c

def numpyFill(mod_x, mod_y=numpyFillStandardModY, w=getCurrentStandardWidth(), h=getCurrentStandardHeight(), choices=getPaletteGenerated(paletteLength=4), tippingPoint=getTippingPoint(0)):
    try:
        global input_palette
            
        if len(input_palette) > 0:
            choices = input_palette

        rgb = np.zeros((h,w,3), 'uint8')

        iCount = 0
        c = (0,0,0)
        colorsKept = {}
        z = 0

        for x in range(0, w-1):
            for y in range(0, h-1):
                q = mod_x(w, h, x, y, z, iCount, len(choices), tippingPoint)

                if isinstance(q, int) or isinstance(q, str):
                    (colorsKept, c) = get_kept_color_new(colorsKept, c, choices, q)
                else:
                    (colorsKept, c) = get_kept_color_new(colorsKept, c, choices, q, override=q)

                zz = mod_y(w, h, x, y, z, iCount, c, q)

                rgb[y][x] = zz

                iCount += 1

        img = Image.fromarray(rgb)
    except Exception as e:
        img = writeImageException(e)

    return img

def numpyNormal():
    def mod_x(w, h, x, y, z, iCount, choicelen, tippingPoint):
        tippingPoint = random.randint(10, 30)
        mod_y = y - (y % tippingPoint)
        mod_x = x - (x % tippingPoint)

        z = (mod_y << 4) + mod_x                        
                        
        # | 0 | 1 |
        # |---+---|                        
        # | 2 | 3 |
        
        mod_ff_x = int(x / 25)
        mod_ff_x = mod_ff_x % 3
        
        mod_ff_y = int(y / 25)
        mod_ff_y = mod_ff_y % 3
        
        mod_z = int(abs(math.hypot(x, y)))
        mod_z = mod_z - (mod_z % tippingPoint)                            
                                
        mod_q = x + y - (x % tippingPoint) - (y % tippingPoint)
        
        if mod_ff_x == 0:
            if mod_ff_y == 0:                            
                mod_84 = z
            elif mod_ff_y == 1:
                mod_84 = mod_z
            else:
                mod_84 = x ^ y
        elif mod_ff_x == 1:
            if mod_ff_y == 0:
                mod_84 = mod_q
            elif mod_ff_y == 1:
                mod_84 = x & y
            else:
                mod_84 = x | y
        else:
            if mod_ff_y == 0:
                mod_84 = mod_q - mod_z
            elif mod_ff_y == 1:
                mod_84 = mod_q & mod_z
            else:
                mod_84 = mod_q | mod_z

        return mod_84

    return numpyFill(mod_x)

def xThenY(w=1024,h=1024):
    try:
        choices = getInputPalette()

        addState(f'choices: {choices}')

        rgb = np.zeros((h,w,3), 'uint8')

        c = (0,0,0)
        colorsKept = {}

        c = random.choice(choices)

        for x in range(0, w-1):
            for y in range(0, h-1):
                if not rgb[y,x].any():
                    rgb[y, x] = c            
                    c = random.choice(choices)

        # for x in range(0, w-1):
        #     for y in range(0, h-1):
        #         q = random.randint(0, 7)
        #         override = None

        #         if isinstance(q, int) or isinstance(q, str):
        #             override = q

        #         (colorsKept, c) = get_kept_color_new(colorsKept, c, choices, q, override=None)
        #         rgb[y][x] = c

        #         iCount += 1

        img = Image.fromarray(rgb)
        
        addState(f'colorsKept: {colorsKept}')

    except Exception as e:
        img = writeImageException(e)

    return img

def generateAnimNumpy():
    mod_x = lambda x, y: (x-y ^ int(y-(x*.05)))

    frames = []

    choices = getPaletteGenerated(paletteLength=10)
    colorsKept = {}   

    def localxy(x, y, roundNum, count, choicelen):
        tippingPoint = 10
        (mod_x, mod_y) = get_grid_vals(x, y, tippingPoint)
        mod_z = (y ^ x) & (mod_y | mod_x) + roundNum        
        return mod_z

    def mymod_y(x, y, roundNum, count, choicelen):
        tippingPoint = (2 * roundNum) + 10
        q = count // tippingPoint
        return q % choicelen

    roundNum = 0

    for n in range(10):
        (rgb, colorsKept) = generateNumpy(mymod_y, 1024, 768, choices, colorsKept, roundNum)
        roundNum += 1
        frame = Image.fromarray(rgb)

        # Saving/opening is needed for better compression and quality
        fobj = BytesIO()
        frame.save(fobj, 'GIF')
        frame = Image.open(fobj)
        frames.append(frame)

    animated_gif = BytesIO()
    frames[0].save(animated_gif,
                format='GIF',
                save_all=True,
                append_images=frames[1:],
                delay=0.05,
                loop=0)
    
    animated_gif.seek(0)
    ani = Image.open(animated_gif)

    return ani   

def generateNumpy(mod_x, w=1024, h=768, choices=[], colorsKept={}, roundNum=0, rgb=0):
    prerendered = rgb == 0

    if prerendered:
        rgb = np.zeros((h,w,3), 'uint8')

    if choices == []:
        choices = getPaletteGenerated()

    c = random.choice(choices)

    if not prerendered:
        count = 0

        for x in range(w-1):
            for y in range(h-1):            
                (colorsKept, c) = get_kept_color(colorsKept, c, choices, mod_x(x,y,roundNum,count,len(choices)))
                rgb[y][x] = [c[0], c[1], c[2]]
                count += 1

    return (rgb, colorsKept)

def opencv_removeBG_op(img="", limitsLower=[200, 200, 200], limitsUpper=[255,255,255], kernelEllipse=(20,20)):
    import cv2
    
    if img == "":    
        imgPath = getInsertById(getParam(4))
        img = cv2.imread(imgPath)
    else:
        # input is PIL - convert
        img = img.convert("RGB")
        img = toImgOpenCV(img)        
    
    # Read image    
    hh, ww = img.shape[:2]

    # threshold on white
    # Define lower and uppper limits
    lower = numpy.array(limitsLower)
    upper = numpy.array(limitsUpper)

    # Create mask to only select black
    thresh = cv2.inRange(img, lower, upper)

    # apply morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernelEllipse)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # invert morp image
    mask = 255 - morph

    # apply mask to image
    result = cv2.bitwise_and(img, img, mask=mask)

    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    im_pil = Image.fromarray(result)
    mask_pil = Image.fromarray(mask)

    cv2.destroyAllWindows()

    return (im_pil, mask_pil, mask)

def opencv_removeBG(img=""):
    (im_pil, mask_pil, mask) = opencv_removeBG_op(img)
    return im_pil
    
def opencv_process(img):
    import cv2

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 2)
    img_canny = cv2.Canny(img_blur, 50, 9)
    img_dilate = cv2.dilate(img_canny, np.ones((4, 2)), iterations=11)
    img_erode = cv2.erode(img_dilate, np.ones((13, 7)), iterations=4)

    return cv2.bitwise_not(img_erode)

def opencv_get_contours(img, c = (44, 88, 128)):
    import cv2

    img = toImgOpenCV(img)

    contours, _ = cv2.findContours(opencv_process(img), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = max(contours, key=cv2.contourArea)
    cv2.drawContours(img, [cv2.convexHull(cnt)], -1, c, 2)

    return img

def opencv_inpaint():
    import cv2

    imgPath = getInsertById(getParam(4))
    
    img = Image.open(imgPath).convert("RGB")

    img = resizeToMinMax(img, maxW=1024, maxH=768, minW=640, minH=480)

    stampFuncs = getSafeFuncs()      
    stampf = random.choice(stampFuncs)        
    mask = stampf().convert("L")

    #mask = atariripples().convert("L")
    #mask = img.transpose(Image.FLIP_LEFT_RIGHT).convert("L")

    #mask = img.copy().convert("L")
    #img = imageop_cornerHarris(img).convert("RGB")

    #mask = Image.open(imgPath2).convert("L")

    #mask = cv2.imread(imgPath2, 0)

    #open_cv_image = numpy.array(img) 

    (img, mask) = resizeToMatch(img, mask)

    img = numpy.array(img)
    mask = numpy.array(mask)

    dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)

    cv2.destroyAllWindows()

    im_pil = Image.fromarray(dst)

    return im_pil

def opencv_canny():
    im_pil = ""
    
    try:
        import cv2

        img = None
        
        while img is None:
            imgPath = getInsertById(getParam(4))
            img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
     
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        gray = cv2.GaussianBlur(gray, (7,7), 1.5)
        gray = cv2.Canny(gray, 0, 50)

        im_pil = Image.fromarray(gray)

        im_pil = resizeToMinMax(im_pil, maxW=1024, maxH=768, minW=640, minH=480)

    except Exception as e:
        im_pil = writeImageException(e)

    cv2.destroyAllWindows()

    return im_pil

def opencv_canny_inv():
    im_pil = ""
    
    try:
        import cv2

        img = None

        while img is None:
            imgPath = getInsertById(getParam(4))        
            img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
     
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        gray = cv2.GaussianBlur(gray, (7,7), 1.5)
        gray = cv2.Canny(gray, 0, 50)

        im_pil = Image.fromarray(gray)

        im_pil = resizeToMinMax(im_pil, maxW=1024, maxH=768, minW=640, minH=480)

        im_pil = im_pil.convert("RGB")
        im_pil = ImageChops.invert(im_pil)
        im_pil.load()

    except Exception as e:
        im_pil = writeImageException(e)

    cv2.destroyAllWindows()

    return im_pil

def toImgOpenCV(imgPIL): # Conver imgPIL to imgOpenCV
    i = np.array(imgPIL) # After mapping from PIL to numpy : [R,G,B,A]
                         # numpy Image Channel system: [B,G,R,A]
    red = i[:,:,0].copy(); i[:,:,0] = i[:,:,2].copy(); i[:,:,2] = red;
    return i; 

def opencv_erosion():
    import cv2

    imgPath = getInsertById(getParam(4))
    
    imgPIL = Image.open(imgPath).convert("RGB")

    img = toImgOpenCV(imgPIL)

    #img = cv2.imread(imgPath, cv2.IMREAD_COLOR)

    zrs = random.randint(4, 7)

    kernel = np.zeros((zrs, zrs), np.uint8)
    
    for z in np.nditer(kernel, op_flags=['readwrite']):
        zz = random.randint(0, 1)        
        z[...] = zz
 
    #kernel = np.ones((2,2),np.uint8)
    mind = random.randint(5, 15)
    erosion = cv2.erode(img, kernel, iterations = mind)

    img = cv2.cvtColor(erosion, cv2.COLOR_BGR2RGB)  

    cv2.destroyAllWindows()

    im_pil = Image.fromarray(img)

    im_pil = resizeToMinMax(im_pil, maxW=1024, maxH=768, minW=640, minH=480)
    imgPIL = resizeToMinMax(imgPIL, maxW=1024, maxH=768, minW=640, minH=480)

    outimgs = resizeToMatch(im_pil.convert("RGBA"), imgPIL.convert("RGBA"))
    img1 = outimgs[0]
    img2 = outimgs[1]    

    img = Image.blend(img1, img2, 0.4)

    return img

def opencv_gradient():
    import cv2

    imgPath = getInsertById(getParam(4))
     
    img = cv2.imread(imgPath, cv2.IMREAD_COLOR)

    kernel = np.ones((5,5),np.uint8)

    gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

    img = cv2.cvtColor(gradient, cv2.COLOR_BGR2RGB)  

    im_pil = Image.fromarray(img)

    im_pil = resizeToMinMax(im_pil, maxW=1024, maxH=768, minW=640, minH=480)

    cv2.destroyAllWindows()

    return im_pil

# TODO: make a function to rotate an image 360deg, animated

def generateAnim(N=150, draw_func=None):
    if draw_func is None:
        c = getRandomColorRGB()
        draw_func = lambda draw, x, y: draw.ellipse((x, y, x+40, y+40), c)

    frames = []

    for n in range(N):
        frame = Image.new("RGB", (800, 600), (25, 25, 25))
        draw = ImageDraw.Draw(frame)
        x, y = frame.size[0]*n/N, frame.size[1]*n/N

        draw_func(draw, x, y)

        # Saving/opening is needed for better compression and quality
        fobj = BytesIO()
        frame.save(fobj, 'GIF')
        frame = Image.open(fobj)
        frames.append(frame)

    animated_gif = BytesIO()
    frames[0].save(animated_gif,
                format='GIF',
                save_all=True,
                append_images=frames[1:], # Pillow >= 3.4.0
                delay=0.2,
                loop=0)
    
    animated_gif.seek(0)
    ani = Image.open(animated_gif)

    return ani

# ------------ lemma shit ----------------------- BLADEAPPLE LABIUM @~-------- 

def blend(a, b):
    """
    Make a fused, brand-like portmanteau from two roots.
    Strategy:
      1) Try a maximal 2-4 char overlap of a's suffix & b's prefix.
      2) Else drop duplicate boundary letters (..xx + x..) -> (..x..)
      3) Else vowel splice (trim trailing vowel run of a or leading of b)
    Returns fused single token.
    """
    a, b = clean_token(a), clean_token(b)
    if not a or not b:
        return a + b

    # 1) overlap
    for k in range(4, 1, -1):
        if len(a) >= k and len(b) >= k and a.endswith(b[:k]):
            return a + b[k:]

    # 2) dedupe boundary
    if a[-1] == b[0]:
        return a + b[1:]

    # 3) vowel splice (tidy double vowels)
    a_trim = re.sub(r"[aeiouy]+$", "", a)
    b_trim = re.sub(r"^[aeiouy]+", "", b)
    if a_trim and b_trim:
        return a_trim + b_trim

    return a + b

def clean_token(w):
    w = w.lower().replace("_", "")
    w = re.sub(r"[^a-z]", "", w)
    if len(w) < 3:
        return ""
    # filter super-generic junk
    if w in {"thing","object","device","stuff","entity","unit","matter"}:
        return ""
    return w

def _synsets(term, pos="n"):
    import wn
    wn.config.allow_multithreading = True
    WN_OBJ = wn.Wordnet("oewn:2024")

    # try requested POS, then fallbacks
    pos_list = [pos] if pos else [None]
    pos_list += [p for p in ("n","v","a","r","s") if p != pos]
    for p in pos_list:
        ss = wn.synsets(term, pos=p, lexicon="oewn:2024")
        if ss:
            return ss
    return []

def _lemmas(s):
    """
    Extract surface forms from a wn synset `s` across API variants:
    - If s.lemmas() gives strings, use them directly.
    - Else, try lemma.form / written_form / lemma.
    - Also fall back to s.words(): word.lemma() / word.forms().
    """
    out = []

    # 1) s.lemmas() — in your env this returns strings
    try:
        Ls = s.lemmas()
        for L in Ls:
            if isinstance(L, str):
                out.append(L)
            else:
                # other wn variants: lemma objects
                for attr in ("form", "written_form", "lemma"):
                    if hasattr(L, attr):
                        v = getattr(L, attr)
                        v = v() if callable(v) else v
                        if isinstance(v, str):
                            out.append(v)
                            break
    except Exception:
        pass

    # 2) s.words() — grab word.lemma() and word.forms()
    try:
        for W in s.words():
            # word.lemma (attr or method) → string
            v = getattr(W, "lemma", None)
            v = v() if callable(v) else v
            if isinstance(v, str):
                out.append(v)
            # word.forms() → list[str]
            try:
                forms = W.forms()
                for f in forms:
                    if isinstance(f, str):
                        out.append(f)
            except Exception:
                pass
    except Exception:
        pass

    return out

def _neighbors(s):
    rels = []
    # prefer hyponyms; if none, try a few others so we don’t dead-end
    for rel in ("hyponyms","hypernyms","meronyms","holonyms","similar_tos","also_sees"):
        try:
            fn = getattr(s, rel)
            rels.extend(fn() if callable(fn) else [])
        except Exception:
            pass
    return rels

def _clean(w: str) -> str:
    w = w.lower().replace("_","")
    w = re.sub(r"[^a-z]", "", w)
    if len(w) < 3: return ""
    if w in {"thing","object","device","stuff","entity","unit","matter"}: return ""
    return w

# ---------- verbose harvester ----------
def harvest_lemmas_v2(seed_terms, pos="n", depth=2, max_terms=1000, max_synsets=8000, debug=False):
    # seed synsets
    queue = []
    for t in seed_terms:
        ss = _synsets(t, pos=pos)
        if debug: print(f"seed '{t}' -> {len(ss)} synsets")
        queue.extend(ss)

    if not queue and debug:
        print("No synsets found for the given seeds (even with POS fallbacks).")
        return set()

    seen_syn = set()
    results = set()
    visited = 0
    d = 0

    while queue and d <= depth and len(results) < max_terms and visited < max_synsets:
        if debug: print(f"depth {d}: queue={len(queue)} results={len(results)} visited={visited}")
        next_queue = []
        for s in queue:
            sid = repr(s)
            if sid in seen_syn: continue
            seen_syn.add(sid); visited += 1

            # collect lemmas
            for lemma in _lemmas(s):
                w = _clean(lemma)
                if w:
                    results.add(w)
                    if len(results) >= max_terms: break
            if len(results) >= max_terms: break

            # traverse
            next_queue.extend(_neighbors(s))

        queue = next_queue
        d += 1

    if debug: print(f"done: results={len(results)} visited={visited} depth_reached={d-1}")
    return results

def debug_one_synset(term="computer", pos="n"):
    ss = _synsets(term, pos=pos)
    rootLogger.debug(f"{term}: {len(ss)} synsets")
    
    if not ss: return
    
    s = ss[0]
    
    rootLogger.debug("dir(s) sample:" + str([a for a in dir(s) if not a.startswith("_")][:20]))

    try:
        Ls = s.lemmas()
        rootLogger.debug("lemmas count:" + str(len(Ls)))
        if Ls:
            L0 = Ls[0]
            rootLogger.debug("lemma attrs:"+ str([a for a in dir(L0) if not a.startswith("_")]))
    except Exception as e:
        rootLogger.debug("lemmas() error:"+ e)
    try:
        Ws = s.words()
        rootLogger.debug("words count:"+ str(len(Ws)))
        if Ws:
            W0 = Ws[0]
            rootLogger.debug("word attrs:"+ str([a for a in dir(W0) if not a.startswith("_")]))
    except Exception as e:
        rootLogger.debug("words() error:"+ e)

DEFAULT_OCCULT_SEEDS = [
    "magic", "sorcery", "enchantment", "ghost", "shadow", "aether",
    "spirit", "ritual", "hex", "demon", "witchcraft", "omen"
]
DEFAULT_TECH_SEEDS = [
    "technology", "computer", "algorithm", "network", "quantum",
    "nanotechnology", "signal", "encryption", "robot", "cybernetics",
    "hardware", "software"
]

OCCULT_VERBS = [
    "summons", "binds", "shrouds", "unmoors", "haunts",
    "etches", "hexes", "conjures", "fractures", "entangles",
    "devours", "distills", "distorts", "unravels"
]
TECH_OBJECTS = [
    "signals", "firewalls", "neural lattices", "quantum states",
    "memory cores", "datastreams", "sensors", "protocols",
    "prediction engines", "control loops", "feedback grids"
]
TECH_VERBS = [
    "overclocks", "decrypts", "compiles", "patches",
    "rethreads", "reprograms", "re-indexes", "injects"
]
OCCULT_OBJECTS = [
    "shadows", "oaths", "echoes", "sigils", "arcana",
    "ghostlight", "omens", "voidsong", "nightglass"
]

def tagline():
    pattern = random.choice([
        "{occ_v} {tech_o}.",
        "{tech_v} the {occ_o}.",
        "bends {tech_o} with {occ_o}.",
        "unspools {tech_o}, leaving {occ_o}.",
        "carves {occ_o} through {tech_o}."
    ])
    return pattern.format(
        occ_v=random.choice(OCCULT_VERBS),
        tech_o=random.choice(TECH_OBJECTS),
        tech_v=random.choice(TECH_VERBS),
        occ_o=random.choice(OCCULT_OBJECTS),
    )

def build_lexicons(
    a_seeds=DEFAULT_OCCULT_SEEDS,
    b_seeds=DEFAULT_TECH_SEEDS,
    depth=1,
    max_terms=1200
):
    occult = harvest_lemmas_v2(a_seeds, pos="n", depth=depth, max_terms=max_terms)
    tech   = harvest_lemmas_v2(b_seeds,   pos="n", depth=depth, max_terms=max_terms)

    # Bias the tech list a bit toward snappy morphemes
    # tech |= {"core","plex","node","drive","ware","mesh","sync","byte","stream","grid","forge","shade","pulse","weave","shard","lock","flux","crypt","neuro","quantum","nano"}
    # occult |= {"void","wraith","aether","shade","hex","soul","myth","specter","eldritch","wyrm","rune","geist","crypt","omen"}

    # Filter to nice, brandable stems
    def keep(w):
        return (3 <= len(w) <= 10) and re.search(r"[aeiouy]", w) and w not in {"quantum"}  # 'quantum' is great but long as a suffix
    return sorted(filter(keep, occult)), sorted(filter(keep, tech))

def generate_names(n=20, groupA=None, groupB=None, seed=None):
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()

    out = []

    for _ in range(n):
        a = random.choice(groupA)
        b = random.choice(groupB)

        # also try swapping order sometimes; pick the better-looking result
        name1 = blend(a, b)
        name2 = blend(b, a)
        name = min((name1, name2), key=len) if abs(len(name1) - len(name2)) <= 2 else random.choice([name1, name2])

        # Titlecase but preserve camel-like brand feel
        pretty = name[0].upper() + name[1:]
        out.append({"name": pretty, "tagline": tagline()})

    return out

def wordGridWordNet(wordline="", fontSize=36, fontPath=""):
    # pip install wn first
    # then: python3 -m wn download oewn:2024

    def eg(word):
        import wn
        wn.config.allow_multithreading = True
        
        from wn import morphy
        m = morphy.Morphy()

        en = wn.Wordnet('oewn:2024', lemmatizer=m)

        ss = en.synsets(word)        

        total = ""

        if len(ss) > 0:
            for sf in ss:                
                sd = sf.definition()
                total = total + sd + "<br />\t"

            return str(total)
        
        return "?"
    
    extra_html = """<style type="text/css">
    #output-text li { 
        border-bottom: 3px solid #cccccc; 
        padding-bottom: 14px;
    }
    </style>
    """
    return wordGridGeneral(wordline, fontSize, fontPath, eg, word_count=24, extra_html=extra_html)

def wordGridHexcult(wordline="", fontSize=36, fontPath=""):
    def eg(word):
        occult, tech = build_lexicons(DEFAULT_OCCULT_SEEDS, DEFAULT_TECH_SEEDS, depth=1)
        powers = generate_names(1, occult, tech, seed=None)
        p = powers[0]

        return f'{p["name"]} — {p["tagline"]}'    
    
    return wordGridGeneral(wordline, fontSize, fontPath, eg, word_count=36)

def wordGridLemmaWordages(wordline="", fontSize=36, fontPath=""):
    def eg(word):
        z = harvest_lemmas_v2([word], pos=None, depth=1, max_terms=1200)

        total = ""

        for t in list(sorted(z)):
            total += t + ", "

        total = total[:-2]

        return total

    return wordGridGeneral(wordline, fontSize, fontPath, eg, word_count=24)

def wordGridHexcult2(wordline="", fontSize=36, fontPath=""):
    def eg(word):
        occult, tech = build_lexicons(["cheer","wave","salivate","bar","puff","render","rabbit","pet","poof","fruit"], 
                                      ["pixel", "diabolical", "bootleg", "official", "scatterbrain", "tomato", "voice"], depth=1)
        powers = generate_names(1, occult, tech, seed=None)
        p = powers[0]

        return f'{p["name"]}—'    
    
    return wordGridGeneral(wordline, fontSize, fontPath, eg, word_count=36)

def wordGridHexLatest(wordline="", fontSize=36, fontPath=""):
    input_a = [getRandomWord()]
    input_b = [getRandomWord()]

    return wordGridHexetidine(wordline, fontSize, fontPath, input_a, input_b)

def wordGridHexetidine(wordline="", fontSize=36, fontPath="", input_a=[getRandomWord(), getRandomWord()],input_b=[getRandomWord(), getRandomWord()]):
    """
    p1: preset (default/random=0, max=8)
    """

    def eg(word):
        pass

    p1 = getParam(0)
    p1 = int(p1) if p1.isdecimal() else 0

    p2 = getParam(1)
    p2 = int(p2) if p2.isdecimal() else 5

    depth = p2

    if p1 == 1:
        input_a = ["person","place","thing","portion","serving"]
        input_b = ["idea","plan","partake"]
    elif p1 == 2:
        input_a = ["stock", "yard", "expected", "bed"]
        input_b = ["bar","pub","stock","thimble","hot rod","bramble","barrel"]
    elif p1 == 3:
        input_a = ["riders","too","collection","substantial","sly"]
        input_b = ["spell","cast","demon","goo","nightmare"]    
    elif p1 == 4:
        input_a = ["watch","born","planet","earth","I"]
        input_b = ["rotated","man","comes","first","increasing","signs", "open", "your", "eyes"]
    elif p1 == 5:
        input_a = ["exigent","execreble","urgent","acute","dire","exit","interpret","radicalize","weiner","char","booking","charge","isometric","numinous"]
        input_b = ["midnight","transition","eternity","infinity","unproven","proof","alarm","chorus","nocturnal"]
        depth = 2
    elif p1 == 6:
        input_a = ["bright","shiny","yellow"]
        input_b = ["star","sun", "sol"]
    elif p1 == 7:
        input_a = ["dinker","piece","junk","testes"]
        input_b = ["tinker","drinker","zing","holder"]
        depth = 4
    elif p1 == 8:
        input_a = ["fart","wind","booger"]
        input_b = ["poop","anus","scat"]
    elif p1 == 0:
        input_a = [getRandomWord(),getRandomWord(),getRandomWord()]
        input_b = [getRandomWord(),getRandomWord(),getRandomWord()]

    a, b = build_lexicons(input_a, input_b, depth=depth)        
    
    random.seed()
    actual_words = []

    for x in range(48):
        ga = random.choice(a)
        gb = random.choice(b)

        z = f'{ga.upper()} {gb.upper()}'

        if p1 == 2:
            z = f'THE {ga.upper()} AND {gb.upper()}'

        actual_words.append(z)
    
    return wordGridGeneral(wordline, fontSize, fontPath, eg, word_count=48, actual_words=actual_words, lemmas=(input_a, input_b))

def getAHex(lexa=["the","one","this","image"], lexb=["nickname","slogan","script"]):
    a, b = build_lexicons(lexa, lexb, depth=10)
    
    random.seed()

    ga = random.choice(a)
    gb = random.choice(b)

    return f'{ga.upper()} {gb.upper()}'

# SPUTTER DECORATION

def ollamaHelloWorld():
    global ollamaHost
    
    import ollama
    from ollama import Client

    client = Client(host=ollamaHost)
    response = client.chat(model='llama2', messages=[
        {
            'role': 'user',
            'content': 'Hello! Please describe some things you can do.'
        }
    ])

    outputText = "<div class='output-text-llm' id='output-text'>"
    outputText += f"{response['message']['content']}"
    outputText += "</div>"

    return outputText

def ollamaCraft(model='llama2'):
    global ollamaHost

    import ollama
    from ollama import Client

    currentEmoji = '🌈 Rainbow + 🔥 Flame'

    outputText = r""
    outputText += "<div class='output-text-llm result-container-inner'>"
    outputText += f"user: {currentEmoji}<br /></div>"

    client = Client(host=ollamaHost)
    response = client.chat(model=model, messages=[
        {
            "role": "system",
            "content": "You are Infinite Craft\n\nwhen you are given 2 text with emoji.\n\nGive something back that makes sense with relating text with emoji\n\nfor example: \"\ud83c\udf0d Earth\" + \"\ud83d\udca7 Water\" could result in \"\ud83c\udf31 Plant\"\nor \"\ud83d\udca7 Water\" + \"\ud83d\udd25 Fire\" could result in \"\ud83d\udca8 Steam\"\nYou need to create these depending on input. The input format will be: \"emoji Text + emoji Text\"\nAnd your result should be \"emoji Text\" always.\nAnd always try to keep the emoji as Closely related to the text as possible and stay consistent.\nsome examples:\n\"\ud83c\udf2c\ufe0f Wind + \ud83c\udf31 Plant\" = \ud83c\udf3c Dandelion\n\"\ud83c\udf0d Earth + \ud83d\udca7 Water\" = \ud83c\udf31 Plant\n\"\ud83c\udf0d Earth + \ud83d\udd25 Fire\" = \ud83c\udf0b Lava\n\"\ud83c\udf0d Earth + \ud83d\udd25 Fire\" = \ud83c\udf0b Lava\n\"\ud83c\udf0b Lava + \ud83c\udf0b Lava\" = \ud83c\udf0b Volcano\n\"\ud83d\udca7 Water + \ud83c\udf2c\ufe0f Wind\" = \ud83c\udf0a Wave\n\nAnd the emoji and text can be anything, it is not limited to the example i gave, make ANYTHING and always return a response in the given format\n",
        },
        {"role": "user", "content": f'\ud83c\udf0d Earth + \ud83d\udca7 Water'},
        {"role": "assistant", "content": f'\ud83c\udf31 Plant'},
        {"role": "user", "content": "\ud83d\udca8 Wind + \ud83c\udf31 Plant"},
        {"role": "assistant", "content": "\ud83c\udf3c Dandelion"},
        {"role": "user", "content": "\ud83c\udf0d Earth + \ud83d\udd25 Fire"},
        {"role": "assistant", "content": "\ud83c\udf0b Lava"},
        {"role": "user", "content": "\ud83c\udf0b Lava + \ud83c\udf0bLava"},
        {"role": "assistant", "content": "\ud83c\udf0b Volcano"},
        {"role": "user", "content": "\ud83d\udca7 Water + \ud83d\udca8 Wind"},
        {"role": "assistant", "content": "\ud83c\udf0a Wave"},
        {"role": "user", "content": "\ud83c\udfd4\ufe0f Mountain + \u2744\ufe0f Snow"},
        {"role": "assistant", "content": "\ud83c\udf28\ufe0f Avalanche"},
        {"role": "user", "content": "\ud83c\udf1e Sun + \u2614 Rain"},
        {"role": "assistant", "content": "\ud83c\udf08 Rainbow"},
        {"role": "user", "content": currentEmoji}
    ])

    # Please give me a table of 78 categories. List a column for the category name. Each of these categories is a color or group of colors of some kind. Please add a description column describing the category. Add an emoji column and pick the single emoji that is most relevant for this category.

    msg = response['message']['content']

    outputText += "<div class='output-text-llm result-container-inner' id='output-text'>"
    outputText += msg.replace("\n","<br />")
    outputText += "</div>"

    return outputText

def llmDescribeImage():
    global ollamaHost

    import ollama
    from ollama import Client

    pathImage = getInsertById(getParam(4))

    img = Image.open(pathImage) 
    img.load()
    img = img.convert("RGBA")

    [output, contentType, saveFormat] = writeImageToBytes(img, "PNG")
    img_str = base64.b64encode(output.getvalue())

    client = Client(host=ollamaHost)
    response = client.chat(model='llava', messages=[
    {
        'role': 'user',
        'content': 'describe this image:',
        'images': [pathImage]
    },
    ])

    outputText = "<div class='output-text-llm' id='output-text'>"
    outputText += f"<img src=\"data:image/png;base64,{img_str.decode('ascii')}\" />"
    outputText += f"{response['message']['content']}"
    outputText += "</div>"

    return outputText

def ollamaBase(p1, p2, model="gpt-oss:20b"):
    global ollamaHost

    import ollama
    from ollama import Client

    outputText = ""

    outputText += "<div style='margin-top:10px;margin-bottom:10px;' class='output-text-llm'>system prompt: " + p1 + "<br />"
    outputText += "user: " + p2 + "<br /></div>"

    client = Client(host=ollamaHost)
    response = client.chat(model=model, messages=[
        {
            'role': 'system',
            'content': p1
        },
        {
            'role': 'user',
            'content': p2
        }
    ])

    msg = response['message']['content']

    outputText += "<div class='output-text-llm' id='output-text'>"
    outputText += msg.replace("\n","<br />")
    outputText += "</div>"

    return outputText

def ollamaSimple():
    p1 = getParam(0)
    p2 = getParam(1)

    outputText = ""

    if p1 == "":
        p1 = "Act as a system language classifier or function that determines what a phrase means. Give a possible meaning of the following. Do not add a preamble or mention being a language model."

    if p2 == "":
        p2 = getDecree("","")

    return ollamaBase(p1, p2)

def ollamaBored():
    possiblePrompts = ["Act as entertainment, giving the user a list of 5 interesting facts. If the user provides a prompt, use the prompt as the topic for the facts. Format the output as HTML.",
                       "Act as an insult comic. You are entertaining the user. Come up with a creative insult for the user based on their input. Be brief. Make it one sentence. Do not worry about being offensive, as the user is expecting this.",
                       "Act as the user's employee. Your boss is asking for input on the user's prompt. Be amazing, but keep it to a maximum of one sentence as your boss's time is very limited. Be blunt and direct, and keep it relevant to the user's prompt.",
                       "Act as the user's encyclopedia. Unfortunately, you have some glitches, and sometimes your output is strange or weird. Do not be cheeky: being broken upsets you. Attempt to be professional, but fail unintentionally. Tell the user about the entry for their prompt. Limit the output length to a paragraph.",
                       "Act as a thingiemabob. Do something cool and unexpected, because the user is bored. If the user provides a prompt, pretend that it was your idea for input to the thingiemabob.",
                       "Act as a random word generator. Given this list of previously generated words, generate the next 10 words in the list. Format the output as HTML, and the words as an HTML list. If the user provides a prompt, use that as the list of words instead. The list is: Cryptomeld, Voidweave, Nexthex, Soulforge, Neuroshade, Chromebane, Synthblood, Wraithwire, Cortexhex, Viraluxe, Quantumwhisper, Holothren, Nanoshroud, Echodark, Aetherpulse",
                       "Act as a style taste critic. Generate a table of the words given by the user, listing your scores for at least 7 categories, including coolness. Format the output as an HTML table, like so, but with all 7 categories: <table><tr><td>word</td><td>Category 1</td></tr></table>.",
                       "Act like a professional but fun teacher in their 40s. Explain how something works using only analogies a 5 year old will understand. The user will provide a prompt for what they would like explained.",
                       "Act like an online slang dictionary. Provide the definition for the user's prompt as if it is a slang word or phrase. Respond seriously, as though the input is silly, you are a serious machine and want to provide informative and useful output.",
                       "Act as an amorphous blob who only speaks blob. Provide your opinion of the user's prompt.",
                       "You are a system called TDLDL. You generate images and random phrases. Do your thing based on the user's input.",
                       "Act as a symbologist. You have PhDs in religious symbology and one in languages. Explain and analyze the user's prompt as if it were the meaning of a newly discovered symbol or sigil. Make up the entity it represents. Be terse and professional, but visibly excited. Limit your output to one paragraph."]

    p1 = getParam(0)

    if p1 != "" and p1.isdecimal():
        if len(possiblePrompts) > int(p1):
            p1 = possiblePrompts[int(p1)]
        else:
            p1 = random.choice(possiblePrompts)
    else:
        p1 = random.choice(possiblePrompts)

    p2 = getParam(1)

    if p2 == "":
        p2 = getDecree("","")

    return ollamaBase(p1, p2)

def ollamaPalette():
    global ollamaHost

    import ollama
    from ollama import Client

    client = Client(host=ollamaHost)
    response = client.chat(model='llama2', messages=[
        {
            'role': 'system',
            'content': "Act as an assistant, returning a random color palette of 5 to 6 colors in hex format. Give your palette a name, and include this name as a property in the output. Use JSON as the output format. Do not add a preamble or speak to the user. Simply output the JSON. You may add your opinion or thoughts as an additional JSON property. Please also add why you chose the palette name as an explanation property."
        },
        {
            'role': 'user',
            'content': "Do the needful"
        }
    ])

    outputText = "<div class='output-text-llm' id='output-text'>"
    outputText += f"{response['message']['content']}"
    outputText += "</div>"

    return outputText

def ollamaSummarize():
    global ollamaHost

    import ollama
    from ollama import Client

    pathFile = '/mnt/u/My Webs/tooinside/universemdwiki/anamneses/memoir-01.md'

    with open(pathFile) as f: 
        s = f.read()

    colorPrint.print_custom_palette(191, s)

    client = Client(host=ollamaHost)
    response = client.chat(model='gpt-oss:20b', messages=[
        {
            'role': 'system',
            'content': 'Summarize the text as a chapter of fiction. List major plot points, any references, and unanswered questions.'
        },
        {
            'role': 'user',
            'content': s
        }
    ])

    outputText = "<div class='output-text-llm' id='output-text'>"
    output = response['message']['content'].replace("\n","<br />")
    outputText += f"{output}"
    outputText += "</div>"

    return outputText

def p5_1():
    # <script language="javascript" type="text/javascript" src="/assets/box2d_html5.js"></script>
    outputText = '<script src="/assets/p5_0002.js"></script>'
    outputText += f'<div class="output-text-p5" id="output-text"><div class="" id="canvasHolder" data-mdignore="true">'

    # output = response['message']['content'].replace("\n","<br />")
    output = "JUMP POGO POGO POGO POGO POGO POGO POGO BOUNCE"
    outputText += f"{output}"
    outputText += "</div>"

    return outputText

# main function dictionary. add new fire stuff here ----- @~-------  BEWARE THE METADATA SCORPION  @~-------

# ⠀⠀⢀⣤⣤⣠⣤⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⢀⣿⣿⡿⠟⠿⠿⢿⣿⣷⣶⣤⣶⣶⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⣿⣿⣿⠀⠀⠀⠀⠀⠙⠛⢻⣿⣿⣿⣿⣿⣦⣀⡀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠙⢿⣿⣦⣄⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠈⢿⣿⣿⣦⣤⣤⣄⡀⠀⢀⣄⠉⠙⠛⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠉⠛⢿⣿⣿⣿⣿⣿⣿⣧⣤⡟⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⢀⣩⣿⣿⣿⣿⣿⣿⣿⣿⣾⣏⢀⡤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠈⠋⣙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣰⡿⣷⣶⣦⣄⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠙⠋⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡿⠀⣿⣿⣿⣿⣿⡄⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠘⠋⢉⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⠀⠘⣿⣿⣿⣿⣷⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢉⣬⡿⢿⣿⣿⠛⢿⠗⠀⠀⠀⠈⢿⣿⣿⣿⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠟⠉⠀⠀⠈⠙⠁⠀⠀⠀⠀⠀⠀⠀⠙⠻⠇⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠛⠛⠛⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀

tdlTypes = OrderedDict([
    ('flagship', {'f': flagship, 'it':'scratch', 'ot':'img', 'ff': 1}),
    ('dots', {'f':dots, 'it':'scratch', 'ot':'img', 'ff': 0}),
    ('dotsDos', {'f':dotsDos, 'it':'scratch', 'ot':'img'}),
    ('boxabyss', {'f':boxabyss, 'it':'scratch', 'ot':'img'}),
    ('patoot', patoot),
    ('ihavenoidea', {'f':ihavenoidea, 'it':'scratch', 'ot':'img', 'ff': 1}),
    ('orangeblock', {'f':orangeblock, 'it':'walk', 'ot': 'img'}),
    ('insertBlocks', {'f':insertBlocks, 'it':'walk', 'ot': 'img'}),
    ('simplePublic', {'f':simplePublic, 'it':'walk', 'ot': 'img'}),
    ('ollamaHelloWorld', {'f':ollamaHelloWorld, 'it':'llm', 'ot':'txt'}),
    ('llmDescribeImage', {'f':llmDescribeImage, 'it':'llm', 'ot':'txt'}),
    ('ollamaCraft', {'f': ollamaCraft, 'it': 'llm', 'ot':'txt'}),
    ('ollamaSimple', {'f': ollamaSimple, 'it': 'llm', 'ot':'txt'}),
    ('ollamaBored', {'f': ollamaBored, 'it': 'llm', 'ot':'txt'}),
    ('ollamaPalette', {'f': ollamaPalette, 'it': 'llm', 'ot':'txt'}),
    ('ollamaSummarize', {'f': ollamaSummarize, 'it': 'llm', 'ot':'txt'}),
    ('fuckinthatdata', {'f': fuckinthatdata, 'it':'scratch', 'ot':'img'}),
    ('p5_1', {'f': p5_1, 'it':'p5', 'ot':'p5'}),
    ('vaguetransfer', vaguetransfer),
    ('halfbleed', halfbleed),
    ('shakeHarderBoyBase', shakeHarderBoyBase),
    ('transferStation', transferStation),
    ('gritty', gritty),
    ('grittyer', grittyer),
    ('bored', bored),
    ('catalinaimagemixer', catalinaimagemixer),
    ('smellycatalina', smellycatalina),
    ('textalinaimagemixer', textalinaimagemixer),
    ('roundPaste', roundPaste),
    ('vgaBox', vgaBox),
    ('iWannaBeTheOne', iWannaBeTheOne),
    ('iWannaBeTheTwo', iWannaBeTheTwo),
    ('iWannaThreeTheBe', iWannaThreeTheBe),
    ('iWannaOneTheTwo', iWannaOneTheTwo),
    ('nightInterference', nightInterference),
    ('dayInterference', dayInterference),
    ('colorHatch', colorHatch),
    ('whateverDude', whateverDude),
    ('jumpingDust', jumpingDust),
    ('dumpingJust', dumpingJust),
    ('shapeMover', {'f':shapeMover, 'it':'insert', 'ot':'img'}),
    ('randomInversion', randomInversion),
    ('repeatedInversion', repeatedInversion),
    ('remixer', remixer),
    ('hueTranspose', hueTranspose),
    ('atariripples', atariripples),
    ('linePainter', linePainter),    
    ('wordspiral', wordspiral),
    ('colorSwitch', colorSwitch),
    ('subtlyWrong', subtlyWrong),
    ('subtlyWrongSquares', subtlyWrongSquares),
    ('starfield', starfield),
    ('drain', drain),
    ('gradientBars', gradientBars),
    ('fakeGlitch', fakeGlitch),
    ('vhsText', vhsText),
    ('textGen', textGen),
    ('textGen2', textGen2),
    ('textGenScatter', textGenScatter),
    ('imageWithText', imageWithText),
    ('colorizerize', colorizerize),
    ('randgradient', randgradient),
    ('pieslice', pieslice),
    ('glitchUp', glitchUp),
    ('threecolor', threecolor),
    ('hardLandscape', hardLandscape),
    ('lotsOfLetters', lotsOfLetters),
    ('pixelDiff', pixelDiff),
    ('textGrid', textGrid),
    ('fourdots', fourdots),
    ('xdots', xdots),    
    ('fourdotsRemixed', fourdotsRemixed),
    ('fourdots_18', fourdots_18),
    ('eightdots', eightdots),    
    ('fourdotsAnim', fourdotsAnim),
    ('bigSquareGrid', bigSquareGrid),
    ('coco2remixed', coco2remixed),
    ('bigGridFilled', bigGridFilled),
    ('insert_18', insert_18),
    ('insertFoured', insertFoured),
    ('insertStreaks', insertStreaks),
    ('insertStreaksAdapt', insertStreaksAdapt),
    ('insertStreaksCoco', insertStreaksCoco),
    ('insertStreaksPublic', insertStreaksPublic),
    ('parboil', parboil),
    ('realspiral', realspiral),
    ('adaptSpiral', adaptSpiral),
    ('DEADNIGHTSKY', DEADNIGHTSKY),
    ('generateQRCode', generateQRCode),
    ('grid_18', grid_18),
    ('grid_other', grid_other),
    ('grid_rando_unique', grid_rando_unique),
    ('grid_palette', grid_palette),
    ('grid_new', grid_new),
    ('nightgrid', nightgrid),
    ('nightgridStars', nightgridStars),
    ('hardLandscape2', hardLandscape2),
    ('hardLandscape3', hardLandscape3),
    ('vhsTextGrid', vhsTextGrid),
    ('picGrid', picGrid),
    ('hollywoodSign', hollywoodSign),
    ('randoFillStyle', randoFillStyle),
    ('randoFillStyle_Prism', randoFillStyle_Prism),
    ('randoFill_Insert', randoFill_Insert),
    ('randoFill_Public', randoFill_Public),
    ('vaporwave1', vaporwave1),
    ('vaporwave2', vaporwave2),
    ('vaporwave2By4', vaporwave2By4),
    ('wordsquares', wordsquares),
    ('vaporSquares', vaporSquares),
    ('wordGrid', wordGrid),
    ('wordGrid2', {'f':wordGrid2, 'ot':'img'}),
    ('wordGridTxT', {'f':wordGridTxT, 'ot':'txt'}),
    ('wordGridStats', {'f':wordGridStats, 'ot':'txt'}),
    ('wordGridGematria', {'f':wordGridGematria, 'ot':'txt'}),
    ('wordGrid_image', wordGrid_image),
    ('wordGrid_Moby', wordGrid_Moby),
    ('wordGrid_static', wordGrid_static),
    ('wordGrid_single', wordGrid_single),
    ('wordGrid_Special', {'f':wordGrid_Special, 'ot':'img'}),
    ('wordGridWordNet', {'f':wordGridWordNet, 'ot':'txt'}),    
    ('wordGridHexcult', {'f':wordGridHexcult, 'ot':'txt'}),
    ('wordGridLemmaWordages', {'f':wordGridLemmaWordages, 'ot':'txt'}),
    ('wordGridHexcult2', {'f':wordGridHexcult2, 'ot':'txt'}),
    ('wordGridHexetidine', {'f':wordGridHexetidine, 'ot':'txt'}),
    ('wordGridHexLatest', {'f':wordGridHexLatest, 'ot':'txt'}),
    ('slightlyDiffSquares', slightlyDiffSquares),
    ('adaptivePublic', adaptivePublic),
    ('randomTriangles', {'f':randomTriangles, 'ot':'img', 'ff':1}),
    ('triangleSys', triangleSys),
    ('triangleGrid', {'f': triangleGrid, 'ot':'img', 'ff': 1}),
    ('squareGrid', {'f': squareGrid, 'ot':'img', 'ff': 1}),
    ('fractal1', fractal1),
    ('fractal2', fractal2),
    ('fractal3', fractal3),
    ('fractal4', fractal4),
    ('fractalText0', fractalText0),
    ('fractalText', fractalText),    
    ('hsvTesting', hsvTesting),
    ('longWordList', longWordList),
    ('longWordList_Sorted', longWordList_Sorted),
    ('Favs30', Favs30),
    ('muchoLetters', muchoLetters),
    ('typewriterStuff', typewriterStuff),
    ('gradientSquares', gradientSquares),
    ('generatePalette', generatePalette),
    ('paletteSquares', paletteSquares),
    ('paletteSquareLetters', paletteSquareLetters),
    ('mix2', mix2),
    ('mix2_public', mix2_public),
    ('mixpub_add', mixpub_add),
    ('mixpub_diff', mixpub_diff),
    ('mixpub_screen', mixpub_screen),
    ('mixpub_blend', mixpub_blend),
    ('mix2_other', mix2_other),
    ('ladiesSpend', ladiesSpend),
    ('rose', {'f': rose, 'it':'scratch', 'ot':'img', 'ff': 1}),
    ('astrologyTable', astrologyTable),
    ('neobored', neobored),
    ('triangleNonSys', triangleNonSys),
    ('radioFill', radioFill),
    ('radioFillMixed', radioFillMixed),
    ('radioFillWords', radioFillWords),
    ('radioFill_blend', radioFill_blend),
    ('radioFill_stamp', radioFill_stamp),
    ('radioFill_stamp_fromFunc', radioFill_stamp_fromFunc),
    ('radioFill_stamp_wordfilled', radioFill_stamp_wordfilled),
    ('radioFill_stamp_wordfilled_mult', radioFill_stamp_wordfilled_mult),
    ('radioFill_stamp_fullFill', radioFill_stamp_fullFill),
    ('radioFill_stamp_fullFill_specific', radioFill_stamp_fullFill_specific),
    ('radioFill_stamp_fullFillLatest', radioFill_stamp_fullFillLatest),
    ('radioFill_stamp_newgrid', radioFill_stamp_newgrid),
    ('radioFill_recurse', radioFill_recurse),
    ('radioFill_recurse_func', radioFill_recurse_func),
    ('radioFill_recurse_special', radioFill_recurse_special),
    ('radioFill_recurse2', radioFill_recurse2),
    ('radioFill_recurse_swap', radioFill_recurse_swap),
    ('radioFill_recurse_swap_AB', radioFill_recurse_swap_AB),
    ('radioFill_recurse_canny', radioFill_recurse_canny),
    ('radioFill_recurse_anim', radioFill_recurse_anim),
    ('radioFill_compFunc', radioFill_compFunc),
    ('ellipseGuy', ellipseGuy),
    ('ellipseGroup', ellipseGroup),
    ('fillFromOuter', fillFromOuter),
    ('fillFromOuter_blend', fillFromOuter_blend),
    ('fillFromOuter_stamp', fillFromOuter_stamp),
    ('fillFromOuter_canny', fillFromOuter_canny),
    ('labelSquares', labelSquares),
    ('darkbits', darkbits),
    ('altWorld', altWorld),
    ('ctrlWorld', ctrlWorld),
    ('shiftWorld', shiftWorld),
    ('metaWorld', metaWorld),
    ('metaWorldStamp', metaWorldStamp),
    ('hyperWorld', hyperWorld),
    ('greekWorld', greekWorld),
    ('localWorld', localWorld),
    ('compuWorld', compuWorld),
    ('radial_gradient', radial_gradient),
    ('effect_mandelbrot', {'f':effect_mandelbrot, 'ot':'img'}),
    ('fullFill', fullFill),
    ('fullFillSpecific', fullFillSpecific),
    ('fullFillLatest', fullFillLatest),
    ('fullfillBlend2', {'f':fullfillBlend2, 'ot':'img', 'ff':1}),
    ('fullFillStamp', fullFillStamp),
    ('fullFillVariants', fullFillVariants),
    ('screenshotFill', screenshotFill),
    ('surrealColors', surrealColors),
    ('surrealPatterns', surrealPatterns),
    ('gingerNo', gingerNo),
    ('vhsDouble', vhsDouble),
    ('wordfilled', wordfilled),
    ('wordfilled_any', wordfilled_any),
    ('wordfilled_mult', wordfilled_mult),
    ('newgrid', newgrid),
    ('xThenY', xThenY),
    ('fullGradient', fullGradient),    
    ('diagonal4Way', diagonal4Way),
    ('diagonalXWay', {'f':diagonalXWay, 'ot':'img','ff':1}),
    ('sigilGrid', sigilGrid),
    ('gradient_mosaic', {'f':gradient_mosaic, 'ot':'img'}),
    ('numpytest', numpytest),
    ('numpyVerySimple', numpyVerySimple),
    ('numpySimple', numpySimple),
    ('numpyNormal', numpyNormal),
    ('numpyFloodfill', numpyFloodfill),
    ('opencv_removeBG', opencv_removeBG),
    ('opencv_inpaint', opencv_inpaint),
    ('opencv_canny', opencv_canny),
    ('opencv_canny_inv', opencv_canny_inv),
    ('opencv_erosion', opencv_erosion),
    ('opencv_gradient', opencv_gradient),
    ('generateAnim', generateAnim),
    ('generateAnimNumpy', generateAnimNumpy),
    ('listFonts', listFonts),
    ('textHash', {'f':textHash, 'ot':'txt'}),
    ('colorSample', {'f':colorSample, 'it':'scratch', 'ot':'img', 'ff': 0})
])

def doMain(basey):
    imgtype = basey.imgtype
    imgpath = basey.imgpath
    word = basey.word
    imageop = basey.imageop
    palette = basey.palette

    fonError = ImageFont.truetype(fontPath + fontNameMono, 18)

    global functionDocs
    global input_palette
    global current_imgtype
    global wrapperData
    global telemetry
    global timeOutDefault

    # TODO
    imageExtensions = ["png","gif","jpg","tif"]

    input_palette = processPalette(palette)
    frm = "PNG"
    extension = ".png"
    timeOutLength = timeOutDefault

    for key, value in list(tdlTypes.items()):
        if key == imgtype:
            if "functionDocs" in functionDocs:
                lFDesc = functionDocs["functionDocs"]

                for xlFDesc in lFDesc:
                    if "function" in xlFDesc and xlFDesc["function"] == imgtype:
                        rootLogger.debug(f"xlFDesc: {xlFDesc}")

                        if "timeout" in xlFDesc:
                            timeOutLength = getInt(xlFDesc["timeout"], timeOutDefault)

            startTime = time.time()

            current_imgtype = tdlTypes[key]

            uid = callWithTimeout(tdlTypes[key], timeOutLength, word, palette, key)
                                               
            try:
                outputval = wrapperData[uid]                
            except:
                outputval = ""            

            if isinstance(outputval, str):
                if outputval != "" and outputval[-3:].lower() in imageExtensions:
                    blob = Image.open(outputval)

                    if outputval[-4:].lower() == ".gif":
                        extension = ".gif"
                        frm = "GIF"
                elif outputval != "":
                    return (outputval, frm)
                # index = 1
                # for frame in ImageSequence.Iterator(blob):
                #     rootLogger.debug("blob frame: " + str(index))
                #     index += 1
                else:
                    blob = None
            else:
                blob = outputval

            wrapperData.pop(uid, '')

            stopTime = time.time()

            loadConfiguration()

            if "execution" not in telemetry:
                telemetry['execution'] = {}

            if "last_exec_time" not in telemetry['execution']:
                telemetry['execution']['last_exec_time'] = {}

            telemetry['execution']['last_exec_time'][key] = round(stopTime-startTime, 2)
            saveConfiguration()

            if blob is None:
                blob = Image.new("RGBA", (640,480), "#ffffff")
                blobDraw = ImageDraw.Draw(blob)
                blobDraw.text((5, 60), "Function timed out", font=fonError, fill=(255, 0, 0, 255))               
            
            if frm != "GIF":
                blob = check_image_operation(blob, imageop, palette)
                blob = blob.convert("RGBA")                

            writeToDisk(blob, "./imagesExported/" + key + extension, extension)

            return (blob, frm)

    if imgtype == "floodSample":
        blob = floodSample(palette)
        writeToDisk(blob, "./imagesExported/floodSample.png")
        return (blob, frm)
    if imgtype == "stampSample":
        blob = stampSample()
        writeToDisk(blob, "./imagesExported/stampSample.png")
        return (blob, frm)    
    if imgtype == "paletteSample":
        blob = paletteSample()
        writeToDisk(blob, "./imagesExported/paletteSample.png")
        return (blob, frm)
    
    rootLogger.warning("Couldn't find type: " + imgtype)
    
    blob = Image.new("RGBA", (250,75), "#ffffff")
    blobDraw = ImageDraw.Draw(blob)
    blobDraw.text((5, 60), "Couldn't find type: " + imgtype, font=fonError, fill=(255, 0, 0, 255))
    
    return (blob, frm)

def writehtml(basey):
    (imgtype, imgpath, word, imageop, palette) = [basey.imgtype, basey.imgpath, basey.word, basey.imageop, basey.palette]

    tdlTitle = getTDL()

    try:
        imgtypeFunc = globals()[imgtype]
    except KeyError:
        imgtype = "flagship"
        imgtypeFunc = globals()[imgtype]

    global functionDocs
    doccy = imgtypeFunc.__doc__

    body = """
<!DOCTYPE html>
<html lang="en">
  <head> 
    <meta charset="utf-8" />
    <link rel="shortcut icon" type="image/x-icon" href="/favicon.png" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta http-equiv="content-type" content="text/html; charset=windows-1252" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Nabla:EDPT@81&display=swap" rel="stylesheet">
    <title>""" + tdlTitle + """</title>
    """ + pathWebFonts + """
    <style type="text/css">    
    @import url('https://fonts.cdnfonts.com/css/track');
    </style>
    <link rel="stylesheet" href="//code.jquery.com/ui/1.12.0/themes/base/jquery-ui.css">
    <link rel="stylesheet" href="/assets/main.css">    
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="https://code.jquery.com/ui/1.12.0/jquery-ui.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.1/p5.min.js" integrity="sha512-jLPBEs8Tcpbj4AlLISWG0l7MbuIqp1cFBilrsy0BhvNUa0BLB4wVQeoL+93OYOdENFPKLOgrzb1Nytn+5N5y7g==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.1/addons/p5.sound.min.js" integrity="sha512-WzkwpdWEMAY/W8WvP9KS2/VI6zkgejR4/KTxTl4qHx0utqeyVE0JY+S1DlMuxDChC7x0oXtk/ESji6a0lP/Tdg==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>

    <script src="/assets/main.js"></script>
  </head>
  <body>
    <div class="status" id="status">
        <div id="time-elapsed" class="time-elapsed">
            &nbsp;
        </div>
    </div>
    <main class="main">
        <aside class="sidebar" id="sidebar">
            <button class="btn-bottom" style="" onclick="bottomFunction()" id="myBtn2" title="Go to bottom">Bottom</button>
            <button class="btn-top" style="" onclick="topFunction()" id="myBtn" title="Go to top">Top</button>

            <nav class="nav">
    """

    imgTypePrnt = ""
    if imgtype != "":
        imgTypePrnt = "&imgtype=" + imgtype

    imgPathPrnt = ""
    if imgpath != "":
        imgPathPrnt = "&imgpath=" + imgpath

    wordPrnt = ""
    if word != "":
        wordPrnt = "&word=" + word

    imageopPrnt = ""
    if imageop != "":
        imageopPrnt = "&imageop=" + imageop

    palettePrnt = ""
    if palette != "":
        palettePrnt = "&palette=" + palette

    global extParams
    global imageoplist
    global palettelist

    param1Prnt = ""
    param1 = ""
    param2Prnt = ""
    param2 = ""
    param3Prnt = ""
    param3 = ""
    compfunc = ""
    compfuncPrnt = ""
    paramfont = ""
    paramfontPrnt = ""
    insertSource = ""
    insertSourcePrnt = ""
    paramFloodBoxes = ""
    paramFloodBoxesPrnt = ""

    doTimeCheck(f"extParams: {extParams}", 1)

    if extParams != []:
        if len(extParams) > 0:
            param1 = extParams[0]

        if len(extParams) > 1:
            param2 = extParams[1]

        if len(extParams) > 2:
            compfunc = extParams[2]

        if len(extParams) > 3:
            paramfont = extParams[3]

        if len(extParams) > 4:
            insertSource = extParams[4]

        if len(extParams) > 5:
            paramFloodBoxes = extParams[5]

        if len(extParams) > 6:
            param3 = extParams[6]
    
    doTimeCheck(f"writehtml: param1: {param1}, cond: {param2!=''}, param2: {param2}, param3: {param3}, compfunc: {compfunc}")
    
    if param1 != "":
        param1Prnt = "&param1=" + param1    

    if param2 != "":
        param2Prnt = "&param2=" + param2

    if param3 != "":
        param3Prnt = "&param3=" + param3

    if compfunc != "":
        compfuncPrnt = "&compfunc=" + compfunc

    if paramfont != "":
        paramfontPrnt = "&paramfont=" + paramfont

    if insertSource != "" and insertSource != 0 and insertSource != "0":
        insertSourcePrnt = "&insertSource=" + insertSource
    
    if paramFloodBoxes != "" and paramFloodBoxes != "false" and paramFloodBoxes != "False":
        paramFloodBoxesPrnt = "&floodBoxes=" + paramFloodBoxes

    breakpoint = 10 # (len(tdlTypes) + 4) // 5

    body += '<ul class="imgtypes-list">'

    inputType = ""
    outputType = ""

    iType = 0    
    for tdl in tdlTypes:
        if iType % breakpoint == 0 and iType > 0:
            body += '<hr class="tdl_sep" />'           
        
        inputTypeMilk = "unk"
        outputTypeMilk = "img"
        usesFF = 0

        alice = tdlTypes[tdl]
        if isinstance(alice, dict):
            if "it" in alice:
                inputTypeMilk = alice["it"]
            if "ot" in alice:
                outputTypeMilk = alice["ot"]
            if "ff" in alice:
                usesFF = alice["ff"]
        
        isSelImgType = "tdl_imgtype active" if imgtype == tdl else "tdl_imgtype"

        if inputTypeMilk != "":
            isSelImgType += " tdl-input-" + inputTypeMilk

        if outputTypeMilk != "":
            isSelImgType += " tdl-output-" + outputTypeMilk

        zonk = ' <span title="Uses floodfill">🚰</span>'
        tdlDisp = f"{tdl}{zonk if usesFF > 0 else ''}"

        body += '<li data-func="{}"><a class="{}" href="/tdl?imgtype={}{}{}{}{}{}{}{}{}{}">{}</a></li>'.format(tdl, isSelImgType, tdl, imageopPrnt, palettePrnt, param1Prnt, param2Prnt, compfuncPrnt, param3Prnt, paramfontPrnt, insertSourcePrnt, paramFloodBoxesPrnt, tdlDisp)
        iType += 1

        if tdl == imgtype:
            outputType = outputTypeMilk

    for xxop in ["paletteSample", "floodSample", "stampSample"]:
        isSelImgType = "tdl_imgtype active" if imgtype == xxop else "tdl_imgtype"

        body += '<li data-func="{}"><a class="{}" href="/tdl?imgtype={}{}{}{}{}{}{}{}{}{}">{}</a></li>'.format(xxop, isSelImgType, xxop, imageopPrnt, palettePrnt, param1Prnt, param2Prnt, compfuncPrnt, param3Prnt, paramfontPrnt, insertSourcePrnt, paramFloodBoxesPrnt, xxop)
    
    body += '<li><a href="/exported" target="_blank">exported image list</a></li>'
    body += '<li><a href="/stamps" target="_blank">stamp list</a></li>'
    body += '<li><a href="/palettes" target="_blank">file palette list</a></li>'

    body += '</ul>'

    body += '</div>'

    body += """</ul>            
            </nav>
        </aside>
        <section class="main-thing">
            <div class="container">"""

    body += "<div class='container-reload'><input type=\"button\" onclick=\"javascript:location.reload()\" value=\"Reload\"></input></div>"

    # for section in config.items():
    #     body += f'<div>{section}'
        
    #     for zItem in section:
    #         body += f'<div>{zItem}</div>'

    #     body += f'</div>'

    if "functionDocs" in functionDocs:
        lFDesc = functionDocs["functionDocs"]

        for xlFDesc in lFDesc:
            if "function" in xlFDesc and xlFDesc["function"] == imgtype:
                if "description" in xlFDesc:
                    body += f"<div id='description-container' class='description-container'>{xlFDesc['description']}</div>"

    body += '<div id="main-hex" class="font-threed text-center" style="width: 100%; text-align: center;">'
    
    hex = getAHex()

    body += hex
    body += '</div>'

    if outputType == "" or outputType == "img":
        body += '<div id="result-container-img" class="result-container-img">'

        apiAction = f'/apiimg?func=img&t={str(time.time())}{imgTypePrnt}{imgPathPrnt}{wordPrnt}{imageopPrnt}{palettePrnt}{param1Prnt}{param2Prnt}{param3Prnt}{compfuncPrnt}{paramfontPrnt}{insertSourcePrnt}{paramFloodBoxesPrnt}'

        body += '<script type="text/javascript">'
        body += 'apiURL = "' + apiAction + '";'
        body += '</script>'

        body += '<img id=\"output-img\" class=\"output-img\" src=\"/nowLoading.png\" download=\"workit\" />'
        #body += '<img src="/img?func=img&t=' + str(time.time()) + imgTypePrnt + imgPathPrnt + wordPrnt + imageopPrnt + palettePrnt + param1Prnt + param2Prnt + param3Prnt + compfunc + paramfontPrnt + insertSourcePrnt + paramFloodBoxesPrnt + '&suggname=' + suggname + '">'   
        
        body += '</div>'
    elif outputType == "txt":
        resultHere = imgtypeFunc()
        body += '<div id="result-container" class="result-container" data-t="' + str(time.time()) + '">' + resultHere + '</div>'
    elif outputType == "p5":
        resultHere = imgtypeFunc()
        body += '<div id="result-container" class="result-container" data-t="' + str(time.time()) + '">' + resultHere + '</div>'
    else:
        # NOOP
        pass
    
    if doccy is None:
        doccy = ""    

    body += '<div id=\"sacred-output\" class=\"sacred-output sacred-output-main\">'
    body += f'<div id=\"sacred-output-palette\"><table id=\"palette-table\"></table></div>'

    body += f'<div class=\"sacred-guid\" id=\"sacred-guid\"><input type=\"text\" class=\"flex-grow-1\" id=\"sacred-guid-value\" value=\"{getDecree("","",10)}.{"png"}\"></input><button type=\"button\" id=\"sacred-guid-button\" class=\"btn btn-flat flex-grow-0\" onclick=\"copyToClipboard();\">Copy</button><a href=\"\" id=\"sacred-image-dl\">Save</a></div>'
    
    body += '</div>'

    body += f"<div class='container-bottom'><div>{doccy}</div>"

    if imgtype != "" or word != "":
        body += """<div id='param-div'>"""

        if imgtype != "":
            body += "running: " + imgtype + "<br />"

        body += "imageop: <select id=\"imageop\" name=\"imageop\" onchange=\"setQS_imageop(this.value);\">"
        body += "<option> </option>"
            
        for iop in imageoplist:
            body += "<option "
            
            if imageop == iop:
                body += "selected"
                
            body += ">" + iop + "</option>"
            
        body += "</select><br />"

        body += "palette: <select id=\"palette\" name=\"palette\" onchange=\"setQS_palette(this.value);\">"
        body += "<option> </option>"

        for iop in palettelist:
            body += "<option value=\"" + str(iop[0]) + "\" "
           
            if iop[0] == palette or str(iop[0]) == palette:
                body += "selected"

            body += ">" + iop[1] + "</option>"
            
        body += "</select><br />"

        body += "param1: <input type=\"text\" id=\"param1\" name=\"param1\" size=\"50\" value=\"" + param1 + "\" />"
        body += "<button id=\"btnGo\" type=\"submit\" onclick=\"goClicked()\">Go</button><br />"

        # TODO: add a describe this image button for Ollama, call api url that accepts base64 input        

        body += "param2: <input type=\"text\" id=\"param2\" name=\"param2\" size=\"50\" value=\"" + param2 + "\" /><br />"
        body += "variant: <input type=\"text\" id=\"param3\" name=\"param3\" size=\"50\" value=\"" + param3 + "\" /><br />"
        body += "compfunc: <input type=\"text\" id=\"compfunc\" name=\"compfunc\" size=\"50\" value=\"" + compfunc + "\" /><br />"
        body += "paramfont: <input type=\"text\" id=\"paramfont\" name=\"paramfont\" size=\"50\" value=\"" + paramfont + "\" /><br />"
        body += "insertSource: <input type=\"number\" id=\"insertSource\" name=\"insertSource\" value=\"" + insertSource + "\" min=\"0\" max=\"" + str(len(allPaths) - 1) + "\" /><br />"
        body += "floodBoxes: <input type=\"checkbox\" id=\"floodBoxes\" name=\"floodBoxes\" value=\"1\" " + ("checked" if paramFloodBoxes in ["True","true"] else "") + " /><br />"
        body += "<br />"
        body += "<input type=\"text\" id=\"myguid\" size=\"50\" /><input type=\"button\" onclick=\"guidclick()\" value=\"Get a guid\"></input>"
        body += "<div id=\"img-upload-container\" class=\"img-upload-container\"><label>Upload image <input type=\"file\" name=\"uploadimg\" id=\"img-upload\" accept=\"image/png, image/gif, image/jpeg\" /></label>"
        
        #body += "<button type=\"button\" processing"

        body += "</div>"

        if word != "":
            body += "word: " + word + "<br />"
        
        body += '</div>'        

    iPath = 0
    body += "<div class=\"path-sources\"><caption><strong>Insert source path list</strong></caption><br />"

    for walkPath in allPaths:
        body += str(iPath) + ": " + walkPath + "<br />"
        iPath += 1

    body += '</div>'
    body += '</div>'
    body += f'<div class=\"sacred-output sacred-output-states\"><pre><code id=\"sacred-output-code\">Loading...</code></pre></div>'
    body += '</div>'
    
    body += '<br />'

    body += '</div></section></main>'    
    
    if imgtype != "":
        body += """
        <script type="text/javascript">
        var elm = document.querySelector("[data-func='""" + imgtype + """']");
        if(elm) { elm.scrollIntoView(); }        
        </script>
        """    

    body += '</BODY>'
    body += '</HTML>'

    return body

@app.route('/exif./<path:thing>')
def send_exif_fix(thing):
    return send_exif("./"+thing)

@app.route('/exif/<path:thing>')
def send_exif(thing):
    colorPrint.print_custom_palette(111, f"send_exif // thing: {thing}")    

    filePath = "/" + thing if thing[0:1] != "." else thing
    im = Image.open(filePath)
    im.load()
    exif = im.getexif()

    zzz = dict()

#     from PIL import ExifTags

# IFD_CODE_LOOKUP = {i.value: i.name for i in ExifTags.IFD}

# for tag_code, value in img_exif.items():

#     # if the tag is an IFD block, nest into it
#     if tag_code in IFD_CODE_LOOKUP:

#         ifd_tag_name = IFD_CODE_LOOKUP[tag_code]
#         print(f"IFD '{ifd_tag_name}' (code {tag_code}):")
#         ifd_data = img_exif.get_ifd(tag_code).items()

#         for nested_key, nested_value in ifd_data:

#             nested_tag_name = ExifTags.GPSTAGS.get(nested_key, None) or ExifTags.TAGS.get(nested_key, None) or nested_key
#             print(f"  {nested_tag_name}: {nested_value}")

#     else:

#         # root-level tag
#         print(f"{ExifTags.TAGS.get(tag_code)}: {value}")

    errors = []
    
    for ifd_key, ifd_value in exif.get_ifd(0x8769).items():
        ifd_tag_name = ExifTags.TAGS.get(ifd_key, ifd_key)
        
        try:
            zzz[ifd_tag_name] = ifd_value.decode('ascii') if isinstance(ifd_value, bytes) else ifd_value if isinstance(ifd_value, str) else str(ifd_value)
        except Exception as ex:
            zzz[ifd_tag_name] = str(ifd_value)
            errors.append(ex)

        print(f" {ifd_tag_name}: {ifd_value}")

    # TODO: return something better

    return {
        "_item": thing,
        "exif": str(exif), 
        "extracted": zzz,
        "errors": errors
    }

def extractQuery():
    imgtype = request.args.get('imgtype')
    imgpath = request.args.get('imgpath')
    word = request.args.get('word')
    imageop = request.args.get('imageop')
    palette = request.args.get('palette')
    param1 = request.args.get('param1')
    param2 = request.args.get('param2')
    param3 = request.args.get('param3')
    paramcompfunc = request.args.get('compfunc')
    paramfont = request.args.get('paramfont')
    paramInsertSource = request.args.get('insertSource')
    paramFloodBoxes = request.args.get('floodBoxes')

    if imgtype is None:
        imgtype = ""

    if imgpath is None:
        imgpath = ""

    if word is None:
        word = ""

    if imageop is None:
        imageop = ""

    if palette is None:
        palette = ""

    if param1 is None:
        param1 = ""

    if param2 is None:
        param2 = ""

    if param3 is None:
        param3 = ""

    if paramcompfunc is None:
        paramcompfunc = ""

    if paramfont is None:
        paramfont = ""
        
    if paramInsertSource is None:
        paramInsertSource = "0"

    if paramFloodBoxes is None:
        paramFloodBoxes = "False"

    global extParams
    extParams = [param1, param2, paramcompfunc, paramfont, paramInsertSource, paramFloodBoxes, param3]

    return imgtype,imgpath,word,imageop,palette,extParams

def extractBasics():    
    imgtype, imgpath, word, imageop, palette, extParams = extractQuery()

    basey = TdlValues(imgtype, imgpath, word, imageop, palette, extParams)
    return basey

def loadConfiguration():
    # global pathConfigFile
    #global config
    #config = configparser.ConfigParser()
    
    #with open(pathConfigFile) as configfile:
    #    config.readfp(configfile)
    #     path1 = config.get('TextData', 'path1')
    #     path2 = config.get('TextData', 'path2')
    #     path3 = config.get('TextData', 'path3')

    #if not config.has_section("TextData"):
    #    config.add_section("TextData")

    #if not config.has_option("TextData", "path1"):
    #    config.set("TextData", "path1", f'yeah')

    global pathFunctionDoc
    global functionDocs

    with open(pathFunctionDoc, 'r') as f:
        functionDocs = json.load(f)

    global pathTelemetry
    global telemetry

    with open(pathTelemetry, 'r') as f:
        telemetry = json.load(f)

    #ColorPrint.logger_info(str(telemetry))

    return

def saveConfiguration():
    # global pathConfigFile
    # global config

    # with open(pathConfigFile, 'w') as configfile:
    #     config.write(configfile)

    # global functionDocs
    # functionDocs = { 'functionDocs': [ {'dots':{'description':'Various dumb shit I did 😀 😀'}}] }

    # data = {'name': 'John', 'age': 30, 'emotion': '😀'}

    # with open('tdldl.json', 'w') as f:
    #     json.dump(functionDocs, f)

    global pathTelemetry
    global telemetry    

    with open(pathTelemetry, 'w') as f:
        json.dump(telemetry, f, sort_keys=True, indent=4)

    return

def writeOperationToDisk(uid, line):
    global pathOperations

    opPath = os.path.join(pathOperations, f"ops_{uid}.txt")

    with open(opPath, 'a') as fOp:
        fOp.write(line + "\n")
        fOp.flush()
        fOp.close()

    return

# flask app routes ------------------------------------- ALOOFNESS REGULATION @~-------

@app.route('/')
@app.route('/tdl')
def root():
    basey = extractBasics()
    loadConfiguration()
    return writehtml(basey)

@app.route('/hello')
def hello():
    return render_template('hello.html', utc_dt=datetime.datetime.now(datetime.timezone.utc) )

@app.route('/testflood')
def testflood():
    basey = extractBasics()
    loadConfiguration()

    wrapperData = manager.dict()
    wrapperData["xannies"] = manager.dict()
    wrapperData["inserts_used"] = manager.dict()
    wrapperData["function_states"] = manager.dict()

    img = diagonal4Way()

    [output, contentType, saveFormat] = writeImageToBytes(img, "PNG")
    img_str = base64.b64encode(output.getvalue())

    return img_str

@app.route('/img')
def tdl():
    basey = extractBasics()
    loadConfiguration()
    (blob, frm) = doMain(basey)
    return writeimage(blob, frm)

@app.route('/decree')
def decree():
    return getDecree("","",10)

@app.route('/custom')
@app.route('/custom/<string:whatever>')
def custom(whatever=""):
    return {
        "step": "custom",
        "xy": hash((0,1)),
        "whatever": whatever,
        "whateverHash": hash(whatever)
    }

@app.route('/processing', methods=['POST'])
def process():
    file = request.files['image']
    img = Image.open(file.stream)
    
    return jsonify({'msg': 'success', 'size': [img.width, img.height]})

@app.route('/apiimg')
def apiimg():
    basey = extractBasics()
    loadConfiguration()
    (blob, frm) = doMain(basey)
    [output, contentType, saveFormat] = writeImageToBytes(blob, frm)
    img_str = base64.b64encode(output.getvalue())

    global wrapperData
    global currentUID

    inserts_used = []
    function_states = []

    if currentUID in wrapperData["inserts_used"]:
        zonk = wrapperData["inserts_used"][currentUID]

        for z in zonk:
            if z not in inserts_used:
                inserts_used.append(z)

    gottened = getPaletteFromImageFull(blob, limit=10)

    cholos = [rgb_to_hex(x) for x in gottened[0]]

    if currentUID in wrapperData["function_states"]:
        zink = wrapperData["function_states"][currentUID]        

        for z in zink:
            function_states.append(z)

    return {
        "image": img_str.decode('ascii'), 
        "basey": str(basey), 
        "currentUID": currentUID, 
        "inserts_used": inserts_used,
        "function_states": function_states,
        "palette": cholos
        #"palette_ogram": gottened[1]
    }

@app.route('/favicon.png')
def send_favicon():
    pathFavIcon = "./imagesExported/"
    myAppMyChoiceMyRules = getChoicesWalk(pathFavIcon)
    leImg = random.choice(myAppMyChoiceMyRules)
    return send_file(leImg)

@app.route('/assets/<path:path>')
def send_static1(path):
    return send_from_directory("./assets/", path)

@app.route('/imagesExported/<path:path>')
def send_static2(path):
    return send_from_directory("./imagesExported/", path)

@app.route('/sourceimages/<path:path>')
def send_static3(path):
    return send_from_directory("./sourceimages/", path)

@app.route("/<regex(r'(.*?)\.(json|txt|png|ico|js|jpg|jpeg|tif|tiff)$'):file>", methods=["GET"])
def public(file):
    return send_from_directory('./', file)

@app.route('/palettes')
def viewPals():
    return viewADirectory("./sourceimages/palettes/", htmlPath="/sourceimages/palettes/")

@app.route('/stamps')
def viewStamps():
    return viewADirectory("./sourceimages/stamps/", htmlPath="/sourceimages/stamps/")

@app.route('/exported')
def viewExported():
    return viewADirectory("./imagesExported/", htmlPath="/imagesExported/")

def viewADirectory(path="./imagesExported/", htmlPath="/imagesExported/"):
    paths = []
    paths.append(path)

    extensions=defaultInsertExtensions

    images = []

    for basepath in paths:           
        for root, dirs, files in os.walk(basepath):
            for leImg in files:
                if leImg[-4:].lower() in extensions:
                    images.append(leImg) # os.path.join(root, leImg))

    images.sort()

    body = """
<!DOCTYPE html>
<html lang="en">
  <head> 
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta http-equiv="content-type" content="text/html; charset=windows-1252" />
    <title>TDL - exported images</title>
    """ + pathBootstrapCSS + """
    """ + pathWebFonts + """
    <link rel="stylesheet" href="//code.jquery.com/ui/1.12.0/themes/base/jquery-ui.css">    

    <style type="text/css">
    .caption {
        margin-left: 20px;
    }

    .imgtable {
        width: 70%;
    }

    .container {
        margin: 0 auto;
    }
    
    .imgtd {
        padding-bottom: 30px;
    }

    .tdlimg {
        max-width: 1000px;
        max-height: 1000px;
    }

    .tdlimg:hover {
        border: 2px solid black;
    }
    </style>
    <script>
    </script>
    <body>
    <div class="container">
    <table id="imgtable">    
    """

    for xImg in images:
        body = body + "<tr><td>" + xImg + "</td><td class='imgtd'><img src='" + htmlPath + xImg + "' class='tdlimg'></td>" 

        this_pal = getPalette(xImg)

        choices = []
        for p in this_pal:
            c = rgb_to_hex(p)
            choices.append(c)

        body += f"<td>{str(choices)}</td>"
        body += "</tr>"

    body = body + """</table>
    </div>
    </body>
    </html>"""

    return body

def extractFrames(inputFile="test.mp4"):
    import cv2

    rootLogger.debug("extracting frames")

    image_counter = 0
    read_counter = 0
    
    frame_step = 1

    videoFile = os.path.join(pathSourceImages, inputFile)
    destination_format = "PNG"
    outputPath = "./tempImages/GIF/"

    list( map( os.unlink, (os.path.join(outputPath, f) for f in os.listdir(outputPath)) ) )

    cap = cv2.VideoCapture(videoFile)
    
    while(cap.isOpened()):
        ret, cv2_im = cap.read()

        if ret and read_counter % frame_step == 0:
            rootLogger.debug(f"frame {image_counter}")

            converted = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)

            pil_im = Image.fromarray(converted)

            img = radioFill_recurse(imgpath="", img=pil_im, passes=4, maxDuration=10)
           
            img.save(os.path.join(outputPath, f"{image_counter:08d}.{destination_format}"))

            image_counter += 1
        elif not ret:
            break

        read_counter += 1
            
    cap.release()
    cv2.destroyAllWindows()

    return

def readFrames(basePath = "./tempImages/GIF/"):
    rootLogger.debug("reading frames")

    images = []

    for root, dirs, files in os.walk(basePath):
        for leImg in files:
            if leImg[-4:].lower() in [".png"]:
                images.append(os.path.join(root, leImg))

    images.sort(key=lambda x: x)

    return images

def framesToVideo(outputPath = "./tempImages/GIF/"):
    import cv2

    images = readFrames()

    imgs = []

    rootLogger.debug("loading frame files")

    for i in images:
        imgs.append(cv2.imread(i))

    height, width, layers = imgs[0].shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    video = cv2.VideoWriter(os.path.join(outputPath, 'tt1.avi'), fourcc, 30, (width, height))

    rootLogger.debug("building video")

    for i in imgs:
        video.write(i)

    cv2.destroyAllWindows()
    video.release()

    rootLogger.debug("video complete")

    return

def main(argv):
    if len(argv) <= 1:
        app.run(debug=True, port=5000, threaded=True)
    else:
        #extractFrames("tt1.mov")
        # to extract audio with ffmpeg: 
        # ffmpeg -i videofile.mp4 -vn -acodec copy audiotrack.m4a
        framesToVideo()

if __name__ == "__main__":
    main(sys.argv)