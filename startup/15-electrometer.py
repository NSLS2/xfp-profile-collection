from ophyd import Signal, EpicsSignalWithRBV, Component as Cpt
from ophyd.areadetector import ADBase
from ophyd.quadem import QuadEM 


class QuadEMPort(ADBase):
    port_name = Cpt(Signal, value="")

    def __init__(self, port_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.port_name.put(port_name)


class ESMQuadEM(QuadEM):
    conf = Cpt(QuadEMPort, port_name="EM180")
    em_range = Cpt(EpicsSignalWithRBV, "Range", string=True)

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


qem1 = ESMQuadEM("XF:17BM-BI{EM:1}EM180:", name="qem1")
#TODO: add later when it's repared
# qem2 = ESMQuadEM("XF:17BM-BI{EM:BPM1}", name='qem2')
for det in [qem1]:
    det.read_attrs = ['current3', 'current3.mean_value']
_
