"""Global variables."""

import os

DATA_FILE = os.path.realpath(os.path.join(os.path.dirname(__file__), '.pocket.json'))

VERSION = '0.0.2'

COUNT_DEFAULT = 10
SHORT_MIN_DEFAULT = 4
LONG_MIN_DEFAULT = 10

"""
Changelog

* 0.0.2
    - Loosen dependency rules
    - Upgrade dependencies
    - Updates to fix issues found in newer testing, linting, and typchecking versions

* 0.0.1
    - Initial commit.
"""
