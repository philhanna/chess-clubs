"""
Entry point for the chess club database creation tool.

This script takes a US Chess Federation (USCF) club ID and optionally an 
output database name to generate a database for the chess club.
"""

import argparse
from .core import main  # Importing the main function from the core module

if __name__ == '__main__':
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Creates a chess club database')
    
    # Required argument: 8-digit USCF club ID
    parser.add_argument('clubid', help='8-digit USCF ID for the chess club')
    
    # Optional argument: output database name (defaults to clubid.db)
    parser.add_argument(
        '-o', '--dbname', 
        help='Output database name (default: clubid.db)'
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # If no database name is provided, default to clubid.db
    if args.dbname is None:
        args.dbname = f"{args.clubid}.db"

    # Call the main function with the provided arguments
    main(args.clubid, args.dbname)
