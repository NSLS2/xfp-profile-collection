from bluesky.suspenders import (SuspendBoolLow, SuspendFloor)

#Borrow ring current suspender code from LiX with some modifications

beam_recovery_time = 600  #time in seconds, 10 minute recovery
beam_threshold = 300
beam_ring_current = EpicsSignalRO('SR:OPS-BI{DCCT:1}I:Real-I')

beam_current_suspender = SuspendFloor(beam_ring_current, beam_threshold, sleep=beam_recovery_time)

def install_beam_suspender():
    RE.install_suspender(beam_current_suspender)

def uninstall_beam_suspender():
    RE.remove_suspender(beam_current_suspender)

# pps_shutter_enabled_suspender = SuspendBoolLow(EpicsSignalRO(pps_shutter.enabled_status.pvname))
# RE.install_suspender(pps_shutter_enabled_suspender)
