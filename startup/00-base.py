import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

import nslsii
import bluesky.plans as bp
import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp
from bluesky.callbacks.best_effort import BestEffortCallback


# Disable Best Effort Callback at the moment (01/18/2018):
nslsii.configure_base(get_ipython().user_ns, 'xfp', bec=False)

# Best effort callback to print a table and show a live plot
bec = BestEffortCallback()
# RE.subscribe(bec)

# nice format string to use in various places
_time_fmtstr = '%Y-%m-%d %H:%M:%S'

# Set ipython startup dir variable (used in 97 and 99):
PROFILE_STARTUP_PATH = Path(f"{os.environ['HOME']}/.ipython/profile_collection/startup")

