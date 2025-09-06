import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Disk cleaner")
    parser.add_argument("--root", type=str, default="", help="Root folder of your disk")
    parser.add_argument("--wavers", action="store_true", help="Remove files whose names start with a tilde character")
    parser.add_argument("--clean", action="store_true", help="Remove similar files (based on hashes or content) from your disk")
    parser.add_argument("--names", action="store_true", help="Remove files with the same name")
    parser.add_argument("--restore_bin", action="store_true", help="Restore file from a disk bin to their original destinations.")
    return parser.parse_args()
