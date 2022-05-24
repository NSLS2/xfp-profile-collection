#Defines classes for front-end and accelerator components

#This stuff should be imported by 10-fp-devices.py

import time
import datetime
from ophyd import (EpicsMotor, Device,
                   Component as Cpt, EpicsSignal,
                   EpicsSignalRO, DeviceStatus)


#ring current
beam_ring_current = EpicsSignalRO('SR:OPS-BI{DCCT:1}I:Real-I', name='ring_current')

#FE slits, real motors only

class FE_WhiteBeam_Slits(Device):
    top = Cpt(EpicsMotor, '1-Ax:T}Mtr')
    bot = Cpt(EpicsMotor, '2-Ax:B}Mtr')
    inb = Cpt(EpicsMotor, '2-Ax:I}Mtr')
    outb = Cpt(EpicsMotor, '1-Ax:O}Mtr')

fe_wb_slits = FE_WhiteBeam_Slits('FE:C17B-OP{Slt:', name='fe_wb_slits')

#FE mirror including thermocouple signals

class XFP_FE_Mirror(Device):
    hor_up = Cpt(EpicsMotor, '-Ax:XU}Mtr')
    hor_down = Cpt(EpicsMotor, '-Ax:XD}Mtr')
    lift_up = Cpt(EpicsMotor, '-Ax:YUI}Mtr')
    lift_ctr = Cpt(EpicsMotor, '-Ax:YO}Mtr')
    lift_down = Cpt(EpicsMotor, '-Ax:YDI}Mtr')
    focus = Cpt(EpicsMotor, '-Ax:Bend}Mtr')
    X = Cpt(EpicsMotor, '-Ax:X}Mtr')
    Y = Cpt(EpicsMotor, '-Ax:Y}Mtr')
    pitch = Cpt(EpicsMotor, '-Ax:P}Mtr')
    yaw = Cpt(EpicsMotor, '-Ax:Yaw}Mtr')
    roll = Cpt(EpicsMotor, '-Ax:P}Mtr')
    temp1 = Cpt(EpicsSignalRO, '}T:1-I')
    temp2 = Cpt(EpicsSignalRO, '}T:2-I')

xfp_fe_mirror = XFP_FE_Mirror('XF:17BM-OP{Mir:1', name='xfp_fe_mirror')

