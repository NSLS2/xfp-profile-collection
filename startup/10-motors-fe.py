#Defines classes for front-end and accelerator components

#This stuff should be imported by 10-fp-devices.py

import time
import datetime
from ophyd import (EpicsMotor, Device,
                   Component as Cpt, EpicsSignal,
                   EpicsSignalRO, DeviceStatus)


#ring current
beam_ring_current = EpicsSignalRO('SR:OPS-BI{DCCT:1}I:Real-I', name='ring_current')

#FE slits, real and virtual motors

class FE_WhiteBeam_Slits(Device):
    top = Cpt(EpicsMotor, '1-Ax:T}Mtr', labels=('FE Slits',))
    bot = Cpt(EpicsMotor, '2-Ax:B}Mtr', labels=('FE Slits',))
    inb = Cpt(EpicsMotor, '2-Ax:I}Mtr', labels=('FE Slits',))
    outb = Cpt(EpicsMotor, '1-Ax:O}Mtr', labels=('FE Slits',))
    hsize = Cpt(EpicsSignalRO, '12-Ax:X}t2.C', labels=('FE Slits',))
    vsize = Cpt(EpicsSignalRO, '12-Ax:Y}t2.C', labels=('FE Slits',))
    hctr = Cpt(EpicsSignalRO, '12-Ax:X}t2.D', labels=('FE Slits',))
    vctr = Cpt(EpicsSignalRO, '12-Ax:Y}t2.D', labels=('FE Slits',))
    
fe_wb_slits = FE_WhiteBeam_Slits('FE:C17B-OP{Slt:', name='fe_wb_slits')

fe_slit_hold_sentinel = EpicsSignal('XF:17BM{Sentinel}slit_hold', name='fe_slit_sentinel')

#FE mirror including thermocouple signals

class XFP_FE_Mirror(Device):
    hor_up = Cpt(EpicsMotor, '-Ax:XU}Mtr', labels=('FE Mirror',))
    hor_down = Cpt(EpicsMotor, '-Ax:XD}Mtr', labels=('FE Mirror',))
    lift_up = Cpt(EpicsMotor, '-Ax:YUI}Mtr', labels=('FE Mirror',))
    lift_ctr = Cpt(EpicsMotor, '-Ax:YO}Mtr', labels=('FE Mirror',))
    lift_down = Cpt(EpicsMotor, '-Ax:YDI}Mtr', labels=('FE Mirror',))
    focus = Cpt(EpicsMotor, '-Ax:Bend}Mtr', labels=('FE Mirror',))
    X = Cpt(EpicsMotor, '-Ax:X}Mtr', labels=('FE Mirror',))
    Y = Cpt(EpicsMotor, '-Ax:Y}Mtr', labels=('FE Mirror',))
    pitch = Cpt(EpicsMotor, '-Ax:P}Mtr', labels=('FE Mirror',))
    yaw = Cpt(EpicsMotor, '-Ax:Yaw}Mtr', labels=('FE Mirror',))
    roll = Cpt(EpicsMotor, '-Ax:R}Mtr', labels=('FE Mirror',))
    temp1 = Cpt(EpicsSignalRO, '}T:1-I', labels=('FE Mirror',))
    temp2 = Cpt(EpicsSignalRO, '}T:2-I', labels=('FE Mirror',))

xfp_fe_mirror = XFP_FE_Mirror('XF:17BM-OP{Mir:1', name='xfp_fe_mirror')

