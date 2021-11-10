from ophyd import Signal, EpicsSignalWithRBV, Component as Cpt
from ophyd.areadetector import ADBase, ADComponent as ADCpt
from ophyd.quadem import QuadEM
from ophyd import DynamicDeviceComponent as DDCpt
from collections import OrderedDict
from nslsii.ad33 import QuadEMV33


class QuadEMPort(ADBase):
    port_name = Cpt(Signal, value="")

    def __init__(self, port_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.port_name.put(port_name)


def _proc_current_fields(attr_base, field_base, range_, **kwargs):
    defn = OrderedDict()
    for i in range_:
        attr = '{attr}{i}'.format(attr=attr_base, i=i)
        suffix = '{field}{i}.PROC'.format(field=field_base, i=i)
        defn[attr] = (EpicsSignal, suffix, kwargs)

    return defn


class TimeSeries(Device):
    current1 = ADCpt(EpicsSignalRO, "Current1:TimeSeries", kind='normal')
    current2 = ADCpt(EpicsSignalRO, "Current2:TimeSeries", kind='normal')
    current3 = ADCpt(EpicsSignalRO, "Current3:TimeSeries", kind='normal')
    current4 = ADCpt(EpicsSignalRO, "Current4:TimeSeries", kind='normal')

    acquire = ADCpt(EpicsSignal, "TSAcquire", kind='omitted')
    acquire_mode = ADCpt(EpicsSignal, "TSAcquireMode", string=True, kind='config')
    acquiring = ADCpt(EpicsSignalRO, "TSAcquiring", kind='omitted')

    time_axis = ADCpt(EpicsSignalRO, "TSTimeAxis", kind='config')
    read_rate = ADCpt(EpicsSignal, "TSRead.SCAN", string=True, kind='config')
    num_points = ADCpt(EpicsSignal, "TSNumPoints", kind='config')
    averaging_time = ADCpt(EpicsSignalWithRBV, "TSAveragingTime", kind="config")
    current_point = ADCpt(EpicsSignalRO, "TSCurrentPoint", kind="omitted")


class XFPQuadEM(QuadEMV33):
    conf = Cpt(QuadEMPort, port_name="EM180")
    em_range = Cpt(EpicsSignalWithRBV, "Range", string=True)
    current_offset_calcs = DDCpt(_proc_current_fields('ch', 'ComputeCurrentOffset',
                                                      range(1, 5)))
    ts = ADCpt(TimeSeries, "TS:")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stage_sigs.update([(self.acquire_mode, "Single")])  # single mode
        self.configuration_attrs = [
            "integration_time",
            "averaging_time",
            "em_range",
            "num_averaged",
            "values_per_read",
        ]

    def set_primary(self, n, value=None):
        name_list = []
        if "All" in n:
            for k in self.read_attrs:
                getattr(self, k).kind = "normal"
            return

        for channel in n:
            cur = getattr(self, f"current{channel}")
            cur.kind |= Kind.normal
            cur.mean_value = Kind.hinted


qem1 = XFPQuadEM("XF:17BM-BI{EM:1}EM180:", name="qem1")
qem1.kind = "normal"
qem1.ts.kind = "normal"
#TODO: add later when it's repared
# qem2 = XFPQuadEM("XF:17BM-BI{EM:BPM1}", name='qem2')
#TODO: read in current1, 2, 4 for qem1
for det in [qem1]:
    det.read_attrs = ['current3', 'current3.mean_value']

#Read-in Experiments NSLS2_EM channels
#TODO: improve readback to match qem1
qem2_ch1 = EpicsSignalRO('XF:17BM-BI{EM:2}Current1:MeanValue_RBV', name='qem2_ch1')
qem2_ch2 = EpicsSignalRO('XF:17BM-BI{EM:2}Current2:MeanValue_RBV', name='qem2_ch2')
qem2_ch3 = EpicsSignalRO('XF:17BM-BI{EM:2}Current3:MeanValue_RBV', name='qem2_ch3')
qem3_ch4 = EpicsSignalRO('XF:17BM-BI{EM:2}Current4:MeanValue_RBV', name='qem2_ch4')


@bpp.run_decorator()
def qem_ts_plan(det=qem1, num=5, delay=1.0, wait_before_collect=0.5):
    yield from bps.mv(qem1.ts.acquire, 1)
    yield from bps.sleep(wait_before_collect)
    for i in range(num):
        yield from bps.trigger_and_read([det.ts])
        if i + 1 < num:
            yield from bps.sleep(delay)
    yield from bps.mv(det.ts.acquire, 0)
