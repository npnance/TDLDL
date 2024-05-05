import sys

class ColorPrint:
    def __init__(self, logger):
        self.logger = logger    

    @staticmethod
    def print_fail(message, end = '\n'):
        sys.stderr.write('\x1b[1;31m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_pass(message, end = '\n'):
        sys.stdout.write('\x1b[1;32m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_warn(message, end = '\n'):
        sys.stderr.write('\x1b[1;33m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_info(message, end = '\n'):
        sys.stdout.write('\x1b[1;34m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_bold(message, end = '\n'):
        sys.stdout.write('\x1b[1;37m' + message.strip() + '\x1b[0m' + end)

    def logger_whatever(self, message, end = '\n'):
        self.logger.debug('\x1b[1;35m' + message.strip() + '\x1b[0m' + end)

    def logger_info(self, message, end = '\n'):
        self.logger.debug('\x1b[1;34m' + message.strip() + '\x1b[0m' + end)

    def color_test(self):       
        zonk = ''
        for iCT in range(255):
            zonk += f'\x1b[38;5;{iCT}m' + f'color: {iCT}' + '\x1b[0m\t'
            
        self.logger.debug(zonk)

        zonk = ''; r=100; g=0; b=0
        zonk += f'\x1b[38;2;{r};{g};{b}m' + f'rgb: ({r},{g},{b}) \x1b[0m'

        self.logger.debug(zonk)

        return
    
    def print_custom_palette(self, iCP, message):
        zonk = f'\x1b[38;5;{iCP}m' + message + '\x1b[0m'
        self.logger.debug(zonk)

        return zonk        

    def get_custom_rgb(self, message, r=255, g=255, b=255):
        zonk = f'\x1b[38;2;{r};{g};{b}m' + str(message) + '\x1b[0m'
        return zonk

    def print_custom_rgb(self, message, r=255, g=255, b=255):
        zonk = self.get_custom_rgb(message, r, g, b)
        self.logger.debug(zonk)

        return zonk
    
    # emotion = getRandomWordSpecial("positive", "")