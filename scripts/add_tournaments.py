#! /usr/bin/python

# ============================================================
# Mainline
# ============================================================
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Program name')
    parser.add_argument('-v', '--version', action='store_true', help='display version number')
    args = parser.parse_args()

