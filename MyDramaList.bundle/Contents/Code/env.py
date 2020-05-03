# pylint: disable=undefined-variable

import io
import os
import sys

def loadenv():
    # roundabout way to get __file__ since RestrictedPython really lives up to its name
    getframe = getattr(sys, "_getframe")
    file = getframe().f_code.co_filename
    Log.Debug("Found current script path (__file__): %s", file)

    p = os.path.join(os.path.dirname(file), ".env")
    Log.Debug("Updating os.environ from %s", p)

    with io.open(p, "r") as f:
        os.environ.update(dict([line.strip().split("=") for line in f]))
