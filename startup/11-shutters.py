from nslsii.devices import TwoButtonShutter, _time_fmtstr


class XFPGalvoShutter(Device):
    # TODO: this needs to be fixed in EPICS as these names make no sense
    # the value coming out of the PV does not match what is shown in CSS
    open_cmd = Cpt(EpicsSignal, 'Cmd:Opn-Cmd.PROC', string=True)
    open_val = 'Open'

    close_cmd = Cpt(EpicsSignal, 'Cmd:Cls-Cmd.PROC', string=True)
    close_val = 'Closed'

    status = Cpt(EpicsSignalRO, 'Pos-Sts', string=True)

    # user facing commands
    open_str = 'Open'
    close_str = 'Close'

    def set(self, val):
        if self._set_st is not None:
            raise RuntimeError(f'trying to set {self.name}'
                               ' while a set is in progress')

        cmd_map = {self.open_str: self.open_cmd,
                   self.close_str: self.close_cmd}
        target_map = {self.open_str: self.open_val,
                      self.close_str: self.close_val}

        cmd_sig = cmd_map[val]
        target_val = target_map[val]

        st = DeviceStatus(self)
        if self.status.get() == target_val:
            st._finished()
            return st

        self._set_st = st
        # print(self.name, val, id(st))
        enums = self.status.enum_strs

        def shutter_cb(value, timestamp, **kwargs):
            value = enums[int(value)]

            if value == target_val:
                self._set_st = None
                self.status.clear_sub(shutter_cb)
                st._finished()

        self.status.subscribe(shutter_cb, run=True)
        cmd_sig.put(1)

        return st

    def stop(self, success):
        # MR: commenting out on 10/30/2018 for manual control of the shutters (see #10).
        '''
        import time
        prev_st = self._set_st
        if prev_st is not None:
            while not prev_st.done:
                time.sleep(.1)
        self._was_open = (self.open_val == self.status.get())
        st = self.set('Close')
        while not st.done:
            time.sleep(.5)
        '''
        pass

    def resume(self):
        import time
        prev_st = self._set_st
        if prev_st is not None:
            while not prev_st.done:
                time.sleep(.1)
        if self._was_open:
            st = self.set('Open')
            while not st.done:
                time.sleep(.5)

    def unstage(self):
        self._was_open = False
        return super().unstage()

    def __init__(self, *args, **kwargs):
        self._was_open = False
        super().__init__(*args, **kwargs)
        self._set_st = None
        self.read_attrs = ['status']


# MR: get rid of the stop() method on 10/30/2018 for manual control of the shutters (see #10).
class TwoButtonShutterXFP(TwoButtonShutter):
    def stop(self):
        pass


pre_shutter = TwoButtonShutterXFP('XF:17BMA-EPS{Sh:1}', name='shutter')
shutter = pre_shutter
pps_shutter = TwoButtonShutterXFP('XF:17BM-PPS{Sh:FE}', name='pps_shutter')
galvo_shutter = XFPGalvoShutter('XF:17BM-ES{Gon:1-Sht}', name='galvo_shutter')

