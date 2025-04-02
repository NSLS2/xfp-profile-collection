from ophyd import (EpicsSignal, EpicsSignalRO, Device, Component as Cpt, DeviceStatus)

class clearXCamPython(Device):
    samples_per_HV = Cpt(EpicsSignal, "SamplesPerHV")
    sample_period = Cpt(EpicsSignal, "SamplePeriod")
    settle_time = Cpt(EpicsSignal, "SettleTime")
    bias = Cpt(EpicsSignal, "Bias")
    forward_bias_after_frame = Cpt(EpicsSignal, "ForwardBiasAfterFrame")
    forward_bias = Cpt(EpicsSignal, "ForwardBias")
    forward_bias_dwell_strips = Cpt(EpicsSignal, "ForwardBiasDwellStrips")
    forward_bias_period_frames = Cpt(EpicsSignal, "ForwardBiasPeriodFrames")
    low_power_adc = Cpt(EpicsSignal, "LowPowerADC")
    temporal_filter_alpha = Cpt(EpicsSignal, "TemporalFilterAlpha")
    concurrent_strips = Cpt(EpicsSignal, "ConcurrentStrips")
    fan = Cpt(EpicsSignal, "Fan")
    n_samples = Cpt(EpicsSignal, "NSamples")
    image = Cpt(EpicsSignalRO, "Image")
    collect_sig = Cpt(EpicsSignal, "Collect")
    filename = Cpt(EpicsSignal, "Filename")
    directory = Cpt(EpicsSignal, "Directory")
    collection = Cpt(EpicsSignal, "Collection")
 
    def do_collect(self):
        self.collect_sig.put(1)

cxc = clearXCamPython(name = 'cxc', prefix = 'XF:17BM:XFP{ClearXCam}')
