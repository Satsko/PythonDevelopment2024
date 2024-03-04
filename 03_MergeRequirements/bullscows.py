import argparse
import urllib.request
import os

parser = argparse.ArgumentParser()
parser.add_argument('dict', type=str)
parser.add_argument('len', nargs='?', default=5, type=int)
args = parser.parse_args()

if args.dict.startswith("http"):
    with urllib.request.urlopen(args.dict) as response:
        data = response.read().decode("utf-8")
        words = [w for w in filter(lambda w : len(w) == args.len, data.split("\n"))]
else:
    with open(args.dict, "r") as f:
        words = [w.strip() for w in filter(lambda w : len(w.strip()) == args.len, f)]

#print(len(words))


