from parser import parse_args
from cleaner import Cleaner

def main():
    args = parse_args()
    Cleaner(args)

if __name__ == "__main__":
    main()