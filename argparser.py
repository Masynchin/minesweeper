from argparse import ArgumentParser


argparser = ArgumentParser(add_help=False)
argparser.add_argument("-w", "--width", type=int, default=12)
argparser.add_argument("-h", "--height", type=int, default=9)
argparser.add_argument("-b", "--bombs-count", type=int, default=10)
argparser.add_argument("--help", action="store_true")
