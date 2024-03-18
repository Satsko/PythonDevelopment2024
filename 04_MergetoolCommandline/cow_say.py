import argparse
import cowsay

parser = argparse.ArgumentParser()

parser.add_argument("text", nargs="?", type=str, default=" ")
parser.add_argument("-t", action="store_true")
parser.add_argument("-f", dest="cow", type=str, default="default")
parser.add_argument("-e", dest="eyes", type=str, default="--")
parser.add_argument("-T", "--tongue_string", dest="tongue", type=str, default="  ")
parser.add_argument("-n", dest="wrap_text", action="store_true")
parser.add_argument("-W", "--column", dest="width", type=str)
parser.add_argument("-l", action="store_true")
parser.add_argument("-b", action="store_true")
parser.add_argument("-d", action="store_true")
parser.add_argument("-g", action="store_true")
parser.add_argument("-p", action="store_true")
parser.add_argument("-s", action="store_true")
parser.add_argument("-w", action="store_true")
parser.add_argument("-y", action="store_true")

args = parser.parse_args()

if args.l:
    print(cowsay.list_cows())
else:
    print(cowsay.cowsay(message=args.text,
                        cow=args.cow,
                        eyes=args.eyes,
                        tongue=args.tongue,
                        width=args.width,
                        wrap_text=args.wrap_text))
