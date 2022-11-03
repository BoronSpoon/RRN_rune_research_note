from vern import *
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("path")
args = parser.parse_args()
Vern(args.path)