from ophyd.status import SubscriptionStatus
from ophyd.sim import NullStatus
from nslsii.devices import TwoButtonShutter, _time_fmtstr

#Comment out GalvoShutter as this is not implemented / running
#class XFPGalvoShutter(Device):
    # TODO: this needs to be fixed in EPICS as these names make no sense
    # the value coming out of the PV does not match what is shown in CSS
#    open_cmd = Cpt(EpicsSignal, 'Cmd:Opn-Cmd.PROC', string=True)
#    open_val = 'Open'

#    close_cmd = Cpt(EpicsSignal, 'Cmd:Cls-Cmd.PROC', string=True)
#    close_val = 'Closed'

#    status = Cpt(EpicsSignalRO, 'Pos-Sts', string=True)

    # user facing commands
#    open_str = 'Open'
#    close_str = 'Close'

#    def set(self, val):
#        if self._set_st is not None:
#            raise RuntimeError(f'trying to set {self.name}'
#                               ' while a set is in progress')

#        cmd_map = {self.open_str: self.open_cmd,
#                   self.close_str: self.close_cmd}
#        target_map = {self.open_str: self.open_val,
#                      self.close_str: self.close_val}

#        cmd_sig = cmd_map[val]
#        target_val = target_map[val]

#        st = DeviceStatus(self)
#        if self.status.get() == target_val:
#            st._finished()
#            return st

#        self._set_st = st
#        # print(self.name, val, id(st))
#        enums = self.status.enum_strs

#        def shutter_cb(value, timestamp, **kwargs):
#            value = enums[int(value)]

#            if value == target_val:
#                self._set_st = None
#                self.status.clear_sub(shutter_cb)
#                st._finished()

#        self.status.subscribe(shutter_cb, run=True)
#        cmd_sig.put(1)

#        return st

#    def stop(self, success):
#        import time
#        prev_st = self._set_st
#        if prev_st is not None:
#            while not prev_st.done:
#                time.sleep(.1)
#        self._was_open = (self.open_val == self.status.get())
#        st = self.set('Close')
#        while not st.done:
#            time.sleep(.5)

#    def resume(self):
#        import time
#        prev_st = self._set_st
#        if prev_st is not None:
#            while not prev_st.done:
#                time.sleep(.1)
#        if self._was_open:
#            st = self.set('Open')
#            while not st.done:
#                time.sleep(.5)

#    def unstage(self):
#        self._was_open = False
#        return super().unstage()

#    def __init__(self, *args, **kwargs):
#        self._was_open = False
#        super().__init__(*args, **kwargs)
#        self._set_st = None
#        self.read_attrs = ['status']



pre_shutter = TwoButtonShutter('XF:17BMA-EPS{Sh:1}', name='shutter')
shutter = pre_shutter
pps_shutter = TwoButtonShutter('XF:17BM-PPS{Sh:FE}', name='pps_shutter')
#galvo_shutter = XFPGalvoShutter('XF:17BM-ES{Gon:1-Sht}', name='galvo_shutter')


class DiodeShutter(Device):
    open_close_cmd = Cpt(EpicsSignal, '1}OutPt00:Data-Cmd')
    status_open = Cpt(EpicsSignalRO, '2}InPt00:Data-Sts')
    status_closed = Cpt(EpicsSignalRO, '2}InPt01:Data-Sts')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_values = {'open': 1, 'close': 0}

    def set(self, value):
        assert value in self.allowed_values.keys(), \
                f'The value "{value}" is not allowed. Allowed ones are {self.allowed_values.keys()}'

        def callback(value, old_value, **kwargs):
            # print(f'old value {old_value} --> new value {value}')
            # print(f'status_open: {self.status_open.get()}')
            # print(f'status_closed: {self.status_closed.get()}')
            if old_value != value:
                return True
            return False

        if self.status_open.get() != self.allowed_values[value]:
            _st_open = SubscriptionStatus(self.status_open, callback, run=False)
        else:
            _st_open = NullStatus()

        if self.status_closed.get() == self.allowed_values[value]:
            _st_closed = SubscriptionStatus(self.status_closed, callback, run=False)
        else:
            _st_closed = NullStatus()

        self.open_close_cmd.put(self.allowed_values[value])

        return _st_open & _st_closed


diode_shutter = DiodeShutter('XF:17BMA-CT{DIODE-Local:', name='diode_shutter')
