import argparse
import sys

from aytemplar_core.replacer import Replacer

def main():
    parser = argparse.ArgumentParser(description="Do something.")
    parser.add_argument("-i", "--input", type=str, required=True)
    parser.add_argument("-o", "--output", type=str, default=None, required=False)
    parser.add_argument("-b", "--blacklist", type=str, action='append', default=[], required=False)
    parser.add_argument("-w", "--whitelist", type=str, action='append', default=[], required=False)
    args = parser.parse_args(sys.argv[1:])
    replacer : Replacer = Replacer()
    replacer.load(args.input)
    replacer.setBlacklist(args.blacklist)
    replacer.setWhitelist(args.whitelist)
    replacer.replace_from_env()
    replacer.store(args.input if args.output is None else args.output)

if __name__ == "__main__":
    main()