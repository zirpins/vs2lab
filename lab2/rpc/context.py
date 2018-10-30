import os
import sys

# Add the toplevel folder of the repository to the module search path
# This way we can import modules from the shared lib package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), '..'), '..')))

# following imports are used by other modules to access shared packages
from lib import lab_channel
from lib import lab_logging
