# Make tests a package for pytest to find
import json
import os
from tests.testdata import TESTDATA

def get_config():
    jsonfile = os.path.join(TESTDATA, "config.json")
    with open(jsonfile) as fp:
        config = json.load(fp)
    return config        