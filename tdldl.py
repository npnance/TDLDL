# -*- coding: utf-8 -*-

# ----------------------- ARCHETYPE EPONYM ------------------------ #

"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@                                                                   @
@                                                                   @
@            ,----,               ,--,                   ,--,       @
@          ,/   .`|            ,---.'|                ,---.'|       @
@        ,`   .'  :   ,---,    |   | :       ,---,    |   | :       @
@      ;    ;     / .'  .' `\  :   : |     .'  .' `\  :   : |       @
@    .'___,/    ,',---.'     \ |   ' :   ,---.'     \ |   ' :       @
@    |    :     | |   |  .`\  |;   ; '   |   |  .`\  |;   ; '       @
@    ;    |.';  ; :   : |  '  |'   | |__ :   : |  '  |'   | |__     @
@    `----'  |  | |   ' '  ;  :|   | :.'||   ' '  ;  :|   | :.'|    @
@        '   :  ; '   | ;  .  |'   :    ;'   | ;  .  |'   :    ;    @
@        |   |  ' |   | :  |  '|   |  ./ |   | :  |  '|   |  ./     @
@        '   :  | '   : | /  ; ;   : ;   '   : | /  ; ;   : ;       @
@        ;   |.'  |   | '` ,/  |   ,/    |   | '` ,/  |   ,/        @
@        '---'    ;   :  .'    '---'     ;   :  .'    '---'         @
@                 |   ,.'                |   ,.'                    @
@                 '---'                  '---'                      @
@                                                                   @
@                                                                   @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""

from multiprocessing.managers import DictProxy
import base64
import colorsys
import configparser
import datetime
import hashlib
import html
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

from collections import OrderedDict, Counter, deque
from operator import itemgetter

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageSequence, ImageOps, ImageChops, ExifTags
from PIL.ImageColor import getrgb
import PIL.GifImagePlugin as pilGif

import numpy as np, numpy.random
from scipy.special import jv, fresnel, ellipeinc, struve, yv
import emoji

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib import cm, colors

from flask import Flask, jsonify, request, send_file, send_from_directory, render_template, Response
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
    "/mnt/t/Pictures/From Lumia920White/Camera roll/",
    "/mnt/t/Pictures/From_iPhone6/",
    "./imagesExported/",
    "/mnt/t/Pictures/stupidshit/",
    "/mnt/t/Pictures/stupidshit/no/",
    "/mnt/t/Pictures/art/created/",
    "/mnt/u/My Webs/bpreloaded/pics/",
    "/mnt/t/Pictures/tarot/",
    "/mnt/t/canoncam/"
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

bucky_labels = ["SHIFT", "ADAPT", "REMIX", "CRTMASK", "STAMPHUE", "TWOED", "FOURED", "SUPER", "HYPER", "META", "ULTRA", "GREEK", "PALCOMP", "PALINVERSE", "PALIGNORE", "PALMAYBE", "EXHAUST", "LEGACY", "EXTRA", "HEX"]

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

#----------- font blacklist. will not be chosen ------- @--~--/--\-/-------

fontBlacklist = ["BNJDigital",
                 "CoolS-Regular",
                 "Embossed Germanica",
                 "Fluted Germanica",
                 "Gottlieb"
                 "HARLOWSI",
                 "Hollywood Capital Hills",
                 "Hollywood Capital",
                 "holomdl2",
                 "LilyPond",
                 "marlett",
                 "mtextra",
                 "OUTLOOK",
                 "PARCHM",
                 "Plain Germanica",
                 "REFSPCL",
                 "romantic",
                 "segmdl2",
                 "Shadowed Germanica",
                 "Swkeys1",
                 "SWMacro",
                 "symbol",
                 "teamviewer",
                 "VISITOR",
                 "webdings", # looks bad todd
                 "wingding",
                 "WINGDNG2", # Wing Dongs
                 "WINGDNG3",
                 ]

#----------- color, palette and iAlg definitions. best not to change. --------

cocoColors = ["00FF00", "0000FF", "FFFFFF", "FF00FF", "FFFF00", "FF0000", "00FFFF", "FF8000", "000000"]
atariColors = ["000000","404040","6C6C6C","909090","B0B0B0","C8C8C8","DCDCDC","ECECEC","444400","646410","848424","A0A034","B8B840","D0D050","E8E85C","FCFC68","702800","844414","985C28","AC783C","BC8C4C","CCA05C","DCB468","ECC878","841800","983418","AC5030","C06848","D0805C","E09470","ECA880","FCBC94","880000","9C2020","B03C3C","C05858","D07070","E08888","ECA0A0","FCB4B4","78005C","8C2074","A03C88","B0589C","C070B0","D084C0","DC9CD0","ECB0E0","480078","602090","783CA4","8C58B8","A070CC","B484DC","C49CEC","D4B0FC","140084","302098","4C3CAC","6858C0","7C70D0","9488E0","A8A0EC","BCB4FC","000088","1C209C","3840B0","505CC0","6874D0","7C8CE0","90A4EC","A4B8FC","00187C","1C3890","3854A8","5070BC","6888CC","7C9CDC","90B4EC","A4C8FC","002C5C","1C4C78","386890","5084AC","689CC0","7CB4D4","90CCE8","A4E0FC","003C2C","1C5C48","387C64","509C80","68B494","7CD0AC","90E4C0","A4FCD4","003C00","205C20","407C40","5C9C5C","74B474","8CD08C","A4E4A4","B8FCB8","143800","345C1C","507C38","6C9850","84B468","9CCC7C","B4E490","C8FCA4","2C3000","4C501C","687034","848C4C","9CA864","B4C078","CCD488","E0EC9C","442800","644818","846830","A08444","B89C58","D0B46C","E8CC7C","FCE08C"]

primaryColors = [(255,0,0), (0,255,0), (0,0,255)]

wackyColors = [(255,255,0),
               (0,255,0),
               (255,0,255)]

randoFillList = [18, 19, 20, 21, 24, 26, 33, 34, 36, 37, 38, 39, 42, 43, 44, 45, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 
                 59, 60, 61, 62, 63, 64, 65, 66, 68, 69, 70, 73, 74, 77, 79, 82, 84, 85, 86, 88, 90, 91, 92, 93, 101, 102, 103, 104,
                 108, 109, 110, 111, 112, 113, 114, 115, 119, 121, 122, 124, 125, 126, 127, 128, 134, 135, 139, 140, 141, 142, 143,
                 149, 150, 151, 152, 153, 154, 155, 156, 157, 159, 161, 163, 164, 165, 166, 167, 168, 169, 170, 172, 173, 174, 175,
                 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191]

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
    "FOUNTAIN WAVE MASKS",
    "i don't remember",
    "SEDUCING MEDUSAS",
    "84-2",
    "circle grid",
    "DUDE LEMONADE",
    "GOD RAYS",
    "BRICK GRID (OINK)",
    "modulated sign interference",
    "JUNGLE DATA",
    "DINO'S DESSERT",
    "BROKEN TARGETS",
    "CUNEUS CONSTELLATIONS",
    "SQUARE STRIPES",
    "PUDDLE KINK",
    "CIRCLE CIRCLES",
    "SQUARES, INTERRUPTED",
    "PARALLELOGRAM PATTERN",
    "SICKO CELLS",
    "HILBERT ROT",
    "MISFIT FATHER",
    "PHI FALSECALYX",
    "AIRHOLE GUILLOCHE",
    "VIBRATION HEMSTITCH",
    "ROSY EXPLOSION",
    "SOUTHEAST CARVING",
    "BADPERSON WHAMMY",
    "STAGGERED BLOCKS",
    "ZIGZAG FEAST",
    "TDLDLT",
    "TESSELATED RHYTHMS", # [sic]
    "BAD PERSPECTIVE",
    "and another one ridesah the bus ahhhh",
    "SIMPLY DOOBY DOO",
    "93-2: 84-3",
    "CHERRIES AND VEGETABLES",
    "WELCOME TO ERF",
    "MANTISSA SIREN",
    "THE REMAINDER CATHEDRAL",
    "BEWB TOOB",
    "HYPERBOLE OMICRON",
    "STARBURST SWORDFIGHT",
    "BESSEL RINGS",
    "NUDE ANTONYM",
    "FAIL WHALE TAIL",
    "ELLIPE INC",
    "ELLIPE IS STANDING ON IT",
    "NUKE FUZZ",
    "RIPPLE RAPPLE",
    "CROSS BOXES",
    "CROSS DIAMONDS",
    "BOSS CROXES",
    "ENNEAD REVISING",
    "GAMMA QUADRANT",    
    "TWELVE TWELVES",
    "145",
    "146",
    "METATRON LATTICE",
    "Līminārus",
    "BOAMOND CRUXES N DIXES",
    "Metatron's Bored",
    "LA DITHERA",
    "DIGITAL EXPLOSION",
    "GOING THE DISTANCE",
    "LIFETIME PLAYGROUND",
    "DISTANT CUM",
    "156",
    "DON'T EAT THE BALL MEAT",
    "ARCHIE'S SPIRAL",
    "VARIED VARIANTS",
    "CARPET CLEANING",
    "FUZZED GRID",
    "162",
    "163",
    "BUBBLE UP BOXES",
    "CIRCLE FACTORY",
    "ANT FACTORY",
    "CROSSHATCH FOCUS",
    "STARBURNST",
    "ROUNDBALL JAZZ",
    "TILTED FLANNEL",
    "DOUBLED-UP ROSES",
    "ADVENTURE INTO THE UNKNOWN",
    "DEMONS FROM DIAMONDS",
    "LOCAL FTARIES",
    "CIRCLY DOOS",
    "ANGULAR SWIRLIES",
    "DIAGONAL SINES",
    "回転したポテト",
    "THE READING LIGHT",
    "GRITTYEST-LIKE",
    "TRIAL TOWERS",
    "HEXAGON ALLEY",
    "CONEYHOME",
    "HEXES AND BANDS",
    "TWO BIRDS ONE ELEPHANT",
    "SIERPINSKI",
    "187",
    "NEXT ONE",
    "ANOTHER ONE",
    "190",
    "191",
    "192 JULIA",
    "SQUARE PATTERN",
    "194"
    # next iAlg goes here - #NXT
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

imageoplist = ["adaptive", "adaptive_dither", "adaptive_mediancut", "adaptive_quant", "fourit", "twoit", "invert", "hueshift", "huerotate", "edge", "contour", "detail", 
               "pixelate", "fourcolorTDL", "godcolor", "fourblend", "redit", "greenit", "blueit", "colorit", "colorize", "colorizeerize", "coloritup", "garlic",
               "findfaces", "grayscale", "minfilter", "maxfilter", "medianfilter",
               "remixed", "remix_blend", "doublediff", "linepainter_inv", "fullfill_diff",
               "copydiff", "colorhatch_diff", "colorhatch_bw_diff", "fullgradient_diff", "canny_inv", "canny_color", "weirderator", 
               "cornerharris", "kmeans", "xanny", "topographica", "autocontrast", "ordered_dither", "halftone", "crt_mask"]

# --- safe funcs ---------------------------------------------

def getSafeFuncs():
    safeFuncs = [altWorld,
                atariripples,
                bigSquareGrid_remixed,
                colorHatch,
                ctrlWorld,
                diagonal4Way,
                diagonalXWay,
                dots_palette,
                dots,
                field_to_image,
                flow_ribbons,
                fourdotsRemixed,                
                gradientSquares,
                gritty,
                grittyerest,
                hardLandscape,
                hsvEnum,
                muchoLetters,
                nightgrid,
                nightgridStars,
                numpy_Fullfill,
                paletteSquares,
                radial_gradient,
                radioFill,
                sigilGrid,
                single_gradient,
                spirograph,
                subtlyWrong,
                textGen,
                triangleSys,
                truchetTiles,
                vaguetransfer,
                voronoiMosaic,
                waveInterference,
                zamb_logo_grid]

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

wrapperData["function_states"]["0"] = manager.list()

words = []
wordsPositive = []
wordsNegative = []
wordsVerb = []
wordsNoun = []
wordsAdjective = []
wordsJargon = []
wordsMoby = dict()
ffSpecificState = 0
ffSpecificState2 = 0
ffSpecificState3 = 0
ffSpecificState4 = 0
ffSpecificState5 = 0

rng = random.Random()

palette100_chosen = None
cached_lexicons = None

def getPaletteText(id=302):
    global palette302_text
    return palette302_text

palettelist = [
    (-1, "-1 (random palette)", "", "rnd,generative"),
    (1, "1 (VAPORWAVE)", "", "wave,digital,retro"),
    (2, "2 (PRIMARY)", "", "basic,tdl"),
    (3, "3 (WACKY)", "", "basic,tdl,novelty"),
    (4, "4 (COCO)", "", "cpu,basic,tdl,retro"),
    (5, "5 (ATARI)", "", "cpu,basic,tdl,retro,gaming"),
    (6, "6 (grylteal)", "", "basic,tdl"),
    (7, "7 (dare to dream)", "", "game,basic,tdl,experimental"),
    (8, "8 (godfilter)", "", "basic,tdl,abstract"),
    (9, "9 (hot dog stand)", "", "novelty,retro,windows"),
    (10, "10 (AAP-DGA16 - CGA/EGA Edit)", "", "cpu,retro,graphics"),
    (11, "11 (CGA MODE 4 1 HIGH - cyan/pink)", "", "cpu,retro,graphics"),
    (12, "12 (CGA MODE 4 0 HIGH - red/green)", "", "cpu,retro,graphics"),
    (13, "13 (HELLDEATH)", "", "dark,edgy,metal"),
    (14, "14 (PICO-8)", "", "cpu,retro,gaming,console"),
    (15, "15 (8-BIT HANDHELD)", "", "cpu,retro,gaming,console"),
    (16, "16 (RESURRECT JUPITER)", "", "cosmic,abstract,universe"),
    (17, "17 (YOUR FRIEND'S CHAMBER)", "", "universe,atmosphere,personal"),
    (18, "18 (THE BRANE OF EQUINOX)", "", "universe,cosmic,abstract"),
    (19, "19 (pastels)", "", "soft,art,palette"),
    (20, "20 (rainbow)", "", "spectrum,bright"),
    (21, "21 (hsv rnd)", "", "rnd,generative"),
    (22, "22 (light text)", "", "ui,minimal"),
    (23, "23 (ALL CGA)", "", "cpu,retro,graphics"),
    (24, "24 (CGA++)", "", "cpu,retro,graphics"),
    (25, "25 (CHASM)", "", "lospec,curated,art"),
    (26, "26 (defective)", "", "experimental,glitch"),
    (27, "27 (8-BIT HVC)", "", "cpu,retro,console"),
    (28, "28 (LIMEDEATH)", "", "novelty,glitch,experimental"),
    (29, "29 (BLUEDEATH)", "", "novelty,glitch,experimental"),
    (30, "30 (DEATHDEATH)", "", "novelty,glitch,experimental"),
    (31, "31 (OUTRUN)", "", "wave,digital,retro,neon"),
    (32, "32 (sunset)", "", "nature,sky,evening"),
    (33, "33 (cappuchino)", "", "food,beverage,earthy"),
    (34, "34 (solemn bob)", "", "novelty,music"),
    (35, "35 (radical)", "", "retro,extreme"),
    (36, "36 (Mystic Nights)", "", "cosmic,dark,mystic"),
    (37, "37 (ice cream lambo (LAMBO!) )", "", "novelty,food,car"),
    (38, "38 (ice cream metal)", "", "novelty,food,music"),
    (39, "39 (ice cream mental)", "", "novelty,food,abstract"),
    (40, "40 (dare to nightmare)", "", "dark,cosmic,experimental"),
    (41, "41 (beachy peach)", "", "nature,beach,fruit"),
    (42, "42 (42)", "", "novelty,hitchhiker,meta"),
    (43, "43 (BOATS AND HOES)", "", "novelty,music,humor"),
    (44, "44 (You and Me)", "", "romantic,personal"),
    (45, "45 (bosdox coobbrack)", "", "novelty,abstract"),
    (46, "46 (boyngirl)", "", "gender,identity,novelty"),
    (47, "47 (metatronWorld)", "", "universe,cosmic,meta"),
    (48, "48 (synthwave)", "", "wave,digital,retro,neon"),
    (49, "49 (TWILIGHT 5)", "", "lospec,curated,evening"),
    (50, "50 (city sunset)", "", "urban,nature,sky"),
    (51, "51 (Amber CRT)", "", "digital,retro,display"),
    (52, "52 (Thermal Camera)", "", "tech,infrared,visual"),
    (53, "53 (Forest Canopy)", "", "nature,forest"),
    (54, "54 (Ocean Waves)", "", "nature,water"),
    (55, "55 (Bauhaus Print)", "", "art,design,print"),
    (56, "56 (Corporate '90s)", "", "corporate,retro,office"),
    (57, "57 (Cyberpunk Alley)", "", "cyberpunk,urban,technoir"),
    (58, "58 (Solarized Variant)", "", "tech,terminal,scheme"),
    (59, "59 (jazz cup)", "", "retro,90s,pattern"),
    (60, "60 (portland carpet)", "", "retro,90s,pattern"),
    (61, "61 (arcade carpet)", "", "retro,90s,pattern,arcade"),
    (62, "62 (trapper keeper)", "", "retro,90s,stationery"),
    (63, "63 (ZEDDY SPECCY)", "", "cpu,retro,console"),
    (64, "64 (MOS6510)", "", "cpu,retro,console"),
    (65, "65 (Desert Sun)", "", "nature,desert,sun"),
    (66, "66 (Tropical Fruit)", "", "nature,fruit,tropical"),
    (67, "67 (glitchwave)", "", "wave,digital,glitch"),
    (68, "68 (BLUELIFE)", "", "novelty,life,abstract"),
    (69, "69 (CYANLIFE)", "", "novelty,life,abstract"),
    (70, "70 (CYANDEATH)", "", "novelty,glitch,abstract"),
    (71, "71 (Green CRT)", "", "digital,retro,display"),
    (72, "72 (Blue CRT)", "", "digital,retro,display"),
    (73, "73 (Rust and Patina)", "", "nature,decay,industrial"),
    (74, "74 (Memphis Design)", "", "art,design,pattern"),
    (75, "75 (Corporate 2000s)", "", "corporate,office,modern"),
    (76, "76 (Neon Tubes)", "", "urban,retro,lighting"),
    (77, "77 (Plastic Toys)", "", "toy,childhood,retro"),
    (78, "78 (CRAYON 8)", "", "real,crayon,childhood"),
    (79, "79 (CRAYON PEOPLE)", "", "real,crayon,childhood"),
    (80, "80 (CRAYON 64)", "", "real,crayon,childhood"),
    (81, "81 (Pastel Goth)", "", "alt,goth,pastel"),
    (82, "82 (Modern SaaS/Corporate Pastel)", "", "corporate,ui,modern"),
    (83, "83 (Aurora Borealis)", "", "nature,sky,northern"),
    (84, "84 (Renaissance Fresco)", "", "art,painting,classical"),
    (85, "85 (Japanese Woodblock)", "", "art,print,traditional"),
    (86, "86 (Pop Art CMYK)", "", "art,print,pop"),
    (87, "87 (Woodgrain MOS6502)", "", "cpu,retro,console"),
    (88, "88 (Toxic Earth)", "", "nature,earth,industrial"),
    (89, "89 (Alice in Wonderland)", "", "literary,fantasy,whimsy"),
    (90, "90 (Bird Cry)", "", "nature,bird,poetic"),
    (91, "91 (Cotton Candy Rainbow)", "", "novelty,candy,bright"),
    (92, "92 (Ice Cream)", "", "food,sweet,novelty"),
    (93, "93 (Loud Amplifiers)", "", "music,volume,novelty"),
    (94, "94 (Vocaloid Girl)", "", "music,anime,idol"),
    (95, "95 (Lawful Evil Contractor)", "", "humor,concept,novelty"),
    (96, "96 (distant 4)", "", "rnd,generative,abstract"),
    (97, "97 (distant 6)", "", "rnd,generative,abstract"),
    (98, "98 (palette from dir)", "", "rnd,generative"),
    (99, "99 (GEN|ERA|TED)", "", "rnd,generative,abstract"),    
    (100, "100 (MEGA GEN 100)", "", "rnd,generative,abstract"),
    (101, "101 (Dot Eaters)", "", "game,80s"),
    (102, "102 (Old Comic)", "", "retro,comic"),
    (103, "103 (Progress Pride)", "", "pride,flag"),
    (104, "104 (Happy Accident Paints)", "", "paint,bob,art"),
    (126, "126 (defectivejunk)", "", "experimental,glitch"),
    (226, "226 (defectivejunk++)", "", "experimental,glitch"),
    (255, "255 (MONSTER GEN 255)", "", "rnd,generative,abstract"),
    (300, "300 (Autumn Glow)", "", "nature,season,fall"),
    (301, "301 (Autumn Harvest)", "", "nature,season,fall"),
    (302, "302 (rnd wn)", "", "rnd,generative"),
    (303, "303 (Grandma's Couch)", "", "retro,pattern,fabric"),
    (304, "304 (Dia de los Muertos)", "", "festival,folk,tradition"),
    (305, "305 (Dashikis)", "", "textile,culture,pattern"),
    (306, "306 (50s Americana)", "", "retro,americana,vintage"),
    (307, "307 (Boring Rich Guy)", "", "muted,corporate,minimal"),
    (308, "308 (Web 1.0)", "", "retro,web,internet"),
    (309, "309 (Flesh and Bone)", "", "organic,material,neutral"),
    (310, "310 (Mech Squadron)", "", "tech,mecha,industrial"),
    (311, "311 (Braided Carrot)", "", "food,vegetable,novelty"),
    (312, "312 (neon red undertone)", "", "abstract,neon,experimental"),
    (313, "313 (pinned greenish mutation)", "", "abstract,experimental"),
    (314, "314 (clashing wrongness)", "", "experimental,clash,novelty"),
    (315, "315 (quad decay green dom)", "", "experimental,abstract"),
    (316, "316 (dried bloods and bile)", "", "dark,grunge,organic"),
    (317, "317 (sinusoidal red-green ramp)", "", "math,experimental"),
    (318, "318 (quad decay blue dom)", "", "experimental,abstract"),
    (319, "319 (xor between channels)", "", "math,glitch,experimental"),
    (320, "320 (hsv rainbow)", "", "rnd,generative,spectrum"),
    (321, "321 (prime-modulated)", "", "math,experimental"),
    (322, "322 (harsh neon inversions)", "", "experimental,neon"),
    (323, "323 (noise based)", "", "experimental,procedural"),
    (324, "324 (log ramp - warped earth tones)", "", "math,earthy,experimental"),
    (325, "325 (Fashion 2025 - Spring/Summer)", "", "fashion,trend,modern"),
    (326, "326 (defectivejunkorama)", "", "experimental,glitch"),
    (327, "327 (US Highway)", "", "transport,signage,standard"),
    (328, "328 (W3Schools Camo)", "", "web,novelty,pattern"),
    (329, "329 (Geno)", "", "cult,character,novelty"),
    (330, "330 (Randy Bill and Previs the Protractor)", "", "novelty,in-joke"),
    (331, "331 (Spicy Cherry and Lemon/Lime)", "", "food,drink,novelty"),
    (332, "332 (Watermelon Game)", "", "game,novelty,fruit"),
    (333, "333 (CLASHING 333 SPECIAL)", "", "experimental,clash,novelty"),
    (334, "334 (\"Memorable\")", "", "meta,novelty"),
    (335, "335 (Bubblegum Pink (I Know It's))", "", "novelty,humor"),
    (336, "336 (Careful With Those Snacks, You Queen)", "", "music,floyd,novelty"),
    (337, "337 (Quay Cur)", "", "music,novelty"),
    (338, "338 (actual forest)", "", "nature,forest"),
    (339, "339 (forest highlights)", "", "nature,forest"),
    (340, "340 (fourth prime)", "", "math,prime,experimental"),
    (341, "341 (Amethyst Storm)", "", "abstract,ethereal,storm"),
    (342, "342 (Neon Coven)", "", "occult,neon,club"),
    (343, "343 (Snow Crash)", "", "literary,cyberpunk"),
    (344, "344 (Paper Lantern)", "", "festival,soft,ambient"),
    (345, "345 (Plasma Bloom)", "", "energy,neon,abstract"),
    (346, "346 (Golden Hour Static)", "", "nature,sunset,grain"),
    (347, "347 (Lemon Circuitry)", "", "tech,circuit,neon"),
    (348, "348 (Cornfield Cathedral)", "", "nature,architecture"),
    (349, "349 (Toxic Mustard)", "", "industrial,grunge,hazard"),
    (350, "350 (Sunbleach Mirage)", "", "desert,faded,illusion"),
    (351, "351 (Fire and Iceberg)", "", "contrast,dual,nature"),
    (352, "352 (Dull Rainbow)", "", "full"),
    (353, "353 (Sophie's Choices)", "", "in-joke,novelty"),
    (354, "354 (Blue Bomber)", "", "game"),
    (355, "355 (HTML Named Colors)", "", "web,css,netscape,x11,quirky")
    ]

# code begins here -- multiproc // timeout ------------- @~-------

# TODOs ---~ we define the magick to become the magick ~----------

# * put tdldl on a vps
# * have fun
# * EXIGENT MIDNIGHT
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

    floodfill_count_reset()

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

    bucky_extra = getParam_Bucky("EXTRA")

    if bucky_extra:
        TIMEOUT = TIMEOUT * 2.0

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
        proc.join(timeout=0.2)
        if proc.is_alive(): proc.terminate()
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

    tot_time = round(t1-timeStart, 5)

    if i == 0:
        stringy = f"elapsed: {tot_time:.5f} | {otherInfo}"
        colorPrint.print_warn(stringy)
        addState(stringy)
    else:
        colorPrint.logger_whatever(f"elapsed: {tot_time:.5f} | {otherInfo}")

    return

def logException(e):
    tback = traceback.format_exc()
    fstack = traceback.format_stack()
    
    rootLogger.error(str(datetime.datetime.now()))
    rootLogger.error(tback)
    rootLogger.error(str(fstack))
    rootLogger.error("---------------------")
    
# utility/supporting functions ------------------------- @~-------

def resetChosenPalette100():
    global palette100_chosen
    palette100_chosen = None

def prep():
    getAllPalettesFromDir()
    global rng
    random.seed()
    resetChosenPalette100()
    
    global cached_lexicons
    cached_lexicons = None
    return

def has_bucky_bit(buckyBits: int, label: str) -> bool:
    global bucky_labels
    try:
        idx = bucky_labels.index(label.upper())
    except ValueError:
        raise ValueError(f"Unknown bucky bit label: {label}")
    return bool((buckyBits >> idx) & 1)

def getParam_Bucky(label: str) -> bool:
    buckyBits = getParam(8)
    buckyBits = int(buckyBits) if buckyBits.isdecimal() else 0
    return has_bucky_bit(buckyBits, label)

def getParam(i, textOnly=False):
    global extParams
   
    result = ""
    
    if extParams != []:
        if i >= 0 and len(extParams) >= (i+1) and extParams[i] != "":
            result = extParams[i]
        elif i < 0 and extParams[i] != "":
            result = extParams[i]
        
    if textOnly:
        result = "" if result.isdecimal() else result

    return result

def getParam_Variant():
    p3 = getParam(6)
        
    variant = int(p3) if p3.isdecimal() else 0
    
    if p3 in [-1,"-1"]:
        variant = random.randint(0, 50)

        addState(f'variant chosen for -1: {variant}')

    return variant

def getIntParams(defaultP1=250, defaultP2=100):
    p1 = getParam(0)
    p2 = getParam(1)
    p1 = int(p1) if p1.isdecimal() else defaultP1
    p2 = int(p2) if p2.isdecimal() else defaultP2

    return (p1, p2)

def getParam_Func(i):
    px = getParam(i)

    stampFuncs = getSafeFuncs()
    stampf = random.choice(stampFuncs)

    if px != "":
        for sf in stampFuncs:
            if sf.__name__ == px:
                stampf = sf
                break      

    return stampf

def getTextPosFromImgAndTextSize(img_size, text_size):
    # |                 |                 |
    # |          |             |          |
    # x = midpoint minus (half the text/2)

    midpoint = int(img_size // 2)
    half_text = int(text_size // 2)
    z = midpoint - half_text if midpoint - half_text >= 0 else 0
        
    return z

def getRandomFloodFill(list_to_avoid=None):
    global maxFloodFillArg

    iAlg = random.randint(1, maxFloodFillArg)

    while iAlg in list_to_avoid:
        iAlg = random.randint(1, maxFloodFillArg)
    
    return iAlg

def getRandomFloodFill_Rando():
    global randoFillList

    return random.choice(randoFillList)

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

def list_hex_to_rgb(hexc):
    choices = []
    for c in hexc:
        choices.append(hex_to_rgb(c))
    return choices

def list_rgb_to_hex(choices):
    hexc = []
    for c in choices:
        hexc.append(rgb_to_hex(c))
    
    return hexc

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

def myhsv_to_rgb(hsv):
    p = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
    p = (int(p[0] * 255.0), int(p[1] * 255.0), int(p[2] * 255.0))

    return p

def quick_contrast(color, bg):
    # crude relative luminance
    # direct luma approximation
    def lummy(c): return 0.299*c[0] + 0.587*c[1] + 0.114*c[2]

    if abs(lummy(color) - lummy(bg)) < 128:
        # bump up or down by 100 in each channel
        if lummy(bg) > 128:
            return tuple(max(0, c-100) for c in color)
        else:
            return tuple(min(255, c+100) for c in color)
        
    return color

def lum(r,g,b,a=0):
    # perceptual brightness hack
    return math.sqrt( .241 * r + .691 * g + .068 * b )

def sort_by_lum(choices):
    choices.sort(key=lambda rgb: lum(*rgb))

    return choices

def sort_by_hue(choices):
    def hue_key(rgb):
        r, g, b = [c / 255.0 for c in rgb]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return (h, s, v)  # hue first, then saturation, then value
    
    choices.sort(key=hue_key)

    return choices

def sort_by_sat(choices):
    def sat_key(rgb):
        r, g, b = [c / 255.0 for c in rgb]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return (s, h, v)
    
    choices.sort(key=sat_key)

    return choices

def sort_by_hsv_band(choices):
    def hsv_band_key(rgb):
        r, g, b = [c / 255.0 for c in rgb]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        
        # Hue bands: 0–1 scaled to 0–360° 
        deg = h * 360
        
        if deg < 30 or deg >= 330:  # Red
            band = 0
        elif deg < 90:             # Yellow/Orange
            band = 1
        elif deg < 150:            # Green
            band = 2
        elif deg < 210:            # Cyan/Teal
            band = 3
        elif deg < 270:            # Blue
            band = 4
        else:                      # Purple/Magenta
            band = 5
        
        # Sort within band by saturation then value
        return (band, -s, -v)
    
    choices.sort(key=hsv_band_key)
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
    
    r = random.randint(0, 255)    
    g = random.randint(0, 255)    
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

def is_gray(rgb, min_dist=10):
    """
    Check if an (r,g,b) tuple is approximately gray.
    
    Args:
        rgb (tuple): A 3-tuple (r,g,b), values 0–255.
        min_dist (int): Minimum allowed distance between channels
                        for the color to NOT be considered gray.
    
    Returns:
        bool: True if the color is gray-like, False otherwise.
    """
    r, g, b = rgb
    return (
        abs(r - g) < min_dist and
        abs(r - b) < min_dist and
        abs(g - b) < min_dist
    )

def classify_palette_colors(
    rgbs,
    *,
    # Saturation/value thresholds for achromatic buckets
    sat_gray_thresh=0.18,   # below this S → likely gray/black/white
    val_black_thresh=0.18,  # below this V → black
    val_white_thresh=0.92,  # above this V (and low S) → white
    # Hue band edges in degrees [0, 360); red wraps around
    bands=None
):
    """
    Classify a list of RGB tuples (0-255 each) into color bands and return counts,
    percentages, and the dominant band.

    Args:
        rgbs: iterable of (r,g,b) tuples
        sat_gray_thresh: S below this → achromatic bucket
        val_black_thresh: V below this (and low S) → 'black'
        val_white_thresh: V above this (and low S) → 'white'
        bands: optional list of (name, start_deg, end_deg) (end exclusive),
               with 'red' handled via wrap-around if start > end.

    Returns:
        {
          "counts": {band: count, ...},
          "percentages": {band: pct_float_0to1, ...},
          "dominant": band_name_or_None,
          "assignments": [band_for_each_input]
        }
    """
    if bands is None:
        # Reasonable defaults; adjust to taste
        bands = [
            ("red",     345,  15),  # wrap-around
            ("orange",   15,  45),
            ("yellow",   45,  70),
            ("green",    70, 170),
            ("cyan",    170, 200),
            ("blue",    200, 255),
            ("purple",  255, 290),
            ("magenta", 290, 345),
        ]

    def _bucket_from_hsv(h, s, v):
        # Achromatic checks first
        if s < sat_gray_thresh:
            if v < val_black_thresh:
                return "black"
            if v > val_white_thresh:
                return "white"
            return "gray"

        deg = (h * 360.0) % 360.0

        for name, start, end in bands:
            # handle wrap bands (e.g., red 345-15)
            if start <= end:
                if start <= deg < end:
                    return name
            else:
                # wrap around 360: [start, 360) U [0, end)
                if deg >= start or deg < end:
                    return name

        # Fallback (shouldn't happen with full coverage)
        return "other"

    assignments = []
    for (r, g, b) in rgbs:
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        assignments.append(_bucket_from_hsv(h, s, v))

    counts = Counter(assignments)
    total = len(assignments) if assignments else 0
    percentages = {k: (counts[k] / total if total else 0.0) for k in counts}

    if percentages:
        values = list(percentages.values())
        # if all percentages equal (within float tolerance), call it even
        if len(values) > 1 and len(set(round(v, 6) for v in values)) == 1:
            dominant = "even"
        else:
            dominant = max(percentages, key=percentages.get)
    else:
        dominant = None

    return {
        "counts": dict(counts),
        "percentages": percentages,
        "dominant": dominant,
        "assignments": assignments
    }

def resizeToMinMax(img, maxW, maxH, minW, minH):
    w, h = img.size
    
    doTimeCheck(f"resizeToMinMax starts - {int(w)},{int(h)}")

    img = resizeToMin(img, maxW, maxH, minW, minH)

    z = resizeToMax(img, maxW, maxH)
    
    doTimeCheck("resizeToMinMax complete")

    return z

def resizeToMin(img, maxW, maxH, minW, minH):
    w, h = img.size
    
    doTimeCheck(f"resizeToMin starts - {int(w)},{int(h)}")
    
    if img.size[0] > maxW or img.size[1] > maxH or img.size[0] < minW or img.size[1] < minH:
        (w, h) = getSizeByMinMax(img.size[0], img.size[1], maxW, maxH, minW, minH)

        if w != img.size[0] or h != img.size[1]:
            doTimeCheck(f'doin\' a resize')
            img = img.resize((w, h), Image.LANCZOS)

    doTimeCheck(f"resizeToMin complete - {int(w)},{int(h)}")

    return img

def resizeToMax(img, maxW, maxH):
    w, h = img.size

    doTimeCheck(f"resizeToMax starts - {int(w)},{int(h)}")

    if img.size[0] > maxW or img.size[1] > maxH:
        (w, h) = getSizeByMax(img.size[0], img.size[1], maxW, maxH)

        w, h = int(w), int(h)
        
        if w != img.size[0] or h != img.size[1]:
            doTimeCheck(f'doin\' a resize')
            img = img.resize((w, h), Image.LANCZOS)

    doTimeCheck(f"resizeToMax complete - {int(w)},{int(h)}")

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

    return (int(resizedW), int(resizedH))

def getSizeByMax(w, h, maxW, maxH):
    # resize the image down to <= the original size
    
    resizedW = w
    resizedH = h

    r = (h * 1.0) / w
    
    while resizedW > maxW or resizedH > maxH:
        resizedW -= 1.0
        resizedH = r * resizedW

    return (int(resizedW), int(resizedH))

def resizeToMatch(img1, img2):
    outputW = 0
    outputH = 0

    if(img1.size[0] >= img2.size[0]):
        outputW = int(img1.size[0])
        outputH = int(img1.size[1])
    else:
        outputW = int(img2.size[0])
        outputH = int(img2.size[1])
    
    doTimeCheck(f'doin\' 2 resizes to {outputW},{outputH}')
    img1 = img1.resize((outputW, outputH))
    img2 = img2.resize((outputW, outputH))

    return (img1, img2)

def getTempFile(tempDir="./"):
    import tempfile
   
    return tempfile.NamedTemporaryFile(dir=tempDir)

def writeImageException(e):
    global fontPathSansSerif
    exc_type, exc_obj, exc_tb = sys.exc_info()
    tback = traceback.format_exc()

    rootLogger.error(sys.exc_info())

    logException(e)

    colorPrint.print_custom_palette(141, f"{e}")
            
    img = Image.new("RGBA", (1024, 768), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    
    fon = ImageFont.truetype(fontPathSansSerif, 18)
    debugFillColor = (0, 0, 0, 255)
    textY = 0
    
    outputMsg = str(e)
    
    draw.text((5, textY), outputMsg, font=fon, fill=debugFillColor)

    outputMsg = "at line: " + str(exc_tb.tb_lineno)
    
    textY += 24

    draw.text((5, textY), outputMsg, font=fon, fill=debugFillColor)

    textY += 48

    draw.multiline_text((5, textY), tback, font=fon, fill=debugFillColor, spacing=25, align="left")

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

    splitCount = totalCount // max(rangeCount, 1)

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

def dropin_text_size(draw, text, font):
    # To get the bounding box of the text:
    left, top, right, bottom = draw.textbbox((0, 0), text, font)
    width = right - left
    height = bottom - top
    return (width, height)

def vflag(v, bit): return (v >> bit) & 1

def getNextPoint(points, pointsChosen):    
    complete = False

    for point in points:
        if point not in pointsChosen:
            return (point, complete)

    complete = True
    return ((-1,-1), complete)

def get_best_contrast_color(rgb):
    """
    Given an (r,g,b) tuple, returns either (0,0,0) for black or (255,255,255) for white
    depending on which has the better contrast.
    """

    r, g, b = rgb

    # Normalize to 0..1
    r, g, b = [x / 255.0 for x in (r, g, b)]

    # Apply gamma correction
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4

    # Relative luminance
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b

    # Choose black or white depending on luminance
    return "black" if luminance > 0.5 else "white"

def seed32_sha(text: str) -> int:
    """Stable 32-bit seed from text using SHA-256 (first 4 bytes)."""
    h = hashlib.sha256(text.encode("utf-8")).digest()
    return int.from_bytes(h[:4], "big")  # 0..2**32-1

def words_to_hex(text: str) -> str:
    return f"0x{seed32_sha(text):08X}"

# ---- axial/cube rounding for hexes ----
def _hex_round_axial(q, r):
    # axial (q,r) -> cube (x,y,z), round, back to axial
    x, z = q, r
    y = -x - z
    rx, ry, rz = round(x), round(y), round(z)
    x_diff, y_diff, z_diff = abs(rx - x), abs(ry - y), abs(rz - z)

    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry - rz
    elif y_diff > z_diff:
        ry = -rx - rz
    else:
        rz = -rx - ry
    return rx, rz  # axial (q,r)

# ---- pointy-topped layout ----
# size s ≈ hex radius in pixels (from center to corner)
def pt_point_to_axial(x, y, s):
    q = (math.sqrt(3)/3 * x - 1/3 * y) / s
    r = (2/3 * y) / s
    return _hex_round_axial(q, r)

def pt_axial_to_point(q, r, s):
    # center of hex (q,r) in pixel space
    cx = s * math.sqrt(3) * (q + r/2.0)
    cy = s * 1.5 * r
    return cx, cy

# ---- flat-topped layout ----
def ft_point_to_axial(x, y, s):
    q = (2/3 * x) / s
    r = (-1/3 * x + math.sqrt(3)/3 * y) / s
    return _hex_round_axial(q, r)

def ft_axial_to_point(q, r, s):
    cx = s * 1.5 * q
    cy = s * math.sqrt(3) * (r + q/2.0)
    return cx, cy

# ---- end utility functions -------------------- @~-------
# image operations ------------------------------ @~-------

def check_image_operation(img, imageop, palette):
    bucky_shift = getParam_Bucky("SHIFT")
    bucky_adapt = getParam_Bucky("ADAPT")
    bucky_crt_mask = getParam_Bucky("CRTMASK")
    bucky_remix = getParam_Bucky("REMIX")
    bucky_twoed = getParam_Bucky("TWOED")
    bucky_foured = getParam_Bucky("FOURED")

    if bucky_shift:
        z105 = random.randint(0, 360)
        rootLogger.debug(f'doing the bucky shift - {z105} --------------------------------------- SHIFT ----')
        
        img = imageop_huerotate(img, z105)

        addState(f'bucky shift: {z105}')

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

        if iop == "huerotate":
            img = imageop_huerotate(img, 180)

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

        if iop == "ordered_dither":
            img = imageop_ordered_dither(img)

        if iop == "halftone":
            img = imageop_halftone(img)

        if iop == "crt_mask":
            img = imageop_crt_mask(img)

    if bucky_twoed:
        rootLogger.debug(f'doing the bucky twoed ------------------------------------------- TWOED ----')
        img = imageop_two_it(img)
        addState(f'bucky twoed')

    if bucky_foured:
        rootLogger.debug(f'doing the bucky foured ----------------------------------------- FOURED ----')
        img = imageop_four_it(img)
        addState(f'bucky foured')

    if bucky_adapt:
        rootLogger.debug(f'doing the bucky adapt ------------------------------------------- ADAPT ----')
        img = imageop_adaptive_palette(img, palette, quantOption=2)
        addState(f'bucky adapt')

    if bucky_remix:
        rootLogger.debug(f'doing the bucky remix ------------------------- RAH RAH RAH RAH REEEEEMIX --')
        img = imageop_remixed(img)
        addState(f'bucky remix')

    if bucky_crt_mask:
        rootLogger.debug(f'doing the bucky crt mask --------------------------------------- CRTMASK ---')
        img = imageop_crt_mask(img)
        addState(f'bucky crt mask')
        
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
    pal = pal.convert("P", palette=Image.Palette.ADAPTIVE)

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

def imageop_huerotate(img: Image.Image, degrees: float) -> Image.Image:
    hsv = img.convert("HSV")
    np_img = np.array(hsv, dtype=np.uint16)  # use larger int to avoid overflow

    # Rotate hue channel
    np_img[..., 0] = (np_img[..., 0] + int(degrees / 360 * 255)) % 256

    # Back to uint8 and RGB
    np_img = np_img.astype(np.uint8)
    return Image.fromarray(np_img, "HSV").convert("RGB")

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

def imageop_ordered_dither(img, bayer_size=8):    
    B2 = np.array([[0,2],[3,1]], dtype=float)
    def bayer(n):
        M = B2
        while M.shape[0] < n:
            M = np.block([[4*M, 4*M+2],
                          [4*M+3, 4*M+1]])
        return (M / (n*n))
    M = bayer(bayer_size)
    a = np.asarray(img.convert("L"), dtype=float) / 255.0
    H, W = a.shape
    T = np.tile(M, (H//bayer_size+1, W//bayer_size+1))[:H,:W]
    out = (a > T).astype(np.uint8) * 255

    return Image.fromarray(out, "L").convert("RGBA")

def imageop_halftone(img, cell=8):
    g = img.convert("L")
    draw = ImageDraw.Draw(img)
    W,H = img.size

    for y in range(0, H, cell):
        for x in range(0, W, cell):
            r = g.crop((x,y,x+cell,y+cell)).resize((1,1)).getpixel((0,0))/255.0
            rad = (1.0 - r) * (cell*0.5)
            draw.ellipse((x+cell/2-rad, y+cell/2-rad, x+cell/2+rad, y+cell/2+rad),
                         fill=None, outline=(0,0,0,255))

    return img

def imageop_crt_mask(img, pitch=3, alpha=90):
    W,H = img.size
    mask = Image.new("RGBA",(W,H),(0,0,0,0))

    d = ImageDraw.Draw(mask)
    for x in range(0, W, pitch):
        d.line((x,0,x,H), fill=(0,0,0,alpha))

    return Image.alpha_composite(img.convert("RGBA"), mask)

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

    word = random.choice(words).strip()

    if match != "":
        # TODO: fix match
        while word[0].lower() != match[0]:
            word = random.choice(words).strip()            

    return word

palette302_text = getRandomWord()

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

# ASPARTAME STEPCHILD

floodFillCount = 0

def floodfill_count_reset():
    global floodFillCount
    floodFillCount = 0

def floodfill_count_add():
    global floodFillCount
    floodFillCount += 1

uncleTouchysPlayhouse = {}

def floodfill(img, xystart, 
              targetcolour, 
              newcolour, 
              dumpEvery=0,
              randomIt=0,
              sizeLimit=(0,0),
              choices=[],
              maxStackDepth=0,
              tippingPoint=25,              
              compFunc=0,
              stamp=None,
              stampTrans=None,
              disobey=0,
              variantOverride=None,
              popLeft=False):

    floodfill_count_add()

    startTimeCheck()
    colorPrint.print_custom_palette(51, f'[   floodfill starts - #{floodFillCount} - {writeTimeCheck()} ---->') # {getDecree("","")}')

    global uncleTouchysPlayhouse
    uncleTouchysPlayhouse = {}

    width = img.size[0]
    height = img.size[1]

    showFloodedBoxes = getParam(5)
    popLeft = getParam(7)
    variant = getParam_Variant()

    if variantOverride != None:
        variant = variantOverride

    global telemetry    

    (startx, starty) = xystart
    debugMode = False
    resetFloodfillStates()
   
    # workpile = []    
    workpile = deque()

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

    tippingPoint = getTippingPoint(randomIt)
   
    minX, maxX = startx, startx
    minY, maxY = starty, starty  
    i, count, maxCount = 0, 0, 0
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

    touched = {}
   
    workpile.append((startx,starty,0))

    current_state = f"op: floodfill, iAlg: {randomIt} - {getAlgName(randomIt)}, tippingPoint: {tippingPoint}, x: {startx}, y: {starty}, maxStackDepth: {maxStackDepth}, variant: {variant}, popLeft: {popLeft}", None
    addState(current_state)    
    rootLogger.debug(current_state)

    iPoint = 0    
    stackDepth = 1
    totalDetailTime = 0
    totalWorkpileTime = 0

    while len(workpile) > 0 and (count < maxCount or maxCount == 0):
        if dumpEvery > 0 and isItTimeToDump(dumpEvery, iPoint):
            colorPrint.print_custom_rgb(f"workpile: {len(workpile)} -- {writeTimeCheck()} ----->", 255, 0, 88)

        if popLeft == False or popLeft == "False":
            x,y,stackDepth = workpile.pop()
        else:            
            x,y,stackDepth = workpile.popleft()

        pointHash = hash((x,y))

        if dumpEvery > 0 and isItTimeToDump(dumpEvery, iPoint):
            colorPrint.print_custom_rgb(f"now: {(x,y)} ----- {writeTimeCheck()} ----->", 255, 0, 88)
            colorPrint.print_custom_rgb(f"x: {x} y: {y}, count: {count}, maxCount: {maxCount}", 255, 0, 188)
               
        if dumpEvery > 0 and isItTimeToDump(dumpEvery, iPoint):            
            colorPrint.print_custom_palette(13, f"| floodfill: workpile loop begin @ {iPoint} --- {writeTimeCheck()} ---->")
            colorPrint.print_custom_palette(113, f"| x: {x}, y: {y}, count: {count}, maxCount: {maxCount} ---->")

        minX = min(x, minX)
        maxX = max(x, maxX)
        minY = min(y, minY)
        maxY = max(y, maxY)
        
        if "floodfill" not in telemetry:
            telemetry['floodfill'] = {}

        if "max_stack_depth" not in telemetry['floodfill']:
            telemetry['floodfill']['max_stack_depth'] = {}        

        if iAlgOrig == -1:
            # now watch this drive
            randomIt = getRandomFloodFill()

        skipItObviously = False

        if disobey > 0:
            uhahah = random.uniform(0, 1)

            if uhahah > disobey:
                skipItObviously = True

        if maxStackDepth > 0 and stackDepth > maxStackDepth:
            skipItObviously = True

        if pointHash in touched or skipItObviously:
            pass
        elif (sizeLimit[0] == 0 or abs(x-startx) < sizeLimit[0]) and (sizeLimit[1] == 0 or abs(y-starty) < sizeLimit[1]):
            try:
                if dumpEvery > 0 and isItTimeToDump(dumpEvery, iPoint):
                    colorPrint.print_custom_palette(33, f"| floodfill: touchy loop begin @ {iPoint} --- {writeTimeCheck()} ---->")
                    colorPrint.print_custom_palette(67, f"| x: {x}, y: {y}, count: {count}, maxCount: {maxCount}, compFunc: {compFunc} ---->")
                    colorPrint.print_custom_palette(37, f"| sizeLimit: {sizeLimit}, your mom's sizeLimit: infinity ---->")
                    colorPrint.print_custom_palette(47, f"| abs(x-startx): {abs(x-startx)}, abs(y-starty): {abs(y-starty)} ---->")
                    colorPrint.print_custom_palette(57, f"| x < img.size[0]: {x < img.size[0]}, y < img.size[1]: {y < img.size[1]} ---->")
                    colorPrint.print_custom_rgb(f"tc: {targetCheck(pixdata,x,y, targetcolour, compFunc)}", 255, 88, 111)

                #if randomIt != 2:
                    # 2 relies on this broken behavior of filling points multiple times

                touched[pointHash] = 1
                
                if x < img.size[0] and y < img.size[1] and targetCheck(pixdata,x,y, targetcolour, compFunc):
                    # ---------- floodfill randomIt iAlgs begin here ----- switch statement tdlIdFloodfill --> 

                    timeBeforeDetail = time.time()
                    newcolour, choices, x, y, switcher = floodFillDetail(randomIt, choices, tippingPoint, stamp, stampTrans, width, height, variant, startx, starty, choicesChosen, count, i, switcher, colorsKept, timesUsed, conseq, last_z, zCol, mod_alg_value, pixdata, stmpdata, x, y, newcolour, stackDepth)
                    timeAfterDetail = time.time()
                    totalDetailTime += timeAfterDetail-timeBeforeDetail

                    #writeOperationToDisk(currentUID, f"x: {x} y: {y} stackDepth: {stackDepth} maxStackDepth: {maxStackDepth} newcolour: {newcolour}")

                    pixdata[x,y] = newcolour
                        
                    count += 1
                    stackDepth += 1

                    timeBeforeWorkpile = time.time()
                    if maxStackDepth == 0 or stackDepth < maxStackDepth:
                        if x-1 >= 0 and x-1 < img.size[0] and y < img.size[1] and hash((x-1,y)) not in touched and targetCheck(pixdata,x-1,y, targetcolour, compFunc):
                            workpile.append((x-1,y,stackDepth))

                        if x+1 < img.size[0] and y < img.size[1] and hash((x+1,y)) not in touched and targetCheck(pixdata,x+1,y, targetcolour, compFunc):
                            workpile.append((x+1,y,stackDepth))

                        if y-1 >= 0 and x < img.size[0] and y-1 < img.size[1] and hash((x,y-1)) not in touched and targetCheck(pixdata,x,y-1, targetcolour, compFunc):
                            workpile.append((x,y-1,stackDepth))

                        if x < img.size[0] and y+1 < img.size[1] and hash((x,y+1)) not in touched and targetCheck(pixdata,x,y+1, targetcolour, compFunc):
                            workpile.append((x,y+1,stackDepth))
                    
                    timeAfterWorkpile = time.time()
                    totalWorkpileTime += timeAfterWorkpile - timeBeforeWorkpile

                    if dumpEvery > 0 and isItTimeToDump(dumpEvery, iPoint):
                        colorPrint.print_custom_palette(143, f"\t[ff dump: {writeTimeCheck()} --> ")
                        colorPrint.print_custom_palette(144, f"\tx: {x}, y: {y}")
                        colorPrint.print_custom_palette(149, f"\tstackDepth: {stackDepth}, maxStackDepth: {maxStackDepth}")
                        colorPrint.print_custom_palette(148, f"\tdump done ----------------------]")

            except Exception as e:
                logException(e)
        
        if dumpEvery > 0 and isItTimeToDump(dumpEvery, iPoint):            
            colorPrint.print_custom_palette(7, f"| floodfill: workpile loop end @ {iPoint} --- {writeTimeCheck()} ---->")            
            colorPrint.print_custom_palette(229, f"| point: {[x,y,stackDepth]}, stackDepth: {stackDepth}, maxStackDepth: {maxStackDepth}")
            colorPrint.print_custom_palette(217, f"| ------------------ {writeTimeCheck()} ------------------")

        iPoint += 1

    rootLogger.debug(f"| detail time taken: {round(totalDetailTime, 3)}s     ---->")
    rootLogger.debug(f"| workpile time taken: {round(totalWorkpileTime, 3)}s ---->")

    if showFloodedBoxes == True or showFloodedBoxes in ["True", "true"]:
        for zX in range(minX, maxX):
            pixdata[zX, minY] = (0,255,0)
            pixdata[zX, maxY] = (0,0,255)

        for zY in range(minY, maxY):
            pixdata[minX, zY] = (255,255,0)
            pixdata[maxX, zY] = (255,0,0)

    # addState(f'colorsKept: {colorsKept}')

    colorPrint.print_custom_palette(228, f"| floodfill complete - {count} pts - {writeTimeCheck()} ----]")

    uncleTouchysPlayhouse = touched

    return count

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
    return

def getDistanceVariant(mode, dx, dy, x=None, y=None):
    """
    Return a numeric value based on the chosen math mode.
    dx, dy = offsets from a center point
    x, y   = absolute coordinates (optional)
    """

    if mode == 0:  # Euclidean / circle
        return math.hypot(dx, dy)

    elif mode == 1:  # Manhattan / diamond
        return abs(dx) + abs(dy)

    elif mode == 2:  # Chebyshev / square
        return max(abs(dx), abs(dy))

    elif mode == 3:  # Polar angle
        return math.atan2(dy, dx)

    elif mode == 4:  # Sinusoidal stripes (absolute coords)
        if x is None or y is None:
            return math.sin(dx) + math.cos(dy)
        return math.sin(x * 0.1) + math.cos(y * 0.1)

    elif mode == 5:  # Radial sine
        r = math.hypot(dx, dy)
        ang = math.atan2(dy, dx)
        return r * math.sin(ang * .1)  # tweak multiplier

    elif mode == 6:  # Multiplicative
        return dx * dy

    elif mode == 7:  # Square root product
        return math.sqrt(abs(dx * dy))

    elif mode == 8:  # Logarithmic radial
        return math.log1p(math.hypot(dx, dy))

    elif mode == 9:  # Exponential absolute
        if x is None or y is None:
            return math.exp(math.sin(dx)) + math.exp(math.cos(dy))
        return math.exp(math.sin(x * 0.1)) + math.exp(math.cos(y * 0.1))

    else:  # Default: just Euclidean
        return math.hypot(dx, dy)

@njit
def rotate_point(x, y, degrees):
    """Rotate (x,y) around origin by 'degrees' and return (xr, yr)."""
    rad = math.radians(degrees)
    ca, sa = math.cos(rad), math.sin(rad)
    xr = x * ca - y * sa
    yr = x * sa + y * ca

    return int(xr), int(yr)

def floodFillDetail(randomIt, choices, tippingPoint, stamp, stampTrans, width, height, variant, startx, starty, choicesChosen, count, i, switcher, colorsKept, timesUsed, 
                    conseq, last_z, zCol, mod_alg_value, pxd, stmpdata, x, y, newcolour, stackDepth):
    global ffSpecificState
    global ffSpecificState2
    global ffSpecificState3
    global ffSpecificState4
    global ffSpecificState5

    pixdata = pxd
    cx, cy = startx, starty
    key_used = ""

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
                newcolour = getRandomColorRGB()
            else:
                newcolour = random.choice(choices)                  
        elif variant < 5:
            z = (y << variant) + x

            (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
        elif variant < 10:
            z = x & y & variant

            (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
        elif variant <= 15:
            z = (x | y) & variant

            (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
                        
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
            newcolour = getRandomColorRGB()

            if choices != []:
                (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, i)

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
                        
        if x % 3 == 0 or x % 7 == 0:
            newcolour = ffSpecificState[0]
        elif y % 5 == 0:
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
        if variant == 0:
            newcolour = getRandomColorRGB()
        elif variant == 1:
            newcolour = (200, random.randint(0, 255), 200)
        elif variant == 2:
            newcolour = (200, 200, random.randint(0, 255))
        elif variant == 3:
            newcolour = (random.randint(0, 255), 200, 200)
        else:
            if random.randint(0, variant) == 0:
                newcolour = random.choice(choices)

        if (variant >= 0 and variant < 4) or count % variant == 0:
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
                            
            (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, ffSpecificState)
    elif randomIt == 15:
        # FLANNEL GRID
        if count % 2 == 0:                            
            switcher = 1
        else:
            switcher = -1

        tippingPoint = tippingPoint if variant == 0 else variant // 2

        do_the_needful = variant & 1
        fuzzy = variant & 2

        if do_the_needful:
            xr, yr = rotate_point(x, y, 45)
        else:
            xr, yr = x, y

        if fuzzy and count % 4 == 0:            
            (mod_x, mod_y) = get_grid_vals(x, y, tippingPoint)            
        else:            
            (mod_x, mod_y) = get_grid_vals(xr, yr, tippingPoint)

        z = mod_y + (mod_x * switcher)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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
        
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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
        fuckFactor = variant + 8 if variant > 0 else 8

        mod_x = (x - (x % 10))
                        
        if y % fuckFactor == 0 or (x % (fuckFactor+2) == 0 and y % fuckFactor != 0):
            random.shuffle(choices)
            newcolour = choices[0]
            colorsKept[str(mod_x)] = newcolour
        else:                            
            (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 19:
        # horizontal bars
        mod_y = y - (y % (5 if variant == 0 else variant))
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_y)
    elif randomIt == 20:
        # small flannel
        if ffSpecificState == 0:
            z = y
            ffSpecificState = 1
        else:
            z = x
            ffSpecificState = 0
                            
        mod_x = z - (z % (tippingPoint if variant == 0 else variant))
                        
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 21:
        # vertical bars
        mod_x = x - (x % (5 if variant == 0 else variant))
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
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
                (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, zzz)
            else:
                zzz = amount + (conseq % tippingPoint)
                (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, zzz)
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
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, zqq)                
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
        if variant % 2 == 0:
            z = abs(x % tippingPoint - y % tippingPoint)
        else:
            z = abs(y % tippingPoint - x % tippingPoint)
                        
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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
                        
        z = mod_y + (mod_x * switcher)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 29:
        # 8 bit sq outline
        zonk = 5 if variant == 0 else variant + 4
        tippingPoint = tippingPoint if variant == 0 else variant + 4

        if x % zonk == 0 or y % zonk == 0:
            newcolour = (0,0,0)
        else:
            z = x - (x % tippingPoint) + y - (y % tippingPoint)

            (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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
                        
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_z)
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
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 32:
        # SOUTHEAST CRUMBO                        
        mod_x = x - y + (x % tippingPoint//2) + (y % tippingPoint//2)                        

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 33:
        # TODDLER SOLDIERS
        if count == 0:
            ffSpecificState2 = random.randint(1, 5) * 5

        if variant == 0:
            z = y - (y % ffSpecificState2)
        elif variant == 1:
            z = x - (x % ffSpecificState2)
        elif variant == 2:
            if count % 2 == 0:
                z = x - (x % ffSpecificState2)
            else:
                z = y - (y % ffSpecificState2)
        else:
            if vflag(variant, 0):
                z = x - (x % ffSpecificState2)
            else:
                z = y - (y % ffSpecificState2)

        if count == 0:
            ffSpecificState = 0
            newcolour = random.choice(choices)
        else:
            if ffSpecificState != z:
                newcolour = random.choice(choices)

        ffSpecificState = z
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
                            
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 37:
        # AND MOD
        mod_x = x & y

        if variant >= 1:
            mod_x = mod_x + (variant - (variant % tippingPoint))

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 38:
        # OR MOD
        mod_x = x | y

        if variant >= 1:
            mod_x = mod_x + (variant - (variant % tippingPoint))

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 39:
        # EXP MOD
        mod_x = x ^ y

        if variant >= 1:
            mod_x = mod_x + (variant - (variant % tippingPoint))
                        
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
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

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 41:
        # mark at the boon
        if variant > 1:
            tippingPoint = variant

        if count % 2 == 0:
            ffSpecificState = abs(x - y)
        else:
            ffSpecificState = abs((y ^ x) & (x ^ y))

        mod_x = ffSpecificState - (ffSpecificState % tippingPoint)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 42:
        # HIGH INDIAN
        vvv = 100 if variant == 0 else 5 * variant
        mod_x = int(abs(math.sin(x) + math.sin(y)) * vvv)
        mod_x = mod_x - (mod_x % tippingPoint)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 43:
        # MUSHROOM EXPRESS
        vvv = 100 if variant == 0 else 5 * variant
        mod_x = int(abs(math.sin(x) + math.cos(y)) * vvv)
        mod_x = mod_x - (mod_x % tippingPoint)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 44:
        # LUIGI IN THE SKY WITH DIAMONDS
        vvv = 100 if variant == 0 else 5 * variant
        mod_x = int(abs(math.cos(x) + math.sin(y)) * vvv)
        mod_x = mod_x - (mod_x % tippingPoint)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 45:
        # KNEE FOLDER BURIED IN THE TUNDRA
        vvv = 100 if variant == 0 else 5 * variant

        mod_x = int(abs(math.sin(x) + math.cos(y)) * vvv)
        mod_y = int(abs(math.cos(x) + math.sin(y)) * vvv)
        
        if count & 1 == 0:
            z = mod_x
        else:
            z = mod_y

        #z = random.choice([mod_x, mod_y])        
        z = z - (z % tippingPoint)                        

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 46:
        # ARC EXPLOSION
        ffSpecificState = tippingPoint if variant == 0 else variant

        x2 = abs(startx - x)
        y2 = abs(y - starty)

        mod_x = int(abs(math.hypot(x2, y2)))
        mod_x = mod_x - (mod_x % ffSpecificState)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 47:
        # SATURN'S BIRTHDAY
        ffSpecificState = 250 if variant == 0 else abs(250 - (variant*5))
        mod_x = int(abs(math.log1p(x) + math.log1p(y)) * ffSpecificState)
                        
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 48:
        # CIRCLE 8
        fuckFactor = tippingPoint 

        mod_x = int(abs(math.exp(x % fuckFactor))) + int(abs(math.exp(y % fuckFactor)))
        
        z = mod_x - (mod_x % fuckFactor)

        if count % 2 == 0 and variant > 0:
            z = mod_x % len(choices)    
                        
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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
                        
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 50:
        # PUSH WALLPAPER 
        mod_x = (x ^ y) % len(choices)
                        
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 51:
        # CRAYON NUKE
        mod_x = int(abs(math.hypot(startx-x, starty-y)))
        mod_x = mod_x - (mod_x % tippingPoint)

        mod_y = int(abs(math.log1p(x) - math.log1p(y)) * abs(math.log1p(x) + math.log1p(y)))

        z = mod_x if count & 1 == 0 else mod_y        
                        
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 52:
        # THE SMELL OF BLUEBERRY MARKERS
        mod_x = x ^ y ^ count
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 53:
        # HEROIN FROM TOPANGA                        
        (mod_x, mod_y) = get_grid_vals(x, y, tippingPoint)

        mod_x = ((y ^ x) % 25) & (mod_y | mod_x)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 54:
        # RESOGROVE FINISH
        ffSpecificState = 50 if variant == 0 else variant * 50

        if ffSpecificState < 100:
            ffSpecificState *= 2

        if ffSpecificState > 500:
            ffSpecificState = ffSpecificState % 200

        mod_x = ((x ^ y) & (int(time.time() * ffSpecificState) % 10))
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 55:
        # N_A_T_I_V_E___B_L_A_N_K_E_T____________________
        qx, qy, qx2 = x, y, x
        dx, dy = x - startx, y - starty

        fuckFactor = vflag(variant, 0)
        fuckFactor2 = vflag(variant, 1)

        if fuckFactor:
            qx2 = y

        if fuckFactor2:
            if count % 2 == 0:
                qx2 = x
            else:
                qx2 = y

        mod_x = int(abs(math.hypot(qx, qy))) ^ qx2
        z = mod_x - (mod_x % tippingPoint)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 57:
        # TURN THE KNOB
        qx, qy = x, y
        fuckFactor = vflag(variant, 0)

        if fuckFactor:
            dx, dy = abs(x - startx), abs(y - starty)
            qx, qy = dx, dy

        z = random.choice([qx, qy])
        mod_x = int(abs(math.hypot(qx, qy))) | z
        mod_x = mod_x - (mod_x % tippingPoint)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 58:
        # X MARKS THE X
        mod_x = x ^ y
        mod_x = mod_x - (mod_x % tippingPoint)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 59:
        # JUTTING URANUS
        mod_x = int(abs(math.hypot(x, y)) * math.pi)                        
        i59 = tippingPoint if variant == 0 else variant
                        
        z = mod_x ^ y
        z = z - (z % i59)
                        
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 60:
        # TINY DECO

        dx, dy = x - startx, y - starty

        if dy > dx:
            mod_x = int(abs(math.hypot(dy, dx)) * math.pi)                        
                            
            z = mod_x ^ dx
        else:
            mod_x = int(abs(math.hypot(dx, dy)) * math.pi)                        
                        
            z = mod_x ^ dy
                            
        z = z - (z % tippingPoint)
                        
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 61:
        # ONCE I SHOT GOD ON BROADWAY
        if random.randint(0, 1) == 0:
            mod_x = x & y
        else:
            mod_x = x | y

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 62:
        # YEAH
        z = random.randint(0, 1)
                        
        if (y > x and z == 0) or (x > y and z == 1):
            mod_x = x & y
        else:
            mod_x = x | y

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
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
                        
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 64:
        # D_I_R_T_Y___C_A_R_P_E_T_________________________
        if count == 0:
            ffSpecificState = 1
            ffSpecificState2 = tippingPoint

        if ffSpecificState >= (5 if variant == 0 else variant):
            mod_x = x ^ y if variant != 15 else x | y
                        
            (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)                            
            ffSpecificState = 1                           
        else:
            tippingPoint = ffSpecificState2 * ffSpecificState
            mod_x = x + y - (x % tippingPoint) - (y % tippingPoint)
                        
            (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
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
                        
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 66:
        # ?_??_???_????_?????________________________________
        mod_x = int(x * math.pi) | int(y * math.pi)
        mod_y = int(x * math.e) | int(y * math.e)

        z = mod_x & mod_y
        z = z - (z % tippingPoint)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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
                            
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 70:
        # EL DITHERO ___________________________________
        if count % 2 == 0:
            mod_x = int(abs(math.hypot(x, y))) ^ x                        
        else:
            mod_x = x ^ y

        mod_x = mod_x - (mod_x % tippingPoint)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
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
                        
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
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

            (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
        else:
            z = x + y - (x % ffSpecificState) - (y % ffSpecificState) 
            (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 75:
        # BIG SQUARE PUSSY
        i75 = tippingPoint if variant <= 1 else variant

        if x % i75 == 0 or y % i75 == 0:
            z = variant
        else:
            mod_y = y - (y % i75)
            mod_x = x - (x % i75)

            z = (mod_y << 4) + mod_x

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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

        z = random.randint(1, len(choices))

        mod_y2 = abs(height - y) % tippingPoint
        mod_x = abs(x - y) % tippingPoint
        mod76 = tippingPoint // 2

        if abs(mod_x - mod76) < 1:
            z = 0
            (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, [skool], z)
        elif abs((x % tippingPoint) - mod_y2) < 1:
            z = 0
            (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, [skool], z)
        else:
            (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
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

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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
                                                
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
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

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_84)
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
                        
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_z)
    elif randomIt == 86:
        # DEMIURGE OVERKILL
        if count == 0:
            ffSpecificState = random.random() * 10

        if count % 4 == 0:
            mod_x = int(x * ffSpecificState) | int(y * ffSpecificState)
            mod_y = int(x // ffSpecificState) | int(y // ffSpecificState)
            z = mod_x | mod_y | int(ffSpecificState)
            z = z - (z % tippingPoint)
            (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
        elif count % 2 == 0:
            mod_x = int(x * ffSpecificState) & int(y * ffSpecificState)
            mod_y = int(x // ffSpecificState) & int(y // ffSpecificState)
            z = mod_x | mod_y | int(ffSpecificState)
            z = z - (z % tippingPoint)
            (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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

            (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
            (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_y)
    elif randomIt == 87:
        # idk yet
        if ffSpecificState == 0:
            ffSpecificState = random.uniform(3,8)   

        mod_y = y - (y % tippingPoint)
        mod_x = x - (x % tippingPoint)

        z = ((mod_y << 2) + (mod_x << 4)) | random.randint(0,8)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 88:
        # no men no bears no women
        if y % 2 == 0:
            z = abs(x + y)
        else:
            z = abs(y - x)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 90:
        # FOUNTAIN WAVE MASKS
        vr = variant if variant != 0 else 20

        if count % 4 == 0:
            # Distance from origin
            
            dx, dy = x - cx, y - cy
            dist = math.hypot(dx, dy)

            # Angle in radians, normalized to 0..1
            angle = (math.atan2(dy, dx) + math.pi) / (2 * math.pi)

            # Create spiral index (z) — distance influences base color, angle offsets it
            z = int((dist / 5) + (angle * len(choices))) % len(choices)
        elif count % 2 == 0:
            a = (x % vr) + (y % vr)
            b = (x % vr + 5) ^ (y % vr + 10)
            z = (a * b) % len(choices)
        else:
            tide_x = math.sin(x / 7.0) * len(choices) / 2
            tide_y = math.cos(y / 9.0) * len(choices) / 2
            z = int((tide_x + tide_y + len(choices)) % len(choices))
            
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 91:
        # i don't remember which this is a mix of
        z1 = int(abs(math.hypot(x, y))) ^ x
        z2 = int(abs(math.hypot(x, y))) ^ y
        z1 = z1 - (z1 % tippingPoint)
        z2 = z2 - (z2 % tippingPoint)

        z = z1 | z2

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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
                        
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_84)
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

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 95:
        # DUDE LEMONADE
        variant = 16 if variant == 0 else variant

        cell = variant + 5
        cx = (x // cell) * cell + cell // 2
        cy = (y // cell) * cell + cell // 2
        d = max(abs(x - cx), abs(y - cy))           # Chebyshev distance
        band = max(1, cell // 8)
        ring = (d // band) % len(choices)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, ring)
    elif randomIt == 96:
        # GOD RAYS
        
        dx, dy = x - cx, y - cy
        ang = (math.atan2(dy, dx) + math.pi) / (2*math.pi)  # 0..1
        r = math.hypot(dx, dy)
        k_ang = 16 if variant == 0 else max(4, variant)
        k_rad = 10
        a_id = int(ang * k_ang)
        r_id = int(r / max(1.0, (width+height) / (2*k_rad)))
        z = (a_id + r_id) % len(choices)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 97:
        # BRICK GRID (OINK)
        w = variant if variant > 0 else 32
        h = max(8, w // 2)
        row = y // h
        col = (x + (w//2 if (row & 1) else 0)) // w
        z = (row + 3*col) % len(choices)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 98:
        # modulated sign interference

        # 98 — Modulated sine-band interference mapped to palette
        # Produces curving, moiré-like ribbons by summing a horizontal sine with a
        # vertically-oriented sine whose phase is modulated by x.

        fuckFactorX = 23.0 if variant == 0 else (variant + 4) * 1.0
        fuckFactorY = 19.0 if variant == 0 else variant * 1.0

        sx = x / fuckFactorX        # horizontal spatial frequency (bigger = wider bands)
        sy = y / fuckFactorY        # vertical spatial frequency

        # Two-term wave:
        #  - sin(sx): horizontal bands
        #  - sin(1.7*sy + 0.6*sin(0.7*sx)): vertical bands whose phase is bent by x
        v = math.sin(sx) + math.sin(1.7 * sy + 0.6 * math.sin(0.7 * sx))

        # v is in [-2, 2]; map to [0,1] then to palette slots
        t = (v + 2.0) * 0.25       # normalize to 0..1
        idx = int(t * len(choices)) % len(choices)

        z = idx
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 99:
        # JUNGLE DATA

        # interleave lower 10 bits
        xx, yy = x & 1023, y & 1023
        m = 0
        
        for b in range(10):
            m |= ((xx >> b) & 1) << (2*b)
            m |= ((yy >> b) & 1) << (2*b+1)
        z = (m // 128) % len(choices)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 100:
        # DINO'S DESSERT
        cell = variant + 10 if variant > 0 else 40
        u = (x % cell) < (cell//2)
        v = (y % cell) < (cell//2)
        over = (u ^ v)
        band = max(2, cell//10)
        near_h = (y % cell) < band or (y % cell) > cell - band
        near_v = (x % cell) < band or (x % cell) > cell - band
        z = (2*over + near_h + 2*near_v) % len(choices)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 101:
        # BROKEN TARGETS
        cell = variant + 10 if variant > 0 else 64
        gx, gy = x // cell, y // cell
        # random center inside this cell
        rnd = _hash2(gx, gy)
        cx = gx*cell + (rnd & (cell-1))
        cy = gy*cell + ((rnd>>16) & (cell-1))
        d = int(math.hypot(x - cx, y - cy))
        z = (d // max(1, cell//6)) % len(choices)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 102:
        # CUNEUS CONSTELLATIONS
        cell = variant + 10 if variant > 0 else 48
        gx, gy = x // cell, y // cell
        lx, ly = x % cell, y % cell
        diag = (lx + ly) < cell
        z = ( (gx + gy) + (1 if diag else 0) ) % len(choices)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 103:
        # SQUARE STRIPES
        cell = variant + 10 if variant > 0 else 56
        gx, gy = x // cell, y // cell
        orient = _hash2(gx, gy) & 1      # 0=horiz, 1=vert
        band = max(2, cell // 10)
        stripe = ((x if orient else y) % (2*band)) < band
        z = ( (gx + 2*gy) + (1 if stripe else 0) ) % len(choices)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 106:
        # SQUARES, INTERRUPTED
        cell = variant + 10 if variant > 0 else 24
        gx, gy = x // cell, y // cell
        n = _hash2(gx, gy) % len(choices)
        # add small intra-cell wobble so edges aren’t too crisp
        wob = ((x % cell) + (y % cell)) // max(1, cell//6)
        z = (n + wob) % len(choices)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 107:
        # PARALLELOGRAM PATTERN
        zonkbonk = y - starty
        s = variant if variant > 0 else 36
        q = (math.sqrt(3)/3 * (x - startx) - 1/3 * (zonkbonk)) / s
        r = (2/3 * (zonkbonk)) / s
        qi, ri = int(round(q)), int(round(r))
        z = (qi + 2*ri) 
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 108:
        # SICKO CELLS
        acc = 0.0
        v0 = vflag(variant, 1)
        v1 = vflag(variant, 2)
        v2 = vflag(variant, 3)

        k = 5 if v0 else 8

        variant = variant % 50

        for i in range(k):
            a = i * (2*math.pi/5)
            acc += math.cos((x*math.cos(a)+y*math.sin(a)) / (12 if variant==0 else max(6,variant)))
        z = int(((acc/k)+1)*0.5 * (len(choices)-1)) % len(choices)

        if v1:
            gx = x ^ (x >> 1)
            gy = y ^ (y >> 1)

            if z == 1:
                z = int(round(gx | gy, 0))

        if v2:
            gx = x ^ (x >> 1)
            gy = y ^ (y >> 1)

            if z == 2:
                z = int(round(gx & gy, 0))

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 109:
        # HILBERT ROT

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
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 110:
        # MISFIT FATHER
        gx = x ^ (x >> 1)
        gy = y ^ (y >> 1)
        z = ((gx ^ gy) // (variant if variant > 0 else 8)) % len(choices)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 111:
        # PHI FALSECALYX

        # Polar coords of current point relative to seed (startx, starty)
        dx, dy = x - startx, y - starty
        r = math.hypot(dx, dy)            # radial distance
        ang = math.atan2(dy, dx)          # angle in radians (-π..π)

        # ---- Gain controls driven by `variant` ----
        # radial_gain: how strongly distance from the seed pushes color changes
        #   variant==0 -> default gentle ripples (0.12)
        #   else       -> 0.00..0.29 in steps of 0.01 (variant % 30 * 0.01)
        radial_gain = 0.12 if variant == 0 else (variant % 30) * 0.01

        # flip the radial contribution every other pixel visit to introduce
        # a subtle alternating banding (prevents big flat swaths)
        if count % 2 == 0:
            radial_gain = -radial_gain

        # angular_gain: how much the angle contributes
        # Angular gain: steps every 30 variants, wraps every 240 variants
        N = 4                           # number of distinct angular levels
        base, top = 3.0, 6.0            # range
        step = (variant // 30) % N
        angular_gain = base + step * ((top - base) / (N - 1))

        # ---- Phase computation ----
        # Combine radius and angle: a simple polar “stripe” field.
        # Larger angular_gain -> more spokes; larger radial_gain -> more rings.
        phase = (r * radial_gain) + (ang * angular_gain)

        # Map the phase (wrapped to 0..2π) to a palette index 0..len(choices)-1
        lc = len(choices)
        z = int(((phase % (2 * math.pi)) / (2 * math.pi)) * lc)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 112:
        # AIRHOLE GUILLOCHE

        # Two foci (roughly top-left and bottom-right thirds)
        # step foci every 30 variants
        step = (variant if variant != 0 else 10) // 30
        t = step * 0.35  # phase
        cx = width * (0.25 + 0.10 * math.sin(t))
        cy = height * (0.33 + 0.08 * math.cos(t))
        dx = width * (0.75 + 0.10 * math.cos(t * 0.8))
        dy = height * (0.66 + 0.08 * math.sin(t * 1.1))

        sx0, sy0 = int(cx), int(cy)
        sx1, sy1 = int(dx), int(dy)

        # L2 distances to each focus
        use_manhattan = (variant & 0x1) != 0
        use_cheby     = (variant & 0x2) != 0

        if use_manhattan:
            d0 = abs(x - sx0) + abs(y - sy0)
            d1 = abs(x - sx1) + abs(y - sy1)
        elif use_cheby:
            d0 = max(abs(x - sx0), abs(y - sy0))
            d1 = max(abs(x - sx1), abs(y - sy1))
        else:
            d0 = int(math.hypot(x - sx0, y - sy0))
            d1 = int(math.hypot(x - sx1, y - sy1))

        # XOR the distances, then coarsen the field so bands are wider
        q = max(3, 3 + (variant % 30))    # 3..32
        z = (d0 ^ d1) // q

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 113:
        # VIBRATION HEMSTITCH

        # scale parameter (spatial wavelength-ish)
        cycle = 20
        vcv = variant % cycle   # reset every 20
        s = 120.0 if variant == 0 else max(40.0, float(vcv) * 10.0)

        # two oriented wavefields
        u = math.sin(y / s) + 0.5 * math.sin((x + y) / (s * 0.7))
        v = math.sin(x / s) - 0.5 * math.sin((x - y) / (s * 0.9))

        # mix to a single phase, then wrap with a full 2π sine
        t = math.sin(2*math.pi * (0.5*u + 0.5*v))

        # map -1..1 → 0..(len-1) and paint
        z = int(((t + 1) * 0.5) * (len(choices) - 1))
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 114:
        # ROSY EXPLOSION

        n = 8 if variant==0 else max(3, variant%16)
        dx, dy = x - startx, y - starty
        ang = (math.atan2(dy, dx) + math.pi) % (2*math.pi)
        wedge = (ang % (2*math.pi/n))
        # mirror within wedge
        if wedge > math.pi/n: wedge = (2*math.pi/n) - wedge
        r = math.hypot(dx, dy)
        z = int((r*0.05 + wedge*(n/3.0)) % len(choices))
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 115:
        # SOUTHEAST CARVING

        cell = variant + 10 if variant > 0 else 24
        gx, gy = x//cell, y//cell
        # carve either east or south per cell deterministically
        carve_east = (((gx*73856093) ^ (gy*19349663)) & 1) == 0
        in_corridor = ((x % cell) < 3) or ((y % cell) < 3) or (carve_east and ((y%cell)<6)) or ((not carve_east) and ((x%cell)<6))
        z = (gy + 2*gx + (3 if in_corridor else 0)) % len(choices)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
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

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 117:
        # STAGGERED BLOCKS

        cl = len(choices)

        # Grid spacing
        pitch = variant + 4 if variant > 0 else 6

        # Checkerboard toggle across pitch-sized cells
        kind = ((x // pitch) ^ (y // pitch)) & 1

        # Use one sub-band per color
        band_count = max(1, cl)

        # Sub-band index along x within a band_count * pitch window
        sub = (x % (band_count * pitch)) // pitch  # 0..band_count-1

        # Shift pattern by 1 on "even" kind cells to stagger the bands
        idx = (sub + (0 if kind else 1)) % band_count
        z = idx 

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 118:
        # ZIGZAG FEAST
        cell = variant + 8 if variant > 0 else 20
        gx, gy = x//cell, y//cell
        lx, ly = x%cell, y%cell

        def random_bit_array(rows=7, width=5):
            return [random.getrandbits(width) for _ in range(rows)]

        if count == 0:
            ffSpecificState = random_bit_array()

        A = ffSpecificState

        # A = [
        #     0b10101,
        #     0b00101,
        #     0b11100,
        #     0b00001,
        #     0b10100,
        #     0b01011,
        #     0b01110,
        # ]        

        sx = (lx * 5) // max(1, cell)
        sy = (ly * 7) // max(1, cell)
        bit = (A[sy] >> (4 - sx)) & 1 if 0<=sx<5 and 0<=sy<7 else 0
        z = (bit + gx + 2*gy) 
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 119:
        # TDLDLT

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
                0b00100, 
                0b00100, 
                0b00100,
                0b00100, 
                0b00100, 
                0b00100,
            ],
            "D": [
                0b11110,
                0b10001, 
                0b10001, 
                0b10001,
                0b10001, 
                0b10001, 
                0b11110,
            ],
            "L": [
                0b10000,
                0b10000, 
                0b10000, 
                0b10000,
                0b10000, 
                0b10000, 
                0b11111,
            ],
        }

        # choose which glyph this cell shows
        glyph = "TDL"[(gx + gy) % 3]
        row_bits = FONT_5x7[glyph][sy] if (0 <= sx < 5 and 0 <= sy < 7) else 0
        bit = (row_bits >> (4 - sx)) & 1   # 1 if inside the glyph stroke

        # palette index: base from cell coords, flipped by glyph bit
        base = (3*gx + 5*gy) % len(choices)
        z = (base + (len(choices)//2 if bit else 0)) % len(choices)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 120:
        # 120 — Paisley ("Grandma's Couch")
        # Tunables (feel free to expose as 'variant' or globals)
        cell = 36                        # base motif cell size (px)
        jitter = 0.18                    # how much to jitter motif within the cell
        rot_max = math.radians(28)       # max rotation per cell
        edge_w = 0.06                    # outline thickness (as fraction of motif size)
        inner_scale = 0.72               # size of inner teardrop
        dot_period = 10.0                # spacing for tiny inner dots/stripes
        stripe_mix = 0.35                # 0..1: 0 = only dots, 1 = only stripes

        # Local cell coordinates + rotation/jitter
        cx = int(math.floor(x / cell))
        cy = int(math.floor(y / cell))

        # Jitter (keeps motifs from looking perfectly gridded)
        jx = ( _h32(cx, cy) - 0.5) * 2.0 * jitter
        jy = ( _h32(cx+17, cy-9) - 0.5) * 2.0 * jitter

        # Rotation per cell
        ang = ( _h32(cx-11, cy+23) - 0.5) * 2.0 * rot_max
        ca, sa = math.cos(ang), math.sin(ang)

        # Normalized local coords in [-1,1] with jitter + rotation
        lx = ((x - (cx + 0.5 + jx) * cell) / (0.5 * cell))
        ly = ((y - (cy + 0.5 + jy) * cell) / (0.5 * cell))
        ux =  ca*lx + sa*ly
        uy = -sa*lx + ca*ly

        # Signed distance to outer and inner boteh
        d_outer = sd_teardrop(ux, uy)
        d_inner = sd_teardrop(ux/inner_scale, uy/inner_scale)  # scaled inward

        # Deterministic color picks per cell
        # - background
        bg_i  = int(_h32(cx*3+1, cy*5+2) * len(choices)) % len(choices)
        # - outline
        out_i = int(_h32(cx*7+4, cy*11+9) * len(choices)) % len(choices)
        # - fill
        fill_i = int(_h32(cx*13+6, cy*17+12) * len(choices)) % len(choices)
        # - deco (dots/stripes)
        deco_i = int(_h32(cx*19+8, cy*23+14) * len(choices)) % len(choices)

        # Background by default
        z = bg_i

        # Inside outer -> choose outline vs fill
        # edge band thickness scales with motif
        if d_outer <= 0.0:
            if abs(d_outer) < edge_w:
                z = out_i
            else:
                z = fill_i

                # Interior decor layer (smaller boteh region only)
                if d_inner <= 0.0:
                    # Angular coordinate in the rotated local space
                    theta = math.atan2(uy, ux)
                    r = math.hypot(ux, uy)

                    # Mix stripes (along angle) and polka-dots (radial grid)
                    # Stripes: periodic in theta; Dots: periodic in (ux,uy) plane
                    stripes = 0.5 + 0.5*math.sin(theta * dot_period)
                    dots    = 0.5 + 0.5*math.sin((ux*dot_period) * 0.8) * math.cos((uy*dot_period) * 0.8)

                    decor = stripe_mix*stripes + (1.0 - stripe_mix)*dots

                    # Place decor near the "belly" of the paisley by biasing with radius
                    if decor * (1.1 - 0.6*r) > 0.65:
                        z = deco_i

        # Hand final color
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 121:
        # BAD PERSPECTIVE

        # --- Tunables (variant controls scale/angle a bit) ---
        n = len(choices)
        var = max(0, int(variant))
        cell = 96 + (var % 5) * 8              # doorframe spacing
        wall0 = 48 + (var % 7) * 2             # half-width at origin
        wall_grow = 0.06 + (variant * .01)     # wall expansion per depth px
        max_rot_deg = 22 + (var % 9)           # slight rotation so it’s not axis-aligned
        edge_band = 0.10 + (variant * .01)     # outline band around frames (0..1 of cell)
        glow_gain = 0.75                       # how much frames brighten
        wall_gain = 0.65                       # how much walls brighten
        vignette = 0.25                        # global dimming away from origin axis

        # rotation (in radians) seeded by start + variant
        phi = math.radians(((_h32(startx+var, starty-var)*2.0 - 1.0) * max_rot_deg))
        ca, sa = math.cos(phi), math.sin(phi)

        # local coords: origin at (startx,starty), rotated so +u is "forward" depth
        dx, dy = abs(x - startx), abs(y - starty)
        u =  ca*dx + sa*dy   # depth
        v = -sa*dx + ca*dy   # lateral

        # corridor half-width grows with depth (only for u >= 0 to keep one-sided)
        halfw = wall0 + wall_grow * max(u, 0.0)
        halfw = max(halfw, 4.0)  # safety

        # how close to walls (0 far … 1 at wall)
        if halfw > 0:
            wall_closeness = max(0.0, 1.0 - (abs(v) / (halfw + 1e-6)))
        else:
            wall_closeness = 0.0

        # doorframes periodically along u
        k = u / float(cell)
        frac = k - math.floor(k)               # 0..1 within each segment
        dist_to_frame = min(frac, 1.0 - frac)  # 0 at frame center lines
        near_frame = max(0.0, 1.0 - dist_to_frame / edge_band)  # 0..1 in a thin band

        # per-segment flicker (fluorescent vibe)
        seg_id = int(math.floor(k))
        flick = 0.85 + 0.15 * _h32(seg_id + 13, seg_id * 7)

        # soft vignette: dim as you move diagonally away from the center axis
        away = abs(v) / (halfw + 1e-6)
        vign = max(0.0, 1.0 - vignette * away)

        # combine contributions: base dim + walls + frames + flicker + vignette
        # clamp to [0,1]
        bright = 0.15 \
                + wall_gain * (wall_closeness ** 1.4) \
                + glow_gain * (near_frame ** 1.6)     \
                + 0.0                                 # (add noise here if you want)
        bright = max(0.0, min(1.0, bright * flick * vign))

        # map brightness to palette index
        idx = int(bright * (n - 1)) % n

        # subtle alternate tint along baseboard near walls
        # (thin line near |v| ~ halfw adds liminal “edge” detail)
        edge_dist = abs(abs(v) - halfw)

        if edge_dist < 1.2:
            # alternate every other segment
            idx = (idx + (seg_id & 1) + 1) % n
       
        z = idx

        if abs(width//2 - x) < 150:
            z += 10 + seg_id

        if abs(width//2 - y) < 150:
            z += 20 - seg_id

        if z == 0:
            #z = (int(u) | int(v)) & (x | y)
            z = int(seg_id) | int(flick)

        z = z % n

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z, key_to_avoid=0)
    elif randomIt == 122:
        # and another one ridesah the bus ahhhh
        q = 2 if variant == 0 else (variant * 2) % 16
        
        if q == 0:
            q = 1

        dx, dy = abs(x - startx) // q, abs(y - starty) // q

        z = (dx + dy) % len(choices)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 123:
        # SIMPLY DOOBY DOO

        # --- Parameters (tunable / variant-driven) ------------------------------
        # Base cell size: larger -> chunkier triangles.
        base = 3 + (variant % 3)
        scale = max(2, base)                # pixels per lattice step

        # Orientation / mirroring every 30 variants for variety
        flipx = ((variant // 10) % 2) == 1
        flipy = ((variant // 20) % 2) == 1

        # Where the big triangle "rests" (apex up). Bottom-center feels natural.
        ox, oy = width // 2, height - 1

        # --- Cartesian -> (u, v) lattice for Sierpiński ------------------------
        # Move origin to (ox, oy), scale to integer lattice steps (u, v).
        # v grows upward; u is sheared so rows nest like triangles.
        px = x - ox
        py = oy - y                          # up is positive

        if flipx: px = -px
        if flipy: py = -py

        # Quantize to lattice
        v = int(py // scale)
        u = int((px // scale)) # + (v >> 1))    # shear so rows interlock

        # Keep non-negative to make the big upright triangle; everything else repeats tiling
        if v < 0:
            v = -v
        if u < 0:
            u = -u

        # --- Sierpiński index ---------------------------------------------------
        # Classic property: points with (u & v) == 0 lie in filled regions.
        # Using bit_length of (u & v) gives bands that repeat across scales.
        mask = (u & v)
        level = mask.bit_length()            # 0 near large solids; grows toward finer holes

        # A little extra modulation with row parity gives nice striping options
        bands = (level + (v & 1))            # remove + (v&1) if you want pure fractal bands

        lc = len(choices)
        z = bands % lc

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 124:
        # 93-2, 84-3
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
        mod_ff_x = (x // mod_84) % 5
        mod_ff_y = (y // mod_84) % 5

        # Distance and sum, floored to tippingPoint multiples
        mod_z = int(math.hypot(x, y)) - (int(math.hypot(x, y)) % tippingPoint)
        mod_q = x + y - (x % tippingPoint) - (y % tippingPoint)

        # Don't over-floor z1/z2; let them keep detail
        z1 = int(abs(math.hypot(x, y))) ^ x
        z2 = int(abs(math.hypot(x, y))) ^ y

        # ---- new: stable, bounded shift amounts ----
        # Always 1..13, varies by ring and coordinates
        rshift = 1 + ((mod_z ^ x ^ (y << 1)) % 13)
        lshift = 1 + ((mod_z ^ y ^ (x << 1)) % 11)

        # ---- new: scramble bucketed values before use ----
        mxs = _scramble(mod_x)  # was just mod_x (very blocky)
        mys = _scramble(mod_y)

        # Keep z bucketed once, but give it texture
        zs  = _scramble(z | (mod_z << 3))

        outcomes = {
            (0, 0): zs,
            (0, 1): _scramble(mod_z),
            (0, 2): x ^ y,
            (0, 3): (z >> rshift),          # was z >> mod_z  (flat 0)
            (0, 4): _scramble(z << lshift), # was z << mod_z  (degenerate huge)
            (1, 0): _scramble(mod_q),
            (1, 1): x & y,
            (1, 2): x | y,
            (1, 3): (x & y) ^ mod_q,        # a touch more entropy than |
            (1, 4): _scramble(z2),
            (2, 0): (mod_q - mod_z) ^ rshift,
            (2, 1): (mod_q & mod_z) ^ lshift,
            (2, 2): (mod_q | mod_z) ^ (x*3 + y*5),
            (2, 3): ((y | x) & z) ^ (mod_z >> 1),
            (2, 4): _scramble(z1),
            (3, 0): (mod_q << lshift),      # bounded shift
            (3, 1): (mod_q >> rshift),      # bounded shift
            (3, 2): x + y,
            (3, 3): x - y,
            (3, 4): (mod_q ^ z) ^ _scramble(mod_z),
            (4, 0): mxs ^ y,                # was mod_x       (flat stripe)
            (4, 1): mys ^ x,                # was mod_y       (flat stripe)
            (4, 2): _scramble(z1 | z2),
            (4, 3): _scramble(z1 & z2),
            (4, 4): _scramble(mod_z | z)
        }

        if count % 4 == 0:
            mod_84 = outcomes[(mod_ff_x, mod_ff_x)]
        elif count % 3 == 0:
            mod_84 = outcomes[(mod_ff_y, mod_ff_y)]
        elif count % 2 == 0:
            mod_84 = outcomes[(mod_ff_x, mod_ff_y)]
        else:
            mod_84 = outcomes[(mod_ff_y, mod_ff_x)]

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_84)
    elif randomIt == 125:
        # CHERRIES AND VEGETABLES

        if count % 2 == 0:
            cell = variant + 10 if variant > 0 else 48
            gx, gy = x // cell, y // cell
            lx, ly = x % cell, y % cell
            diag = (lx + ly) < cell
            z = ( (gx + gy) + (1 if diag else 0) ) % len(choices)
        else:
            cell = variant + 10 if variant > 0 else 56
            gx, gy = x // cell, y // cell
            orient = _hash2(gx, gy) & 1      # 0=horiz, 1=vert
            band = max(2, cell // 10)
            stripe = ((x if orient else y) % (2*band)) < band
            z = ( (gx + 2*gy) + (1 if stripe else 0) ) % len(choices)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 126:
        # WELCOME TO ERF

        if count == 0:
            ffSpecificState = random.uniform(.5, (variant+1) * .25)

        v = 1 if variant == 0 else variant
        scale = 18.0 + (v % 30) * 0.9              # field scale

        dx, dy = x - startx, y - starty
        r = math.hypot(dx, dy) / (scale + 1e-6)
        a = math.atan2(dy, dx)

        # safe transforms with "odd" math bits
        e1 = math.erf( math.sin(a) * 0.8 + math.expm1(-r) )     # erf + expm1
        e2 = math.erfc( math.cos(a*1.5) * 0.6 + math.log1p(r) ) # erfc + log1p
        v  = 0.5*e1 + 0.5*(1.0 - e2)

        # normalize to 0..1 and map to palette
        t = (v + 1.0) * ffSpecificState
        z = int(t * (len(choices)-1)) % len(choices)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 127:
        # MANTISSA SIREN

        v = 1 if variant == 0 else variant
        grid = 11.0 + (v % 25) * 0.7
        tw   = 0.8 + ((v // 5) % 7) * 0.15         # tilt / warp amount

        # warp coords into a tilted lattice and extract mantissas
        u = x + tw * math.sin(y / grid)
        w = y + tw * math.cos(x / grid)

        # frexp -> mantissa in [-1, -0.5) U [0.5, 1); take abs to fold
        mu, ex = math.frexp(u if u != 0 else 1.0)
        mw, ey = math.frexp(w if w != 0 else 1.0)
        mu, mw = abs(mu), abs(mw)                   # 0.5..1.0

        # blend mantissas; modf to pull fractional texture
        frac_u, _ = math.modf(mu * 7.0)
        frac_w, _ = math.modf(mw * 9.0)
        t = 0.6 * frac_u + 0.4 * frac_w

        # mild exponent striping (wrap a small palette band)
        band = ((ex ^ ey) & 3) / 3.0
        t = 0.75*t + 0.25*band

        z = int(t * (len(choices)-1)) % len(choices)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 128:
        # THE REMAINDER CATHEDRAL

        qqX = x if count % 2 == 0 else y
        qqY = y if count % 2 == 0 else x

        fuckFactor = 1e-6 if variant == 0 else 1e-6

        v = 1 if variant == 0 else variant
        s = 28.0 + (v % 40) * 0.8                   # spatial scale
        k = 0.9 + ((v // 6) % 6) * 0.17             # frequency

        # normalize to a compact, positive domain for lgamma stability
        nx = (abs(qqX - startx) / (s + fuckFactor)) + 0.9   # >= 0.9
        ny = (abs(qqY - starty) / (s + fuckFactor)) + 0.9

        # lgamma grows fast; push through trig & modular folding
        g1 = math.lgamma(nx)
        g2 = math.lgamma(ny)

        # wrap to a manageable phase space
        p1 = math.fmod(g1 * k, math.tau)
        p2 = math.remainder(g2 * (k*1.3), math.tau)

        fuckFactor2 = 0.4 if variant == 0 else .1 * variant
        fuckFactor3 = 0.6 if variant == 0 else .2 * variant

        val = math.sin(p1) * fuckFactor3 + math.cos(p2) * fuckFactor2
        t = (val + 1.0) * 0.5
        z = int(t * (len(choices)-1)) % len(choices)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 129:
        # BEWB TOOB
        dx, dy = abs(x - startx), abs(y - starty)
        
        ang = (math.atan2(dy, dx) + math.pi) / (2*math.pi)

        q = .5 if variant == 0 else .15 * variant

        r = math.hypot(dx, dy) * ang * q

        z = int(r) % len(choices)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 130:
        # HYPERBOLE OMICRON 
        z = (count // (stackDepth + 1)) | (y % 8) >> (x % 4)
        q = abs(y - starty)

        r = math.hypot(x, y)
        z = z ^ (q|int(r))
        z = z % (len(choices) * max(2, (q % tippingPoint)))

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 131:
        # STARBURST SWORDFIGHT
        dx, dy = abs(x - startx), abs(y - starty)
        r = math.hypot(dx, dy)
        ang = (math.atan2(dy, dx) + math.pi) / (2*math.pi)
        deg = 180 / math.pi
        
        if count % 4 == 0 and vflag(variant, 2):
            z = int(ang * 12) % len(choices)
        if count % 2 == 0 and vflag(variant, 0):
            z = int(ang * deg) % len(choices)
        else:
            z = int(abs(math.log1p(dx) - math.log1p(dy)) * abs(math.log1p(dx) + math.log1p(dy)))

        if vflag(variant, 1):
            z += int(r // 5)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 132:
        # 132 — BESSEL RINGS
        
        r = math.hypot(x - cx, y - cy)

        # ring density sweeps slowly across variants
        base = 0.08
        k = base + 0.003 * (max(variant, 1) % 30)   # 0.08–0.17 overall

        val = jv(0, k * r)                  # Bessel J0, ~[-1, 1]
        t = (val + 1.0) * 0.5               # normalize to [0, 1]
        z = int(t * (len(choices) - 1))
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 133:
        # NUDE ANTONYM
        
        # LAMBERT-W WARP
        cx, cy = width // 2, height // 2

        # normalize coords into ~unit disk
        sx, sy = width * 0.35, height * 0.35
        u, v = (x - cx) / sx, (y - cy) / sy
        rr = u*u + v*v + 1e-9  # avoid zero

        # gentle variant modulation
        mod = 1.0 + 0.25 * math.sin((variant % 30) * 0.21)
        wval = float(rr * mod)

        ang = (math.atan2(v, u) + 2*math.pi) % (2*math.pi)
        # mix warped radius with angle
        t = 0.65 * (wval % 1.0) + 0.35 * (ang / (2*math.pi))

        z = int(t * (len(choices) - 1))
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 134:
        # FAIL WHALE TAIL
        # center + scaled polar coords
        
        dx, dy = x - cx, y - cy
        r = math.hypot(dx, dy)
        ang = math.atan2(dy, dx)

        # sweep frequency slowly with variant (period 30)
        alpha = 0.015 + 0.0015 * (variant % 30)  # 0.015–0.0585

        # Fresnel integrals (fast in scipy.special)
        S, C = fresnel(alpha * r)

        # blend radial Fresnel with angular phase for nice moiré
        t = 0.6 * (C * C + S * S) % 1.0 + 0.4 * ((ang + math.tau) % math.tau) / math.tau
        z = int(t * (len(choices) - 1))
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 135:
        # ELLIPE INC
        dx, dy = x - cx, y - cy
        r = math.hypot(dx, dy)
        ang = math.atan2(dy, dx)

        # modulus m in (0,1); step it every 20 variants for noticeable phase shifts
        m = 0.15 + 0.7 * ((variant // 20) % 4) / 3.0   # 0.15 → 0.85
        # scale the amplitude a bit with variant for density changes
        k = 0.02 + 0.001 * (variant % 20)

        # φ grows with r; incomplete E(φ|m) is smooth & fast
        phi = k * r + 0.35 * math.sin(3.0 * ang)
        E = ellipeinc(phi, m)

        # normalize: E grows roughly linearly in φ; mod 1.0 gives tiled bands
        t = (E * 0.5) % 1.0
        # small angular tint to break symmetry
        t = 0.8 * t + 0.2 * ((ang + math.tau) % math.tau) / math.tau

        z = int(t * (len(choices) - 1) * 2)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 136:
        # ELLIPE IS STANDING ON IT
        
        if count == 0:
            ffSpecificState = random.randint(3, 7)

        dx, dy = x - cx, y - cy
        r = math.hypot(dx, dy)
        ang = math.atan2(dy, dx)        
        sector = int(((ang + math.pi) / (math.pi/6))) % 30

        phi = r - math.sin(7.2 * ang) - math.cos(1.7 * ang)
        m = min(variant * .4, .1)
        E = ellipeinc(phi, m)

        z = int(E // ffSpecificState)

        z = (sector, z)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 137:
        # NUKE FUZZ
        
        dx, dy = x - cx, y - cy
        r = math.hypot(dx, dy)
        ang = math.atan2(dy, dx)

        z = (int(r/4) & stackDepth) % len(choices)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 138:
        # RIPPLE RAPPLE
        
        dx, dy = abs(x - cx), abs(y - cy)
        r = math.hypot(dx, dy)
        ang = math.atan2(dy, dx)
        deg = 180 / math.pi

        # ---- Variant-driven parameters (cheap but diverse) ----
        band    = variant % 30                     # cycle every 30 like your other algs
        nu      = 0.5 + 0.5 * (band % 6)           # Struve/Bessel order: 0.5..3.0
        rscale  = 0.02 + 0.01 * (band // 6)        # radial frequency: 0.02..0.06
        ag      = [1.6, 2.3, 3.1, 4.2, 5.0][(band // 3) % 5]  # angular gain palette
        mixH    = 0.25 + 0.15 * (band % 4)         # weight on Struve vs Bessel: 0.25..0.70
        phase   = (variant * 1.61803398875) % (2*math.pi)     # golden-ratio phase hop

        # ---- Mild angular/radial warp (adds star/flower morphing) ----
        # small sinusoidal warp in radius that depends on angle
        rw = r * (1.0 + 0.12 * math.sin(3.0*ang + phase))

        # ---- Special functions blended ----
        H = struve(nu, rscale * rw)                # Struve H_ν
        J = jv(nu, rscale * rw + ag * ang)         # Bessel J_ν with angular term
        s = mixH * H + (1.0 - mixH) * J            # blended field

        # ---- Map to color with extra variety knobs ----
        # ring toggler: flips/offsets bands every N pixels radially
        ringFreq = 0.04 + 0.01 * ((band // 5) % 3) # 0.04..0.06
        ring = (int(r * ringFreq) & 1)

        # squash to [0,1] in a contrasty way, then add ring offset
        val = 0.5 + 0.5 * math.tanh(2.2 * s)
        val = (val + 0.15 * ring) % 1.0

        # occasional chevron-like inversion to break homogeneity
        if ((int(ang * 3.183) + int(r * 0.07)) & 1):
            val = 1.0 - val

        z = int(val * len(choices)) % len(choices)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 139:
        # CROSS BOXES
        
        dx, dy = abs(x - cx), abs(y - cy)

        z = dx if dy > dx else dy

        if variant > 1 and (variant % 25 != 0):
            z = z - (z % (variant % 25))

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 140:
        # CROSS DIAMONDS
        
        dx, dy = abs(x - cx), abs(y - cy)
        
        z = dx - dy

        if variant > 1 and (variant % 25 != 0):
            z = z - (z % (variant % 25))

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 141:
        # BOSS CROXES
        
        dx, dy = abs(x - cx), abs(y - cy)

        z = dx if dy > dx else dy

        if count % 2 == 0:
            z = dx - dy

        if variant > 1 and (variant % 25 != 0):
            z = z - (z % (variant % 25))

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 142:
        # ENNEAD REVISING
        
        dx, dy = abs(x - cx), abs(y - cy)
        z = dx / max(dy, .1) if dy < dx else dy / max(dx, .1)
        z *= (variant % 10) if variant > 0 else 2.7
        z = round(z) % len(choices)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 143:
        # GAMMA QUADRANT
        dx, dy = abs(x - cx), abs(y - cy)        
        zq = int(time.time() * 1000) & 15

        if x < cx and y < cy:
            z = zq ^ (dx | dy)
        elif x > cx and y > cy:
            z = x | y | dx | dy | variant
        else:
            ddx, ddy = x - cx, y - cy
            r = math.hypot(ddx, ddy)
            ang = math.atan2(ddy, ddx)
            zonkbonk = (ddx * ddy) << 2

            z = ddx | ddy | variant | int(ang) | zonkbonk

        z = round(z) % len(choices)

        if z == 4:            
            z = (dx // max(dy, 1)) ^ zq

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 144:
        # TWELVE TWELVES
        dx, dy = abs(x - startx), abs(y - starty)

        for i in range(12, 0, -1):
            if x % i == 0:
                z = dx
                break
            elif y % i == 0:
                z = dy
                break

        if count % 2 == 0:
            z = dx - dy
            if variant > 1 and (variant % 25 != 0):
                z = z - (z % (variant % 25))

        z = round(z) % len(choices)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 145:       
        dx, dy = abs(x - cx), abs(y - cy)
        qx, qy = abs(x - cy), abs(y - cx)

        if count % 8 == 0:
            z = (qx ^ qy) | (dx ^ dy)
        elif count % 4 == 0:
            z = qx ^ qy
        elif count % 2 == 0:
            z = qx & qy
        else:
            z = qx | qy

        z = round(z) % len(choices)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 146:
        
        dx, dy = abs(x - cx), abs(y - cy)

        if dy % 8 == 0:
            z = dy // max(1, dx)
        elif dx % 8 == 0:
            z = dx // max(1, dy)
        elif count % 4 == 0:
            z = abs(cx - dx + dy - y)
        elif count % 2 == 0:
            z = abs(dx - dy - x - y)
        else:
            z = abs(dx * dy * cx * cy)

        z = round(z) % len(choices)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 147:
        # METATRON LATTICE  — flower-of-life distance + 12-fold polar aliasing
        # Fast, integer-heavy, and variant-tunable.
        
        dx, dy = x - cx, y - cy

        # radial + angle (in radians)
        r = math.hypot(dx, dy) + 1e-9
        ang = math.atan2(dy, dx)

        # 12-fold angular aliasing to push rosette/gear shapes
        a12 = (ang * 12.0) % (2.0 * math.pi)

        # base cell tuned off tippingPoint; clamp so very small tippingPoints still work
        cell = max(6, int(tippingPoint) if tippingPoint > 0 else 16)

        # ring radius for flower centers (distance between lattice circles)
        # variants nudge radius and add mild twist
        ring = 2.0 * cell + (variant % 5) * (cell / 5.0)
        twist = (vflag(variant, 0) * 0.15 + vflag(variant, 1) * -0.10)

        # 7 circle centers: origin + 6 around it at 60°
        # compute the min distance to any center (cheap distance field)
        min_d = r  # start with origin
        for k in range(6):
            th = k * (math.pi / 3.0) + twist * (r / (8.0 * cell))
            cxk = ring * math.cos(th)
            cyk = ring * math.sin(th)
            ddx, ddy = dx - cxk, dy - cyk
            d = math.hypot(ddx, ddy)
            if d < min_d:
                min_d = d

        # quantize the distance into bands, then bit-mix with angle & radius
        band = int(min_d // max(1.0, cell / 2.0))
        a_tick = int(a12 * 57.2957795)  # deg-ish for more churn
        r_tick = int(r // max(1.0, cell / 3.0))

        # optional ripple & xor flavors (variants)
        if vflag(variant, 2):
            band += int(6.0 * math.sin(ang * 3.0 + r / (1.5 * cell)))
        if vflag(variant, 3):
            band ^= (a_tick ^ r_tick)

        # fold down to palette index space using tippingPoint-like bucketing
        z = band - (band % max(1, cell))
        z ^= (a_tick << 1) ^ (r_tick << 2)

        # keep/choose color
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 148:
        # Līminārus 
        if count == 0:
            ffSpecificState = random.triangular(.333, 1.3, .745)
        
        dx, dy = abs(x - cx), abs(y - cy)

        r = math.hypot(dx, dy) + 1e-9
        ang = math.atan2(dy, dx)

        if count % 4 == 0:
            z = dx - dy
        else:
            z = round(abs(r * ang * ffSpecificState), 0) % len(choices)

        if variant > 1 and (variant % 25 != 0):
            z = z - (z % (variant % 25))

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 149:
        # BOAMOND CRUXES N DIXES
        
        dx, dy = abs(x - cx), abs(y - cy)

        z = dy if dy > dx else dx

        if count % 2 == 0:
            z = dy - dx

        if variant > 1 and (variant % 25 != 0):
            z = z - (z % (variant % 25))

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 150:        
        
        dx, dy = abs(x - cx), abs(y - cy)
        r = math.hypot(dx, dy)
        r2 = math.degrees(r)

        ang = math.atan2(dy, dx)
        ang2 = math.degrees(ang)

        z = round(abs(r2 / max(ang2, .01)), 0) % len(choices)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 151:
        # LA DITHERA
        
        dx, dy = abs(x - cx), abs(y - cy)

        if x % 2 == 0 or y % 2 == 0:
            mod_x = int(abs(math.hypot(dx, dy))) ^ dx                        
        else:
            mod_x = dx ^ dy

        mod_x = mod_x - (mod_x % tippingPoint)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, mod_x)
    elif randomIt == 152:
        # DIGITAL EXPLOSION
        
        dx, dy = abs(x - cx), abs(y - cy)

        if x % 4 == 0 or y % 4 == 0:
            z = int(abs(math.hypot(dx, dy))) ^ dx                        
            z = z - (z % tippingPoint)
        else:
            #z = dx ^ dy
            gx = x ^ (x >> 1)
            gy = y ^ (y >> 1)
            z = ((gx ^ gy) // (variant if variant > 0 else 8)) % len(choices)        

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 153:
        # GOING THE DISTANCE
        
        dx, dy = abs(x - cx), abs(y - cy)

        #val = getDistanceVariant(4, dx, dy, x, y)
        ffSpecificState = variant if variant != 1 else 10
        mult = max(ffSpecificState % 30, 1) * .00625

        val = math.sin(x * mult) + math.cos(y * mult)
        z = round(abs(val), 0) % len(choices)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 154:        
        # LIFETIME PLAYGROUND
        
        dx, dy = abs(x - cx), abs(y - cy)

        if count == 0:
            ffSpecificState = random.randint(0, 10)

        val = getDistanceVariant(variant % 10, dx, dy, x, y)
        val2 = getDistanceVariant(ffSpecificState % 10, dx, dy, x, y)

        if x % 2 == 0 or y % 2 == 0:
            val = val2

        z = round(abs(val), 0) % len(choices)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 155:
        # DISTANT CUM
        
        dx, dy = abs(x - cx), abs(y - cy)

        #val = getDistanceVariant(4, dx, dy, x, y)
        ffSpecificState = variant if variant != 1 else 10
        mult = max(ffSpecificState % 30, 1) * .0051

        val = math.sin(x * mult) + math.cos(y * mult)
        z = round(abs(val), 0) % len(choices)

        if z == 0:
            z = (dx & dy) % len(choices)
        elif z == 1:
            z = dx ^ dy
        elif z == 2 and count % 2 == 0:
            z = 222

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 156:
        
        dx, dy = abs(x - cx), abs(y - cy)
        z2 = dx - dy

        if variant > 1 and (variant % 25 != 0):
            z2 = z2 - (z2 % (variant % 25))
        
        ffSpecificState = variant % 30 if variant > 1 else 10
        ffSpecificState2 = ffSpecificState % 15 if variant > 1 else 2

        z = math.log1p(math.hypot(dx, dy)) * ffSpecificState

        if count % 2 == 0:
            z = z2

        z = round(abs(z), 0) % len(choices)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 157:
        # DON'T EAT THE BALL MEAT
        
        dx, dy = abs(x - cx), abs(y - cy)

        if dy > dx:
            z = int(abs(math.hypot(dy, dx))) | dx
        else:
            z = int(abs(math.hypot(dx, dy))) | dy
                            
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 158:
        # ARCHIE'S SPIRAL
        
        dx, dy = (x - cx), (y - cy)
        r   = math.hypot(dx, dy)  # pixels
        ang = math.atan2(dy, dx)  # radians

        # Archimedean params (tweak these)
        a = 0.0              # radial offset in pixels (shifts spiral outwards)
        b = 6.0 if variant == 0 else .75 * variant # pixels per radian (controls spacing between turns)
        turn = b * (2.0 * math.pi)   # radial spacing between successive arms

        # Residual distance from the spiral r = a + b*ang
        # Wrap to one "turn" so you get repeating bands around each arm
        residual = (r - (a + b * ang)) % turn

        # Optional: thickness control (how wide a "track" you consider close to the arm)
        # thickness in pixels; use this to bias z toward a particular color near the arm
        thickness = 3.0
        near_arm = residual < thickness or residual > (turn - thickness)

        # Map residual in [0, turn) to a color index
        # Close to the arm → lower residual → lower idx (you can invert if you want)
        frac = residual / turn                    # 0..1
        idx  = int(frac * len(choices)) % len(choices)

        # You can bias the arm itself to a specific color family if you like
        if near_arm:
            z = idx
        else:
            # Away from the arm, offset for contrast (play with the multiplier)
            z = (idx + len(choices)//3) % len(choices)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 159:
        # VARIED VARIANTS
        dx, dy = x - cx, y - cy
        r   = math.hypot(dx, dy)
        ang = math.atan2(dy, dx)
        
        if count == 0:
            ffSpecificState = getParam(1)
            try:
                ffSpecificState2 = float(ffSpecificState)
            except:
                ffSpecificState2 = 6.0
        
        b = ffSpecificState2

        q = (b * 2 * math.pi)
        
        qq = variant % 9

        if qq == 0:
            # 6-petal rose
            z = (r - b * math.cos(ang * 6)) % q
        elif qq == 1:
            # Concentric circles
            z = r % q
        elif qq == 2:
            # Angular pie slices
            z = (ang % (2 * math.pi)) * b
        elif qq == 3:
            # Radial sine waves
            z = (r + b * math.sin(ang * 3)) % q
        elif qq == 4:
            # Star / flower style
            z = (r * math.cos(ang * 5)) % q
        elif qq == 5:
            # Ripple interference
            z = (r * math.sin(r / b) + ang * b) % q
        elif qq == 6:
            # Quadratic spiral growth
            z = (r * r + b * ang) % q
        elif qq == 7:
            # 4-petal rose
            z = (r - b * math.sin(ang * 4)) % q
        else:
            # fallback: plain Archimedes again
            z = (r - b * ang) % q
        
        z = int((z / q) * len(choices)) % len(choices)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 160:
        # CARPET CLEANING
        cell = variant if variant > 0 else 5
        
        dx, dy = x - cx, y - cy
        gx, gy = x // cell, y // cell
        #hx, hy = dx // cell, dy // cell
        
        #r   = math.hypot(dx, dy)
        ang = math.atan2(dy, dx)

        z = int(round(ang, 0)) ^ int(gx | gy)

        #z = abs((gx - hx) & (gy - hy)) % len(choices)

        z = z % (len(choices) * 4)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 161:
        # FUZZED GRID
        cell = variant + 10 if variant > 0 else 25        
        dx, dy = x - cx, y - cy
        gx, gy = x // cell, y // cell
        hx, hy = dx // cell, dy // cell

        if y % 2 == 0:
            z = (gx << 8) | gy
        elif x % 2 == 0:
            z = (gy << 8) | gx
        else:
            z = (hy << 8) | hx
           
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 162:
        cell = variant + 10 if variant > 0 else 25        
        dx, dy = x - cx, y - cy
        gx, gy = x // cell, y // cell
        hx, hy = dx // cell, dy // cell
        
        zq = int(time.time() * 1000) & 15
        
        if (count & 1) == 0:
            # diagonals along x=y (↘︎)
            z1 = abs(gx - gy)
            z2 = abs(hx - hy)
        else:
            # diagonals along x=-y (↗︎)  <-- the “other grid direction”
            z1 = abs(gx + gy)
            z2 = abs(hx + hy)
        
        z = z1 | z2

        if math.sin(x * 0.3) + math.cos(y * 0.3) > 0:
            z |= zq
        elif math.sin(dx * 0.3) + math.cos(dy * 0.3) > 0:
            z = z ^ zq

        z = z % len(choices)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 163:
        cell = variant + 10 if variant > 0 else 25        
        dx, dy = x - cx, y - cy
        gx, gy = x // cell, y // cell
        hx, hy = dx // cell, dy // cell

        mod_x = x - (x % tippingPoint)
        mod_y = y - (y % tippingPoint)
        mod_dx = dx - (dx % tippingPoint)
        mod_dy = dy - (dy % tippingPoint)

        if count & 3 == 0:
            z = (hx << 8) | hy
        elif count & 2 == 0:
            z = (gx << 8) | gy
        elif count & 1 == 0:
            z = (mod_x << 8) | mod_y
        else:
            z = (mod_dx << 8) | mod_dy

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 164:
        # BUBBLE UP BOXES

        if count == 0:
            ffSpecificState = words_to_hex(getAHex())
        
        bx, by = x // tippingPoint, y // tippingPoint
        lx, ly = x % tippingPoint, y % tippingPoint
        cx, cy = tippingPoint // 2, tippingPoint // 2
        seed = ffSpecificState
        h = hash((bx, by, seed)) & 0xFFFFFFFF

        if h % 6 in [0,1]:            
            dx, dy = lx - cx, ly - cy
            r2 = dx*dx + dy*dy
            band = r2 // max(1, (tippingPoint // 4)**2 // 6 + 1)
        else:
            band = ((lx // max(1, tippingPoint // 6)) ^ (ly // max(1, tippingPoint // 6)))

        z = (bx, by, band)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 165:
        # CIRCLE FACTORY

        if count == 0:
            ffSpecificState = words_to_hex(getAHex())
               
        # Block id and local coords
        bx, by = x // tippingPoint, y // tippingPoint
        lx, ly = x % tippingPoint, y % tippingPoint

        # Circle inscribed in the square cell
        r = tippingPoint * 0.45                 # radius
        cx, cy = r, r                          # center in local coords (cell is 0..tippingPoint-1)
        dx, dy = lx - cx, ly - cy
        inside = (dx*dx + dy*dy) <= (r*r)
        band = 1 if inside else 0

        z = (bx, by, band)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z, key_to_avoid = (bx,by,1 if band == 0 else 0))
    elif randomIt == 166:
        if count == 0:
            ffSpecificState = words_to_hex(getAHex())

        W = tippingPoint * 4
        bx, by = x // W, y // W          # supercell id
        r = W * 0.24
        r2 = W * 0.14

        def randomIt166(x, y, r, W):
            lx, ly = x % W, y % W
            rr = r * r

            centers = (
                (r, r),                # top-left
                (W - r, r),            # top-right
                (r, W - r),            # bottom-left
                (W - r, W - r),        # bottom-right
            )

            # inside if within any of the four circles
            # (avoid sqrt: compare squared distances)
            dx0, dy0 = lx - centers[0][0], ly - centers[0][1]
            dx1, dy1 = lx - centers[1][0], ly - centers[1][1]
            dx2, dy2 = lx - centers[2][0], ly - centers[2][1]
            dx3, dy3 = lx - centers[3][0], ly - centers[3][1]

            inside1 = (dx0*dx0 + dy0*dy0 <= rr)
            inside2 = (dx1*dx1 + dy1*dy1 <= rr)
            inside3 = (dx2*dx2 + dy2*dy2 <= rr)
            inside4 = (dx3*dx3 + dy3*dy3 <= rr)

            return (inside1, inside2, inside3, inside4)
        
        (inside1, inside2, inside3, inside4) = randomIt166(x, y, r, W)
        (inside5, inside6, inside7, inside8) = randomIt166(x, y, r2, W)

        if inside5:
            band = 5
        elif inside6:
            band = 6
        elif inside7:
            band = 7
        elif inside8:
            band = 8
        elif inside1:
            band = 1
        elif inside2:
            band = 2
        elif inside3:
            band = 3
        elif inside4:
            band = 4
        else:
            if count % 2 == 0:
                band = x & y
            else:
                band = x | y

        z = (bx, by, band) if band != 0 else 0

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z, key_to_avoid=0)
    elif randomIt == 167:
        # CROSSHATCH FOCUS
        fuckFactor = 8 if variant == 0 else variant

        if count % 2 == 0:
            z = ((x ^ (y << 1)) // fuckFactor)
        else:
            z = ((x // fuckFactor) ^ (y // fuckFactor))

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 168:
        # STARBURNST
        dx, dy = x - startx, y - starty
        ang = math.atan2(dy, dx)
        vvv = 10 if variant == 0 else variant
        z = (x & y) | int(round(ang * vvv, 0))

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 169:
        # ROUNDBALL JAZZ
        dx, dy = x - startx, y - starty
        r = math.hypot(dx, dy)
        ang = math.atan2(dy, dx)
        z = int(round(r, 0)) | int(round(ang*10,0))
        # z = x | int(round(ang*10,0)) | y

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 170:
        # TILTED FLANNEL

        vvv = 16 if variant == 0 else variant

        if count % 4 == 0:
            z = ((x * -3 + y * -7) // vvv) % len(choices)
        if count % 2 == 0:
            z = ((y * 3 + x * 7) // vvv) % len(choices)
        else:
            z = ((x * 3 + y * 7) // vvv) % len(choices)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 171:
        # DOUBLED-UP ROSES
        dx, dy = x - startx, y - starty
        r = math.hypot(dx, dy)
        ang = math.atan2(dy, dx)

        vvv = 5 if variant == 0 else max(variant % 12, 1)

        if count & 1 == 0:
            z = int(((r - 12*math.sin(vvv*ang)) % 32) / 32 * len(choices))
        else:
            z = int(((r + 12*math.sin(vvv*ang)) % 32) / 32 * len(choices))
        
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 172:
        # ADVENTURE INTO THE UNKNOWN
        dx, dy = x - startx, y - starty
        r = math.hypot(dx, dy)
        ang = math.atan2(dy, dx)
        z = (x ^ y) ^ (int(r)) ^ (int(ang))
        z = z - (z % tippingPoint)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 173:
        # DEMONS FROM DIAMONDS
        
        variant = variant % 6

        if variant == 0:
            # Classic 32px diamond grid
            z = (abs((x % 32) - 16) + abs((y % 32) - 16)) // 8

        elif variant == 1:
            # Smaller diamonds (tighter pattern)
            z = (abs((x % 16) - 8) + abs((y % 16) - 8)) // 4

        elif variant == 2:
            # Larger diamonds
            z = (abs((x % 64) - 32) + abs((y % 64) - 32)) // 16

        elif variant == 3:
            # Rotate 45° by swapping x,y
            z = (abs((y % 32) - 16) + abs((x % 32) - 16)) // 8

        elif variant == 4:
            # Checker-diamonds (alternate fill direction)
            z = ((abs((x % 32) - 16) + abs((y % 32) - 16)) // 8) ^ ((x // 32 + y // 32) & 1)

        elif variant == 5:
            # Wobbly diamonds: jitter with sine
            jx = x + int(4 * math.sin(y * 0.1))
            jy = y + int(4 * math.cos(x * 0.1))
            z = (abs((jx % 32) - 16) + abs((jy % 32) - 16)) // 8

        else:
            # Concentric diamond rings
            z = (abs(x - startx) + abs(y - starty)) // 16

        z = z % len(choices)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 174:
        # LOCAL FTARIES
        bx, by = x // (tippingPoint), y // (tippingPoint)
        lx, ly = x % tippingPoint, y % tippingPoint
        dx, dy = x - startx, y - starty
        r = math.hypot(dx, dy)
        ang = math.atan2(dy, dx)

        vvv = max(3 * (variant % 6), 3) if variant != 0 else 6

        z = ((lx if ((bx^by)&1)==0 else ly) // max(1, tippingPoint//vvv))
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 175:
        # CIRCLY DOOS
        bx, by = x // tippingPoint, y // tippingPoint
        lx, ly = x % tippingPoint, y % tippingPoint        
        cx, cy = tippingPoint//2, tippingPoint//2
        z = int(math.hypot(lx-cx, ly-cy) // max(1, tippingPoint//16))
        z = (bx, by, z)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 176:
        # ANGULAR SWIRLIES
        dx, dy = x - startx, y - starty
        r = math.hypot(dx, dy)
        ang = math.atan2(dy, dx)

        rot_rate = 0.05 if variant == 0 else 0.01 * variant
        
        switcher = 1 if switcher == -1 else -1
        nnn = ang * 4 + (r * rot_rate * switcher)
        z = int(((nnn % (2*math.pi)) / (2*math.pi)) * len(choices))
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 177:
        # DIAGONAL SINES
        bx, by = x // tippingPoint, y // tippingPoint
        lx, ly = x % tippingPoint, y % tippingPoint
        dx, dy = x - startx, y - starty
        r = math.hypot(dx, dy)
        ang = math.atan2(dy, dx)

        # frequency
        k = 0.15

        def stripe_at(x, y, deg, ncolors):
            a = math.radians(deg)
            s = x * math.cos(a) + y * math.sin(a)  # rotated axis
            return int((0.5 + 0.5 * math.sin(k * s)) * (ncolors - 1))

        if count % 3 == 0:
            z = stripe_at(x, y, 45.0, len(choices))    # ~x+y
        elif count % 3 == 1:
            z = stripe_at(x, y, -45.0, len(choices))   # ~x-y
        else:
            z = stripe_at(x, y, 15.0, len(choices))    # slightly rotated

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 178:
        # 回転したポテト (ROTATED TATERS)
        dx, dy = x - startx, y - starty
        xr, yr = rotate_point(dx, dy, 45)

        z = (dx | xr) & (dy | yr)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 179:
        # THE READING LIGHT
        bx, by = x // tippingPoint, y // tippingPoint
        dx, dy = bx - starty, by - startx
        xr, yr = rotate_point(dx, dy, 45)
        xr2, yr2 = rotate_point(dx, dy, 22.5)

        if count & 2 == 0:
            z = (xr ^ yr) & (x ^ y) & (xr2 ^ yr2)
        elif count & 1 == 0:
            z = (xr ^ yr) | (dx ^ dy) | (xr2 ^ yr2)
        else:
            z = (xr ^ yr) | (x ^ y) | (xr2 ^ yr2)

        z = (z, by)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 180:
        # GRITTYEST-LIKE

        if count == 0:
            ffSpecificState = random.randint(5, 179)

        bx, by = x // tippingPoint, y // tippingPoint

        xr, yr = rotate_point(x, y, ffSpecificState)

        z = (xr | yr | x | y)

        if z == -1 and (x & 1 == 0 or y & 1 == 0):
            z = (xr | yr) ^ (x | y)
            
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 181:
        if count == 0:
            ffSpecificState = random.randint(11, 301)

        bx, by = x // tippingPoint, y // (tippingPoint / 2)
        dx, dy = bx - starty, by - startx
        xr, yr = rotate_point(x, y, ffSpecificState)

        z = (xr | yr | x | y) 

        if z == -1:
            z = xr ^ yr if x % 2 == 0 and y % 2 == 0 else (by - bx + y)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 182:
        # HEXAGON ALLEY
        
        # hex "radius" in px
        s = max(8, tippingPoint)
        s2 = max(4, tippingPoint//2)

        q, r = pt_point_to_axial(x, y, s)
        #cx, cy = pt_axial_to_point(q, r, s)
        q2, r2 = pt_point_to_axial(x, y, s2)

        z = (q, r) if count & 1 != 0 else (q2, r2)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 183:
        # CONEYHOME
        s = max(8, tippingPoint)
        q, r = pt_point_to_axial(x, y, s)
        cx, cy = pt_axial_to_point(q, r, s)
        lx, ly = x - cx, y - cy

        z = ((q * 2654435761 ^ r * 2246822519) & 0x7FFFFFFF)

        band = int((math.hypot(lx, ly) / (s / 5 + 1)))  # ring width ~ s/5
        zAvoid = z
        z = (z + band)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z, key_to_avoid=zAvoid)
    elif randomIt == 184:        
        # HEXES AND BANDS

        if count == 0:
            ffSpecificState = random.choice([15,20,25,30,40,45,50,55,60,65,75])
            ffSpecificState2 = random.choice([15,20,25,30,40,45,50,55,60,65,75])

        s = max(8, tippingPoint)
        q, r = pt_point_to_axial(x, y, s)
        cx, cy = pt_axial_to_point(q, r, s)
        lx, ly = x - cx, y - cy

        z = ((q * 2654435761 ^ r * 2246822519) & 0x7FFFFFFF)        
        zAvoid = z

        dx, dy = math.cos(math.radians(ffSpecificState)), math.sin(math.radians(ffSpecificState2))

        # stripe spacing
        if x % 2 == 0 and y % 2 == 0:
            t = int((lx * dx - ly * dy) / (s / 3 + 1))
        else:
            t = int((lx * dx + ly * dy) / (s / 3 + 1))

        z = (z + (t & 3)) 

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z, key_to_avoid=zAvoid)
    elif randomIt == 185:
        # TWO BIRDS ONE ELEPHANT

        s = max(8, tippingPoint)
        q, r = pt_point_to_axial(x, y, s)
        cx, cy = pt_axial_to_point(q, r, s)
        lx, ly = x - cx, y - cy

        ang = math.atan2(ly, lx)   # angle in radians [-π, π]
        sector = int(((ang + math.pi) / (math.pi/3))) % 6
        z = (q, r, sector)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z, key_to_avoid=0)
    elif randomIt == 186:
        # SIERPINSKI
        s = max(0, variant % 5)           # scale knob: 0=finest, 1=2x, 2=4x...
        u, v = x >> s, y >> s
        z = (u & v).bit_count()
        z %= len(choices)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 187:
        # 187
        s = max(8, tippingPoint)
        q, r = ft_point_to_axial(x, y, s)

        if x & 1 == 0:
            z = (q + r) / 2
        elif y & 1 == 0:
            z = (r - q) / 2
        else:
            z = (q - r) / 2

        z = round(z, 0)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 188:
        s = max(8, tippingPoint)
        q, r = ft_point_to_axial(x, y, s)
        cx, cy = ft_axial_to_point(q, r, s)
        lx, ly = x - cx, y - cy
        ang = math.atan2(ly, lx)
        sector = int(((ang + math.pi) / (math.pi/3))) % 6

        z = sector
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 189:
        dx, dy = x - startx, y - starty
        ang = math.atan2(dy, dx)
        ang2 = math.degrees(ang)
        sector = int(round(ang2 / 45, 0))
        r = math.hypot(dx, dy) / 25

        rq = int(round(r, 0))
        z = (sector, rq)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 190:
        bx, by = x // (tippingPoint//4), y // (tippingPoint//4)
        dx, dy = x - startx, y - starty
        ang = math.atan2(dy, dx)
        ang2 = math.degrees(ang)        
        
        r = math.hypot(dx, dy)
        rot_rate = 0.05 if variant == 0 else 0.01 * variant
        sector = int(round(ang2 / 15 * r * rot_rate, 0)) % len(choices)

        bx %= len(choices)
        by %= len(choices)

        z = (sector, bx, by)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 191:
        bx, by = x // (tippingPoint*4), y // (tippingPoint*4)
        qx, qy = x // (tippingPoint*2), y // (tippingPoint*2)
        zx, zy = x // (tippingPoint), y // (tippingPoint)

        if count & 2 == 0:
            z = _h32(bx, by)
        elif count & 1 == 0:
            z = _h32(qx, qy)
        else:
            z = _h32(zx, zy)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 192:
        # center & scale 
        sx = (x - startx) / 330
        sy = (y - starty) / 480
        zr, zi = sx, sy
        cr, ci = -0.8, 0.156
        it, maxit = 0, 96
        
        for _ in range(maxit):
            zr, zi = zr*zr - zi*zi + cr, 2*zr*zi + ci
            if zr*zr + zi*zi > 4.0: break
            it += 1

        z = (it * 3) % len(choices)

        if z in [0]:
            z = int(x) ^ int(y) | max(z, 2)
        elif z == 3:
            if count & 1 == 0:
                z = round(sx, 2)
            else:
                z = round(sy, 2)

        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
    elif randomIt == 193:
        # SQUARE PATTERN
        (mod_x, mod_y) = get_grid_vals(x, y, tippingPoint)

        if count == 0:
            ffSpecificState = random.randint(5, 15)
            ffSpecificState2 = random.randint(3, 6)

        if variant == 0:
            fuckFactor = ffSpecificState
        else:
            fuckFactor = variant

        mod_ff_x = (x // fuckFactor) % ffSpecificState2
        mod_ff_y = (y // fuckFactor) % ffSpecificState2

        z = (mod_ff_y, mod_ff_x)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)        
    elif randomIt == 194:
        (mod_x, mod_y) = get_grid_vals(x, y, tippingPoint)

        if count == 0:
            ffSpecificState = random.randint(5, 15)
            ffSpecificState2 = random.randint(3, 6)

        if variant == 0:
            fuckFactor = ffSpecificState
        else:
            fuckFactor = variant

        mod_ff_x = (x // fuckFactor) % ffSpecificState2
        mod_ff_y = (y // fuckFactor) % ffSpecificState2

        s = max(8, tippingPoint)
        q, r = ft_point_to_axial(x, y, s)
        cx, cy = ft_axial_to_point(q, r, s)
        lx, ly = x - cx, y - cy
        ang = math.atan2(ly, lx)
        sector = int(((ang + math.pi) / (math.pi/3))) % 6

        z = (mod_ff_y, mod_ff_x, sector)
        (colorsKept, newcolour, key_used) = get_kept_color(colorsKept, newcolour, choices, z)
        
    if not randomIt in [25, 34]:
        if key_used not in timesUsed:
            timesUsed[key_used] = 1
        else:
            timesUsed[key_used] += 1

    # the end of the tour - #NXT
    return newcolour, choices, x, y, switcher
   
# Palette picks (deterministic per cell so it tiles nicely)
def _h32(a, b):  # tiny, fast, deterministic hash -> 0..1
    v = (a * 73856093) ^ (b * 19349663)
    v ^= (v >> 13); v *= 1274126177; v &= 0xFFFFFFFF
    return (v / 0xFFFFFFFF)

def _scramble(v: int) -> int:
    # 32-bit integer hash (Knuth-ish). Keeps structure but kills flats.
    v ^= (v >> 13)
    v = (v * 2654435761) & 0xFFFFFFFF
    v ^= (v >> 17)
    return v

# Signed "distance" (soft) to a teardrop shape centered at (0,0) in [-1,1] box.
# It’s a biased superellipse with a quadratic tail to get the paisley hook.
def sd_teardrop(u, v):
    # squash/stretch + tail curve
    n = 2.9                       # superellipse exponent (2=circle … higher=boxier)
    sx, sy = 1.00, 0.78           # aspect ratio (taller than wide)
    tail = 0.42 * (u + 0.25)**2   # curved “comma” hook
    vv = (v + tail)
    # Lp norm (soft)
    lp = (abs(u/sx)**n + abs(vv/sy)**n)**(1.0/n)
    # < 1 is inside; convert to signed distance-ish
    return lp - 1.0

def _hash2(i, j, seed=0x9E3779B1):
    v = (i * 0x27d4eb2d) ^ (j * 0x85ebca6b) ^ seed
    v ^= (v >> 15); v *= 0x2c1b3c6d; v ^= (v >> 12); v *= 0x297a2d39; v ^= (v >> 15)
    return v & 0xffffffff

@njit
def isItTimeToDump(dumpEvery, iPoint):
    return dumpEvery > 0 and (iPoint > 0) and (iPoint % dumpEvery == 0 or iPoint % dumpEvery == 1)

@njit
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

def get_kept_color(colorsKept, newcolour, choices, mod_x, force_exhaust=False, key_to_avoid=None):
    key = str(mod_x)

    bucky_exhaust = getParam_Bucky("EXHAUST")

    if key not in colorsKept:
        if len(choices) == 0:
            newcolour = getRandomColorRGB()
        else:
            if bucky_exhaust or force_exhaust:
                # filter out already used colors
                used = set(colorsKept.values())
                available = [c for c in choices if c not in used]

                if not available:  # all have been used, reset pool
                    available = choices

                newcolour = random.choice(available)
            else:
                if mod_x == "darkest":                    
                    newcolour = sort_by_lum(choices)[0]
                elif mod_x == "lightest":
                    newcolour = sort_by_lum(choices)[-1]
                else:
                    if key_to_avoid is not None and str(key_to_avoid) in colorsKept:                        
                        oldcolour = colorsKept[str(key_to_avoid)]
                        available = [c for c in choices if c != oldcolour]
                        newcolour = random.choice(available)
                    else:
                        newcolour = random.choice(choices)

        colorsKept[key] = newcolour
    else:
        newcolour = colorsKept[key]

    return (colorsKept, newcolour, key)

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
            newcolour = getRandomColorRGB()
        else:
            newcolour = random.choice(choices)
    else:
        newcolour = colorsKept[str(mod_x)]
        
    return newcolour    
            
def get_grid_vals(x, y, tippingPoint):
    mod_x = x - (x % max(tippingPoint, 1))
    mod_y = y - (y % max(tippingPoint, 1))

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

# CRAP BRAINCASE

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

        if not is_gray(thisc, min_dist=distance) and (r > distance or g > distance or b > distance):
            if not thisc in choices:
                choices.append(thisc)

        if len(choices) >= limit:
            break

    return (choices, sc)

def getAllPalettesFromDir():
    (pals, isPublic) = getInsertWalkPathsInner([palettesPath], extensions=defaultInsertExtensions)

    global palettelist

    i = 5000
    for p in pals:
        detail = os.path.splitext(os.path.basename(p))
        nameOnly = detail[0]

        x = (i, f'{i} ({nameOnly}) [💾]', nameOnly + ".png")
        palettelist.append(x)

        i += 1

    return

def getPalette(choiceStatic=""):
    palette = getInsertWalk(palettesPath, choiceStatic=choiceStatic)

    choices = []

    addState(f"palette in getPalette: {palette}")

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

    return choices

def getStamp(choiceStatic=""):
    doTimeCheck("getStamp starts")
    
    stamp = getInsertWalk(stampPath, choiceStatic=choiceStatic)
    doTimeCheck("stamp gotten")

    img = Image.open(stamp)
    img = img.convert("RGBA")
    img = resizeToMinMax(img, maxW=300, maxH=300, minW=150, minH=150)

    bucky_z = getParam_Bucky("STAMPHUE")

    if bucky_z:
        img = imageop_huerotate(img, 180)

    return img

def getStampGenerated():
    img = ""

    try:
        width = 250
        height = 250
        
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

def getInsertWalkPathsInner(paths, extensions):
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
    
    return (images, isPublic)

def getInsertWalkPaths(paths, choiceStatic="", extensions=defaultInsertExtensions):
    (images, isPublic) = getInsertWalkPathsInner(paths, extensions)

    chosen = ""    
    
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
   
    addState(f'font chosen: {chosen}')

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

# GARB GANG

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

def saveToWrapper(key, path, uid=None, skip_zero=True):
    global wrapperData
    global currentUID

    if uid is None:
        uid = currentUID

    try:
        if uid not in [0, "0"] or not skip_zero:
            # rootLogger.debug(f"key: {key} uid: {uid} path: {path}")
            wrapperData[key][uid].append(path)

    except Exception as ex:
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

def addState(statement, params={}, self=None, uid=None, skip_zero=True):
    stm = TdlState(statement)
    saveToWrapper("function_states", str(stm), uid=uid, skip_zero=skip_zero)

    return

def get_palettelist_classifications():
    results = []

    for entry in palettelist:
        num = entry[0]
        name = entry[1]
        choices = getPaletteSpecific(num)
        classifications = classify_palette_colors(choices)
        dom = classifications["dominant"] or "zzz"  # fallback if None
        results.append((entry, dom))
    
    return results

def get_palettelist_classifications_dict():
    results = {}
    for entry in palettelist:
        num = entry[0]
        choices = getPaletteSpecific(num)
        classifications = classify_palette_colors(choices)
        dom = classifications["dominant"] or "zzz"  # fallback if None
        results[num] = (entry, dom)
    return results

def sort_palettelist_by_dominant():
    results = get_palettelist_classifications()

    # Use a custom order if desired
    band_order = ["red","orange","yellow","green","cyan","blue","purple","magenta","gray","white","black","even"]
    order_map = {c:i for i,c in enumerate(band_order)}

    # Sort by dominant band, using order_map
    results.sort(key=lambda x: order_map.get(x[1], 999))

    # Return only the original entries (in new order)
    return [entry for entry, dom in results]

def get_palette_name(num):
    for entry in palettelist:
        if num == entry[0]:
            return entry[1]
    
    return ""

# TDL functions ---------------------------------------- @~-------

def flagship(fontSize=128):   
    try:        
        choices = getInputPalette()

        fImg = getOneSafeFunc()
        img = fImg()
       
        draw = ImageDraw.Draw(img)

        fontPath = getFont()
        word = getTDL(primer="tdl")

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

def dots_palette():
    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        img = Image.new("RGBA", (width, height), "#000000")
        draw = ImageDraw.Draw(img)

        xStep = random.randint(4, 8)
        yStep = random.randint(4, 8)

        choices = getInputPalette()
        
        for x in range(0, width - 1, xStep):
            (r,g,b) = random.choice(choices)

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

        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()
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

                rotChoice = random.randint(0, 5)
                if rotChoice == 5:
                    pasteFile = pasteFile.rotate(180, expand=1)
                elif rotChoice == 4:
                    pasteFile = pasteFile.rotate(90, expand=1)
                elif rotChoice == 3:
                    pasteFile = pasteFile.rotate(270, expand=1)

                leMask = Image.new("L", pasteFile.size, 255)

                if random.randint(0, 3) == 0:
                    pasteEdit = pasteFile.convert("RGB")
                    pasteFile = ImageOps.invert(pasteEdit)                
                
                img.paste(pasteFile, (random.randint(-50, width + y), random.randint(-50, height + y)), leMask)
                
    except Exception as e:
        img = writeImageException(e)    
        
    return img

def ihavenoidea():
    img = ""

    try:    
        width = 1024
        height = 1024
        c = getRandomColor()
        
        img = Image.new("RGBA", (width,height), c)        

        addState(f"width: {width}, height: {height}", None)

        global maxFloodFillArg

        iAlg = getRandomFloodFill()

        addState(f"iAlg: {iAlg}", None)

        choices = getPaletteGenerated()

        addState(f"choices: {choices}", None)
        
        # floodfill(img, (50, 30),
        #           targetcolour = c,
        #           newcolour=(255,255,0),
        #           randomIt = iAlg,
        #           choices = choices)

        img = numpy_Fullfill(width, height, iAlg)
        draw = ImageDraw.Draw(img)

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
    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()
        palette = getInputPalette()
        bucky_legacy = getParam_Bucky("LEGACY")

        img = Image.new("RGB", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        i = 0
        stripeRuined = 0
    
        yGritty = random.randint(3, 11)
        fuckFactor = 3 if bucky_legacy else random.randint(2, 12)

        addState(f'fuckFactor: {fuckFactor}')

        for y in range(0, img.size[1], yGritty):
            for x in range(img.size[0]):
                currentColor = random.choice(palette)
                
                if stripeRuined == 0:
                    if random.randint(1, 7) == 4:
                        prevColor = currentColor
                        currentColor = random.choice(palette)

                        if bucky_legacy:
                            stripeRuined = 1 
                        else:
                            if prevColor != currentColor:
                                stripeRuined = 1

                for jjjj in range(0, yGritty):
                    if y + jjjj < img.size[1]:
                        pixdata[x,y+jjjj] = currentColor

                i += 1

                if i % fuckFactor == 0:
                    stripeRuined = 0

    except Exception as e:
        img = writeImageException(e)    
        
    return img

def grittyer(img = None, evenWeirder=0):
    """p1: weirdFactor (default=7)<br />
    p2: divisor (default=26.75)<br />
    p3: mod value (default=45)
    """

    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        if img == None:
            img = Image.new("RGBA", (width,height), "#ffffff")

        draw = ImageDraw.Draw(img)
        
        pixdata = img.load()

        r, g, b, i, j = 0, 0, 0, 0, 0

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
                            if x+wr < img.size[0]:
                                pixdata[x+wr, y] = (r, g, b, j)                
                    except Exception as ex:
                        rootLogger.debug(f"{ex} {img.size[0]} {x+wr} {(r,g,b,j)}")
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

        if evenWeirder == 1:
            img = img.rotate(90, expand=1)

    except Exception as e:
        img = writeImageException(e)    
    
    return img

def grittyerest():
    try:
        img1 = grittyer()
        img2 = grittyer(img1, evenWeirder=1)

        leMask = Image.new("L", img2.size, 128)
                
        img1.paste(img2, (0, 0), leMask)
        img = img1
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
    """p1: word choice (default=0, 0=random [0,4,6])<br />
    1: "COME ON GET NAKED"<br />
    2: "BUTT ASS"<br />
    3: "THE MERE FACT..."<br />
    4: hex<br />
    5: "STARS ENCLOSE THE SKY"<br />
    6: 3 * getRandomWord()<br />

    """
    img = ""

    cat = getParam(0)
    cat = int(cat) if cat.isdecimal() else random.choice([0,4,6])

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
        elif cat == 4:
            startPos = (random.randint(0, 200), random.randint(0, 200))
            fonSize = 72
            line = getAHex()
            lines = line.split(' ')
            fillStroke = (0,0,0)
            fillText = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
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
            lines = text
            fillStroke = (0,0,0)
            fillText= getRandomColorRGB()
        
        img = smellycatalina(startPos, fonSize, lines, fillStroke, fillText, squares, fontPath=getFont())

    except Exception as e:
        img = writeImageException(e)
        
    return img

# GEMINI POSTMORTEM

def roundPaste():
    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        img = Image.new("RGB", (width,height), "#ffffff")
        fImg = getOneSafeFunc()
        img = fImg()

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

        draw = ImageDraw.Draw(mask)
        draw.ellipse([(0,0),(mask.size[0],mask.size[1])], 255, 255, 1)

        img.paste(zimg, (maxSquareWidth,maxSquareHeight), mask)

    except Exception as e:
        img = writeImageException(e)
        
    return img

# SLAVE BALLET

def vgaBox():
    fImg = getOneSafeFunc()
    img = fImg()

    draw = ImageDraw.Draw(img)

    width = img.size[0]
    height = img.size[1]
    
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
        width = getCurrentStandardWidth()
        height = int(getCurrentStandardHeight() * .75)

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

        iAlg = getRandomFloodFill_Rando()
        
        choices = getInputPalette(generate=False, noneIfNoInput=True)

        if not choices or len(choices) == 0:
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
        inputFile = resizeToMinMax(inputFile, maxW=1280, maxH=1024, minW=800, minH=600)
        
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
                inverse = hex_to_rgb(color)

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
        width = 2000
        height = 2500
        
        choices = []

        if palette != "":
            choices = processPalette(palette)

        img = Image.new("RGB", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)
         
        fillTestTotal = 204
        rows, cols, gridStep = buildGrid(width - 300, height, fillTestTotal, maxCols=12)
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
                          newcolour = (108,164,96),
                          randomIt = iAlg,
                          maxStackDepth = 0,
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
    p1 = <br />
    <a href="javascript:setParam1('lum');">lum</a> -> sort_by_lum(choices)<br />
    <a href="javascript:setParam1('hue');">hue</a> -> sort_by_hue(choices)<br />
    <a href="javascript:setParam1('hsv');">hsv</a> -> sort_by_hsv_band(choices)<br />
    <a href="javascript:setParam2('dom');">dom</a> -> sort by dominant color band
    """

    try:
        global palettelist

        rowCount = 0
        for p in palettelist:
            rowCount += 1
            pass
        
        recSize = 40
            
        height = rowCount * (recSize + 15) * 2
        width = getCurrentStandardWidth()

        p1 = getParam(0)
        p2 = getParam(1)

        pal_comp = getParam_Bucky("PALCOMP")
        pal_inverse = getParam_Bucky("PALINVERSE")
        buckyBits = getParam(8)

        fon = ImageFont.truetype(fontPath + fontNameMono, 18)
        fonSmall = ImageFont.truetype(fontPath + fontNameMono, 14)
    
        img = Image.new("RGBA", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        cOutline = (0,0,0,255)
        
        spacer = 5

        doms = []

        palettelist_sorted = sort_palettelist_by_dominant() if p1 == "dom" or p2 == "dom" else palettelist

        y = 0
        for i in palettelist_sorted:
            choices = getPaletteSpecific(i[0])
            rootLogger.debug(f'paletteSample(): buckyBits: {buckyBits} pal_comp: {pal_comp} pal_inverse: {pal_inverse}')

            classifications = classify_palette_colors(choices)

            if p1 == "lum":
                choices = sort_by_lum(choices)
            elif p1 == "hue":
                choices = sort_by_hue(choices)
            elif p1 == "hsv":
                choices = sort_by_hsv_band(choices)

            x = 25
            kz = ((width - x) / len(choices) - 3)
            
            kz = 3 if kz < 3 else kz

            boxWidth = int(kz if len(choices) > 10 else 50)

            dom = classifications["dominant"]
            percs = classifications["percentages"]

            doms.append(dom)

            sorted_items = sorted(percs.items(), key=lambda kv: kv[1], reverse=True)

            # Format as "(color XX%)"
            formatted_perkys = ", ".join(f"{k} {int(v*100)}%" for k, v in sorted_items)

            label = f'{i[1]}'
            draw.text((x, y), label, font=fon, fill=cOutline)
            text_size_x, text_size_y = dropin_text_size(draw, label, font=fon)

            mapping = {
                "even": "black",
                "white": (128, 128, 100),
            }
            test_line_fill = mapping.get(dom, dom)

            label = f' ({dom}) [{len(choices)}]'
            draw.text((x+text_size_x, y), label, font=fon, fill=test_line_fill)

            y += spacer + text_size_y
            boxHeight = recSize - spacer - text_size_y

            for c in choices:
                draw.rectangle(((x,y),(x+boxWidth,y+boxHeight)), fill=c, outline=cOutline)
                x += boxWidth

            y += boxHeight + 4
            x = 25

            label2 = f"{formatted_perkys}"
            draw.text((x, y), label2, font=fonSmall, fill=cOutline)
            text_size_x, text_size_y = dropin_text_size(draw, label2, font=fonSmall)

            y += text_size_y
            y += recSize // 2

        y += spacer

        all_counts = Counter(doms)

        rootLogger.debug(f"all_counts: {all_counts}")

        label = f'EOF'
        x = 25
        draw.text((x, y), label, font=fon, fill="black")
        text_size_x, text_size_y = dropin_text_size(draw, label, font=fon)

        y += text_size_y + 20

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

def buildGrid(width, height, fillTestTotal=90, maxCols=None):
    squareCount = 0
    rows = 0
    cols = 0

    while squareCount < fillTestTotal:
        if rows < cols:
            rows += 1
        elif cols < rows and (maxCols is None or cols < maxCols):
            cols += 1
        else:
            # tie-breaker case
            if height > width:
                rows += 1
            else:
                if maxCols is None or cols < maxCols:
                    cols += 1
                else:
                    rows += 1

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
    try:
        width = 1000
        height = 900
        img = Image.new("RGB", (width,height), "#ffffff")

        draw = ImageDraw.Draw(img)
        
        x = 0
        y = 0

        pixdata = img.load()

        choices = getInputPalette()
        
        r, g, b = 0, 0, 200

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        
        recSize = random.randint(50, 250)
        spacing = 10

        global maxFloodFillArg
        
        # level 1

        i = 0

        maxX, maxY = 0, 0

        switcher = random.choice([-1, 1])

        outline = random.choice(choices)
        
        # draw some 'tangles and fill 'em
        for y in range(spacing, height-recSize, recSize + spacing):
            for x in range(spacing, width-recSize, recSize + spacing):
                if switcher == 1:
                    draw.rectangle(((x,y),(x+recSize,y+recSize)), fill=(255,255,255,128), outline=outline)
                else:
                    draw.ellipse([x,y,x+recSize,y+recSize], fill=(255,255,255,128), outline=outline)

                thisX = x+(recSize//2)
                thisY = y+(recSize//2)

                fillAlg = i

                floodfill(img, (thisX, thisY),
                        targetcolour = pixdata[thisX, thisY],
                        newcolour = (r,g,b),
                        randomIt = fillAlg,
                        choices = choices)

                i += random.randint(1, 7)

                if i > maxFloodFillArg:
                    i = 0

                maxX = max(maxX, x+recSize)
                maxY = max(maxY, y+recSize)

        fillAlg = random.randint(0, maxFloodFillArg)
        floodfill(img, (1, 1),
                        targetcolour = pixdata[0,0],
                        newcolour = (r,g,b),
                        randomIt = fillAlg, 
                        choices = choices)
        
        img = img.crop((0, 0, maxX+spacing, maxY+spacing))

    except Exception as e:        
        img = writeImageException(e)       

    return img

def _intersect_box(box, w, h):
    # clip (left, top, right, bottom) to image bounds
    L, T, R, B = box
    L = max(0, min(L, w))
    T = max(0, min(T, h))
    R = max(0, min(R, w))
    B = max(0, min(B, h))

    if R <= L or B <= T:
        return None
    
    return (L, T, R, B)

def shapeMover(imgPath=""):
    """
    p1: mode (0=rectangle, 1=circle) (default=1)
    """
    global rootLogger

    try:
        if imgPath == "":
            imgPath = getInsert("", publicDomainImagePath)

        img = Image.open(imgPath).convert("RGBA")
        img = resizeToMinMax(img, maxW=1280, maxH=1024, minW=640, minH=480)
        inputFile = img.copy()

        W, H = inputFile.size
        squareCount = random.randint(10, 45)

        # param: 0=rect, 1=circle
        p1 = getParam(0)
        p1 = int(p1) if str(p1).isdigit() else 1
        p1 = 1 if p1 > 1 else p1

        for _ in range(squareCount):
            try:
                # source size
                w = random.randint(20, 350)
                h = random.randint(20, 350)

                # source top-left
                sx = random.randint(0, W - 1)
                sy = random.randint(0, H - 1)

                # compute and clip source box
                src_box = _intersect_box((sx, sy, sx + w, sy + h), W, H)
                if not src_box:
                    continue  # nothing to copy

                region = inputFile.crop(src_box)
                rw, rh = region.size  # actual region size after clipping

                # build mask if circular mode
                mask = None
                if p1 == 1:
                    mask = Image.new("L", (rw, rh), 0)
                    d = ImageDraw.Draw(mask)
                    # inset by 0.5 px to avoid alias seam
                    d.ellipse([0, 0, rw - 1, rh - 1], fill=255)

                # destination top-left
                dx = random.randint(0, W - 1)
                dy = random.randint(0, H - 1)

                # destination box, clipped; keep size == region size
                dst_box = _intersect_box((dx, dy, dx + rw, dy + rh), W, H)
                if not dst_box:
                    continue

                # If clipping reduced destination size, crop region/mask to match
                dL, dT, dR, dB = dst_box
                need_w, need_h = dR - dL, dB - dT
                if (need_w, need_h) != (rw, rh):
                    region = region.crop((0, 0, need_w, need_h))
                    if mask is not None:
                        mask = mask.crop((0, 0, need_w, need_h))

                img.paste(region, dst_box, mask)

            except Exception as inner_e:
                if 'rootLogger' in globals() and rootLogger:
                    rootLogger.error(inner_e)
                else:
                    print(inner_e)
                continue

        return img

    except Exception as e:
        return writeImageException(e)

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
    try:
        if imgPath == "":
            imgPath = getInsertById(getParam(4))

        img = Image.open(imgPath)
        img.load()
        img = resizeToMinMax(img, maxW=1024, maxH=768, minW=640, minH=480)
               
        orig = img.convert("RGB")
        orig = ImageOps.invert(orig)

        errors = 0

        w = orig.size[0]
        h = orig.size[1]
        
        for i in range(random.randint(30, 80)):
            try:
                a = random.randint(1, w)
                b = random.randint(1, h)
                c = random.randint(a, w)
                d = random.randint(b, h)
                
                box = (a, b, c, d)
                
                region = orig.crop(box)
                img.paste(region, box)

                orig = ImageOps.invert(orig)    
            except Exception as exx:
                errors += 1
                pass  
    
    except Exception as e:
        img = writeImageException(e)
    
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

def QRCoder(input_data="https://www.defectivejunk.com", fillColor="black", bgColor="white"):
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

    r, g, b, i = 0, 0, 0, 0
    (r, g, b, i) = getRandomColor()    
    j = i

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

    img = img.convert("RGBA")    
    img = resizeToMinMax(img, maxW=1024, maxH=768, minW=800, minH=600)
    w = img.size[0]
    h = img.size[1]

    x, y = 0, 0

    draw = ImageDraw.Draw(img)

    botString = getAHex() # getRandomWord() + " " + getRandomWord()

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
    try:
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
    except Exception as e:
        img = writeImageException(e)
        return img
    
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
    img = img.convert("RGBA")

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

    qqq = random.choice([1,2])
    qqq = getRandomWord() + " " + getRandomWord() if qqq == 1 else getAHex()

    textString = p1 if p1 != "" else qqq
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
    img = None

    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        fontPathz = getFont()
        fontSize = 38
        img = Image.new("RGBA", (width,height), (255,255,255,0))
        fon = ImageFont.truetype(fontPathz, fontSize)

        jCount = 9
        textString = getAHex()

        colors = getInputPalette()

        if len(colors) <= 0:
            for j in range(jCount):
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)

                color = (r, g, b, 255)
                colors.append(color)
            
        for i in range(4):
            draw = ImageDraw.Draw(img)
            
            for j in range(jCount):            
                strokeColor = random.choice(colors) # (0, 0, 0, 255)
                textColor = colors[j % len(colors)] 

                if strokeColor == textColor:
                    strokeColor = getInverse(textColor)

                x = width // 2
                y = (height // 2) + (j * fontSize)
                
                # textStroke(draw, x, y, textString, fon, fillColor)
                draw.text((x, y), textString, font=fon, fill=textColor, stroke_width=2, stroke_fill=strokeColor)
                
            img = img.rotate(90)

        img = img.rotate(45)

    except Exception as e:
        img = writeImageException(e)

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
    img = textGen2(getAHex(), getFont(), 1, targ)

    pixdata = img.load()
    
    touched = {}

    global uncleTouchysPlayhouse

    choices = getInputPalette()

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            c = pixdata[x,y]

            pointHash = hash((x,y))

            # rootLogger.debug(f'pointHash: {pointHash} is it in yet? {pointHash in touched}')

            if c == targ and pointHash not in touched:
                rit = random.randint(13, 15)
                
                floodfill(img, (x, y), targetcolour = targ,
                              newcolour = (0,0,0),
                              randomIt = rit,
                              choices=choices)

                for utp in uncleTouchysPlayhouse:
                    touched[utp] = uncleTouchysPlayhouse[utp]

                    # rootLogger.debug(f"utp: {utp}")
            
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

def grandradiant():
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
                
    return img

def pieslice():
    width = 800
    height = 800
    
    img = Image.new("RGBA", (width,height), "#000000")
    draw = ImageDraw.Draw(img)
    pixdata = img.load()

    pieWidth = 800
    pieHeight = 800

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

    boxes = [(0,0,800,800)]

    angles = []
    colors = []

    palette = getInputPalette()
    
    for y in range(0, len(boxes)):    
        for x in range(0, random.randint(200,600), 15):
            startAngle = random.randint(0, 360)
            endAngle = random.randint(startAngle + 20, startAngle+180)

            endAngle = endAngle % 360

            color = random.choice(palette)
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
                      randomIt = getRandomFloodFill(),
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
                              randomIt = getRandomFloodFill(),
                              choices = colors)

                    break
                
    except Exception as e:
        img = writeImageException(e)
        
    return img

def lotsOfLetters():
    width = getCurrentStandardWidth()
    height = getCurrentStandardHeight()
    
    try:
        (r,g,b) = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
    
        choices = getInputPalette()

        img = Image.new("RGBA", (width, height), random.choice(choices))        
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

        palette = getInputPalette()

        yStep = random.randint(30, 70)
        xStep = random.randint(15, 30)
        
        for y in range(0, img.size[1], yStep):
            for x in range(0, img.size[0], xStep):
                c = random.choice(palette)

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

        palette =  getInputPalette()

        zonk = random.randint(8, 30)

        yStep, xStep = zonk, zonk
        
        for y in range(0, img.size[1], yStep):
            for x in range(0, img.size[0], xStep):
                c = random.choice(palette)

                for i in range(xStep):
                    for j in range(yStep):
                        if x+i < width and y+j < height:
                            pixdata[x+i,y+j] = c

        #imgOrig = img
        
        for i in range(random.randint(1000, 5000)):
            x = random.randint(0, img.size[0]-1)
            y = random.randint(0, img.size[1]-1)
            
            targ = pixdata[x,y]
            
            floodfill(img, (x, y), targetcolour = targ,
                  newcolour = (0,0,0),
                  randomIt = random.randint(18, 19),
                  sizeLimit=(xStep,yStep),
                  choices = palette)

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

        palette = getInputPalette()

        starting = [(0,0,25,25,""),
                    (12,12,50,25,""),
                    (37,37,100,25,"")]        
        
        startingFloodAlg = getRandomFloodFill()

        for start in starting:
            yStep = start[2]
            xStep = start[2]
            xSize = start[3]
            ySize = start[3]
            override = start[4]
            
            for y in range(start[1], img.size[1], yStep):
                for x in range(start[0], img.size[0], xStep):
                    if override == "":
                        c = random.choice(palette)
                    else:
                        c = hex_to_rgb(override)

                    for i in range(xSize):
                        for j in range(ySize):
                            if x+i < width and y+j < height:
                                pixdata[x+i,y+j] = c
            
        for y in range(0, img.size[1], 50):
            for x in range(0, img.size[0], 50):
                targ = pixdata[x,y]

                floodalg = startingFloodAlg
                if x % 100 == 0 and y % 100 == 0:
                    floodalg = getRandomFloodFill()
                    
                floodfill(img, (x, y), targetcolour = targ,
                  newcolour = (0,0,0),
                  randomIt = floodalg,
                  sizeLimit=(100,100),
                  choices = palette)
                
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

def bigSquareGrid_remixed():
    img = bigSquareGrid()
    img = remixer("", img)

    return img

def bigGridFilled():
    iAlg = getRandomFloodFill_Rando()
    
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

# MATRIX NURSE

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

def insertStreaks(imgpath="", maxIterations=250, pointCount=25):
    if imgpath == "":
        imgpath = getInsert("", publicDomainImagePath)

    img = Image.open(imgpath)
    img = img.convert("RGBA")

    img = resizeToMinMax(img, maxW=1024, maxH=768, minW=640, minH=480)
    
    try:
        pixdata = img.load()

        choices = getInputPalette()
        
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

            iAlg = getRandomFloodFill_Rando()
            
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
       
        floodLimit = int(pixCount // 4.0)

        while floodedCount < floodLimit and iteration < maxIterations:
            (x,y) = (random.randint(0, img.size[0]-1), random.randint(0, img.size[1]-1))

            iAlg = getRandomFloodFill_Rando()

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

                doTimeCheck(f"allowed - floodedCount is now: {floodedCount} — {floodedCount/floodLimit:.2%} (of a requested: {floodLimit}/{pixCount})")

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

# BADGUY WHAMMY

def radioFill(imgpath="", img="", choices=[]):
    """p1: maxStackDepth<br />
    p2: flood count max (default: -1 => pixel count / 4)"""

    p1 = getParam(0)
    p2 = getParam(1)

    p1 = int(p1) if p1.isdecimal() else 0
    p2 = int(p2) if p2.isdecimal() else -1
    
    floodLimit = p2    

    return radioFill_process(imgpath=imgpath, choices=choices, img=img, maxStackDepth=p1, floodLimit=floodLimit, sizeLimit=(250,250))[0]

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
            
            p1 = getParam(0)
            iAlg = int(p1) if p1.isdecimal() else 0

            if iAlg == 0:
                iAlg = getRandomFloodFill_Rando()

            temp = img.copy()
            pixdata = temp.load()
            targ = pixdata[x,y]
            
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

                doTimeCheck(f"allowed - floodedCount is now: {floodedCount} — {floodedCount/floodLimit:.2%} (of a requested: {floodLimit}/{pixCount})")

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

# SLUR TREATISE

def radioFillMixedPalette():
    choices = getInputPalette()
    img = mix2_public()
    img = radioFill(img=img, choices=choices)

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
        choices = getInputPalette()

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
            stamp = getStamp()
        
        stampTrans = None
        
        if imgpath != "":
            img = Image.open(imgpath)
            choices = [] 
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
    """
    p2: func name
    """

    try:
        global input_palette

        imgpath = getInsertById(getParam(4))
        img = Image.open(imgpath)

        stampf = getParam_Func(1)
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

def radioFill_recurse(imgpath="", img=None, passes=7, maxDuration = 25):
    try:
        if img is None:
            if imgpath == "":
                imgpath = getInsertById(getParam(4))
            img = Image.open(imgpath)

        startTime = time.time()        

        for i in range(passes):
            now = time.time()
            duration = now - startTime

            if duration > maxDuration:
                break

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
            iAlg = getRandomFloodFill_Rando()
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

        maxDuration = 25
        startTime = time.time()
        
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

            now = time.time()
            duration = now - startTime

            if duration > maxDuration:
                break

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
        
        img = Image.open(imgpath)

        stamp = Image.open(stamppath)
        iicount = 7 # random.randint(2, 4)
        
        for i in range(iicount):
            if random.randint(0, 1) == 0:
                stamp = stamp.convert("RGB")
                stamp = ImageOps.invert(stamp)
                stamp = stamp.convert("RGBA")
        
            stamp = resizeToMinMax(stamp, maxW=200, maxH=100, minW=100, minH=50)

            img = radioFill_stamp(imgpath="", img=img, stamp=stamp)
            stamp = img
        
    except Exception as e:
        img = writeImageException(e)
        
    return img

def radioFill_recurse_func():
    try:
        img = ""
       
        p1 = getParam(0)

        if img == "":            
            stampf = getParam_Func(1)            

            if p1 == "wordGrid2":
                stampf = wordGrid2

            img = stampf()

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
            
            x += 1
        
    except Exception as e:
        img = writeImageException(e)

    return img

def radioFill_compFunc(imgpath="", img=None, passes=5, maxDuration = 10):
    try:
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
                break

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
            (r,g,b,a) = safetyCheck(r, g, b, a)
            
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
    width = getCurrentStandardWidth()
    height = getCurrentStandardHeight()

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
    width = getCurrentStandardWidth()
    height = getCurrentStandardHeight()

    img = ""
    
    try:
        img = Image.new("RGBA", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        myy = random.randint(10, height - 10)

        draw.line((0, myy, img.size[0], myy), "black")

        iAlg = getRandomFloodFill_Rando()

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

        choices = getInputPalette()

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
                          maxStackDepth = 0,
                          choices = choices)
    except Exception as e:
        img = writeImageException(e)

    return img

def grid_other(choices=[], lineColor="black"):
    width = getCurrentStandardWidth()
    height = getCurrentStandardHeight()

    img = ""
    
    try:
        if len(choices) == 0:
            choices = getInputPalette()

        if lineColor == "staticChoice":
            lineColor = random.choice(choices)
            
        squareSize = random.randint(25, 125)
        i = random.randint(50, 75)
        c = (i, i, i)
        
        img = Image.new("RGBA", (width,height), c)
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        iAlg = getRandomFloodFill_Rando()

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
                    iAlg = getRandomFloodFill_Rando()

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

        # words = [getRandomWord() + " " + getRandomWord()]
        words = [getAHex()]

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
        width, height = 1280, 1024
        img = Image.new("RGB", (width, height), "#FFFFFF")
        
        pixdata = img.load()

        x, y = width // 2, height // 2
        targ = pixdata[x,y]        

        if choices == []:
            choices = getInputPalette()

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

        randomIt = getRandomFloodFill_Rando()
        
        floodfill(img, (x, y), targetcolour = targ,
                  newcolour = (0,0,0),
                  randomIt = randomIt,
                  choices = choices,
                  compFunc=-1)
            
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
    try:
        textSize = 48
        wordCount = 15
        spacing = 15

        w = 1024
        h = (wordCount + 1) * (textSize) + 25

        maxX = 0

        choices = getInputPalette()

        bgColor = random.choice(choices)
        fill = random.choice(choices)

        bucky_legacy = getParam_Bucky("LEGACY")

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
            text = getRandomWord() if bucky_legacy else getAHex()

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

        palette = getInputPalette(generate=False, noneIfNoInput=True)

        if len(palette) > 0:
            choices = palette

        coco = bigSquareGrid(choices)
        coco = coco.convert("P", palette=Image.ADAPTIVE)
        
        img = img.quantize(method=2, palette=coco)
        
    except Exception as e:
        img = writeImageException(e)
        
    return img

def wordGrid():
    """
    HEX: get a hex instead of grid word<br />
    LEGACY: skip lum increase which avoids black on black
    """

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

        bucky_hex = getParam_Bucky("HEX")
        bucky_legacy = getParam_Bucky("LEGACY")
        
        while maxX < img.size[0]:            
            x = maxX + 25

            for y in range(5, img.size[1]-1 - (fontSize+xTra), fontSize+xTra):
                iAlg = random.randint(0, 15)
                word = getGridWord(iAlg, 0, p1) if not bucky_hex else getAHex()
               
                fon = ImageFont.truetype(fontPath + fontNameWordReg, fontSize)

                text_size_x = draw.textlength(word, font=fon)

                if text_size_x + x > maxX:
                    maxX = x + text_size_x + 5

                fillColor = random.choice(choices)

                while fillColor[:3] == (0,0,0):
                    fillColor = random.choice(choices)

                if not bucky_legacy:
                    fillColor = quick_contrast(fillColor, (0,0,0))

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

def wordGrid2(wordline="", fontSize=36, fontPath="", showFontName=False):
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
    
    p1 = getParam(0, textOnly=True)
    p2 = getParam(1, textOnly=True)
    
    try:
        bgColor = (0,0,0)
        bucky_hex = getParam_Bucky("HEX")

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
                    word = getDecree(p1, p2).upper() if not bucky_hex else getAHex()
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
        
        if showFontName:
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

        stringy = f"Decree: iAlg: {iAlg} w1, w2: {w1} {w2}"
        colorPrint.print_custom_rgb(stringy, 160, 160, 255)
        addState(stringy)

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
        
    p1 = getParam(0)
    p2 = getParam(1)
    
    outputs = []

    try:
        things = [time.time(), "ABC", "123", 255, 128, 0, (0,0), (0, 5), (50, 5)]

        for y in things:
            v2 = hashlib.sha256(str(y).encode('utf-8')).hexdigest()
            line = [y, hash(y), v2]
            
            outputs.append(line)
        
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
    
def wordGridGeneral(wordline="", fontSize=36, fontPath="", filterFunc=lambda w: w, word_count=48, extra_html="", actual_words=None, lemmas=None, lemma_depth=None):
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
        
        if lemma_depth is not None:
            outputText += f"depth: {lemma_depth}<br />"

        outputText += "</div>"
        
    outputText += extra_html + "<div class='output-text' id='output-text'>"
    outputText += f'<ul>'

    for o in outputs:
        outputText += f'<li>{o}</li>'

    outputText += "</ul></div>"

    return outputText

def wordGrid_image(showFontName=False):
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
        
        if showFontName:
            fontName = fontPathZ.split("/")[-1]
            fonSans = ImageFont.truetype(fontPathSansSerif, 16)
            text_size_x, text_size_y = dropin_text_size(draw,fontName, font=fonSans)
            draw.text((img.size[0] - text_size_x - 5, img.size[1] - text_size_y - 5), fontName, font=fonSans, fill=(255,255,255))

    except Exception as e:
        rootLogger.error(e)
        img = writeImageException(e)  
        
    return img

def wordGrid_Moby(wordline="", fontSize=42, fontPath="", showFontName=False):
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

        if showFontName:
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
    bucky_hex = getParam_Bucky("HEX")

    if wordline == "":
        if bucky_hex:
            wordline = getAHex()
        else:
            wordline = (getRandomWord() + " " + getRandomWord()).upper()
        
    return wordGrid2(wordline, 30)

def wordGrid_Special(wordline="", fontSize=36, fontPath="", showFontText=False):
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

        addState(f'filename: {filename}')

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
        
        if showFontText:
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
                      randomIt = getRandomFloodFill(),
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
    """
    p1: iAlg (default random)<br />
    p2: switcher (1=static palette, 2=new each tri)
    """

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

        cFill = random.choice(choices)
        cStroke = random.choice(choices)
        cStroke = (0,0,0) if cStroke == cFill else cStroke

        p0 = getParam(0)
        p0 = int(p0) if p0.isdecimal() else 0

        p1 = getParam(1)
        p1 = int(p1) if p1.isdecimal() else 0

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
                    
                draw.polygon(pts, fill=cFill, outline=cStroke)

                global maxFloodFillArg                
                iAlg = getRandomFloodFill() if p0 == 0 else p0

                try:
                    if p1 == 1:
                        choices = getPalette()
                    elif p1 == 2:
                        if k == 0:
                            choices = getPalette()

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
    """
    p1: iAlg<br />
    """

    img = ""

    try:
        img = Image.new("RGBA", (getCurrentStandardWidth(), getCurrentStandardHeight()), "#ffffff")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()
       
        p1 = getParam(0)
        iAlg = int(p1) if p1.isdecimal() else getRandomFloodFill_Rando()
        
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

def hsvEnum():
    img = ""

    try:
        w = random.randint(640, 1280)
        h = random.randint(480, 1024)
        
        img = Image.new("RGB", (w, h), "#ffffff")
        d = ImageDraw.Draw(img)

        pixdata = img.load()
        
        x, y = 0, 0
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
            
        fontPath = getFont()
        fon = ImageFont.truetype(fontPath, fontSize)

        h, s, v = 0, 1, 1
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
        width = 1400
        height = 100000
        
        img = Image.new("RGBA", (width, height), "#FFFFFF")        
        draw = ImageDraw.Draw(img)
        
        fontSize = 25
        y = 10
        
        getFont()

        global possibleFonts
        global fontBlacklist
        global fontPathSansSerif
                        
        fon = ImageFont.truetype(fontPathSansSerif, fontSize)

        sampleString = "AaBbCcDdEeFfGgHhIiJj  "

        choices = getInputPalette(generate=False, noneIfNoInput=True)
        
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

                if len(choices) > 0:
                    c = random.choice(choices)

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
        
        img = numpy_Fullfill(width, height)
        draw = ImageDraw.Draw(img)
        pixdata = img.load()
        
        fontPath = getFont()
        letter_count = random.randint(250, 1000)
        choices = getInputPalette(paletteLength=letter_count)

        c = getRandomColorRGB()

        for i in range(letter_count):
            fontSize = random.randint(10, 128)
            strokeSize = random.randint(2, 5)
            
            x = random.randint(-50, img.size[0])
            y = random.randint(-50, img.size[1])

            fon = ImageFont.truetype(fontPath, fontSize)
            
            word = random.choice(string.ascii_letters)

            c = random.choice(choices)
            cStroke = getInverse(c)
            
            draw.text((x, y), word, font=fon, fill=c, stroke_width=strokeSize, stroke_fill=cStroke)
            
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
        choices = getInputPalette()

        img = Image.new("RGBA", (1200, 1024), "#FFFFFF")
     
        jSize = 50
        i = random.randint(3, 7) * jSize
        j = i
        sizes = [i]
        
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

def getInputPalette(paletteLength=7, generate=True, noneIfNoInput=False):
    global input_palette

    bucky_ignore = getParam_Bucky("PALIGNORE")

    if input_palette != "" and input_palette != [] and not bucky_ignore:
        choices = input_palette
    else:         
        if generate:
            choices = getPaletteGenerated(paletteLength=paletteLength)
        elif not noneIfNoInput:
            choices = getPalette() # from directory
        else:
            choices = []

    return choices

def getPaletteSpecificName(palette_number):
    global palettelist

    for entry in palettelist:
        num = entry[0]
        name = entry[1]
        
        if num == palette_number:
            return name
        
    return "Unknown"

def getPaletteSpecific(palette):
    global rootLogger
    global input_palette

    if isinstance(palette, str) and str != "":
        try:
            palette = int(palette)
        except:
            palette = 0

    choices = []

    # colorPrint.print_custom_palette(191, f"palette: {palette}")
    
    pal_comp = getParam_Bucky("PALCOMP")
    pal_inverse = getParam_Bucky("PALINVERSE")
    pal_maybe = getParam_Bucky("PALMAYBE")

    if pal_maybe and random.randint(0, 1) == 1:
        if not pal_comp:
            pal_comp = True
            addState(f'maybeing pal_comp')
    
    if pal_maybe and random.randint(0, 1) == 1:
        if not pal_inverse:
            pal_inverse = True
            addState(f'maybeing pal_inverse')

    if palette == -1:
        # COMPLEXION HEADER
        global palette100_chosen
        if palette100_chosen == None:
            newone_data = random.choice([p for p in palettelist if p[0] != -1])
            newone = newone_data[0]
            addState(f'palette chosen for -1: {newone_data[1]}')
            palette100_chosen = newone_data[0]
        else:
            newone = palette100_chosen
            addState(f'palette read as -1 choice: {getPaletteSpecificName(newone)}')

        choices = getPaletteSpecific(newone)
    elif palette == 1:
        # V_A_P_O_R_W_A_V_E______________________ONE
        hexchoices = ["#00f9ff","#c36fbf","#6cffa2","#fff400","#ff00ce"]

        for c in hexchoices:
            c1 = hex_to_rgb(c)
            choices.append(c1)
    elif palette == 2:
        # primary
        global primaryColors
        choices = primaryColors.copy()
    elif palette == 3:
        # wacky
        global wackyColors
        choices = wackyColors.copy()          
    elif palette == 4:
        # coco
        global cocoColors

        for c in cocoColors:
            c1 = hex_to_rgb(c)
            choices.append(c1)          
    elif palette == 5:
        # atari
        global atariColors

        for c in atariColors:
            c1 = hex_to_rgb(c)
            choices.append(c1)
    elif palette == 6:
        hexc = ["#e3fb68","#c1ee73","#52a3ba","#344d78","#27292b"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 7:
        hexc = ["#ff0000","#310000","#ef0000","#ff9999","#faf999"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 8:
        hexc = ["#000000","#FF0000","#fcc10f","#68068c","#0e30c7"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 9:
        hexc = ["#000000","#FF0000","#FFFFFF","#FFFF00"]

        for c in hexc:
            c1 = hex_to_rgb(c)
            choices.append(c1)
    elif palette == 10:
        hexc = ["#010101","#031b75","#108c00","#17bbd3","#720c0a","#6c1c9e","#b25116","#b8b0a8","#4a4842","#0b63c4","#9bce00","#73f5d5","#e89e00","#ff7bdb","#fef255","#fffffe"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 11:
        hexc = ["#000000","#ff55ff","#55ffff","#ffffff"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 12:
        hexc = ["#000000","#55ff55","#ff5555","#ffff55"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 13:
        choices.append((0,0,0))

        for ipfreely in range(4, 255, 4):
            choices.append((ipfreely, 0, 0))
    elif palette == 14:
        hexc = ["#000000","#1D2B53","#7E2553","#008751","#AB5236","#5F574F","#C2C3C7","#FFF1E8","#FF004D","#FFA300","#FFEC27","#00E436","#29ADFF","#83769C","#FF77A8","#FFCCAA"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 15:
        hexc = ["#332c50","#46878f","#94e344","#e2f3e4"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 16:
        hexc = ["#ffffff","#fb6b1d","#e83b3b","#831c5d","#c32454","#f04f78","#f68181","#fca790","#1ebc73","#91db69","#fbff86","#cd683d","#9e4539","#7a3045","#6b3e75","#905ea9","#a884f3","#FF0000"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 17:
        hexc = ["#ff0546","#9c173b","#660f31","#450327","#270022","#17001d","#09010d","#0ce6f2","#0098db","#1e579c"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 18:
        hexc = ["#ff7b23","#474eff","#010afb","#ffaf47","#f48b01","#fd9206","#0a0a0a","#ffffff"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 19:
        hexc = ["#CCF1FF", "#E0D7FF", "#FFCCE1", "#D7EEFF", "#FAFFC7", "#E0BBE4", "#957DAD", "#D291BC", "#FEC8D8", "#FFDFD3"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 20:
        hexc = ["#FF0000", "#FF6600", "#FFFF00", "#00FF00", "#0000FF", "#000066", "#990099"]

        choices = list_hex_to_rgb(hexc)
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

        choices = list_hex_to_rgb(hexc)
    elif palette == 24:
        hexc = ["#000000","#55ff55","#88ff88","#ff5555","#ff8888","#ffff55","#ffff88"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 25:
        hexc = ["#85daeb","#5fc9e7","#5fa1e7","#5f6ee7","#4c60aa","#444774","#32313b","#463c5e","#5d4776","#855395","#ab58a8","#ca60ae","#f3a787","#f5daa7","#8dd894","#5dc190","#4ab9a3","#4593a5","#5efdf7","#ff5dcc","#fdfe89","#ffffff"]

        choices = list_hex_to_rgb(hexc)    
    elif palette == 26:
        hexc = ["#FF0000", "#00FF00", "#FFFF00", "#0000FF"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 27:
        hexc = ["#000000","#fcfcfc","#f8f8f8","#bcbcbc","#7c7c7c","#a4e4fc","#3cbcfc","#0078f8","#0000fc","#b8b8f8","#6888fc","#0058f8","#0000bc","#d8b8f8","#9878f8","#6844fc","#4428bc","#f8b8f8","#f878f8","#d800cc","#940084","#f8a4c0","#f85898","#e40058","#a80020","#f0d0b0","f87858","#f83800","#a81000","#fce0a8","#fca044","#e45c10","#881400","#f8d878","#f8b800","#ac7c00","#503000","#d8f878","#b8f818","#00b800","#007800","#b8f8b8","#58d854","#00a800","#006800","#b8f8d8","#58f898","#00a844","#005800","#00fcfc","#00e8d8","#008888","#000458","#f8d8f8","#787878"]

        choices = list_hex_to_rgb(hexc)
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

        choices = list_hex_to_rgb(hexc)
    elif palette == 32:
        hexc = ["#ffd319", "#ff901f", "#ff2975", "#f222ff", "#8c1eff"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 33:
        hexc = ["#4b3832","#854442","#fff4e6","#3c2f2f","#be9b7b"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 34:
        hexc = ["#338833","#1da27c","#30105a","#fbe82d","#510e0e","#632812","#0c4540"]
        
        choices = list_hex_to_rgb(hexc)
    elif palette == 35:
        hexc = ["#9A52FF","#FF5500","#980000","#FFE100","#63FFFC"]
        
        choices = list_hex_to_rgb(hexc)
    elif palette == 36:
        hexc = ["#3498DB", "#2E3E70", "#1A1D23", "#3495B7", "#5C6BC0"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 37:
        hexc = ["#99dd99","#dd99dd", "#9999dd", "#dd9999","#dddd99","#99dddd"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 38:
        hexc = ["#99ff99","#ff99ff", "#9999ff", "#ff9999","#ffff99","#99ffff"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 39:
        hexc = ["#ddff99","#f55df5", "#65faff", "#ffdd99","#f0f09d","#ddffff"]

        choices = list_hex_to_rgb(hexc)  
    elif palette == 40:
        hexc = ["#ff1b1b","#bc99dd","#0000ff","#00d21f","#ffffff","#ffff00"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 41:
        hexc = ["#dd9999","#ffdd99","#ff9999","#1C1919","#d49292"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 42:
        hexc = ["#00446f", "#6e2774", "#205061", "#6e6963", "#22aa22"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 43:
        hexc = ["#001f26","#003f4d","#33bdbd","#99e5e5", "#ce4993","#ff0000","#FFD700"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 44:
        hexc = ["#001f26","#b91010", "#003f4d", "#887788", "#9E16C4", "#3E3210"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 45:
        hexc = ["#b91010", "#c8ff00", "#366E36", "#042A02", "#FF7300"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 46:
        hexc = [ "#9E16C4", "#3300aa", "#f9d79f", "#ff4395", "#0099ff"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 47:
        hexc = ["#FFD700", "#c8b400", "#006400", "#3CB371"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 48:
        hexc = ["#ff00c1","#9600ff","#4900ff","#00b8ff","#00fff9"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 49:
        hexc = ["#fbbbad","#ee8695","#4a7a96","#333f58","#292831"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 50:
        hexc = ["#eeaf61","#fb9062","#ee5d6c","#ce4993","#6a0d83"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 51:
        hexc = ["#000000","#1a0a00","#331400","#662800","#994d00","#cc7700","#ff9900","#ffbb33","#ffcc66"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 52:
        hexc = ["#000000","#1e004f","#3b00a6","#6f00cc","#b000a6","#e6005c","#ff3300","#ff6600","#ffcc00","#ffff66","#ffffff"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 53:
        hexc = ["#0b1a0f","#1f3d1a","#335c26","#4d7f33","#6ba64d","#99c27a","#c2d9aa","#8c6239","#5c3b1e","#332011"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 54:
        hexc = ["#001f26","#003f4d","#005c66","#007a80","#009999","#33bdbd","#66d1d1","#99e5e5","#cceeee","#e6ffff"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 55:
        hexc = ["#ffffff","#000000","#e41a1c","#377eb8","#4daf4a","#984ea3","#ff7f00","#ffff33"]

        choices = list_hex_to_rgb(hexc)
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
        choices = list_hex_to_rgb(hexc)

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
        choices = list_hex_to_rgb(hexc)

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
        choices = list_hex_to_rgb(hexc)
    elif palette == 59:
        hexc = [
            "#29abe2",  # bright teal / turquoise
            "#93278f",  # bold purple stroke
            "#f2f2f2",  # paper cup white
            "#0d3b66",  # dark navy accent
            "#ff66cc",  # neon pink highlight (optional exaggeration for vaporwave feel)
        ]

        choices = list_hex_to_rgb(hexc)
    elif palette == 60:
        hexc = [
            "#3b9c9c",  # teal base
            "#264653",  # dark navy lines
            "#6a4c93",  # purple accents
            "#e63946",  # red dots
        ]

        choices = list_hex_to_rgb(hexc)
    elif palette == 61:
        hexc = [
            "#000000",  # black base
            "#ff00ff",  # neon pink
            "#00ffff",  # neon cyan
            "#39ff14",  # neon green
            "#ffea00",  # neon yellow
            "#8000ff",  # neon purple
        ]

        choices = list_hex_to_rgb(hexc)
    elif palette == 62:
        hexc = [
            "#ff66cc",  # hot pink
            "#00ccff",  # bright turquoise
            "#9933ff",  # electric purple
            "#66ff66",  # neon green
            "#ffff66",  # pastel yellow highlight
            "#ffffff",  # white accents
        ]

        choices = list_hex_to_rgb(hexc)
    elif palette == 63:
        hexc = [    "#000000",    "#0000d8",    "#0000ff",    "#d80000",    "#ff0000",    "#d800d8",    "#ff00ff",    "#00d800",    "#00ff00",    "#00d8d8",    "#00ffff",    "#d8d800",    "#ffff00",    "#d8d8d8",    "#ffffff"]
        
        choices = list_hex_to_rgb(hexc)
    elif palette == 64:
        hexc = ["#000000","#626262","#898989","#adadad","#ffffff","#9f4e44","#cb7e75","#6d5412","#a1683c","#c9d487","#9ae29b","#5cab5e","#6abfc6","#887ecb","#50459b","#a057a3"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 65:  # Desert Sun
        hexc = [
            "#e6c27a",  # warm sand
            "#d98e04",  # ochre
            "#c1440e",  # rust red
            "#732c02",  # deep clay
            "#87a6c1"   # washed-out sky blue
        ]
        choices = list_hex_to_rgb(hexc)

    elif palette == 66:  # Tropical Fruit
        hexc = [
            "#ffe135",  # banana yellow
            "#ff6f61",  # guava pink
            "#ff9f1c",  # papaya orange
            "#2ec4b6",  # teal/palm leaf
            "#6ee16e"   # lime green
        ]
        choices = list_hex_to_rgb(hexc)

    elif palette == 67:  # Glitchwave
        hexc = [
            "#ff00ff",  # harsh magenta
            "#00ffff",  # neon cyan
            "#00ff00",  # toxic green
            "#000000",  # deep black
            "#aaaaaa"   # static gray
        ]
        choices = list_hex_to_rgb(hexc)
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

        choices = list_hex_to_rgb(hexc)
    elif palette == 72:  # Blue CRT
        hexc = ["#000000","#001a0a","#00331a","#004d33","#00664d","#008066","#339999","#66b2b2","#99cccc"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 73:  # Rust and Patina
        hexc = ["#2f1b0c","#5e2d15","#8c3f1d","#b85a28","#d98c4d","#35524a","#4f7c72","#6fa69a","#9cc9b8"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 74:  # Memphis Design
        hexc = ["#ff6f61","#6b5b95","#88b04b","#f7cac9","#92a8d1","#ffde59","#ffb347","#ff77ff","#40e0d0"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 75:  # Corporate 2000s
        hexc = ["#003366","#336699","#6699cc","#99ccff","#cce6ff","#e6e6e6","#cccccc","#999999","#333333"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 76:  # Neon Tubes
        hexc = ["#ff00ff","#00ffff","#39ff14","#ff3131","#ffff33","#ff6ec7","#00ffcc","#ff9a00","#ff0055"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 77:  # Plastic Toys
        hexc = ["#ff0000","#0000ff","#ffff00","#00ff00","#ff7f00","#ff00ff","#00ffff","#ff3399","#9933ff"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 78: 
        hexc = ["#ED0A3F","#FF8833","#FBE870","#01A368","#0066FF","#8359A3","#AF593E","#000000"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 79:
        hexc = ["#FFFFFF","#FDD5B1","#FFCBA4","#FA9D5A","#E97451","#9E5B40","#CA3435","#000000"]
        choices = list_hex_to_rgb(hexc)
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

        choices = list_hex_to_rgb(hexc)
            
    elif palette == 81:  # Pastel Goth
        hexc = ["#b28ccf","#a0c4ff","#ffafcc","#cdb4db","#000000","#444444","#777777"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 82:  # Modern SaaS (Corporate Pastel)
        hexc = ["#e0f7fa","#80deea","#4dd0e1","#00acc1","#7e57c2","#f8bbd0","#263238"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 83:  # Aurora Borealis
        hexc = ["#0b3d91","#0d1b2a","#1b4332","#00ffb3","#5efc8d","#8a2be2","#000000"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 84:  # Renaissance Fresco
        hexc = ["#a37c40","#c9a66b","#6d8b99","#bfb9a3","#ede3d0","#8c5a3c","#4a403a"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 85:  # Japanese Woodblock
        hexc = ["#0f4c81","#b22222","#f5deb3","#2e8b57","#000000","#c0c0c0","#ffffff"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 86:  # Pop Art (CMYK style)
        hexc = ["#00bfff","#ff00ff","#ffff00","#000000","#ffffff","#ff4500","#32cd32"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 87:  # MOS6502 Woodgrain
        hexc = ["#2c1b0f","#8b5a2b","#cdaa7d","#f4a460","#ffd700","#000000","#556b2f"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 88:  # Toxic Earth
        hexc = ['#361313', '#a9593d', '#ff5c5c', '#d3ea54', '#c7ff5c']
        choices = list_hex_to_rgb(hexc)

    elif palette == 89:  # Alice in Wonderland
        hexc = ['#f4ed46', '#b4f2ff', '#5ce1f4', '#ffffff', '#ffeaca']
        choices = list_hex_to_rgb(hexc)

    elif palette == 90:  # Bird Cry
        hexc = ['#7abac7', '#89cedd', '#9afffc', '#fcceff', '#eeb0ff']
        choices = list_hex_to_rgb(hexc)

    elif palette == 91:  # Cotton Candy Rainbow
        hexc = ['#fbc0c0', '#ffdaa1', '#f9ffc9', '#baffe5', '#a9cdff']
        choices = list_hex_to_rgb(hexc)

    elif palette == 92:  # Ice Cream
        hexc = ['#6b3e26', '#ffc5d9', '#c2f2d0', '#fdf5c9', '#ffcb85']
        choices = list_hex_to_rgb(hexc)

    elif palette == 93:  # Loud Amplifiers
        hexc = ['#ff0000', '#ffa700', '#fff400', '#009fff', '#0011ff']
        choices = list_hex_to_rgb(hexc)
    elif palette == 94:
        hexc = ['#52c7ad', '#47dfd3', '#b46464', '#695b5b', '#f0caa4']
        choices = list_hex_to_rgb(hexc)
    elif palette == 95:
        hexc = ['#2175d9', '#00308f', '#e30074', '#b8d000', '#ff9900']
        choices = list_hex_to_rgb(hexc)
    elif palette == 96:
        c1 = getRandomColorRGB()
        c2 = getRandomColorRGB()

        c3 = getColorComplement(c1)
        c4 = getColorComplement(c2)

        choices = [c1, c2, c3, c4]
    elif palette == 97:
        c1 = getRandomColorRGB()
        c2 = getRandomColorRGB()
        c3 = getRandomColorRGB()

        c4 = getColorComplement(c1)
        c5 = getColorComplement(c2)
        c6 = getColorComplement(c3)

        choices = [c1, c2, c3, c4, c5, c6]
    elif palette == 98:
        choices = getPalette()        
    elif palette == 99:
        input_palette = []
        choices = getPaletteGenerated(rgb = (0,0,0), paletteLength = random.randint(3, 8))
    elif palette in [100, 255]:
        input_palette = []
        choices = getPaletteGenerated(rgb = (0,0,0), paletteLength = palette)
    elif palette == 101:
        hexc = ["#ffff00","#ff0000","#ff93c7","#00ffff","#ff7f00"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 102:
        hexc = ["#1a2635","#d26c94","#584c8e","#00685f","#b1104f","#58a7ac","#00638d","#f1e170"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 103:
        hexc = [
            "#dd0303",  # red
            "#fdf000",  # yellow
            "#007f26",  # green
            "#004ff5",  # blue
            "#543011",  # brown
            "#70c1d1",  # light blue
            "#fdb4cd",  # pink
            "#030003",  # black
            "#fdfffe"   # white
            ]
        choices = list_hex_to_rgb(hexc)
    elif palette == 104:
        hexc = [
            "#0a3410",  # Sap Green
            "#4e1500",  # Alizarin Crimson
            "#221b15",  # Van Dyke Brown
            "#5f2e1f",  # Dark Sienna
            "#000000",  # Midnight Black
            "#021e44",  # Prussian Blue
            "#0c0040",  # Phthalo Blue
            "#102e3c",  # Phthalo Green
            "#ffec00",  # Cadmium Yellow
            "#c79b00",  # Yellow Ochre
            "#ffb800",  # Indian Yellow
            "#db0000",  # Bright Red
            "#ffffff",  # Titanium White
        ]
        choices = list_hex_to_rgb(hexc)
    elif palette == 126:
        hexc = ["#FF0000", "#00FF00", "#FFFF00", "#0000FF", "#ac4313", "#ff00ff", "#00ffff"]

        choices = list_hex_to_rgb(hexc)
    elif palette == 226:
        hexc = ["#FF0000", "#00FF00", "#FFFF00", "#0000FF", "#ac4313", "#ff00ff", "#00ffff"]

        for c in hexc:
            z = hex_to_rgb(c)
            choices.append(z)
            zc = getColorComplement(z)
            choices.append(zc)
    elif palette == 326:
        hexc = ["#FF0000", "#00FF00", "#FFFF00", "#0000FF", "#ac4313", "#ff00ff", "#00ffff"]

        for c in hexc:
            z = hex_to_rgb(c)
            choices.append(z)
            zc = getInverse(z)
            choices.append(zc)
            zc = getColorComplement(z)
            choices.append(zc)
    elif palette == 300:
        hexc = ["#003049","#d62828","#f77f00","#fcbf49","#eae2b7"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 301:
        hexc = ["#6f1d1b","#bb9457","#432818","#99582a","#ffe6a7"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 302:
        global palette302_text
        hexc = wordnet_palette(palette302_text, k=6)        
        choices = list_hex_to_rgb(hexc)
    elif palette == 303:
        hexc = [
            "#5A3A29",  # deep brown (wood frame / dark fabric)
            "#A47551",  # lighter brown / tan threads
            "#BFA58A",  # beige upholstery
            "#7B8F4B",  # avocado green
            "#E07A2E",  # burnt orange
            "#FFD77B"   # goldenrod accent
        ]
        choices = list_hex_to_rgb(hexc)
    elif palette == 304:
        hexc = ["#5d0865","#fae53a","#ed3196","#6a91cf","#f18018"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 305:
        hexc = ["#D71920","#F6BE00","#009739","#0067B9","#EF3340","#FF6F20","#FFD100","#582C83"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 306:
        hexc = ["#FCD5CE","#F9C74F","#FF99AC","#A9DEF9","#6BCB77","#FF6B6B","#FFEEDD","#3D405B"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 307:
        hexc = ["#2F2F2F","#595959","#8C7B75","#C4B7A6","#D9D9D9","#ECECEC","#7A6F5F","#9C9583"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 308:
        hexc = ["#00FF41","#00CFFF","#9900FF","#FF00CC","#FF9900","#FFFF00","#3333FF","#00FFFF"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 309:
        hexc = ["#e3dac9","#E3B6A4","#C48A6E","#8B5E3C","#E0CDB2","#8A0303", "#880808", "#980002"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 310:
        hexc = ["#0000ff","#ffc0cb","#ff0000","#ffff00","#000000"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 311:
        hexc = ["#e88325","#ff9029","#ff9c3f","#062800","#066f00"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 312:
        # Channel twist – neon red undertone
        hexc = ["#ff0050","#ff3399","#ff6600","#ff3300","#ff99cc"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 313:
        # Channel twist – pinned greenish mutation
        hexc = ["#00ff80","#40ffb3","#80ffc0","#00cc99","#009966"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 314:
        # Forbidden fruit – clashing wrongness
        hexc = ["#7fff00","#e0b0ff","#556b2f","#00ffff","#ff2400"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 315:
        # Quadratic decay with green dominance
        choices = [
            (int((255 - (i*i*8)) % 256),            
            200 + ((i*37) % 55),
            int((i*23) % 256))
            for i in range(6)
        ]
    elif palette == 316:
        # Medical slide – dried bloods and bile tones
        hexc = ["#e32636","#b22222","#704214","#f3e5ab","#556b2f"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 317:
        # Sinusoidal red-green ramp
        choices = [
            (int((math.sin(i) + 1) * 127),
            int((math.cos(i * 1.3) + 1) * 127),
            64 + (i * 15) % 191)
            for i in range(12)
        ]
    elif palette == 318:
        # Quadratic decay with blue dominance
        choices = [
            (int((255 - (i*i)) % 256),
            int((i*23) % 256),
            200 + ((i*37) % 55))
            for i in range(12)
        ]
    elif palette == 319:
        # XOR pattern between channels
        choices = [
            ((i*40) % 256,
            (i*85) % 256,
            ((i*40) ^ (i*85)) % 256)
            for i in range(12)
        ]
    elif palette == 320:
        # HSV rainbow, converted manually
        choices = [
            tuple(int(c*255) for c in colorsys.hsv_to_rgb(i/16.0, 1.0, 1.0))
            for i in range(16)
        ]
    elif palette == 321:
        # Prime-modulated palette
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
        choices = [
            ((p * 37) % 256,
            (p * 73) % 256,
            (p * 109) % 256)
            for p in primes
        ]
    elif palette == 322:
        # Harsh neon inversions
        choices = [
            (255 - ((i*53) % 256),
            255 - ((i*89) % 256),
            255 - ((i*149) % 256))
            for i in range(12)
        ]
    elif palette == 323:
        # Noise-based palette (seeded for reproducibility)
        rng = np.random.default_rng(42)
        choices = [
            (rng.integers(0, 256),
            rng.integers(0, 256),
            rng.integers(0, 256))
            for _ in range(12)
        ]
    elif palette == 324:
        # Logarithmic ramp (warped earth tones)
        choices = [
            (int(math.log(i+2)*70) % 256,
            int(math.log(i+3)*90) % 256,
            int(math.log(i+4)*110) % 256)
            for i in range(12)
        ]
    elif palette == 325:
        hexc = ["#A6634A","#C67FAE","#D7E8BC","#98DDDF","#A6BE47","#2E5283","#6F8D6A","#E3BD33","#E2552D","#C9B27C"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 327:
        hexc = ["#633517","#a6001a","#e06000","#ee9600","#ffab00","#004d33","#00477e"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 328:
        hexc = [
            "#594d45", # camo brown
            "#79533d", # camo red
            "#595142", # camo olive
            "#745d46", # camo field
            "#ac7e54", # camo earth
            "#a9947b", # camo sand
            "#b49d80", # camo tan
            "#bcab90", # camo sandstone
            "#535640", # camo dark green
            "#54504b", # camo forest
            "#63613e", # camo light green
            "#4a5444", # camo green
            "#5c5c5b", # camo dark gray/grey
            "#9495a5", # camo gray/grey
            "#373538"  # camo black
        ]
        choices = list_hex_to_rgb(hexc)
    elif palette == 329:
        hexc = ["#dcd4c9",  # skin/light base
                "#555555",  # hoodie/dark grey
                "#3b3b3b",  # pants/shadow grey
                "#8e8e8e",  # shoes/lighter grey
                "#f5f0e9"]  # background/white-ish
        choices = list_hex_to_rgb(hexc)
    elif palette == 330:
        hexc = ["#890024","#C5023C","#FBFCF6","#000000"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 331:
        hexc = ["#890024","#C5023C","#215d38","#14a651","#F5DE05"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 332:
        hexc = ["#ff6174","#078a42","#6db105","#ffd602","#f5624b","#B13D4C","#38b91c","#1c5c0e"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 333:
        hexc = [
            "#e94a31", "#a1331e", "#f1ceba", "#ff6400",
            "#f69e34", "#9e7e49", "#d0d31b", "#344526",
            "#255641", "#013631", "#00a6bf", "#2c3547",
            "#2e3677", "#f221da", "#d1425f", "#5f1123",
        ]
        choices = list_hex_to_rgb(hexc)
    elif palette == 334:
        hexc = ["#b00ba0","#de1e7e","#e1e100","#BADA55","#F0FEAF","#ac1d1c","#facade","#c0ffee","#defec8","#deface","#0ff1ce","#a55"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 335:
        hexc = ["#ffb1b7","#ffb9be","#ffc1c5","#ffc8cd","#ffd0d4","#ffd8db"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 336:
        hexc = ["#dd1a20","#2a125c","#fefefe","#db7248"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 337:
        hexc = [
            "#4A7F7D",  # dark teal
            "#69A6A1",  # light seafoam
            "#2F5C59",  # deep green-teal
            "#88B7B3",  # pale aqua
            "#D2E2E4",  # very light cyan/gray
            "#4E7E9A",  # slate blue
            "#94BFCF",  # pastel sky blue
            "#C6DEE2",  # soft ice blue
            "#A3C9D5",  # muted pastel aqua
            "#DEE9EB",  # near white, bluish tint
            ]
        choices = list_hex_to_rgb(hexc)
    elif palette == 338 or palette == 339:
        hexc = ["#121c10",  # Almost-black green, like dense canopy shadows
                "#1c2e1a",  # Deep forest green, ancient and heavy
                "#2a4225",  # Moss-covered bark green
                "#355e3b",  # Balanced earthy green, classic forest tone
                "#4a6f4f",  # Muted sage green for softer foliage
                "#2f5d50",  # Shaded bluish green, cool and misty
                "#5b8a5a",  # Brighter mid-green for leaf highlights
                ]
        
        if palette == 339:
            hexc.append("#9bbf80") # Sunlit canopy green, slightly yellowed

        choices = list_hex_to_rgb(hexc)
    elif palette == 340:
        hexc = ["#b56afc","#a740ef","#fa818a","#590316","#1a4d59","#360178","#2e2d3d","#2f2e40"]
        choices = list_hex_to_rgb(hexc)
    elif palette == 341:  # Amethyst Storm (purple-leaning)
        hexc = ["#3b0a57","#5e2b97","#7a3eb1","#a675d1","#c89aff","#d1b3ff","#2e1a47","#1b1024"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 342:  # Neon Coven (neon purple/magenta with darks)
        hexc = ["#ff00cc","#c400ff","#7a00ff","#ff66e3","#39ffd5","#2b004d","#1a0033","#0d001a"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 343:  # Snow Crash (white-dominant, cool accent)
        hexc = ["#ffffff","#f5f7fa","#e6e9ef","#d8dbe2","#bfc5cf","#8a90a1","#00baff","#ff2fb2"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 344:  # Paper Lantern (white/cream-dominant, warm accent)
        hexc = ["#fffaf0","#fff4e6","#f8eddc","#f0e6d8","#e6dccb","#d8cfc0","#bfae9a","#ffcc88"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 345:  # Plasma Bloom (magenta-forward gradient)
        hexc = ["#ff1e8a","#ff4fb3","#ff7ad9","#ffa3e2","#d1006f","#8a0060","#3a003a","#2a0f2b"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 346:  # Golden Hour Static
        hexc = ["#ffcc33","#ffb347","#ff9933","#e67300","#b35900","#806040","#404040","#f2e6d9"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 347:  # Lemon Circuitry
        hexc = ["#f7ff00","#d4e100","#a8c800","#7f9a00","#4d6600","#000000","#ffffff","#c0c0c0"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 348:  # Cornfield Cathedral
        hexc = ["#fff5cc","#ffe680","#ffcc00","#e6b800","#997a00","#664d00","#87ceeb","#f0e6d2"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 349:  # Toxic Mustard
        hexc = ["#d4c400","#a69f00","#807a00","#666600","#4c4c19","#333300","#99cc33","#cccc00"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 350:  # Sunbleach Mirage
        hexc = ["#fff9db","#fff2b2","#ffe680","#ffd966","#e6cc4d","#ccb233","#ffccaa","#f2e6e6"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 351:
        hexc = ["#31176b","#7dc2e7","#e74140","#f8d849","#f94a39","#cbecf8","#a7c5e1"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 352:
        hexc = ["#c080c0","#8080c0","#80c0c0","#80c080","#c0c080","#c08080"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 353:
        hexc = ["#fe581d","#0c0a0a","#70442c","#8f5852","#e6201b","#e5e3e4"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 354:
        hexc = ["#5f7fbc","#8acde8","#050505","#e7581c","#dd2324","#d5ba09","#f3ea07"]
        choices = list_hex_to_rgb(hexc)

    elif palette == 355:
        hexc = [
            "#F0F8FF", "#FAEBD7", "#00FFFF", "#7FFFD4", "#F0FFFF", "#F5F5DC", "#FFE4C4", "#000000",
            "#FFEBCD", "#0000FF", "#8A2BE2", "#A52A2A", "#DEB887", "#5F9EA0", "#7FFF00", "#D2691E",
            "#FF7F50", "#6495ED", "#FFF8DC", "#DC143C", "#00FFFF", "#00008B", "#008B8B", "#B8860B",
            "#A9A9A9", "#006400", "#BDB76B", "#8B008B", "#556B2F", "#FF8C00", "#9932CC", "#8B0000",
            "#E9967A", "#8FBC8F", "#483D8B", "#2F4F4F", "#00CED1", "#9400D3", "#FF1493", "#00BFFF",
            "#696969", "#1E90FF", "#B22222", "#FFFAF0", "#228B22", "#FF00FF", "#DCDCDC", "#F8F8FF",
            "#FFD700", "#DAA520", "#808080", "#008000", "#ADFF2F", "#F0FFF0", "#FF69B4", "#CD5C5C",
            "#4B0082", "#FFFFF0", "#F0E68C", "#E6E6FA", "#FFF0F5", "#7CFC00", "#FFFACD", "#ADD8E6",
            "#F08080", "#E0FFFF", "#FAFAD2", "#D3D3D3", "#90EE90", "#FFB6C1", "#FFA07A", "#20B2AA",
            "#87CEFA", "#778899", "#B0C4DE", "#FFFFE0", "#00FF00", "#32CD32", "#FAF0E6", "#FF00FF",
            "#800000", "#66CDAA", "#0000CD", "#BA55D3", "#9370DB", "#3CB371", "#7B68EE", "#00FA9A",
            "#48D1CC", "#C71585", "#191970", "#F5FFFA", "#FFE4E1", "#FFE4B5", "#FFDEAD", "#000080",
            "#FDF5E6", "#808000", "#6B8E23", "#FFA500", "#FF4500", "#DA70D6", "#EEE8AA", "#98FB98",
            "#AFEEEE", "#DB7093", "#FFEFD5", "#FFDAB9", "#CD853F", "#FFC0CB", "#DDA0DD", "#B0E0E6",
            "#800080", "#663399", "#FF0000", "#BC8F8F", "#4169E1", "#8B4513", "#FA8072", "#F4A460",
            "#2E8B57", "#FFF5EE", "#A0522D", "#C0C0C0", "#87CEEB", "#6A5ACD", "#708090", "#FFFAFA",
            "#00FF7F", "#4682B4", "#D2B48C", "#008080", "#D8BFD8", "#FF6347", "#40E0D0", "#EE82EE",
            "#F5DEB3", "#FFFFFF", "#F5F5F5", "#FFFF00", "#9ACD32"
        ]
        choices = list_hex_to_rgb(hexc)

    elif palette >= 5000:
        pal = next((p for p in palettelist if p[0] == palette), None)
        choices = getPalette(pal[2]) if pal is not None else getPalette()
    else:
        input_palette = []
        choices = getPaletteGenerated()

    # rootLogger.debug(f'palette: {palette} // pal_comp: {pal_comp} // pal_inverse: {pal_inverse}')

    if pal_comp or pal_inverse:
        c2 = []

        if pal_comp:
            for c in choices:
                zc = getColorComplement(c)
                c2.append(zc)

        if pal_inverse:
            for c in choices:
                zc = getInverse(c)
                c2.append(zc)

        for c in c2:
            choices.append(c)

    seen = {}
    choices = [seen.setdefault(x, x) for x in choices if x not in seen]

    # rootLogger.debug(f'choices chosen: {choices}')

    return choices

def wordnet_palette(seed="forest", k=6):
    import wn
    wn.config.allow_multithreading = True
    WN_OBJ = wn.Wordnet("oewn:2024")

    syns = wn.synsets(seed)
    if not syns: return ["#888888"]*k

    s = random.choice(syns)

    LEX2HUE = { 'noun.artifact':20, 'noun.plant':110, 'noun.body':350, 'noun.feeling':300, 'noun.location':210, 'noun.shape':45, 'noun.substance':170, 'noun.time':200 }
    
    hue = LEX2HUE.get(s.lexfile(), random.randrange(360))
    
    hexc = []
    for i in range(k):
        h = ((hue + i*11)%360)/360.0
        v = 0.55 + 0.40*((i%2))
        s_ = 0.45 + 0.35*((i//2)%2)
        r,g,b = [int(255*c) for c in colorsys.hsv_to_rgb(h,s_,v)]
        hexc.append(f"#{r:02x}{g:02x}{b:02x}")

    return hexc

def getPaletteGenerated(rgb=(0,0,0), paletteLength=5, bgColor=None, minContrast=3):
    global input_palette
    palette = []

    if len(input_palette) == 0 or input_palette == "":
        # generate a palette
        if rgb == (0,0,0):
            c = getRandomColor()
        else:
            c = rgb

        hsv = colorsys.rgb_to_hsv(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)

        tries = 0

        while len(palette) < paletteLength and tries < 1000:
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

            tries += 1
    else:
        # use the one that was specified elsewhere
        palette = input_palette
        
    palette = sort_by_lum(palette)

    return palette

def generatePalette(palette=[], w=900, h=600):
    img = ""
    
    try:
        img = Image.new("RGB", (w, h))
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
        img = Image.new("RGBA", (getCurrentStandardWidth(), getCurrentStandardHeight()), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()        

        sizes = [random.choice([20,30,40,50,60,70])]

        iDirection = random.choice([0, 1, 2])
        
        palette = getInputPalette()

        for squareSize in sizes:
            for x in range(0, img.size[0], squareSize):
                for y in range(0, img.size[1], squareSize):
                    if sizes[0] == squareSize or random.randint(1, 5) < 3:
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

                        random.shuffle(palette)
                            
    except Exception as e:
        img = writeImageException(e)   

    return img

# SHITTER ADDRESS

def pieslice():
    try:
        width = 800
        height = 800
        
        img = Image.new("RGBA", (width,height), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        boxes = [(0,0,width,height)]

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
            try:
                draw.pieslice(boundingBox, startAngle, endAngle, fill=color, outline=(0,0,0))
            except:
                pass

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

    except Exception as e:        
        img = writeImageException(e)       

    return img

def insertFoured(imgpath=""):
    if imgpath == "":
        imgpath = getInsertById(getParam(4))
        
    img = Image.open(imgpath)

    try:
        mirror1 = img.transpose(Image.FLIP_LEFT_RIGHT)
        rot1 = img.rotate(180)
        mirror2 = mirror1.rotate(180)
        
        blendAmount = .50
        
        img = Image.blend(img, rot1, blendAmount)
        mirror = Image.blend(mirror1, mirror2, blendAmount)
        
        img = Image.blend(img, mirror, blendAmount)

        img = resizeToMax(img, maxW=1024, maxH=1024)

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

# PUSSYCAT REST

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
        cropX = 0
        cropY = 0
        
        img = Image.new("RGBA", (w, h), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        inserts = []        
        
        for i in range(2):
            insert = Image.open(getInsertById(getParam(4)))
            insert = resizeToMax(insert, maxW=w, maxH=h)
            
            img0 = Image.new("RGBA", (w, h), "#FFFFFF")
            img0.paste(insert, (0, 0))            

            cropX = max(cropX, insert.size[0])
            cropY = max(cropY, insert.size[1])
                
            inserts.append(img0)            

        img.paste(inserts[0], (0, 0))

        img = ImageChops.darker(img, inserts[1])

        img = img.crop((0, 0, cropX, cropY))
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
        w = 800
        h = 800

        interval = 0.001
        strokeWidth = random.randint(2, 12)
        colorSwitch = random.randint(10, 250)
        
        choices = getInputPalette()

        bucky_legacy = getParam_Bucky("LEGACY")
      
        img = Image.new('RGBA', (w, h), "#ffffff")
        
        x = w // 2
        y = h // 2        

        if not bucky_legacy:
            img = numpy_Fullfill(w, h, getRandomFloodFill())

        pixdata = img.load()
               
        n = random.randint(1, 7)
        d = n

        while d == n:
            d = random.randint(1, 8)
        
        # r = cos k theta
        # k = n // d

        k = (n * 1.0) / (d * 1.0)
        
        addState(f"n: {n} d: {d}")
            
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

        for pt in pts:
            x = pt[0]
            y = pt[1]
            
            if not bucky_legacy:
                floodfill(img, (x, y), targetcolour = pixdata[x,y],
                                newcolour = (0,0,0),
                                randomIt = getRandomFloodFill_Rando(),
                                choices=choices)
        
    except Exception as e:
        img = writeImageException(e)   

    return img

def spirograph():
    img = None

    try:
        # hypotrochoids

        height = getCurrentStandardHeight()
        width = getCurrentStandardWidth()

        choices = getInputPalette()
        bg = getInverse(random.choice(choices))
        
        if bg in choices:
            bg = getColorComplement(random.choice(choices))

        img = Image.new('RGB', (width, height), bg)
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        bucky_legacy = getParam_Bucky("LEGACY")

        # R is the radius of the fixed outer circle
        # r is the radius of the inner rolling circle
        # h is the distance from the center of the rolling circle to the tracing point
        # t is the parameter (angle)
        
        # Fit the figure nicely inside the viewport.
        R = 0.40 * min(width, height)       # big circle radius
        r = 0.17 * min(width, height)       # inner circle radius
        h = 0.80 * r                         # offset of drawing point

        # Center of the figure on the image:
        cx, cy = width / 2.0, height / 2.0

        # --- hypotrochoid parametric equations (θ in radians) ---------------
        # x(θ) = (R - r) cos θ + h cos( (R - r)/r * θ )
        # y(θ) = (R - r) sin θ - h sin( (R - r)/r * θ )
        # NOTE: we add the image center (cx, cy) so it’s visible on canvas.

        # How far to run θ so the curve closes:
        # The curve closes after θ reaches 2π * (r / gcd(R, r)).
        # Use integer-like gcd by rounding R,r to ints.
        g = math.gcd(max(1, int(round(R))), max(1, int(round(r))))
        theta_max = 2.0 * math.pi * (r / g)

        # Step small for a smooth curve; connect points with short segments.
        dtheta = 0.002  # ~ 3k–5k segments depending on theta_max

        def point_at(theta):
            k = (R - r) / r
            x = (R - r) * math.cos(theta) + h * math.cos(k * theta)
            y = (R - r) * math.sin(theta) - h * math.sin(k * theta)
            return (cx + x, cy + y)

        pts = [(width//2, height//2)]
        max_y = 0
        t = 0.0
        x0, y0 = point_at(t)        
        stroke_width = 3
        stroke = random.choice(choices)
        colorsKept = {}

        while t <= theta_max:
            t += dtheta
            x1, y1 = point_at(t)
            
            (colorsKept, stroke, key_used) = get_kept_color(colorsKept, stroke, choices, int(t))

            # Draw a short segment; round to pixel coords for robustness
            draw.line((x0, y0, x1, y1), fill=stroke, width=stroke_width)
            x0, y0 = x1, y1

            if y1 > max_y:
                max_y = int(y1)

        pts.append((width//2, max_y+stroke_width+1))

        for pt in pts:
            if not bucky_legacy:
                floodfill(img, pt, targetcolour = pixdata[pt],
                                newcolour = (0,0,0),
                                randomIt = getRandomFloodFill(),
                                choices=choices)
            
            # draw.point(pt, (0,0,0))

    except Exception as e:
        img = writeImageException(e)   

    return img

def flow_ribbons():
    img = None

    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        rnd = random.Random()
        img = Image.new("RGBA", (width, height), (255,255,255,0))
        draw = ImageDraw.Draw(img)

        palette = getInputPalette()

        seeds=random.randint(100, 400)
        steps=random.randint(100, 400)
        step_len=2.0
        s=90.0

        addState(f'seeds: {seeds}, steps: {steps}, step_len: {step_len}, s: {s}')

        def angle(x, y):
            return math.sin(x/s)*1.7 + math.sin(y/s)*1.3

        for i in range(seeds):
            x = rnd.uniform(0, width); y = rnd.uniform(0, height)
            pts = [(x,y)]
            for k in range(steps):
                θ = angle(x,y)
                x += math.cos(θ)*step_len
                y += math.sin(θ)*step_len
                if not (0<=x<width and 0<=y<height): break
                pts.append((x,y))
            if len(pts) > 1:
                col = palette[i % len(palette)] if palette else (255,255,255,90)
                draw.line(pts, fill=col, width=1)
    
    except Exception as e:
        img = writeImageException(e) 

    return img

# VICTIM CHARADE

def phyllotaxis(palette=None):
    img = None

    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        rnd = random.Random()
        img = Image.new("RGBA", (width, height), (255,255,255,0))
        draw = ImageDraw.Draw(img)
        palette = getInputPalette()

        count=random.randint(200, 3000)
        c=None
        jitter=0.0

        draw_lines = random.choice([False, True])

        addState(f'count: {count}, jitter: {jitter}')

        cx, cy = width/2, height/2
        φ = math.radians(137.507764)  # golden angle
        R = min(width, height) * 0.48
        if c is None: c = R / (count**0.5)  # scale so seeds fill nicely

        last_x = cx; last_y = cy;

        for n in range(count):
            θ = n*φ
            r = c*math.sqrt(n)
            x = cx + r*math.cos(θ)
            y = cy + r*math.sin(θ)
            if jitter: x += rnd.uniform(-jitter, jitter); y += rnd.uniform(-jitter, jitter)

            size = 1.5 + 2.5*(r/R)  # bigger toward outer ring

            if palette:
                idx = n % len(palette)
                col = palette[idx]
            else:
                col = (255,255,255,220)

            draw.ellipse([x-size,y-size,x+size,y+size], fill=col)

            if draw_lines:
                draw.line((last_x, last_y, x, y), col)

            last_x = x
            last_y = y

    except Exception as e:
        img = writeImageException(e) 

    return img

def sampleThing(palette=None):
    img = None

    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        rnd = random.Random()
        img = Image.new("RGBA", (width, height), (255,255,255,0))
        draw = ImageDraw.Draw(img)
        choices = getInputPalette()

    except Exception as e:
        img = writeImageException(e) 

    return img

def voronoiMosaic(palette=None, n_points=60, downsample=1):
    img = None

    try:
        W = getCurrentStandardWidth()
        H = getCurrentStandardHeight()

        rnd = random.Random()
        palette = getInputPalette() if palette is None else palette
        pal = np.array(palette, dtype=np.uint8)[:, :3]  # (K,3)

        # optional speed-up: compute on a smaller grid, then scale up
        w = max(1, W // downsample)
        h = max(1, H // downsample)

        # seeds in the *working* resolution
        seeds = np.column_stack([
            np.random.randint(0, w,  size=n_points),
            np.random.randint(0, h,  size=n_points)
        ])  # (N,2)

        # colors per seed
        color_idx = np.random.randint(0, len(pal), size=n_points)
        seed_colors = pal[color_idx]  # (N,3)

        # coordinate grid (h,w,2)
        yy, xx = np.mgrid[0:h, 0:w]
        # distances to all seeds, fully vectorized -> (N,h,w)
        dx = xx[None, :, :] - seeds[:, 0][:, None, None]
        dy = yy[None, :, :] - seeds[:, 1][:, None, None]
        dist2 = dx*dx + dy*dy

        nearest = np.argmin(dist2, axis=0)       # (h,w), int index of seed
        rgb = seed_colors[nearest]               # (h,w,3) uint8

        small = Image.fromarray(rgb, mode="RGB")
        if downsample > 1:
            # scale up with NEAREST to keep hard Voronoi edges
            small = small.resize((W, H), resample=Image.NEAREST)

        # return RGBA, fully opaque
        img = Image.new("RGBA", (W, H))
        img.paste(small.convert("RGBA"))

    except Exception as e:
        img = writeImageException(e)

    return img

def waveInterference(palette=None):
    img = None

    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        rnd = random.Random()
        img = Image.new("RGBA", (width, height), (255,255,255,0))
        draw = ImageDraw.Draw(img)
        palette = getInputPalette()         

        cx1, cy1 = rnd.randint(0,width), rnd.randint(0,height)
        cx2, cy2 = rnd.randint(0,width), rnd.randint(0,height)
        freq = random.randint(3, 10) * .01

        for x in range(width):
            for y in range(height):
                d1 = math.hypot(x - cx1, y - cy1)
                d2 = math.hypot(x - cx2, y - cy2)
                val = math.sin(d1*freq) + math.sin(d2*freq)
                idx = int(((val+2)/4) * (len(palette)-1))
                draw.point((x,y), fill=palette[idx])

    except Exception as e:
        img = writeImageException(e) 

    return img

def truchetTiles(palette=None):
    img = None

    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        rnd = random.Random()
        img = Image.new("RGBA", (width, height), (255,255,255,0))
        draw = ImageDraw.Draw(img)
        palette = getInputPalette()         

        tile_size = random.randint(20, 60)

        for x in range(0, width, tile_size):
            for y in range(0, height, tile_size):
                color = random.choice(palette)
                
                if rnd.random() > 0.5:
                    draw.pieslice([x,y,x+tile_size,y+tile_size], 0, 90, fill=color)
                    draw.pieslice([x,y,x+tile_size,y+tile_size], 180, 270, fill=color)
                else:
                    draw.pieslice([x,y,x+tile_size,y+tile_size], 90, 180, fill=color)
                    draw.pieslice([x,y,x+tile_size,y+tile_size], 270, 360, fill=color)

    except Exception as e:
        img = writeImageException(e) 

    return img

def touchéTiles(palette=None):
    img = None

    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        rnd = random.Random()
        img = Image.new("RGBA", (width, height), (255,255,255,0))
        draw = ImageDraw.Draw(img)
        palette = getInputPalette()         

        tile_size = random.randint(20, 60)

        for x in range(0, width, tile_size):
            for y in range(0, height, tile_size):
                color = random.choice(palette)

                if rnd.random() > 0.5:
                    rng1 = random.randint(0, 90)
                    rng2 = random.randint(rng1, 180)
                    rng3 = random.randint(rng2, 270)
                    rng4 = random.randint(rng3, 360)

                    draw.pieslice([x,y,x+tile_size,y+tile_size], rng1, rng2, fill=color)
                    draw.pieslice([x,y,x+tile_size,y+tile_size], rng3, rng4, fill=color)
                else:
                    rng1 = random.randint(90, 180)
                    rng2 = random.randint(rng1, 270)
                    rng3 = random.randint(rng2, 360)
                    rng4 = random.randint(rng3, 360)

                    draw.pieslice([x,y,x+tile_size,y+tile_size], rng1, rng2, fill=color)
                    draw.pieslice([x,y,x+tile_size,y+tile_size], rng3, rng4, fill=color)                    

    except Exception as e:
        img = writeImageException(e) 

    return img

def interferenceGrids(palette=None):
    """
    Moiré/beat patterns from a few angled sine grids.
    Fast enough for typical sizes; maps the interference value to the input palette.
    """
    img = None
    try:
        width  = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        rnd = random.Random()
        img = Image.new("RGBA", (width, height), (255,255,255,255))
        draw = ImageDraw.Draw(img)
        palette = getInputPalette()

        # Build 2–4 sine layers at different angles/frequencies
        layers = rnd.randint(2, 4)
        params = []

        for _ in range(layers):
            theta = rnd.uniform(0, math.pi)                 # grid angle
            # frequency in cycles per image; convert to radians/pixel
            cycles = rnd.uniform(2.5, 8.0)                  # tweak for tighter/looser bands
            k = 2.0 * math.pi * cycles / max(width, height)
            ax, ay = math.cos(theta) * k, math.sin(theta) * k
            amp = rnd.uniform(0.6, 1.2)
            phase = rnd.uniform(0, 2*math.pi)
            params.append((ax, ay, amp, phase))

        # Precompute amplitude sum to normalize quickly
        A = sum(abs(p[2]) for p in params)
        if A == 0:
            A = 1.0

        px = img.load()
        lc = len(palette)

        # Evaluate field per pixel and map to palette
        for y in range(height):
            for x in range(width):
                s = 0.0
                for ax, ay, amp, ph in params:
                    s += amp * math.sin(ax * x + ay * y + ph)
                # Normalize to 0..1, then to palette index
                v = (s + A) / (2.0 * A)
                idx = int(v * (lc - 1))
                px[x, y] = palette[idx] + (255,)

    except Exception as e:
        img = writeImageException(e)

    return img

def orbitSwarmsOnInterferonGrids():
    img = None
    
    try:
        img = interferenceGrids()
        img = orbitSwarms(img, N=20)

    except Exception as e:
        img = writeImageException(e)

    return img

def orbitSwarms(img=None, palette=None, N=-1):
    """
    Swirling particle orbits that leave soft trails—think cosmic dust / flow rings.
    """

    try:
        rnd = random.Random()
        
        if img is None:            
            width  = getCurrentStandardWidth()
            height = getCurrentStandardHeight()
            img = Image.new("RGBA", (width, height), (255,255,255,255))
        else:
            width = img.size[0]
            height = img.size[1]

        draw = ImageDraw.Draw(img)
        palette = getInputPalette()

        cx, cy = width // 2, height // 2
        mind = min(width, height)

        # Swarm setup
        if N < 0:
            N      = rnd.randint(120, 220)           # particles
        steps  = rnd.randint(220, 420)           # time steps
        dt     = rnd.uniform(0.006, 0.012)       # time increment

        # Optional slight drift of the center to create spiral bias
        drift_ang = rnd.uniform(0, 2*math.pi)
        drift_mag = rnd.uniform(0.0, 0.004) * mind

        # Particle state
        parts = []
        for _ in range(N):
            r0   = rnd.uniform(0.10, 0.45) * mind
            amp  = rnd.uniform(0.02, 0.12) * mind      # radial wobble
            f    = rnd.uniform(0.8, 2.2)               # wobble freq
            th0  = rnd.uniform(0, 2*math.pi)
            w    = rnd.uniform(0.8, 3.2) * rnd.choice([-1, 1])  # angular vel
            clr  = rnd.choice(palette)
            a    = rnd.randint(48, 96)                 # trail alpha
            parts.append([r0, amp, f, th0, w, clr, a, None])

        # Animate
        for t in range(steps):
            # drift the system center a touch
            cdx = cx + math.cos(drift_ang) * drift_mag * (t/steps)
            cdy = cy + math.sin(drift_ang) * drift_mag * (t/steps)

            for p in parts:
                r0, amp, f, th0, w, clr, alpha, prev = p
                # radial oscillation + slow shrink/expand
                r = r0 + amp * math.sin(f * t * dt) + 0.02 * amp * math.sin(0.25 * t * dt)
                th = th0 + w * t * dt

                x = int(cdx + r * math.cos(th))
                y = int(cdy + r * math.sin(th))

                dot_size = 3

                if prev is not None:
                    # thin lines, low alpha; occasional dots at endpoints for sparkle
                    draw.line([prev, (x, y)], fill=clr + (alpha,), width=1)
                    if t % rnd.randint(18, 36) == 0:
                        draw.ellipse([x-dot_size, y-dot_size, x+dot_size, y+dot_size], fill=clr + (min(255, alpha+40),))

                p[7] = (x, y)
                if prev is None:
                    p[7] = (x, y)

    except Exception as e:
        img = writeImageException(e)

    return img

def orbitInterferenceHybrid(palette=None):
    img = None
    try:
        width  = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        rnd = random.Random()
        img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        palette = getInputPalette()

        cx, cy = width // 2, height // 2
        lc = max(1, len(palette))

        # ---------- interference field (continuous) ----------
        # returns a smooth scalar in [-1, 1]
        def field(x, y):
            # normalize
            fx, fy = (x - cx) / float(width), (y - cy) / float(height)
            # 3 blended sines with slightly different frequencies & rotations
            a = math.sin( 8.0*fx + 0.0*fy)
            b = math.sin( 0.7*fx + 9.0*fy)
            # rotate coords for the third wave
            rx, ry = (fx*0.866 - fy*0.5, fx*0.5 + fy*0.866)
            c = math.sin( 11.0*rx - 7.5*ry )
            return (a + b + c) / 3.0

        # ---------- paint the background as quantized “cells” ----------
        # 5–7 bands from the palette
        bands = min(7, lc)
        for y in range(height):
            for x in range(width):
                v = field(x, y)                  # [-1,1]
                t = int(((v + 1.0) * 0.5) * (bands - 1))
                r, g, b = palette[t % lc]
                img.putpixel((x, y), (r, g, b, 255))

        # soft vignette to give depth
        maxd = math.hypot(cx, cy)
        for y in range(height):
            for x in range(width):
                d = math.hypot(x - cx, y - cy) / maxd
                if d > 0.85:
                    r, g, b, a = img.getpixel((x, y))
                    k = 1.0 - (d - 0.85) * 0.9
                    img.putpixel((x, y), (int(r*k), int(g*k), int(b*k), a))

        # ---------- orbit swarms steered by the field ----------
        # number of swarms & base radii
        swarms = rnd.randint(18, 28)

        for _ in range(swarms):
            base_r   = rnd.uniform(min(width, height)*0.10, min(width, height)*0.47)
            thickness= rnd.randint(1, 2)
            steps    = rnd.randint(900, 1400)
            # each swarm gets a small per-step “drag” and field coupling
            drag     = rnd.uniform(0.998, 0.9996)       # radial decay
            coupling = rnd.uniform(0.9, 2.0)            # how strongly field affects path
            # choose color from palette, slightly darker for lines
            cr, cg, cb = palette[rnd.randrange(lc)]
            line = (max(0, cr-25), max(0, cg-25), max(0, cb-25), 255)
            dot  = (cr, cg, cb, 255)

            # random initial phase & radial wobble
            theta = rnd.random()*math.tau
            r     = base_r
            wobble= rnd.uniform(0.6, 2.5)

            last = None
            for i in range(steps):
                # sample field at current point to modulate angular velocity and radius
                x = cx + r * math.cos(theta)
                y = cy + r * math.sin(theta)

                # field-driven angular velocity; normalize field to ~[-1,1]
                v = field(x, y)
                dtheta = (0.008 + 0.004*v) * coupling     # “refractive” twist
                theta += dtheta

                # gentle radial wobble + drag
                r = r * drag + math.sin(i*0.02 + wobble) * 0.15

                p = (x, y)
                if last:
                    draw.line([last, p], fill=line, width=thickness)
                last = p

                # occasional beads on the path
                if i % rnd.randint(45, 75) == 0:
                    rr = rnd.randint(2, 4)
                    draw.ellipse([x-rr, y-rr, x+rr, y+rr], fill=dot)

        # optional: crisp highlight ring to anchor composition
        ring_r = min(width, height)*0.34
        # draw.ellipse([cx-ring_r, cy-ring_r, cx+ring_r, cy+ring_r],
        #              outline=(0, 0, 0, 70), width=1)

    except Exception as e:
        img = writeImageException(e)
    return img

# ****************************************************************
# *                         FLOWER BOX                           *
# ****************************************************************

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

# FRY MASTERPLAN

def neobored():
    img = ""
    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()
               
        img = Image.new("RGB", (width,height), "#ffffff")
        draw = ImageDraw.Draw(img)

        pixdata = img.load()   

        global maxFloodFillArg
        
        choices = getInputPalette()

        pts = []

        for i in range(width-1, 0, -100):
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
           
            pts.append((i-50, 30))
            pts.append((30, i-50))

        pts.append((3, 5))
        pts.append((5, 3))

        used_iAlgs = []

        for pt in pts:
            iAlg = getRandomFloodFill(used_iAlgs)

            random.shuffle(choices)

            floodfill(img, pt,
                      targetcolour = (255,255,255),
                      newcolour=(255,255,0),
                      randomIt = iAlg,
                      choices = choices)

            used_iAlgs.append(iAlg)
            
    except Exception as e:
        img = writeImageException(e)
        
    return img

# ORGANISM CHUNKING

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

# MARTINIQUE FERRYMAN

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
       
        lastX = img.size[0]-1
        while iteration < maxIterations and lastX >= 0:
            (x,y) = (lastX, random.randint(0, img.size[1]-1))

            iAlg = 0

            if alg != 0:
                iAlg = alg
            else:
                while iAlg == 0:
                    iAlg = getRandomFloodFill_Rando()

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
        origImg = img
        draw = ImageDraw.Draw(img)
        
        fon = ImageFont.truetype(fontPathSansSerif, 18)
        debugFillColor = (0, 0, 0, 255)
        textY = 100
        
        draw.text((5, textY), "imgpath: " + imgpath, font=fon, fill=debugFillColor)
    
    return [img, origImg]

def fillFromOuter_blend():
    try:
        global input_palette

        iAlg = getRandomFloodFill_Rando()

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

# DARKBLUE HEART

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
        choices = getInputPalette()
        iAlg = getRandomFloodFill_Rando()
        
        # floodfill(img, (width // 2, height // 2),
        #                   targetcolour = pixdata[5,5],
        #                   newcolour = (160,128,100),
        #                   randomIt = iAlg,
        #                   maxStackDepth = 0,
        #           choices = choices)

        img = numpy_Fullfill(width, height, iAlg)
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

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
                      grandradiant,
                      wordGrid_single,
                      paletteSquares,
                      generatePalette,
                      ellipseGuy,
                      colorHatch,
                      hsvEnum]
    
    doTimeCheck("stampFuncs gotten")

    stampf = random.choice(stampFuncs)        
    
    doTimeCheck("stampf gotten")

    stamp = stampf()
    
    doTimeCheck("stampf ran")

    stamp = resizeToMinMax(stamp, maxW=400, maxH=200, minW=200, minH=100)

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
    stamp = resizeToMinMax(stamp, maxW=400, maxH=200, minW=200, minH=100)

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
    """
    p1: distance (default=5)
    """

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

        addState(f'colors length: {len(colors)}, colors2 length: {len(colors2)}')

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
        iAlg = getRandomFloodFill()

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

def effect_mandelbrot_anim():
    """
    Smooth Mandelbrot zoom.<br />
    - n_frames: number of frames<br />
    - zoom_per_frame: multiplicative scale (<1 shrinks view each frame)<br />
    - center: complex-plane point to zoom into (Seahorse Valley by default)<br />
    """

    img = ""
    frames = []

    mandelbrot_regions = {
        "seahorse_valley": {
            "center": (-0.743643135, 0.131825963),
            "zoom_rate": 0.95,
            "max_iter_start": 200,
            "max_iter_growth": 5,
            "desc": "Canonical Seahorse Valley, infinite spirals."
        },
        "elephant_valley": {
            "center": (-0.7435, 0.1314),
            "zoom_rate": 0.96,
            "max_iter_start": 180,
            "max_iter_growth": 4,
            "desc": "Elephant-like trunks and arches."
        },
        "triple_spiral_valley": {
            "center": (-0.088, 0.654),
            "zoom_rate": 0.97,
            "max_iter_start": 220,
            "max_iter_growth": 6,
            "desc": "Three-armed spirals radiating infinitely."
        },
        "seahorse_elephant_xover": {
            "center": (-0.7435669, 0.1314023),
            "zoom_rate": 0.95,
            "max_iter_start": 200,
            "max_iter_growth": 5,
            "desc": "Hybrid spirals and elephant trunks."
        },
        "valley_of_the_birds": {
            "center": (-0.1015, 0.633),
            "zoom_rate": 0.96,
            "max_iter_start": 210,
            "max_iter_growth": 6,
            "desc": "Wing- or feather-like structures."
        },
        "spiral_hub": {
            "center": (-0.761574, -0.0847596),
            "zoom_rate": 0.94,
            "max_iter_start": 250,
            "max_iter_growth": 8,
            "desc": "Chaotic deep spirals and branching filaments."
        },
        "needle_point": {
            "center": (-0.743643887037151, 0.13182590420533),
            "zoom_rate": 0.92,
            "max_iter_start": 300,
            "max_iter_growth": 10,
            "desc": "Extremely detailed dendritic tendrils."
        },
        "satellite_valley": {
            "center": (-1.748, 0.0),
            "zoom_rate": 0.97,
            "max_iter_start": 180,
            "max_iter_growth": 4,
            "desc": "Lots of miniature Mandelbrots chained along tendrils."
        }
    }

    try:
        width  = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        # Start with a view that shows most of the set (keeps aspect correct)
        # Typical Mandelbrot width ~ 3.0 around x ~ -0.75
        start_half_width = 1.8  # half-span in x; 2*1.8 = 3.6 total width
        aspect = height / float(width)

        n_frames=120
        zoom_per_frame=0.85

        # Colorize (effect_mandelbrot returns L)
        pal = getInputPalette() 
        pal = sort_by_lum(pal)

        choice = "elephant_valley"
        params = mandelbrot_regions[choice]

        center = params["center"]        
        max_iter = params["max_iter_start"]
        cx, cy = center

        for i in range(n_frames):
            rootLogger.debug(f'frame {i} rendering')

            # Ease a little for smoother feeling (optional)
            t = i / max(1, n_frames - 1)
            ease = t**1.6  # gentle ease-in

            # Current half-width shrinks each frame
            half_w = start_half_width * (zoom_per_frame ** (i + ease))
            half_h = half_w * aspect

            # PIL expects extent as (x1, y1, x2, y2)
            extent = (cx - half_w, cy - half_h, cx + half_w, cy + half_h)

            # Increase iterations as we zoom so fine detail stays crisp
            iters = int(80 + 2.5 * i)  # ~80 → ~380 over 120 frames
            mb = Image.effect_mandelbrot((width, height), extent, iters)

            a = pal[0]
            b = pal[-1]
            frame = ImageOps.colorize(mb, black=a, white=b).convert("RGB")

            frames.append(frame)

        # --- build a SINGLE palette from the first frame and quantize all frames to it
        pal_img = frames[0].quantize(colors=256, method=Image.MEDIANCUT)
        locked_palette = pal_img.getpalette()  # 768-length list

        def quantize_with_locked_palette(im_rgb):
            q = im_rgb.quantize(palette=pal_img, dither=Image.FLOYDSTEINBERG)
            q.putpalette(locked_palette)  # ensure identical palette table
            return q

        frames_p = [quantize_with_locked_palette(fr) for fr in frames]

        # Build animated GIF (duration in ms)
        buf = BytesIO()
        frames_p[0].save(
            buf,
            format='GIF',
            save_all=True,
            append_images=frames_p[1:],
            duration=50,
            loop=0,
            disposal=2, # clear between frames
            optimize=False
        )
        buf.seek(0)
        img = Image.open(buf)

    except Exception as e:
        img = writeImageException(e)

    return img

def radial_gradient():
    img = ""
    
    try:
        width = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        img = Image.radial_gradient("L")
        pal = getInputPalette()
        pal = sort_by_lum(pal)

        a = pal[0]
        b = pal[-1]
        img = ImageOps.colorize(img, black=a, white=b).convert("RGB")

        img = resizeToMax(img, width, height)                
         
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
        img = Image.new("RGBA", (w, h), "#ffffff")
        pixdata = img.load()

        global maxFloodFillArg
        
        if iAlg == 0:
            iAlg = getRandomFloodFill()

        c = pixdata[w//2,h//2]

        parmies = getIntParams(iAlg, random.randint(10, 25))
        pl1 = parmies[1]
        iAlg = parmies[0]
        
        choices = getInputPalette(paletteLength=pl1)
        
        floodfill(img, (w//2,h//2),
                          targetcolour = c,
                          newcolour = (160,128,100),
                          randomIt = iAlg,
                          maxStackDepth = 0,
                          compFunc=-1,
                  choices = choices)
         
    except Exception as e:
        img = writeImageException(e)

    return img

def fullFillLatest():
    global maxFloodFillArg

    return fullFill(iAlg=maxFloodFillArg)

def fullfillBlend2():
    """
    p1 = iAlg (default 0)<br />
    p2 = palette length when generated
    """

    try:
        whatever = getRandomFloodFill()
        width, height = getCurrentStandardWidth(), getCurrentStandardHeight()
        img = numpy_Fullfill(width, height, whatever)
        img2 = numpy_Fullfill(width, height, whatever)

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
            iAlg = getRandomFloodFill()   

        width = int(getCurrentStandardWidth() * 1.25)
        height = int(getCurrentStandardHeight() * 1)
        
        img = Image.new("RGB", (width,height), "#ffffff")        
        draw = ImageDraw.Draw(img)
        pixdata = img.load()
         
        fillTestTotal = 50
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

        iAlg = getRandomFloodFill_Rando()

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
        w = getCurrentStandardWidth()
        h = getCurrentStandardHeight()
        
        img = Image.new("RGBA", (w, h), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        pixdata = img.load()

        y = 30
        x = 40

        sqX = 80
        sqY = 50

        xText = x + sqX + 20

        fontPath = getFont()

        addState(f'font chosen: {fontPath}')

        fon = ImageFont.truetype(fontPath, 22) 
        
        for i in range(14):
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

            txt = f'{colorName} — {rgb_to_hex(c)} ({str(c[0])},{str(c[1])},{str(c[2])})'            
            
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
        fon = ImageFont.truetype(fontPath, 22)

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
            fillAlg = getRandomFloodFill()

            while fillAlg in fillAlgs:
                fillAlg = getRandomFloodFill()    

            fillAlgs.append(fillAlg)

            choices = getPaletteGenerated()

            floodfill(img, (x+1, y+1),
                      targetcolour = pixdata[x+1,y+1],
                      newcolour = (0,0,0),
                          randomIt = fillAlg,
                          maxStackDepth = 0,
                      choices = choices)            

            txt = colorName + " "
            
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

def garlicItUp():
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
                     grandradiant,
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

def wordfilled(wordline="", fontSize=128, width=800, height=250, iAlg=None, spacing=15, stroke_w=3, font_preset=""):
    try:
        if iAlg is None:
            iAlg = getRandomFloodFill_Rando()

        choices = getInputPalette()

        # background flood
        # floodfill(
        #     img, (width//2, height//2),
        #     targetcolour=img.getpixel((width//2, height//2)),
        #     newcolour=(0, 0, 0, 255),
        #     randomIt=iAlg,
        #     maxStackDepth=0,
        #     choices=choices
        # )

        img = numpy_Fullfill(width, height, iAlg)
        draw = ImageDraw.Draw(img)

        word = (wordline or getRandomWord()).upper()
        font_path = getFont(font_preset)

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

        addState(f'word: {word}')

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
    iAlg = getRandomFloodFill()

    return wordfilled(iAlg=iAlg)

def wordfilled_mult(width=800, height=300):
    wf = []

    totalHeight = 0

    ySize = random.randint(4, 10)
    
    for i in range(0, ySize):        
        iAlg = getRandomFloodFill()
        
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

def newgrid_orig(width=getCurrentStandardWidth(),height=getCurrentStandardHeight()):
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

        choices = getInputPalette()

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

def newgrid(width=getCurrentStandardWidth(), 
            height=getCurrentStandardHeight(),
            rows=10, 
            cols=10, 
            line_thickness=1):
    """
    Draws a grid of black lines on a white background.<br />
    <br />
    Args:<br />
        width (int): image width in pixels<br />
        height (int): image height in pixels<br />
        rows (int): number of rows in the grid<br />
        cols (int): number of columns in the grid<br />
        line_thickness (int): thickness of grid lines in pixels        
    """
    
    grid = np.full((height, width), 255, np.uint8)  # white

    # Centers of lines as pixel indices (inclusive end at width-1/height-1)
    xs = np.linspace(0, width  - 1, cols + 1, dtype=int)
    ys = np.linspace(0, height - 1, rows + 1, dtype=int)

    half = line_thickness // 2

    # Vertical lines
    for x in xs:
        x0 = max(0, x - half)
        x1 = min(width, x + half + 1)   # +1 because slicing is exclusive at the end
        grid[:, x0:x1] = 0

    # Horizontal lines
    for y in ys:
        y0 = max(0, y - half)
        y1 = min(height, y + half + 1)
        grid[y0:y1, :] = 0

    # Convert to image
    img = Image.fromarray(grid, mode="L")
    img = img.convert("RGB")

    return img

def gptsNewDots(width=getCurrentStandardWidth(), height=getCurrentStandardHeight()):
    """
    Make a colored grid from a random-walk value field.<br / >
    - Build a cols×rows scalar field via cumulative 1..4 steps.<br / >
    - Optionally flip signs in a checker to create banding.<br / >
    - Normalize to 0..1 and map to either the input palette or HSV.
    """
    try:
        # --- layout ------------------------------------------------------------
        rng = random.Random()
        cols = rng.randint(20, 120)         # keep cells >= ~6–10 px at 1280
        rows = rng.randint(20, 120)

        col_w = max(1, width  // cols)
        row_h = max(1, height // rows)

        # snap to full tiles; crop later
        grid_w = col_w * cols
        grid_h = row_h * rows

        img = Image.new("RGBA", (grid_w, grid_h), (0, 0, 0, 255))
        draw = ImageDraw.Draw(img)

        # --- value field (random-walk + optional checker flip) -----------------
        # Use numpy for speed; treat first dim as rows (y), second as cols (x).
        field = np.zeros((rows, cols), dtype=np.int32)

        zz = 0
        # Fill row-major for a pleasing drift; you can try column-major for different shear.
        steps = np.random.randint(1, 5, size=(rows, cols), dtype=np.int16)  # 1..4
        # cumulative sum over flattened view → random ramp
        zz_arr = np.cumsum(steps.ravel(), dtype=np.int64).reshape(rows, cols)
        field[:] = zz_arr

        # Variant: flip signs in a checker or stripes for banding
        # --- value field (random-walk + optional checker/stripe flip) ---
        field = field.astype(np.int32)  # already rows x cols

        if rng.random() < 0.6:
            yy, xx = np.ogrid[:rows, :cols]           # yy: (rows,1), xx: (1,cols)
            if rng.random() < 0.5:
                # checkerboard
                checker = ((xx + yy) & 1) == 0        # shape (rows, cols)
            else:
                # stripes (randomly vertical or horizontal)
                if rng.random() < 0.5:
                    checker = (xx % 2) == 0           # vertical stripes, (rows, cols)
                else:
                    checker = (yy % 2) == 0           # horizontal stripes, (rows, cols)
            try:
                field[checker] *= -1
            except:
                pass

        # Slight regional drift: add a low-freq gradient
        if rng.random() < 0.7:
            gy = np.linspace(-1.0, 1.0, rows)[:, None]
            gx = np.linspace(-1.0, 1.0, cols)[None, :]
            grad = (0.15 + 0.25 * rng.random()) * (gx * rng.choice([1, -1]) + gy * rng.choice([1, -1]))
            field = field + (grad * field.std()).astype(np.int32)

        # --- normalize 0..1 ----------------------------------------------------
        f32 = field.astype(np.float32)
        vmin, vmax = float(f32.min()), float(f32.max())
        if vmax == vmin:
            norm = np.zeros_like(f32)
        else:
            norm = (f32 - vmin) / (vmax - vmin)  # 0..1

        # Option A: palette mapping (discrete)
        palette = getInputPalette()
        use_palette = len(palette) >= 3
        palette = sort_by_lum(palette)

        if use_palette:
            idx = np.clip((norm * (len(palette) - 1)).astype(np.int32), 0, len(palette) - 1)
            # jitter to avoid flat bands
            if rng.random() < 0.5:
                jitter = (np.random.rand(rows, cols) * 0.999).astype(np.float32)
                idx = np.clip(((norm + 0.12 * jitter) * (len(palette) - 1)).astype(np.int32), 0, len(palette) - 1)
        else:
            # Option B: HSV ramp; hue from norm, subtle sat/value shaping
            hue = (norm + 0.03 * np.random.rand(rows, cols)).clip(0, 1)
            sat = 0.55 + 0.4 * (norm ** 0.85)
            val = 0.85 - 0.15 * (norm ** 1.2)
            hsv = np.stack([hue, sat, val], axis=-1)
            # fast HSV→RGB
            h = hsv[..., 0] * 6.0
            i = np.floor(h).astype(np.int32) % 6
            f = h - np.floor(h)
            p = val * (1.0 - sat)
            q = val * (1.0 - f * sat)
            t = val * (1.0 - (1.0 - f) * sat)
            rgb = np.zeros((*h.shape, 3), dtype=np.float32)
            m = (i == 0); rgb[m] = np.stack([val[m], t[m], p[m]], axis=-1)
            m = (i == 1); rgb[m] = np.stack([q[m], val[m], p[m]], axis=-1)
            m = (i == 2); rgb[m] = np.stack([p[m], val[m], t[m]], axis=-1)
            m = (i == 3); rgb[m] = np.stack([p[m], q[m], val[m]], axis=-1)
            m = (i == 4); rgb[m] = np.stack([t[m], p[m], val[m]], axis=-1)
            m = (i == 5); rgb[m] = np.stack([val[m], p[m], q[m]], axis=-1)
            rgb = (rgb * 255.0).clip(0, 255).astype(np.uint8)

        # --- render tiles ------------------------------------------------------
        # (Loops are fine here because we draw rects; the heavy math was vectorized.)
        for r in range(rows):
            y0 = r * row_h
            for c in range(cols):
                x0 = c * col_w
                if use_palette:
                    color = palette[int(idx[r, c])]
                else:
                    rr, gg, bb = map(int, rgb[r, c])
                    color = (rr, gg, bb)
                draw.rectangle((x0, y0, x0 + col_w, y0 + row_h), fill=color)

        # optional thin grid lines for definition
        if rng.random() < 0.25 and min(col_w, row_h) > 6:
            line = (0, 0, 0, int(40 + 80 * rng.random()))
            for c in range(1, cols):
                x0 = c * col_w
                draw.line((x0, 0, x0, grid_h), fill=line, width=1)
            for r in range(1, rows):
                y0 = r * row_h
                draw.line((0, y0, grid_w, y0), fill=line, width=1)

        # crop to requested size
        img = img.crop((0, 0, width, height))
        return img

    except Exception as e:
        return writeImageException(e)

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

        img = resizeToMinMax(img, maxW=w, maxH=h, minW=800, minH=600)
        img = img.convert("RGBA")

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

        choices = getPaletteGenerated()

        pnt = [(width // 2, height // 4),
               (width - 1, height // 2),
               (width // 2, height - 1),
               (width // 4, height // 2)]
        
        for p in pnt:
            iAlg = getRandomFloodFill_Rando()

            x = pixdata[p[0],p[1]]

            floodfill(img, p, targetcolour = x,
                    newcolour = (0,0,0),
                    choices=choices,
                    randomIt = iAlg)

        if random.randint(0, 3) == 2:
            p = (width//2,height//2)
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

        if seed is None:
            seed = random.randint(0, 1<<30)

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
    Draw N radial lines (3..14 by default) from the center to the image bounds,<br />
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

        choices = getInputPalette()

        # zonk = random.randint(0, min(width//2, height//2))
        # draw.ellipse((zonk, zonk, width - zonk, height - zonk), outline=(0,0,0), width=line_w)

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

            iAlg = getRandomFloodFill_Rando()
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
    """Create (pos, color) stops with pos in [0,1], including 0 and 1."""
    k = random.randint(2, n)
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
    stops = _make_stops(n=random.randint(2,len(choices)),choices=choices)

    if kind == "linear":
        theta = random.uniform(0, 2*math.pi)
        t = np.cos(theta)*X + np.sin(theta)*Y
        t = (t - t.min()) / (t.max() - t.min() + 1e-8)

    elif kind == "radial":
        cx, cy = random.uniform(0.3, 0.7), random.uniform(0.3, 0.7)
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
        t = random.choice([X,Y])

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
   
def single_gradient():
    try:
        choices = getInputPalette()

        width, height = getCurrentStandardWidth(), getCurrentStandardHeight()

        p2 = getParam(1)

        opts = ["linear","radial","conic","banded","split"]

        kind = random.choices(
            opts,
            weights=[3,2,2,2,2], k=1
        )[0]

        if p2 != "" and (p2 in opts or p2 == "default"):
            kind = p2
            addState(f'preset kind: {kind}')
        else:
            addState(f'kind: {kind}')

        tile = _tile_gradient(width, height, kind=kind, choices=choices)

        return tile
    except Exception as e:
        img = writeImageException(e)
        return img
    
def numpytest():
    def mymod_x1(x, y, z, count, choicelen):
        if count % 2 == 0:
            return int(abs(math.hypot(x, y))) ^ x                        
        else:
            return x ^ y

    def mymod_x2(x, y, z, count, choicelen):
        q = x ^ y | x
        return q % choicelen

    choices = getPaletteGenerated(paletteLength=10)

    w, h = 1280, 1024
    (rgb, colorsKept) = generateNumpy(mymod_x2, w, h, choices)
    img = Image.fromarray(rgb)
    
    return img

def numpyVerySimple():
    def mod_x(w, h, x, y, z, iCount, choicelen, tippingPoint):
        y2 = y // 30
        x2 = x // 30
        q = (x2 << 16) | y2

        return q 

    return numpyFill(mod_x)

def numpySimple():
    def mod_x(w, h, x, y, z, iCount, choicelen, tippingPoint):
        q = ((x&y) % 255,y % 255,(x | y) % 255)

        return q

    return numpyFill(mod_x)

def numpyFloodfill(iAlg=78):
    parmies = getIntParams(iAlg, 0)
    iAlg = parmies[0]

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
        if tippingPoint == 0:
            tippingPoint = 5

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

    # TODO: change getKeptColorNew to use few choices but have a second modifier that modifies that color by sat/lightness so we can blend
    
    choices = getPaletteGenerated(paletteLength=10)

    mod_x_touse = mod_x_1
    mod_y_touse = mod_x_1

    if iAlg == 47:
        mod_x_touse = mod_x_47
        mod_y_touse = mod_x_47
    elif iAlg == 78:
        mod_x_touse = mod_x_78
        mod_y_touse = mod_x_78
        tippingPoint = 5
    elif iAlg == 5001:
        mod_x_touse = mod_x_5001
        mod_y_touse = mod_x_5001
    
    return numpyFill(mod_x_touse, mod_y=mod_y_touse, choices=choices, tippingPoint=tippingPoint)
   
def numpyFillStandardModY(width, height, x, y, z, count, c, q):
    return c

def numpyFill(mod_x, mod_y=numpyFillStandardModY, w=getCurrentStandardWidth(), h=getCurrentStandardHeight(), choices=[], tippingPoint=getTippingPoint(0)):
    try:
        if len(choices) <= 0:
            choices = getInputPalette()

        rgb = np.zeros((h,w,3), 'uint8')

        iCount = 0
        c = (0,0,0)
        colorsKept = {}
        z = 0

        for x in range(0, w-1):
            for y in range(0, h-1):
                q = mod_x(w, h, x, y, z, iCount, len(choices), tippingPoint)

                if isinstance(q, int) or isinstance(q, str):
                    (colorsKept, c, key_used) = get_kept_color(colorsKept, c, choices, q)
                else:                    
                    c = q

                zz = mod_y(w, h, x, y, z, iCount, c, q)

                try:
                    if isinstance(zz, int):
                        rgb[y][x] = zz % 256
                    else:
                        rgb[y][x] = zz
                except Exception as pex:
                    pass

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

def numpy_Fullfill(w=1024, h=1024, iAlg=None):
    """
    p1: iAlg (default=0)<br />
    SUPER: double up/fuzz with iAlg2<br />
    HYPER: triple up/fuzz with iAlg2/iAlg3<br />
    """

    try:
        choices = getInputPalette()
        parmies = getIntParams(iAlg, 0)
        iAlg = parmies[0]

        if iAlg is None:
            iAlg = getRandomFloodFill()

        variant = getParam_Variant()

        bucky_super = getParam_Bucky("SUPER")
        bucky_hyper = getParam_Bucky("HYPER")

        addState(f'iAlg: {iAlg} - {getAlgName(iAlg)}')

        rgb = np.zeros((h, w, 3), dtype=np.uint8)

        newcolour = (0, 0, 0)
        colorsKept = {}

        startx = w // 2
        starty = h // 2

        tippingPoint = getTippingPoint(iAlg)
        switcher = 0
        stackDepth = 1
        timesUsed = {}
        conseq = 0
        last_z = 0
        zCol = []
        mod_alg_value = 0
        fakeI = 0

        # Hot-path locals
        ff = floodFillDetail
        rgb_arr = rgb

        iCount = 0        

        iAlg2 = getRandomFloodFill()

        if bucky_super:
            addState(f'iAlg2: {iAlg2} - {getAlgName(iAlg2)}')

        iAlg3 = getRandomFloodFill()

        if bucky_hyper:
            addState(f'iAlg3: {iAlg3} - {getAlgName(iAlg3)}')

        totalDetailTime = 0

        # Better bounds and cache-friendly order: y outer, x inner
        for y in range(h):
            row = rgb_arr[y]  # local view to cut indexing overhead
            for x in range(w):
                px = row[x]

                if bucky_hyper:
                    iAlgZ = iAlg3 if iCount % 4 == 0 else iAlg if iCount % 2 == 0 else iAlg2
                elif bucky_super:
                    iAlgZ = iAlg if iCount % 2 == 0 else iAlg2
                else:
                    iAlgZ = iAlg

                timeBeforeDetail = time.time()

                newcolour, choices, x2, y2, switcher = ff(
                    iAlgZ, choices, tippingPoint,
                    None, None, w, h, variant,
                    startx, starty, True,
                    iCount, fakeI, switcher,
                    colorsKept, timesUsed, conseq, last_z, zCol,
                    mod_alg_value, None, None,
                    x, y, newcolour, stackDepth
                )

                timeAfterDetail = time.time()
                totalDetailTime += timeAfterDetail-timeBeforeDetail

                # write color
                try:
                    px[:] = newcolour
                except OverflowError:
                    pass

                iCount += 1

        addState(f'totalDetailTime: {round(totalDetailTime, 2)}s')

        sorted_used = sorted(timesUsed.items(), key=lambda x: x[1], reverse=True)
        rootLogger.debug(f'timesUsed: {sorted_used}')

        img = Image.fromarray(rgb)

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

def generateNumpy(mod_x, w=1024, h=768, choices=[], colorsKept={}, roundNum=0):
    rgb = np.zeros((h,w,3), 'uint8')

    if choices == []:
        choices = getInputPalette()

    c = random.choice(choices)

    count = 0

    for x in range(w-1):
        for y in range(h-1):
            z = mod_x(x, y, roundNum, count, len(choices))
            (colorsKept, c, key_used) = get_kept_color(colorsKept, c, choices, z)
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

# DIGEST TURDUS

def build_lexicons(
    a_seeds=DEFAULT_OCCULT_SEEDS,
    b_seeds=DEFAULT_TECH_SEEDS,
    depth=1,
    max_terms=1200
):
    occult = harvest_lemmas_v2(a_seeds, pos="n", depth=depth, max_terms=max_terms)
    tech   = harvest_lemmas_v2(b_seeds, pos="n", depth=depth, max_terms=max_terms)

    # Filter to nice, brandable stems
    def keep(w):
        return (2 <= len(w) <= 11) and re.search(r"[aeiouy]", w)
    
    return sorted(filter(keep, occult)), sorted(filter(keep, tech))

def generate_names(n=20, groupA=None, groupB=None, seed=None):
    if seed is not None:
        random.seed(seed)

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

def lemmas_by_lexfile(lexfile="noun.state", pos="n", lang="en"):
    out = set()

    import wn
    wn.config.allow_multithreading = True
    WN_OBJ = wn.Wordnet("oewn:2024")

    for s in wn.synsets(lexicon="oewn:2024", pos=pos, lang=lang):
        if s.lexfile() == lexfile:
            for l in s.lemmas():
                out.add(l.replace("_", " "))
                
    return sorted(out)

def lexfiles_by_lexicon(lex="oewn:2024"):
    import wn
    wn.config.allow_multithreading = True

    lexfiles = sorted({s.lexfile() for s in wn.synsets(lexicon=lex)})
    return lexfiles

def wordnet_test(word):
    import wn
    wn.config.allow_multithreading = True
    WN_OBJ = wn.Wordnet("oewn:2024")

    for syn in WN_OBJ.synsets(word):
        print(f"\n=== {syn.id} | {syn.lemmas()} ===")

        # See what relation types exist on this synset
        relations = syn.relations()
        if not relations:
            print("  (No relations found)")
        else:
            for rel, targets in relations.items():
                print(f"  {rel}: {[t.lemmas() for t in targets]}")

        # If you want to inspect raw attributes/methods:
        # print(dir(syn))

def wordnet_relations(word):
    import wn
    wn.config.allow_multithreading = True
    WN_OBJ = wn.Wordnet("oewn:2024")

    def lemma_name(l):
        # Handle both Lemma objects and raw strings
        return l.name() if hasattr(l, "name") else str(l)

    def call_list_method(obj, name):
        """Call obj.name() if it exists and is callable; else return []."""
        m = getattr(obj, name, None)
        return m() if callable(m) else []

    out = set()

    for syn in wn.synsets(word):

        # --- Princeton-style methods (use when present) ---
        for rsyn in call_list_method(syn, "hyponyms"):
            out.update((lemma_name(l), "hyponym") for l in rsyn.lemmas())

        for rsyn in call_list_method(syn, "hypernyms"):
            out.update((lemma_name(l), "hypernym") for l in rsyn.lemmas())

        # Meronyms
        for meth in ("part_meronyms", "substance_meronyms", "member_meronyms"):
            for rsyn in call_list_method(syn, meth):
                out.update((lemma_name(l), "meronym") for l in rsyn.lemmas())

        # Holonyms
        for meth in ("part_holonyms", "substance_holonyms", "member_holonyms"):
            for rsyn in call_list_method(syn, meth):
                out.update((lemma_name(l), "holonym") for l in rsyn.lemmas())

        for rsyn in call_list_method(syn, "similar_tos"):
            out.update((lemma_name(l), "similar_to") for l in rsyn.lemmas())

        for rsyn in call_list_method(syn, "also_sees"):
            out.update((lemma_name(l), "also_see") for l in rsyn.lemmas())

        # --- Oewn-style (if exposed) ---
        relmap = {
            "hypo": "hyponym",
            "hyper": "hypernym",
            "mero_part": "meronym",
            "mero_substance": "meronym",
            "mero_member": "meronym",
            "holo_part": "holonym",
            "holo_substance": "holonym",
            "holo_member": "holonym",
            "similar": "similar_to",
            "also": "also_see",
        }

        related = getattr(syn, "related", None)
        if callable(related):
            for key, tag in relmap.items():
                try:
                    for rsyn in related(key):
                        if hasattr(rsyn, "lemmas"):
                            out.update((lemma_name(l), tag) for l in rsyn.lemmas())
                except Exception as e:                    
                    # rootLogger.error(e)
                    pass

    return sorted(out)

def wordGridWordNet(wordline="", fontSize=36, fontPath=""):
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

def wordGridHex_Nyms(wordline="", fontSize=36, fontPath=""):
    eg = lambda: None

    p1 = getParam(0)

    word = getRandomWord() if p1 == "" else p1
    test_lemmas = wordnet_relations(word)
    formatted = [f"<span title='{rel}'>{w.upper()}</span>" for w, rel in test_lemmas]

    return wordGridGeneral(wordline, fontSize, fontPath, eg, word_count=len(formatted), actual_words=formatted, lemmas=[word])

def wordGridHexLatest(wordline="", fontSize=36, fontPath=""):
    # lemmys = lemmas_by_lexfile("noun.time", pos="n", lang="en")

    eg = lambda: None

    p1 = getParam(0)

    word = getRandomWord() if p1 == "" else p1
    test_lemmas = wordnet_test(word)

    if test_lemmas == None:
        test_lemmas = []
        
    #formatted = [f"{w.upper()} - {rel}" for w, rel in test_lemmas]

    return wordGridGeneral(wordline, fontSize, fontPath, eg, word_count=len(test_lemmas), actual_words=test_lemmas, lemmas=[word])

# STEEPER BODYCOUNT

def wordGridHexetidine(wordline="", fontSize=36, fontPath="", input_a=[getRandomWord(), getRandomWord()],input_b=[getRandomWord(), getRandomWord()]):
    """
    p1: preset (<br />
    &nbsp;&nbsp;&nbsp;default/random=0,<br />
    &nbsp;&nbsp;&nbsp;max=19,<br />
    &nbsp;&nbsp;&nbsp;sex=69,<br />
    &nbsp;&nbsp;&nbsp;wn=420
    ),<br />
    p2: depth override (default=2)
    """

    rootLogger.debug(f'SHIFT: {getParam_Bucky("SHIFT")}')

    maxHex = 18

    def eg(word):
        pass

    p1 = getParam(0)
    p1 = int(p1) if p1.isdecimal() else 0

    p2 = getParam(1)
    p2 = int(p2) if p2.isdecimal() else 2

    if p1 == 0:
        p1 = random.randint(1, maxHex)

        addState(f'p1 set to: {p1}', skip_zero=False)

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
    elif p1 == 9:
        input_a = ["synergy","out-of-the-box", "organizing"]
        input_b = ["matrix", "performance", "execution", "management"]
        depth = 2
    elif p1 == 10:
        input_a = ["acre","place","city","hectare"]
        input_b = ["action","job","verb"]
    elif p1 == 11:
        input_a = ["quantum", "neon", "velvet", "static", "whisper"] 
        input_b = ["symphony", "glitch", "obsidian", "murmur", "labyrinth"]
    elif p1 == 12:
        input_a = ["crack","egg","fetus","cosmos"]
        input_b = ["egg","sealed","galaxy","daimon"]
    elif p1 == 13:
        input_a = ["theta","polar","nova","vortex"]
        input_b = ["petal","bloom","ankh","lattice","foam"]
    elif p1 == 14:
        input_a = [    "lattice",    "tessellation",    "waveform",    "diffraction",    "modulus",    "grating",    "array",    "interference",    "operator",    "resonance"]
        input_b = [    "brocade",    "arabesque",    "damask",    "scrollwork",    "paisley",    "filigree",    "mosaic",    "motif",    "embroidery",    "frieze"]
    elif p1 == 15:
        input_a = ["POTPOURRI","MISCELLANEOUS"]
        input_b = ["experiments","abstracts","playground"]
        depth = 3
    elif p1 == 16:
        input_a = ["ENDGAME","START"]
        input_b = ["REWARD","GOAL"]
        depth = 1
    elif p1 == 17:
        input_a = ["SUPER","HYPER","ALT","META","GREEK","FRONT","TOP","COMPUTER"]
        input_b = ["BUCKY","BIT","BYTE","KEY","FLAG"]
        depth = 1
    elif p1 == 18:
        input_a = ["SHIFT", "ADAPT", "REMIX", "MASK", "FIVE", "FORECOLOR", "TUBE"]
        input_b = input_a
        depth = 2
    elif p1 == 19:
        input_a = ["NATIVE","OVERWROUGHT"]
        input_b = ["BLANKET", "PATTERN"]
        depth = 2
    elif p1 == 69:
        input_a = ["sexy","horny","cum","orgasm","clitoris"]
        input_b = ["slut","whore","vagina","pussy","rake","hoe","dominatrix"]
    elif p1 == 420:
        input_a = ["weed","pot","wacky"]
        input_b = ["number","tobacco","gummy","flower"]
    elif p1 == 500:
        input_a = [getRandomWord(),getRandomWord(),getRandomWord()]
        input_b = [getRandomWord(),getRandomWord(),getRandomWord()]
    else:
        input_a = [getRandomWordSpecial("noun"),getRandomWordSpecial("noun")]
        input_b = [getRandomWordSpecial("noun"),getRandomWordSpecial("noun")]

    a, b = build_lexicons(input_a, input_b, depth=depth)
    
    actual_words = []

    for x in range(48):
        ga = random.choice(a)
        gb = random.choice(b)

        z = f'{ga.upper()} {gb.upper()}'

        if p1 == 2:
            z = f'THE {ga.upper()} AND {gb.upper()}'

        actual_words.append(z)
    
    return wordGridGeneral(wordline, fontSize, fontPath, eg, word_count=48, actual_words=actual_words, lemmas=(input_a, input_b), lemma_depth=depth)

def wordGridGetLexfiles(wordline="", fontSize=36, fontPath=""):
    import wn
    wn.config.allow_multithreading = True
    WN_OBJ = wn.Wordnet("oewn:2024")

    lemmas = [getRandomWord()]
    syns = wn.synsets(lemmas[0])

    lexes = [s.lexfile() for s in syns]

    eg = lambda: None

    return wordGridGeneral(wordline, fontSize, fontPath, eg, word_count=len(lexes), actual_words=lexes, lemmas=lemmas)

# BONER MICE

def getAHex(lexa=None, lexb=None):
    global cached_lexicons

    if lexa is None and lexb is None:
        lexa=[getRandomWord(),getRandomWord(),getRandomWord(),getRandomWord()]
        lexb=[getRandomWord(),getRandomWord(),getRandomWord(),getRandomWord()]

        if cached_lexicons is None:
            rootLogger.debug(f'no cached lexicons - building from: {lexa},{lexb}')

            cached_lexicons = dict()
            a, b = build_lexicons(lexa, lexb, depth=10)
            cached_lexicons["a"] = a
            cached_lexicons["b"] = b

            rootLogger.debug(f'lexicon length: a={len(a)},b={len(b)}')
        else:
            a = cached_lexicons["a"]
            b = cached_lexicons["b"]
    else:
        a, b = build_lexicons(lexa, lexb, depth=10)

    banlist = set(["NEGROID","BLACKPERSON"]) # whoopsie doodle
    a = [x for x in a if x not in banlist]
    b = [x for x in b if x not in banlist]

    ga = random.choice(a)
    gb = random.choice(b)

    stringy = f'{ga.upper()} {gb.upper()}'
    addState("hex: " + stringy)

    return stringy

def metatronsCube(skipFF=0):
    """
    Draws Metatron's Cube:<br />
      - 13 points on a hex lattice (center, inner ring, outer ring)<br />
      - Lines between every pair of points (complete graph on 13 vertices)<br />
      - A circle centered on each point (radius = lattice spacing)<br />
    """
    try:
        width  = getCurrentStandardWidth()
        height = getCurrentStandardHeight()

        img  = Image.new("RGBA", (width, height), (0,0,0,0))        

        choices = getInputPalette()
        iAlg = getRandomFloodFill()

        bucky_legacy = getParam_Bucky("LEGACY")

        if bucky_legacy:
            skipFF = 1

        if skipFF != 1:
            img = numpy_Fullfill(width, height, iAlg)
        
        draw = ImageDraw.Draw(img, "RGBA")

        # --- layout ---------------------------------------------------------
        cx, cy = width * 0.5, height * 0.5

        # lattice spacing (distance between adjacent inner-ring centers)
        a = min(width, height) * 0.166

        # line widths
        w_main  = max(1, int(min(width, height) * 0.004))
        w_glow  = max(1, int(w_main * 2.2))

        # colors (soft glow + crisp stroke). swap these to taste / palette.
        col_glow = random.choice(choices)
        col_glow = (*col_glow, 64)
        
        col_line = random.choice(choices)
        
        col_circ = random.choice(choices)
        col_circ = (*col_circ, 200)

        # 6 directions (hex) in radians
        angles = [k * (math.pi/3.0) for k in range(6)]

        # inner and outer ring centers
        inner = [(cx + a*math.cos(t),     cy + a*math.sin(t))     for t in angles]
        outer = [(cx + 2*a*math.cos(t),   cy + 2*a*math.sin(t))   for t in angles]

        # 13 points total
        pts = [(cx, cy)] + inner + outer

        # --- draw complete graph (all pairwise connections) -----------------
        # subtle glow pass
        for i in range(len(pts)):
            for j in range(i+1, len(pts)):
                draw.line((pts[i][0], pts[i][1], pts[j][0], pts[j][1]),
                          fill=col_glow, width=w_glow)
        # crisp pass
        for i in range(len(pts)):
            for j in range(i+1, len(pts)):
                draw.line((pts[i][0], pts[i][1], pts[j][0], pts[j][1]),
                          fill=col_line, width=w_main)

        # --- draw the 13 circles -------------------------------------------
        # Traditionally each circle’s radius equals the lattice spacing.
        R = a
        def circle_bbox(x, y, r):
            return (x - r, y - r, x + r, y + r)

        # circle glow
        for (x, y) in pts:
            draw.ellipse(circle_bbox(x, y, R), outline=col_glow, width=w_glow)

        # circle crisp
        for (x, y) in pts:
            draw.ellipse(circle_bbox(x, y, R), outline=col_circ, width=w_main)

        # optional: outer boundary circle to frame the figure
        # draw.ellipse(circle_bbox(cx, cy, 2.6*a), outline=col_line, width=w_main)

    except Exception as e:
        img = writeImageException(e)

    return img

def zombiesAteMyBrainAlmost(
    count=3,
    color=(0, 255, 85),
    bg=(0, 0, 0),
    scale=0.86,            # overall symbol size vs canvas
    gap_frac=0.035,        # black gap between rings (fraction of current outer radius)
    thick_range=(0.14, 0.22),   # ring thickness as fraction of current outer radius
    offset_range=(0.28, 0.5),  # inner-cut center offset as fraction of current outer radius
    wobble_deg=(-16, 16),       # per-ring rotation range
    seed=None
):
    """
    Draw concentric *randomized* crescent rings.
    - Each inner ring is guaranteed to be fully contained within the previous one.
    - A black gap is preserved between rings.
    - Per-ring crescent offset & rotation are randomized for organic variation.
    """
    try:
        if seed is not None:
            rnd = random.Random(seed)
        else:
            rnd = random

        W = getCurrentStandardWidth()
        H = getCurrentStandardHeight()
        cx, cy = W // 2, H // 2
        R0 = int(min(W, H) * 0.5 * scale)  # outermost radius

        img = Image.new("RGBA", (W, H), (*bg, 255))
        mask_all = Image.new("L", (W, H), 0)

        current_outer = R0
        for i in range(count):
            if current_outer <= 4:
                break  # nothing meaningful left to draw

            # --- choose geometry for this ring ---
            # thickness and gap are fractions of *current* outer radius
            thick_frac = max(0.05, min(0.9, rnd.uniform(*thick_range)))
            gap_px = max(2, int(current_outer * gap_frac))

            r_outer = current_outer
            r_inner = int(r_outer * (rnd.triangular(.8, 1.2, 1) - thick_frac))

            # ensure we still have a green ring after carving the gap for the next ring
            if r_inner - gap_px <= 2:
                # shrink thickness a bit to salvage a small ring
                r_inner = max(2, r_outer - max(2, int(0.12 * r_outer)))

            # max allowable offset that keeps the inner cut well inside the outer disk
            # we subtract a little safety margin (& the upcoming gap) so rings never touch.
            max_offset_px = max(0, (r_outer - r_inner) - gap_px // 2)
            if max_offset_px <= 0:
                break
            # map offset_range (fractions) into [0 .. max_offset_px]
            off_px = int(min(max_offset_px, rnd.uniform(*offset_range) * r_outer))

            # --- build this crescent mask ---
            m = Image.new("L", (W, H), 0)
            d = ImageDraw.Draw(m)

            # outer disk
            bbox_o = (cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer)
            d.ellipse(bbox_o, fill=255)

            # inner cut disk (offset to one side to create a crescent)
            # offset first along +x; we’ll rotate the whole ring afterward
            bbox_i = (cx - r_inner + off_px, cy - r_inner, cx + r_inner + off_px, cy + r_inner)
            d.ellipse(bbox_i, fill=0)

            # random “wobble” rotation so each ring tilts a bit
            rot = rnd.uniform(*wobble_deg)
            m = m.rotate(rot, resample=Image.BICUBIC, center=(cx, cy), expand=False)

            # composite into the global mask (lighter = OR for masks)
            mask_all = ImageChops.lighter(mask_all, m)

            # update available radius for the next ring so there’s a guaranteed black gap
            current_outer = r_inner - gap_px

        # paint crescents onto background
        paint = Image.new("RGBA", (W, H), (*color, 255))
        img = Image.composite(paint, img, mask_all)

    except Exception as e:
        img = writeImageException(e)

    return img

def zombiesAteMyBrain(
    scale=0.86,                 # overall size vs canvas
    n_rings=2,                  # number of annuli between outer disk & inner disk
    min_gap_frac=0.07,          # guaranteed green gap as a fraction of R0
    jitter_frac=0.444,           # max center offset allowed (fraction of ring thickness)
    rng_seed=None               # for reproducibility
):
    """
    Concentric logo with gentle 'organic' offsets on each inner carve.<br />
    <br />
    Guarantees:<br />
      - Every inner carve stays *inside* its parent ring (no break-through).<br />
      - A green gap is always left between features.<br />
    <br />
    Notes:<br />
      - Outer disk is centered.<br />
      - Each ring is drawn centered, then its *inner hole* is carved at a small offset.<br />
      - Final inner solid disk is also offset a bit.<br />
    """

    try:
        if rng_seed is not None:
            random.seed(rng_seed)

        W = getCurrentStandardWidth()
        H = getCurrentStandardHeight()
        cx, cy = W // 2, H // 2
        R0 = int(min(W, H) * 0.5 * scale)   # radius of the outermost circle

        choices = getInputPalette(generate=False, noneIfNoInput=True)

        bg=(0, 255, 64)             # bright green background
        ring=(16, 84, 32)           # dark green rings

        if choices and len(choices) > 0:
            bg = random.choice(choices)
            available = [c for c in choices if c != bg]

            if not available or len(available) == 0:
                available = choices

            ring = random.choice(available)

        # canvas (green background) + working layer for dark parts
        canvas = Image.new("RGBA", (W, H), (*bg, 255))
        layer  = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw   = ImageDraw.Draw(layer)

        # 1) Outer disk (dark)
        draw.ellipse((cx - R0, cy - R0, cx + R0, cy + R0), fill=ring)

        # 2) Build a descending set of radii for rings + inner disk
        #    Split the radial space into (n_rings + 1) segments: [ring, ring, ..., inner disk]
        gap_px  = max(1, int(R0 * min_gap_frac))
        radius  = R0 - gap_px  # leave initial green rim
        rings   = []

        # Generate n_rings annuli with decreasing thickness
        for i in range(n_rings):
            # thickness tapers toward the center
            base_thick = max(6, int((R0 * 0.22) * (0.85 ** i)))
            thick      = min(base_thick, radius - 2 * gap_px)
            if thick <= 3: break

            r_out = radius
            r_in  = r_out - thick
            rings.append((r_out, r_in))
            radius = r_in - gap_px  # leave a green gap before the next feature
            if radius <= 8:
                break

        # inner solid disk
        inner_r = max(4, radius)

        # Helper: constrained random offset that keeps the inner carve inside the outer circle
        def safe_offset(r_out, r_in):
            thick = r_out - r_in
            # how far we *could* move the inner carve without touching the outer boundary:
            max_allow = max(0, thick - gap_px)
            # allow only a fraction of that (smoother look)
            dmax = int(max_allow * jitter_frac)
            if dmax <= 0:
                return 0, 0
            # random small offset
            dx = random.randint(-dmax, dmax)
            dy = random.randint(-dmax, dmax)
            # clip to circle so the *farthest* inner edge remains inside r_out - gap_px
            if dx or dy:
                # effective radius margin
                limit = max(0.0, (r_out - gap_px) - r_in)
                mag = math.hypot(dx, dy)
                if mag > limit and mag > 0:
                    scale = limit / mag
                    dx, dy = int(dx * scale), int(dy * scale)
            return dx, dy

        # 3) Draw rings: centered fill, then offset carve for inner hole
        for (r_out, r_in) in rings:
            # draw the ring as a solid disk first
            draw.ellipse((cx - r_out, cy - r_out, cx + r_out, cy + r_out), fill=ring)
            # carve the hole with a small offset to create the organic asymmetry
            dx, dy = safe_offset(r_out, r_in)
            draw.ellipse((cx + dx - r_in, cy + dy - r_in, cx + dx + r_in, cy + dy + r_in),
                         fill=(0, 0, 0, 0))

        # 4) Inner solid disk, also slightly offset (but keep a gap from the last ring)
        dx_i, dy_i = safe_offset(inner_r + gap_px + 4, inner_r)  # use a looser bound
        draw.ellipse((cx + dx_i - inner_r, cy + dy_i - inner_r,
                      cx + dx_i + inner_r, cy + dy_i + inner_r),
                     fill=ring)

        # composite dark layer over the green canvas
        out = Image.alpha_composite(canvas.convert("RGBA"), layer)

    except Exception as e:
        out = writeImageException(e)

    return out

def zamb_logo_grid(cell_size=-1, seed=None):
    """
    Make a grid of concentric-green logos, each randomized.<br />
    <br />
    n_cols, n_rows : how many across and down<br />
    cell_size      : size of each logo in pixels<br />
    seed           : optional random seed<br />
    """
    try:
        if seed is not None:
            random.seed(seed)

        n_cols = random.randint(2, 8)
        n_rows = n_cols

        if cell_size == -1:
            cell_size = random.choice([100,125,150,200,250])

        # output canvas
        W, H = n_cols * cell_size, n_rows * cell_size
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))

        for row in range(n_rows):
            for col in range(n_cols):
                # make a randomized logo
                img = zombiesAteMyBrain(
                    rng_seed=random.randint(0, 1_000_000),
                    n_rings=random.randint(2, 3),    # vary number of rings
                    jitter_frac=random.uniform(0.35, 0.5), # vary wobbliness
                )

                # resize it to fit the cell
                img = img.resize((cell_size, cell_size), Image.LANCZOS)

                # paste in grid position
                x, y = col * cell_size, row * cell_size
                canvas.paste(img, (x, y))

    except Exception as e:
        canvas = writeImageException(e)

    return canvas

def fig_to_pillow(fig) -> Image.Image:
    canvas = FigureCanvas(fig)
    canvas.draw()
    buf = canvas.buffer_rgba()          # already RGBA
    img = Image.frombuffer('RGBA', fig.canvas.get_width_height(), buf, 'raw', 'RGBA', 0, 1)
    plt.close(fig)

    return img

def matplotlibHelloWorld():
    fig, ax = plt.subplots()
    ax.set_title("hello, agg")
    
    #ax.set_facecolor("#00ff00")

    ax.plot([1, 2, 3, 4], color="#789878")
    ax.set_ylabel('some numbers')
    
    img = fig_to_pillow(fig)

    return img

def field_to_image(W=getCurrentStandardWidth(), H=getCurrentStandardHeight(), cmap_name=None):
    try:
        if cmap_name is None:
            cmap_name = random.choice(['viridis', 'plasma', 'inferno', 'magma', 'cividis', 
                                    'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                                    'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                                    'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',
                                    'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone',
                                    'pink', 'spring', 'summer', 'autumn', 'winter', 'cool',
                                    'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper',
                                    'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu',
                                    'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic',
                                    'berlin', 'managua', 'vanimo',
                                    'twilight', 'twilight_shifted', 'hsv',
                                    'Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2',
                                    'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b','tab20c',
                                    'flag', 'prism', 'ocean', 'gist_earth', 'terrain',
                                    'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap',
                                    'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet',
                                    'turbo', 'nipy_spectral', 'gist_ncar'])

        bucky_ignore = getParam_Bucky("PALIGNORE")

        if bucky_ignore:
            addState(f'cmap_name: {cmap_name}')

        x = np.linspace(-3, 3, W)
        y = np.linspace(-3, 3, H)
        X, Y = np.meshgrid(x, y)

        p2 = getParam(1)

        zonk = {
            # 1. Concentric waves
            "radial_sine": lambda X, Y: np.sin(np.sqrt(X**2 + Y**2)),

            # 2. Spiral
            "spiral": lambda X, Y: np.sin(np.sqrt(X**2 + Y**2) + 5*np.arctan2(Y, X)),

            # 3. Lissajous interference
            "lissajous": lambda X, Y: np.sin(3*X) + np.cos(5*Y),

            # 4. Checkerboard / moiré
            "checker": lambda X, Y: np.sin(5*X) * np.sin(5*Y),

            # 5. Polar rose
            "rose": lambda X, Y: np.sin(6*np.arctan2(Y, X)) * np.cos(np.sqrt(X**2 + Y**2)),

            # 6. Gamma-style warp
            "gamma_warp": lambda X, Y: np.sin(np.log1p(X**2)) * np.cos(np.log1p(Y**2)),

            # 7. Cross interference
            "cross": lambda X, Y: np.sin(X*Y) * np.cos(X-Y),

            # 8. Ripple grid
            "ripples": lambda X, Y: np.sin(X**2 - Y**2) * np.cos(0.5*X*Y),

            "tan_madness": lambda X, Y: np.tan(np.sin(X) * np.cos(Y)),

            # 10. Nested sine/cosine
            "nested": lambda X, Y: np.sin(np.cos(3*X) + np.sin(3*Y)),

            "standard": lambda X, Y: np.sin(X**2 + Y**2) * np.cos(2*X) * np.sin(2.3*Y)
        }

        zonklist = list(zonk.keys())

        if p2 != "" and p2 in zonklist:
            Zz = p2
        else:
            Zz = random.choice(zonklist)

        Z = zonk[Zz](X, Y)

        rootLogger.debug(Z)

        addState(f'alg: {Zz}')

        choices = getInputPalette()

        random.shuffle(choices)

        norm = colors.Normalize(vmin=Z.min(), vmax=Z.max())

        if bucky_ignore:
            cmap = matplotlib.colormaps[cmap_name]
        else:
            my_rgbs = [rgb_to_hex(x) for x in choices]

            cmap = matplotlib.colors.ListedColormap(my_rgbs, name='my_colormap_name')
        
        rgba = (cmap(norm(Z)) * 255).astype("uint8")

        img = Image.fromarray(rgba)
    
    except Exception as e:
        img = writeImageException(e)

    return img

def polar_lissajous():
    fig, ax = plt.subplots(subplot_kw={"projection":"polar"}, figsize=(4,4), dpi=300)
    
    t = np.linspace(0, 2*np.pi, 4000)
    r = 1 + 0.35*np.sin(7*t) + 0.25*np.cos(5*t)
    ax.plot(t, r, linewidth=1.0, color="#ff0000")
    ax.set_axis_off()

    return fig_to_pillow(fig)

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
    ('flagship', {'f': flagship, 'it':'scratch', 'ot':'img', 'ff': 1, 'ess': 1}),
    ('dots', {'f':dots, 'it':'scratch', 'ot':'img', 'ff': 0, 'ess': 1}),
    ('dotsDos', {'f':dotsDos, 'it':'scratch', 'ot':'img'}),
    ('dots_palette', {'f':dots_palette, 'it':'scratch', 'ot':'img', 'ff':0, 'ess': 0}),
    ('boxabyss', {'f':boxabyss, 'it':'scratch', 'ot':'img'}),
    ('patoot', patoot),
    ('ihavenoidea', {'f':ihavenoidea, 'it':'scratch', 'ot':'img', 'ff': 1}),
    ('orangeblock', {'f':orangeblock, 'it':'walk', 'ot': 'img'}),
    ('simplePublic', {'f':simplePublic, 'it':'walk', 'ot': 'img', 'ess': 1}),
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
    ('gritty', {'f':gritty, 'ot':'img', 'ess': 1}),
    ('grittyer', grittyer),
    ('grittyerest', {'f':grittyerest, 'ot':'img', 'ess':0}),
    ('bored', bored),
    ('catalinaimagemixer', catalinaimagemixer),
    ('smellycatalina', {'f': smellycatalina, 'ot':'img', 'ess': 1}),
    ('textalinaimagemixer', textalinaimagemixer),
    ('roundPaste', {'f':roundPaste, 'it':'func', 'ot':'img', 'ff': 0, 'ess':0}),
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
    ('textGen', {'f':textGen, 'it':'scratch', 'ot':'img', 'ff': 0, 'ess': 1}),
    ('textGen2', textGen2),
    ('textGenScatter', textGenScatter),
    ('imageWithText', imageWithText),
    ('colorizerize', colorizerize),
    ('grandradiant', {'f':grandradiant, 'it':'scratch', 'ot':'img'}),
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
    ('bigSquareGrid_remixed', bigSquareGrid_remixed),
    ('bigGridFilled', bigGridFilled),
    ('insert_18', insert_18),
    ('insertFoured', {'f':insertFoured, 'ot':'img', 'ff':0, 'ess':1}),
    ('insertStreaks', insertStreaks),
    ('insertStreaksAdapt', insertStreaksAdapt),
    ('insertStreaksCoco', insertStreaksCoco),
    ('insertStreaksPublic', insertStreaksPublic),
    ('parboil', parboil),
    ('realspiral', realspiral),
    ('adaptSpiral', adaptSpiral),
    ('DEADNIGHTSKY', DEADNIGHTSKY),
    ('generateQRCode', generateQRCode),
    ('grid_18', {'f':grid_18, 'it':'scratch', 'ot':'img', 'ff':1}),
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
    ('randoFill_Public', {'f':randoFill_Public, 'ot':'img', 'ff': 1, 'ess': 1}),
    ('vaporwave1', vaporwave1),
    ('vaporwave2', vaporwave2),
    ('vaporwave2By4', vaporwave2By4),
    ('wordsquares', wordsquares),
    ('vaporSquares', vaporSquares),
    ('wordGrid', wordGrid),
    ('wordGrid2', {'f':wordGrid2, 'ot':'img', 'ess': 1}),
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
    ('wordGridHexetidine', {'f':wordGridHexetidine, 'ot':'txt', 'ess': 1}),
    ('wordGridHexLatest', {'f':wordGridHexLatest, 'ot':'txt'}),
    ('wordGridHex_Nyms', {'f':wordGridHex_Nyms, 'ot':'txt'}),
    ('wordGridGetLexfiles', {'f':wordGridGetLexfiles, 'ot':'txt'}),
    ('slightlyDiffSquares', slightlyDiffSquares),
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
    ('hsvEnum', hsvEnum),
    ('longWordList', longWordList),
    ('longWordList_Sorted', longWordList_Sorted),
    ('Favs30', Favs30),
    ('muchoLetters', muchoLetters),
    ('typewriterStuff', typewriterStuff),
    ('gradientSquares', gradientSquares),    
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
    ('rose', {'f': rose, 'it':'scratch', 'ot':'img', 'ff': 1, 'ess': 1}),
    ('spirograph', {'f':spirograph, 'it':'scratch', 'ot':'img', 'ff': 1}),
    ('flow_ribbons', {'f':flow_ribbons, 'it':'scratch', 'ot':'img', 'ff':0, 'ess':0}),
    ('phyllotaxis', {'f':phyllotaxis, 'it':'scratch', 'ot':'img', 'ff':0, 'ess':0}),
    ('voronoiMosaic', {'f':voronoiMosaic, 'it':'scratch', 'ot':'img', 'ff':0, 'ess':0}),
    ('waveInterference', {'f':waveInterference, 'it':'scratch', 'ot':'img', 'ff':0, 'ess':0}),
    ('truchetTiles', {'f':truchetTiles, 'it':'scratch', 'ot':'img', 'ff':0, 'ess':0}),
    ('touchéTiles', {'f':touchéTiles, 'it':'scratch', 'ot':'img', 'ff':0, 'ess':0}),
    ('interferenceGrids', {'f':interferenceGrids, 'it':'scratch', 'ot':'img', 'ff':0, 'ess':0}),
    ('orbitSwarms', {'f':orbitSwarms, 'it':'scratch', 'ot':'img', 'ff':0, 'ess': 0}),
    ('orbitSwarmsOnInterferonGrids', {'f':orbitSwarmsOnInterferonGrids, 'it':'scratch', 'ot':'img', 'ff':0, 'ess': 0}),
    ('orbitInterferenceHybrid', {'f':orbitInterferenceHybrid, 'it':'scratch', 'ot':'img', 'ff':0, 'ess': 0}),
    ('astrologyTable', astrologyTable),
    ('neobored', neobored),
    ('triangleNonSys', triangleNonSys),
    ('radioFill', radioFill),
    ('radioFillMixed', radioFillMixed),
    ('radioFillMixedPalette', {'f':radioFillMixedPalette, 'it':'insert', 'ot':'img', 'ff':1, 'ess':0}),
    ('radioFillWords', radioFillWords),
    ('radioFill_blend', radioFill_blend),
    ('radioFill_stamp', {'f':radioFill_stamp, 'ot':'img', 'ff': 1, 'ess': 1}),
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
    ('effect_mandelbrot_anim', {'f':effect_mandelbrot_anim, 'ot':'img'}),
    ('fullFill', {'f':fullFill, 'ot':'img', 'ff':1, 'ess': 1}),
    ('fullFillLatest', fullFillLatest),
    ('fullfillBlend2', {'f':fullfillBlend2, 'ot':'img', 'ff':1}),
    ('fullFillStamp', fullFillStamp),
    ('fullFillVariants', {'f':fullFillVariants, 'ot':'img', 'ff': 1, 'ess': 1}),
    ('numpy_Fullfill', {'f':numpy_Fullfill, 'ot':'img', 'ff': 2, 'ess': 1}),
    ('screenshotFill', screenshotFill),
    ('surrealColors', {'f':surrealColors, 'it':'scratch', 'ot':'img', 'ff':0}),
    ('surrealPatterns', surrealPatterns),
    ('garlicItUp', garlicItUp),
    ('vhsDouble', vhsDouble),
    ('wordfilled', {'f':wordfilled, 'it':'scratch', 'ot':'img', 'ff':1, 'ess': 1}),
    ('wordfilled_any', wordfilled_any),
    ('wordfilled_mult', {'f':wordfilled_mult, 'it':'scratch', 'ot':'img', 'ff':1, 'ess':1}),
    ('newgrid', newgrid),
    ('gptsNewDots', {'f': gptsNewDots, 'it':'scratch', 'ot':'img', 'ff':0}),
    ('fullGradient', fullGradient),    
    ('diagonal4Way', diagonal4Way),
    ('diagonalXWay', {'f':diagonalXWay, 'ot':'img','ff':1}),
    ('sigilGrid', sigilGrid),
    ('gradient_mosaic', {'f':gradient_mosaic, 'ot':'img'}),
    ('single_gradient', {'f':single_gradient, 'ot':'img', 'it':'scratch', 'ff': 0}),
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
    ('metatronsCube', {'f':metatronsCube, 'it':'scratch', 'ot':'img' }),
    ('zombiesAteMyBrain', {'f':zombiesAteMyBrain, 'it':'scratch', 'ot':'img'}),
    ('zamb_logo_grid', {'f':zamb_logo_grid, 'it':'scratch', 'ot':'img'}),
    ('matplotlibHelloWorld', {'f':matplotlibHelloWorld}),
    ('field_to_image', {'f':field_to_image}),
    ('polar_lissajous', {'f':polar_lissajous}),
    ('generatePalette', generatePalette),
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
    
    resetChosenPalette100()

    imageExtensions = ["png","gif","jpg","tif"]

    input_palette = processPalette(palette)
    frm = "PNG"
    extension = ".png"
    timeOutLength = timeOutDefault

    uid = str(uuid.uuid4())

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
            
            if uid:
                writeToDisk(blob, "./savedExports/" + uid + extension, extension)

            return (blob, frm)
    
    if imgtype == "floodSample":
        blob = floodSample(palette)
        writeToDisk(blob, "./imagesExported/floodSample.png")
        if uid:
            writeToDisk(blob, "./savedExports/" + uid + extension, extension)
        return (blob, frm)
    if imgtype == "stampSample":
        blob = stampSample()
        writeToDisk(blob, "./imagesExported/stampSample.png")
        if uid:
            writeToDisk(blob, "./savedExports/" + uid + extension, extension)
        return (blob, frm)
    if imgtype == "paletteSample":        
        blob = paletteSample()
        writeToDisk(blob, "./imagesExported/paletteSample.png")
        if uid:
            writeToDisk(blob, "./savedExports/" + uid + extension, extension)
        return (blob, frm)
    
    rootLogger.warning("Couldn't find type: " + imgtype)
    
    blob = Image.new("RGBA", (250,75), "#ffffff")
    blobDraw = ImageDraw.Draw(blob)
    blobDraw.text((5, 60), "Couldn't find type: " + imgtype, font=fonError, fill=(255, 0, 0, 255))
    
    return (blob, frm)

def get_time_class(run):
    try:
        if float(run) > 5:
            return "tdl-img-slow"
        elif float(run) > 2:
            return "tdl-img-norm"
        else:
            return "tdl-img-fast"
    except ValueError:
        return "tdl-img-norm"

    return "tdl-img-norm"

def make_list_item(
    func, 
    link_class, 
    disp, 
    last_run, 
    use_ess=False,
    imageopPrnt="", palettePrnt="", param1Prnt="", param2Prnt="", 
    compfuncPrnt="", param3Prnt="", paramfontPrnt="", insertSourcePrnt="", 
    paramFloodBoxesPrnt="", param4Prnt="",
    buckyBitsPrnt = ""
):    
    href = (f"/tdl?imgtype={func}{imageopPrnt}{palettePrnt}{param1Prnt}{param2Prnt}"
            f"{compfuncPrnt}{param3Prnt}{paramfontPrnt}{insertSourcePrnt}"
            f"{paramFloodBoxesPrnt}{param4Prnt}{buckyBitsPrnt}")
    return (
        f'<li data-func="{func}" class="{"tdl-ess" if use_ess else "tdl-normal"}">'
        f'<a class="{link_class}" href="{href}">{disp}</a> '
        f'<div class="tdl-imgtype {get_time_class(last_run)}">{last_run}s</div></li>'
    )

def writehtml(basey):
    (imgtype, imgpath, word, imageop, palette) = [basey.imgtype, basey.imgpath, basey.word, basey.imageop, basey.palette]

    tdlTitle = getTDL()

    try:
        imgtypeFunc = globals()[imgtype]
        wrapperData["function_states"]["0"] = manager.list()
    except KeyError:
        imgtype = "flagship"
        imgtypeFunc = globals()[imgtype]

    global functionDocs
    doccy = imgtypeFunc.__doc__

    palette_classes = get_palettelist_classifications_dict()

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
    <link rel="stylesheet" href="/palettecss">

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="https://code.jquery.com/ui/1.12.0/jquery-ui.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.1/p5.min.js" integrity="sha512-jLPBEs8Tcpbj4AlLISWG0l7MbuIqp1cFBilrsy0BhvNUa0BLB4wVQeoL+93OYOdENFPKLOgrzb1Nytn+5N5y7g==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.1/addons/p5.sound.min.js" integrity="sha512-WzkwpdWEMAY/W8WvP9KS2/VI6zkgejR4/KTxTl4qHx0utqeyVE0JY+S1DlMuxDChC7x0oXtk/ESji6a0lP/Tdg==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>

    <link href="https://cdn.jsdelivr.net/npm/choices.js/public/assets/styles/choices.min.css" rel="stylesheet"/>
    <script src="https://cdn.jsdelivr.net/npm/choices.js/public/assets/scripts/choices.min.js"></script>

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
            <button onclick="toggleEss()" class="btn-toggle" title="Toggle Essential">⭐</button>
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
    param4 = ""
    param4Prnt = ""
    buckyBits = ""
    buckyBitsPrnt = ""

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

        if len(extParams) > 7:
            param4 = extParams[7]

        if len(extParams) > 8:
            buckyBits = extParams[8]
    
    doTimeCheck(f"writehtml: param1: {param1}, cond: {param2!=''}, param2: {param2}, param3: {param3}, compfunc: {compfunc}, param4: {param4}, buckyBits: {buckyBits}")
    
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

    if param4 != "" and param4 != "false" and param4 != "False":
        param4Prnt = "&param4=" + param4

    if buckyBits != "" and buckyBits != 0 and buckyBits != "0":
        buckyBitsPrnt = "&buckyBits=" + buckyBits

    breakpoint = 10 # (len(tdlTypes) + 4) // 5

    body += '<ul class="imgtypes-list">'

    inputType = ""
    outputType = ""

    hr_separator = '<hr class="tdl_sep" />'

    iType = 0    
    for tdl in tdlTypes:
        if iType % breakpoint == 0 and iType > 0:
            body += hr_separator
        
        inputTypeMilk = "unk"
        outputTypeMilk = "img"
        usesFF = 0
        usesEssential = 0

        alice = tdlTypes[tdl]
        if isinstance(alice, dict):
            if "it" in alice:
                inputTypeMilk = alice["it"]
            if "ot" in alice:
                outputTypeMilk = alice["ot"]
            if "ff" in alice:
                usesFF = alice["ff"]
            if "ess" in alice:
                usesEssential = alice["ess"]
        
        isSelImgType = "tdl_imgtype active" if imgtype == tdl else "tdl_imgtype"

        if inputTypeMilk != "":
            isSelImgType += " tdl-input-" + inputTypeMilk

        if outputTypeMilk != "":
            isSelImgType += " tdl-output-" + outputTypeMilk

        iconFF = ' <span title="Uses floodfill">🚰</span>'
        iconEssential = ' <span title="Essential function">⭐</span>'

        tdlDisp = f"{tdl}{iconFF if usesFF > 0 else ''}{iconEssential if usesEssential > 0 else ''}"

        try:
            last_run = telemetry['execution']['last_exec_time'][tdl]
        except KeyError as ke:
            last_run = "N/A"

        body += make_list_item(
            tdl,
            isSelImgType,
            tdlDisp,
            last_run,
            use_ess=(usesEssential > 0),
            imageopPrnt=imageopPrnt, palettePrnt=palettePrnt, 
            param1Prnt=param1Prnt, param2Prnt=param2Prnt, 
            compfuncPrnt=compfuncPrnt, param3Prnt=param3Prnt, 
            paramfontPrnt=paramfontPrnt, insertSourcePrnt=insertSourcePrnt, 
            paramFloodBoxesPrnt=paramFloodBoxesPrnt, param4Prnt=param4Prnt,
            buckyBitsPrnt=buckyBitsPrnt
        )

        iType += 1

        if tdl == imgtype:
            outputType = outputTypeMilk

    body += hr_separator

    for xxop in ["paletteSample", "floodSample", "stampSample"]:
        isSelImgType = "tdl_imgtype active" if imgtype == xxop else "tdl_imgtype"
        
        usesFF = 0
        usesEssential = 1

        try:
            last_run = telemetry['execution']['last_exec_time'][xxop]
        except KeyError as ke:
            last_run = "N/A"

        body += make_list_item(
            xxop,
            isSelImgType,
            f"{xxop}{iconFF if usesFF > 0 else ''}{iconEssential if usesEssential > 0 else ''}",
            last_run,
            use_ess=True,
            imageopPrnt=imageopPrnt, palettePrnt=palettePrnt,
            param1Prnt=param1Prnt, param2Prnt=param2Prnt,
            compfuncPrnt=compfuncPrnt, param3Prnt=param3Prnt,
            paramfontPrnt=paramfontPrnt, insertSourcePrnt=insertSourcePrnt,
            paramFloodBoxesPrnt=paramFloodBoxesPrnt, param4Prnt=param4Prnt,
            buckyBitsPrnt=buckyBitsPrnt
        )
    
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

    body += "<div class='container-reload'><input type=\"button\" onclick=\"location.reload()\" value=\"Reload\"></input>"
    body += f'<div class="container-down"><button type="button" onclick="scrollBelowImage()">Down</button></div></div>'

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

        apiAction = f'/apiimg?func=img&t={str(time.time())}{imgTypePrnt}{imgPathPrnt}{wordPrnt}{imageopPrnt}{palettePrnt}{param1Prnt}{param2Prnt}{param3Prnt}{compfuncPrnt}{paramfontPrnt}{insertSourcePrnt}{paramFloodBoxesPrnt}{param4Prnt}{buckyBitsPrnt}'

        body += '<script type="text/javascript">'
        body += 'apiURL = "' + apiAction + '";'
        body += '</script>'

        body += '<img id=\"output-img\" class=\"output-img\" src=\"/nowLoading.png\" download=\"workit\" />'
        #body += '<img src="/img?func=img&t=' + str(time.time()) + imgTypePrnt + imgPathPrnt + wordPrnt + imageopPrnt + palettePrnt + param1Prnt + param2Prnt + param3Prnt + compfunc + paramfontPrnt + insertSourcePrnt + paramFloodBoxesPrnt + '&suggname=' + suggname + '">'   
        
        body += '</div>'
    elif outputType == "txt":
        resultHere = imgtypeFunc()
        body += '<div id="result-container" class="result-container" data-t="' + str(time.time()) + '">' + resultHere + '</div>'

        global currentUID

        if currentUID in wrapperData["function_states"]:
            zink = wrapperData["function_states"][currentUID]        

            for z in zink:
            #    function_states.append(z)                
                colorPrint.print_custom_palette(191, z)
    elif outputType == "p5":
        resultHere = imgtypeFunc()
        body += '<div id="result-container" class="result-container" data-t="' + str(time.time()) + '">' + resultHere + '</div>'
    else:
        # NOOP
        pass
    
    if doccy is None:
        doccy = ""    

    body += '<div id=\"sacred-output\" class=\"sacred-output sacred-output-main\">'
    body += f'<div id=\"sacred-output-palette\"><table id=\"palette-table\"><caption id=\"palette-caption\"></caption></table><div id=\"sacred-palette-hex\"></div></div>'

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

        body += "palette: <select id=\"palette\" name=\"palette\" onchange=\"setQS_palette(this.value, this);\" class=\"js-choice\">"
        body += "<option> </option>"

        for iop in palettelist:
            entry, dom = palette_classes[iop[0]]

            tags = ""
            if len(iop) > 3:
                tags = iop[3]

            props = {"band": dom, "tags": tags}
            data_cp = html.escape(json.dumps(props))

            body += f'<option id="{iop[0]}" value="{iop[0]}" data-key="{iop[0]}" data-custom-properties="{data_cp}" {"selected" if iop[0] == palette or str(iop[0]) == palette else ""}>{iop[1]}</option>'
            
        body += "</select><br />"

        body += """<button type="button" id="param1-decr">−</button>
                   <button type="button" id="param1-clear">🗑️</button>
                   <button type="button" id="param1-incr">+</button>
                """
        
        body += "param1: <input type=\"text\" id=\"param1\" name=\"param1\" size=\"50\" value=\"" + param1 + "\" />"
        body += "<button id=\"btnGo\" type=\"submit\" onclick=\"goClicked()\">Go</button><br />"

        # TODO: add a describe this image button for Ollama, call api url that accepts base64 input

        body += """<button type="button" id="param2-decr">−</button>
            <button type="button" id="param2-clear">🗑️</button>
            <button type="button" id="param2-incr">+</button>
        """

        body += f'param2: <input type="text" id="param2" name="param2" size="50" value="{param2}" /><br />'

        body += """<button type="button" id="variant-decr">−</button>
            <button type="button" id="variant-clear">🗑️</button>
            <button type="button" id="variant-incr">+</button>
        """
        
        body += f'variant: <input type="text" id="param3" name="param3" size="50" value="{param3}" /><br />'
        body += f'compfunc: <input type="text" id="compfunc" name="compfunc" size="50" value="{compfunc}" /><br />'
        body += f'paramfont: <input type="text" id="paramfont" name="paramfont" size="50" value="{paramfont}" /><br />'
        body += f'insertSource: <input type="number" id="insertSource" name="insertSource" value="{insertSource}" min="0" max="{len(allPaths) - 1}" /><br />'
        body += f'floodBoxes: <input type="checkbox" id="floodBoxes" name="floodBoxes" value="1" {"checked" if paramFloodBoxes in ["True","true","1",1] else ""} /><br />'
        body += f'popLeft: <input type="checkbox" id="param4" name="param4" value="1" {"checked" if param4 in ["True","true","1",1] else ""} /><br />'

        global bucky_labels

        body += f'<fieldset><legend>buckyBits</legend>'
        body += f'<input type="number" id="buckyBits" name="buckyBits" min="0" max="{pow(2,len(bucky_labels)) - 1}" value="{buckyBits}" /><br />'       
        
        body += f'<div id="buckyCheckboxes" class="buckyCheckboxes">'
        for i, label in enumerate(bucky_labels):
            body += f'<label><input type="checkbox" id="bit{i}"> {label}</label><br>'
        body += f'</div></fieldset>'

        body += "<br />"
        body += "<input type=\"text\" id=\"myguid\" size=\"50\" /><input type=\"button\" onclick=\"guidclick()\" value=\"Get a guid\"></input>"
        body += "<div id=\"img-upload-container\" class=\"img-upload-container\"><label>Upload image <input type=\"file\" name=\"uploadimg\" id=\"img-upload\" accept=\"image/png, image/gif, image/jpeg\" /></label>"
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

# EXUDE WEAKPOINT

@app.route('/exif./<path:thing>')
def send_exif_fix(thing):
    return send_exif("./"+thing)

@app.route('/exif/<path:thing>')
def send_exif(thing):
    try:
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
                rootLogger.error(ex)

                zzz[ifd_tag_name] = str(ifd_value)
                errors.append(str(ex))

            print(f" {ifd_tag_name}: {ifd_value}")

        # TODO: return something better

        return {
            "_item": thing,
            "exif": str(exif), 
            "extracted": zzz,
            "errors": errors
        }
    except Exception as e:
        rootLogger.error(e)

        return {
            "_item": thing
        }

def extractQuery():
    defaults = {
        "imgtype": "",
        "imgpath": "",
        "word": "",
        "imageop": "",
        "palette": "",
        "param1": "",
        "param2": "",
        "param3": "",
        "compfunc": "",
        "paramfont": "",
        "insertSource": "0",
        "floodBoxes": "False",
        "param4": "False",
        "buckyBits": "0"
    }

    params = {k: request.args.get(k, v) for k, v in defaults.items()}

    global extParams
    extParams = [
        params["param1"],
        params["param2"],
        params["compfunc"],
        params["paramfont"],
        params["insertSource"],
        params["floodBoxes"],
        params["param3"],
        params["param4"],
        params["buckyBits"]
    ]

    return (
        params["imgtype"],
        params["imgpath"],
        params["word"],
        params["imageop"],
        params["palette"],
        extParams,
    )

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

@app.route('/hex')
def route_hex():
    return getAHex()

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

    gottened = getPaletteFromImageFull(blob, distance=25, limit=10)

    zonketydonketyhonkety = sort_by_sat(gottened[0])[::-1]
    cholos = [rgb_to_hex(x) for x in zonketydonketyhonkety]

    if currentUID in wrapperData["function_states"]:
        zink = wrapperData["function_states"][currentUID]        

        for z in zink:
            function_states.append(z)

    global palette100_chosen
    pal_name = get_palette_name(palette100_chosen)

    choices = getInputPalette()
    choices = [rgb_to_hex(c) for c in choices]

    return {
        "image": img_str.decode('ascii'), 
        "basey": str(basey), 
        "currentUID": currentUID, 
        "inserts_used": inserts_used,
        "function_states": function_states,
        "palette": cholos,
        "rnd_palette_chosen": palette100_chosen,
        "rnd_palette_name": pal_name,
        "zzz_choices": choices
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

@app.route("/palettedata")
def get_palettes_route():
    data = get_palettes()
    return jsonify(data)

def get_palettes():
    data = []
    global palettelist

    for item in palettelist:
        if len(item) == 2:
            pid, pname = item
            palette = getPaletteSpecific(int(pid))

            data.append({"id": pid, "name": pname, "palette": list_rgb_to_hex(palette)})
        elif len(item) == 3:
            pid, pname, pextra = item
            palette = getPaletteSpecific(int(pid))

            data.append({"id": pid, "name": pname, "path": pextra, "palette": list_rgb_to_hex(palette)})
        elif len(item) == 4:
            pid, pname, pextra, ptags = item
            palette = getPaletteSpecific(int(pid))

            data.append({"id": pid, "name": pname, "path": pextra, "palette": list_rgb_to_hex(palette)})
   
    return data

@app.route("/palettecss")
def get_palette_css():
     # serve pure CSS (no <style> tag)
    lines = []
    for p in get_palettes():
        pid = p["id"]
        cols = p.get("palette", ["#ffffff","#ffff00"])

        grad = "linear-gradient(to right, " + ", ".join(cols) + ")"

        # dropdown items (the list Choices renders)
        lines.append(
            f'.choices__list--dropdown .choices__item[data-value="{pid}"]'
            '{background:' + grad + '; color:'+get_best_contrast_color(hex_to_rgb(cols[0]))+'}'
        )

        # selected pill (we toggle a class on the container via JS below)
        lines.append(
            f'.choices.palette-numba-{pid} .choices__inner'
            '{background:' + grad + ';color:#00ff00;'
            'box-shadow:0 0 0 2px #2e7d32 inset}'
        )

    css = "\n".join(lines)

    return Response(css, mimetype='text/css')

@app.route("/buckybits")
def get_bucky_bit_labels():
    global bucky_labels

    return jsonify(bucky_labels)

def main(argv):
    if len(argv) <= 1:
        prep()
        app.run(debug=True, port=5000, threaded=True)        
    else:
        #extractFrames("tt1.mov")
        # to extract audio with ffmpeg: 
        # ffmpeg -i videofile.mp4 -vn -acodec copy audiotrack.m4a
        framesToVideo()

if __name__ == "__main__":
    main(sys.argv)