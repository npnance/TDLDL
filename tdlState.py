import sys

class TdlState:
    def __init__(self, statement):
        self.statement = statement
        pass

    @staticmethod
    def print_test(message, end = '\n'):
        sys.stderr.write('\x1b[1;31mHello Woild\x1b[0m' + end)

    def __str__(self):
        return f"({self.statement})"

    def __repr__(self):
        return object.__repr__(self)
    
class TdlValues:
    def __init__(self, imgtype, imgpath, word, imageop, palette, extParams):
        self.imgtype = imgtype
        self.imgpath = imgpath
        self.word = word
        self.imageop = imageop
        self.palette = palette
        self.extParams = extParams

    def __str__(self):
        return f'imgtype: {self.imgtype}, imgpath: {self.imgpath}, word: {self.word}, imageop: {self.imageop}, palette: {self.palette}, extParams: {self.extParams}'