import os
import pandas as pd
import matplotlib.pyplot as plt

import nslsii
import bluesky.plans as bp
import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp


nslsii.configure_base(get_ipython().user_ns, 'xfp')

# nice format string to use in various places
_time_fmtstr = '%Y-%m-%d %H:%M:%S'

