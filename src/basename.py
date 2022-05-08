import argparse


def perform_basename(s:str, suffix=None):
    s = s.rpartition("/")[2].rpartition("\\")[2]
    if suffix:
        s = s.replace(suffix, "")
    return s

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("NAME", type=str)
    parser.add_argument("SUFFIX", nargs="?", type=str)
    args = parser.parse_args()
    print(perform_basename(args.NAME, args.SUFFIX))

if __name__ == "__main__":
    main()