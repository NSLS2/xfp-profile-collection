from ophyd.status import SubscriptionStatus
from ophyd.sim import NullStatus
from nslsii.devices import TwoButtonShutter, _time_fmtstr


pre_shutter = TwoButtonShutter('XF:17BMA-EPS{Sh:1}', name='shutter')
shutter = pre_shutter
pps_shutter = TwoButtonShutter('XF:17BM-PPS{Sh:FE}', name='pps_shutter')


class DiodeShutter(Device):
    open_close_cmd = Cpt(EpicsSignal, '1}OutPt00:Data-Sel')
    status_open = Cpt(EpicsSignalRO, '2}InPt00:Data-Sts')
    status_closed = Cpt(EpicsSignalRO, '2}InPt01:Data-Sts')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_values = {'Open': 1, 'Close': 0}

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
