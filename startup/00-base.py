import os
import sys
from pathlib import Path

import appdirs
import bluesky.plan_stubs as bps
import bluesky.plans as bp
import bluesky.preprocessors as bpp
import matplotlib.backends.backend_qt5
import matplotlib.pyplot as plt
import nslsii
import pandas as pd
import yaml
from bluesky.callbacks.best_effort import BestEffortCallback
#from bluesky.utils import PersistentDict
from matplotlib._pylab_helpers import Gcf
from matplotlib.backends.backend_qt5 import _create_qApp
import redis
from redis_json_dict import RedisJSONDict
#
uri = "info.xfp.nsls2.bnl.gov"
# # Provide an endstation prefix, if needed, with a trailing "-"
new_md = RedisJSONDict(redis.Redis(uri), prefix="")

# Disable Best Effort Callback at the moment (01/18/2018):
nslsii.configure_base(get_ipython().user_ns, "xfp", bec=False, pbar=False, publish_documents_with_kafka=True)

# nice format string to use in various places
_time_fmtstr = "%Y-%m-%d %H:%M:%S"

# Set ipython startup dir variable (used in 97 and 99):
PROFILE_STARTUP_PATH = Path(get_ipython().profile_dir.startup_dir)


def xfp_print(string, stdout=sys.stdout, flush=True):
    print(string, file=stdout, flush=flush)


#runengine_metadata_dir = appdirs.user_data_dir(appname="bluesky") / Path(
#    "runengine-metadata"
#)

# PersistentDict will create the directory if it does not exist
#RE.md = PersistentDict(runengine_metadata_dir)

RE.md = new_md

app = _create_qApp()
