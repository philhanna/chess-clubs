# Make tests a package for pytest to find
import json
import os

thisfile = os.path.abspath(__file__)
thisdir = os.path.dirname(thisfile)
jsonfile = os.path.join(thisdir, "test_config.json")
with open(jsonfile) as fp:
    config = json.load(fp)

__all__ = [
    'config',
]