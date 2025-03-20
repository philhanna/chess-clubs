import argparse
from .core import main

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creates a chess club database')
    parser.add_argument('clubid', help='8-digit USCF ID for the chess club')
    parser.add_argument(
        '-o', '--dbname', help='output database name (default=clubid.db)')
    args = parser.parse_args()
    if args.dbname is None:
        args.dbname = f"{args.clubid}.db"

    main(args.clubid, args.dbname)
