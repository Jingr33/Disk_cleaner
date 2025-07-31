import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Disk cleaner")
    parser.add_argument("--root", type=str, default=".", help="Root folder of your disk")
    parser.add_argument("--autosim", type=float, help="similarity percentage above which one of the compared files is automatically deleted")
    parser.add_argument("--minsim", type=float, help="the percentage of similarity at which it is necessary to manually compare the similarity of files")
    parser.add_argument("--wavers", type=bool, help="Remove files whose names start with a tilde character")
    parser.add_argument("--clean", type=bool, default=True, help="Remove similar files (based on hashes or content) from your disk")
    parser.add_argument("--names", type=bool, help="Remove files with the same name")
    return parser.parse_args()
