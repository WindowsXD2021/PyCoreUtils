import argparse
import re
import string
import sys


def cat(f, numerate=None, show_tabs=None, show_ends=None, show_noprt=None):
    out = []
    lines = f.readlines()
    for i in range(len(lines)):
        out.append(lines[i])
        if numerate:
            out.insert(i*2, str(i+1)+"  ") if i+1 > 9 else out.insert(i*2, str(i+1)+"   ")
        if show_tabs:
            out[i] = lines[i].replace("    ", "^I").replace("\t", "^I")
        if show_ends:
            out[i] = lines[i].replace("\n", "$\n")
        if show_noprt:
            # https://stackoverflow.com/a/13928029/15395078
            nonprt = re.compile("([^" + re.escape(string.printable) + "])")
            def nonprt_hex(match):
                return r"\x{0:02x}".format(ord(match.group()))
            nonprt.sub(nonprt_hex, out[i])
    return "".join(out)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("FILE", nargs="?", type=str)
    parser.add_argument("-A", "--show-all", help="Show all characters", action="store_true")
    parser.add_argument("-e", "--show-ends", help="Display $ at end of each line", action="store_true")
    parser.add_argument("-T", "--show-tabs", help="Display TAB characters as ^I", action="store_true")
    parser.add_argument("-n", "--number", help="Number all output lines", action="store_true")
    parser.add_argument("-v", "--show-nonprinting", help="Show non-printable characters", action="store_true")
    args = parser.parse_args()
    if args.FILE:
        try:
            f = open(args.FILE, "r", encoding="utf-8", errors="replace")
        except OSError:
            print("cat: error: file not found")
        if args.show_all:
            print(cat(args.FILE, numerate=1, show_ends=1, show_noprt=1, show_tabs=1))
        else:
            print(cat(args.FILE, numerate=args.number, show_ends=args.show_ends, show_noprt=args.show_nonprinting, show_tabs=args.show_tabs))
    else:
        try:
            print(cat(sys.stdin, numerate=args.number, show_ends=args.show_ends, show_noprt=args.show_nonprinting, show_tabs=args.show_tabs))
        except (KeyboardInterrupt, EOFError): # Exit gracefully
            pass

if __name__ == "__main__":
    main()