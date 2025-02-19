import logging

RESET = "\x1b[0m"
COLOR_CODES = {
    'BLACK': "\x1b[30m",
    'RED': "\x1b[31m",
    'GREEN': "\x1b[32m",
    'YELLOW': "\x1b[33m",
    'BLUE': "\x1b[34m",
    'PURPLE': "\x1b[35m",
    'CYAN': "\x1b[36m",
    'WHITE': "\x1b[37m",
    'BOLD': "\x1b[1m",
    'UNDERLINE': "\x1b[4m",
    'REVERSE': "\x1b[7m",
    'BG_BLACK': "\x1b[40m",
    'BG_RED': "\x1b[41m",
    'BG_GREEN': "\x1b[42m",
    'BG_YELLOW': "\x1b[43m",
    'BG_BLUE': "\x1b[44m",
    'BG_PURPLE': "\x1b[45m",
    'BG_CYAN': "\x1b[46m",
    'BG_WHITE': "\x1b[47m",
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        return super().format(record)

handler = logging.StreamHandler()
formatter = ColoredFormatter('%(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)