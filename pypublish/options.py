import getopt
import sys

class Options:
    def __init__(self):
        self.debug = False
        self.args = []

def get_options(args):
    try:
        opts, args = getopt.getopt(args[1:], "",
            ["debug"])
    except getopt.GetoptError as err:
        print(err)
        raise

    options = Options()

    for opt, arg in opts:
        if opt == "--debug":
             options.debug = True

    if options.debug:
        print(opts)
        print(args)

    options.args = args

    return options
