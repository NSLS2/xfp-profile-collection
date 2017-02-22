import ophyd
from ophyd.status import Status
import epics
import time as ttime

def local_set_and_wait(signal, val, poll_time=0.01, timeout=10, rtol=None,
                 atol=None, log_backoff=2):
    """Set a signal to a value and wait until it reads correctly.

    For floating point values, it is strongly recommended to set a tolerance.
    If tolerances are unset, the values will be compared exactly.

    Parameters
    ----------
    signal : EpicsSignal (or any object with `get` and `put`)
    val : object
        value to set signal to
    poll_time : float, optional
        how soon to check whether the value has been successfully set
    timeout : float, optional
        maximum time to wait for value to be successfully set
    rtol : float, optional
        allowed absolute tolerance between the readback and setpoint values
    atol : float, optional
        allowed relative tolerance between the readback and setpoint values

    Raises
    ------
    TimeoutError if timeout is exceeded
    """
    if atol is None and hasattr(signal, 'tolerance'):
        atol = signal.tolerance
    if rtol is None and hasattr(signal, 'rtolerance'):
        rtol = signal.rtolerance

    signal.put(val)
    expiration_time = ttime.time() + timeout
    current_value = signal.get()
    try:
        es = signal.enum_strs
    except AttributeError:
        es = ()

    if atol is not None:
        within_str = ['within {!r}'.format(atol)]
    else:
        within_str = []

    if rtol is not None:
        within_str.append('(relative tolerance of {!r})'.format(rtol))

    if within_str:
        within_str = ' '.join([''] + within_str)
    else:
        within_str = ''

    while not _compare_maybe_enum(val, current_value, es, atol, rtol):
        print('*', end='')
        ttime.sleep(poll_time)
        poll_time *= log_backoff  # logarithmic back-off
        current_value = signal.get()
        if ttime.time() > expiration_time:
            raise TimeoutError("Attempted to set %r to value %r and timed "
                               "out after %r seconds. Current value is %r." %
                               (signal, val, timeout, current_value))


def _compare_maybe_enum(a, b, enums, atol, rtol):
    if enums:
        # convert enum values to strings if necessary first:
        if not isinstance(a, str):
            a = enums[a]
        if not isinstance(b, str):
            b = enums[b]
        # then compare the strings
        return a == b

    # if either relative/absolute tolerance is used, use numpy
    # to compare:
    if atol is not None or rtol is not None:
        return np.allclose(a, b,
                           rtol=rtol if rtol is not None else 1e-5,
                           atol=atol if atol is not None else 1e-8,
                           )
    return a == b



class AgressiveSignal(ophyd.EpicsSignal):
    def set(self, value, *, timeout=None, settle_time=None):
        '''Set is like `put`, but is here for bluesky compatibility

        Returns
        -------
        st : Status
            This status object will be finished upon return in the
            case of basic soft Signals
        '''
        def set_thread():
            nonlocal timeout
            success = False
            if timeout is None:
                timeout = 10
                # TODO set_and_wait does not support a timeout of None
                #      and 10 is its default timeout

            try:
                local_set_and_wait(self, value, timeout=timeout, atol=self.tolerance,
                                   rtol=self.rtolerance, poll_time=.001, log_backoff=1.1)
            except TimeoutError:
                success = False
            except Exception as ex:
                success = False
            else:
                success = True
                if settle_time is not None:
                    time.sleep(settle_time)
            finally:
                st._finished(success=success)
                self._set_thread = None

        if self._set_thread is not None:
            raise RuntimeError('Another set() call is still in progress')

        st = Status(self)
        self._status = st
        self._set_thread = epics.ca.CAThread(target=set_thread)
        self._set_thread.daemon = True
        self._set_thread.start()
        return self._status
