import logging


def configure_logging(verbose=False):
    console = ColorLog()
    console.setLevel(logging.DEBUG if verbose else logging.WARNING)
    logging.getLogger('').addHandler(console)
    logging.getLogger('').setLevel(logging.DEBUG)


def _wrap_with(code):
    def inner(text, bold=False):
        c = code
        if bold:
            c = "1;%s" % c
        return u"\033[%sm%s\033[0m" % (c, text)

    return inner


red = _wrap_with('31')
green = _wrap_with('32')

yellow = _wrap_with('33')
blue = _wrap_with('34')
magenta = _wrap_with('35')
cyan = _wrap_with('36')
white = _wrap_with('37')


def print_color(color,bold=False):
    def inner(text):
        print(color(text,bold))
    return inner


print_red = print_color(red)
print_red_bold = print_color(red,True)


class ColorLog(logging.Handler):
    """
    A class to print colored messages to stdout
    """
    COLORS = {
        logging.CRITICAL: red,
        logging.ERROR: red,
        logging.WARNING: yellow,
        logging.INFO: green,
        logging.DEBUG: lambda x: x,
    }

    def __init__(self):
        logging.Handler.__init__(self)

    def usesTime(self):
        return False

    def emit(self, record):
        color = self.COLORS.get(record.levelno, lambda x: x)
        print(color(self.format(record)))
        # print(color(record.msg))
