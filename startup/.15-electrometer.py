from ophyd import Signal, EpicsSignalWithRBV, Component as Cpt
from ophyd.areadetector import ADBase
from ophyd.quadem import QuadEM 
from ophyd import DynamicDeviceComponent as DDCpt
from collections import OrderedDict


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


class XFPQuadEM(QuadEM):
    conf = Cpt(QuadEMPort, port_name="EM180")
    em_range = Cpt(EpicsSignalWithRBV, "Range", string=True)
    current_offset_calcs = DDCpt(_proc_current_fields('ch', 'ComputeCurrentOffset',
                                                      range(1, 5)))
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
