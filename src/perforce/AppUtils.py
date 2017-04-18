import os
import sys
import re
import logging

import perforce.Utils as Utils

def importClass(className):
    mod = __import__('perforce.%s' % className, fromlist=[className])
    return getattr(mod, className)

def in_unittest():
    # http://stackoverflow.com/questions/25025928/how-can-a-piece-of-python-code-tell-if-its-running-under-unittest
    current_stack = inspect.stack()
    for stack_frame in current_stack:
        # This element of the stack frame contains
        for program_line in stack_frame[4]:
            if "unittest" in program_line:       # some contextual program lines
                return True
    return False

# Import app specific utilities, maya opens scenes differently than nuke etc
# Are we in maya or nuke?
if re.match("maya", os.path.basename(sys.executable), re.I):
    try:
        import maya.standalone
        maya.standalone.initialize()
    except:
        pass

    Utils.p4Logger().info("Configuring for Maya")
    DCCInterop = importClass('MayaInterop')
elif re.match("nuke", os.path.basename(sys.executable), re.I):
    Utils.p4Logger().info("Configuring for Nuke")
    DCCInterop = importClass('NukeInterop')
elif in_unittest:
    Utils.p4Logger().info("Configuring for testing")
    DCCInterop = importClass('TestInterop')

else:
    Utils.p4Logger().warning("Couldn't find app configuration")
    raise ImportError(
        "No supported applications found that this plugin can interface with")
