################################################################
# TODO: remove it after bluesky<1.6 is not used/needed here.
import bluesky
from distutils.version import LooseVersion
if bluesky.__version__ < LooseVersion('1.6'):
    OLD_BLUESKY = True
else:
    OLD_BLUESKY = False
################################################################

import os
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

import nslsii
import bluesky.plans as bp
import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp
from bluesky.callbacks.best_effort import BestEffortCallback


# Disable Best Effort Callback at the moment (01/18/2018):
nslsii.configure_base(get_ipython().user_ns, 'xfp', bec=False, pbar=False)

# nice format string to use in various places
_time_fmtstr = '%Y-%m-%d %H:%M:%S'

# Set ipython startup dir variable (used in 97 and 99):
PROFILE_STARTUP_PATH = Path(get_ipython().profile_dir.startup_dir)

def xfp_print(string, stdout=sys.stdout, flush=True):
    print(string, file=stdout, flush=flush)


#####################################################################################
# DAMA drop-in hack for PersistentDict for 2019-3.0 envs.


from pathlib import Path

import appdirs


try:
    from bluesky.utils import PersistentDict
except ImportError:
    import msgpack
    import msgpack_numpy
    import zict

    class PersistentDict(zict.Func):
        """
        A MutableMapping which syncs it contents to disk.
        The contents are stored as msgpack-serialized files, with one file per item
        in the mapping.
        Note that when an item is *mutated* it is not immediately synced:
        >>> d['sample'] = {"color": "red"}  # immediately synced
        >>> d['sample']['shape'] = 'bar'  # not immediately synced
        but that the full contents are synced to disk when the PersistentDict
        instance is garbage collected.
        """
        def __init__(self, directory):
            self._directory = directory
            self._file = zict.File(directory)
            self._cache = {}
            super().__init__(self._dump, self._load, self._file)
            self.reload()

            # Similar to flush() or _do_update(), but without reference to self
            # to avoid circular reference preventing collection.
            # NOTE: This still doesn't guarantee call on delete or gc.collect()!
            #       Explicitly call flush() if immediate write to disk required.
            def finalize(zfile, cache, dump):
                zfile.update((k, dump(v)) for k, v in cache.items())

            import weakref
            self._finalizer = weakref.finalize(
                self, finalize, self._file, self._cache, PersistentDict._dump)

        @property
        def directory(self):
            return self._directory

        def __setitem__(self, key, value):
            self._cache[key] = value
            super().__setitem__(key, value)

        def __getitem__(self, key):
            return self._cache[key]

        def __delitem__(self, key):
            del self._cache[key]
            super().__delitem__(key)

        def __repr__(self):
            return f"<{self.__class__.__name__} {dict(self)!r}>"

        @staticmethod
        def _dump(obj):
            "Encode as msgpack using numpy-aware encoder."
            # See https://github.com/msgpack/msgpack-python#string-and-binary-type
            # for more on use_bin_type.
            return msgpack.packb(
                obj,
                default=msgpack_numpy.encode,
                use_bin_type=True)

        @staticmethod
        def _load(file):
            return msgpack.unpackb(
                file,
                object_hook=msgpack_numpy.decode,
                raw=False)

        def flush(self):
            """Force a write of the current state to disk"""
            for k, v in self.items():
                super().__setitem__(k, v)

        def reload(self):
            """Force a reload from disk, overwriting current cache"""
            self._cache = dict(super().items())

runengine_metadata_dir = appdirs.user_data_dir(appname="bluesky") / Path("runengine-metadata")

# PersistentDict will create the directory if it does not exist
RE.md = PersistentDict(runengine_metadata_dir)

# TODO: remove the first condition along with the part on the top of the file.
################################################################
if OLD_BLUESKY:
    from bluesky.utils import install_qt_kicker
    install_qt_kicker()
else:
################################################################
    import matplotlib.backends.backend_qt5
    from matplotlib._pylab_helpers import Gcf
    from matplotlib.backends.backend_qt5 import _create_qApp

    _create_qApp()
    qApp = matplotlib.backends.backend_qt5.qApp
