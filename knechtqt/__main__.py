import argparse

from . import KnechtQT

if __name__ == '__main__':

    cli = argparse.ArgumentParser()
    cli.add_argument("-p", "--port", default=60602,
                     type=int, help="port to listen on")
    cli.add_argument("-l", "--listen", default="0.0.0.0",
                     help="ip to listen on")

    args = cli.parse_args()

    knechtqt = KnechtQT(args)

    knechtqt.launch()
