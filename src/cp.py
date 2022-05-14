import argparse
import os
import os.path as ospath


def cp(src, dst, block):
    srcfd = open(src, "rb")
    dstfd = open(dst, "wb")
    while True:
        buf = srcfd.read(block)
        if not buf:
            break
        dstfd.write(buf)

def cp_dir(src, dst, block):
    src = ospath.abspath(src)+"\\"
    dst = ospath.abspath(dst)+"\\"
    os.mkdir(dst)
    for i in os.listdir(src):
        if ospath.isfile(src+i):
            cp(src+i, dst+i, block)
        else:
            cp_dir(src+i, dst+i, block)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("SRC", type=str)
    parser.add_argument("DST", type=str)
    parser.add_argument("-b", "--block-size", help="file block size", type=int, default=1024)
    parser.add_argument("-R", "--recursive", help="recursive copy directories", action="store_true")
    parser.add_argument("-H", "--dereference", help="follow symbolic links", action="store_true")
    args = parser.parse_args()
    if args.SRC and args.DST:
        if args.dereference:
            src = os.readlink(args.SRC)
            if args.recursive:
                cp_dir(src, args.DST, args.block_size)
            else:
                cp(src, args.DST, args.block_size)
        else:
            if args.recursive:
                cp_dir(args.SRC, args.DST, args.block_size)
            else:
                cp(args.SRC, args.DST, args.block_size)

if __name__ == "__main__":
    main()