"""
Utility script expanding the module search path
This way we can import modules from the shared lib package
"""

import os
import sys


def add_parent_path(steps_up=1):
    # construct path by stepping up the path hierarchy <steps_up> times
    path = os.path.dirname(__file__)
    for _ in range(steps_up):
        path = os.path.join(path, '..')
    # add the path to the system search path
    sys.path.insert(0, path)


# Add the toplevel folder of the repository to the module search path
add_parent_path()

# following imports are used by other modules to access shared packages
from lib import lab_logging, lab_channel
