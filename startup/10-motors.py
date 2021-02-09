#Defines classes for beamline / endstation motors
#Includes: all components in XFP PDS, ES:1, and ES:2
#Excludes: ES:3, front end slits, and front end mirror

#This stuff should be imported by 10-fp-devices.py
import time
import datetime
from ophyd import (EpicsMotor, Device,
                   Component as Cpt, EpicsSignal,
                   EpicsSignalRO, DeviceStatus)

#CF stage, 100mm travel
class ModXY_CF(Device):
    x = Cpt(EpicsMotor, 'X}Mtr')
    y = Cpt(EpicsMotor, 'Y}Mtr')

cf = ModXY_CF('XF:17BMA-ES:1{Stg:5-Ax:', name='cf')
modx = EpicsMotor('XF:17BMA-ES:1{Stg:5-Ax:X}Mtr', name = 'modx')

#Beampipe manipulator, not usually connected
class BeamPipeStage(Device):
    x = Cpt(EpicsMotor, 'X}Mtr')
    y = Cpt(EpicsMotor, 'Y}Mtr')

pipe = BeamPipeStage('XF:17BMA-OP{Stg:2-Ax:', name='pipe')

#ES:1 3-axis table
class Table1(Device):
    x = Cpt(EpicsMotor, 'X}Mtr')
    y = Cpt(EpicsMotor, 'Y}Mtr')
    z = Cpt(EpicsMotor, 'Z}Mtr')

tbl1 = Table1('XF:17BMA-ES:1{Tbl:1-Ax:', name='tbl1')

#HT stage (200mm travel)
class HT(Device):
    x = Cpt(EpicsMotor, 'X}Mtr')
    y = Cpt(EpicsMotor, 'Y}Mtr')

ht = HT('XF:17BMA-ES:2{Stg:7-Ax:', name='ht')

#HTFly XY stages (shutterless HT)
class HTFly(Device):
    x = Cpt(EpicsMotor, 'X}Mtr')
    y = Cpt(EpicsMotor, 'Y}Mtr')

htfly = HT('XF:17BMA-ES:2{HTFly:1-Ax:', name='htfly')

#Sydor BPM motors and readback in 20-bpm.py
#class BPM(Device):
#    x = Cpt(EpicsMotor, 'X}Mtr')
#    y = Cpt(EpicsMotor, 'Y}Mtr')
#
#bpm1 = BPM('XF:17BMA-OP{Bpm:1-Ax:', name='bpm1')

#Amazon 50mm-100mm slides
class CVDViewer(Device):
    x = Cpt(EpicsMotor, 'X}Mtr')
    y = Cpt(EpicsMotor, 'Y}Mtr')

cvd = CVDViewer('XF:17BMA-ES:1{CVD:1-Ax:', name='cvd')

#CF sample collector (Amaazon slide)
class CFSample(Device):
    z = Cpt(EpicsMotor, 'Z}Mtr')

cfsam = CFSample('XF:17BMA-ES:1{Sam:1-Ax:', name='cfsam')

#Real and virtual XFP PB Slit axes in a single class.
class PBSlits(Device):
    top = Cpt(EpicsMotor, 'T}Mtr')
    bot = Cpt(EpicsMotor, 'B}Mtr')
    inb = Cpt(EpicsMotor, 'I}Mtr')
    outb = Cpt(EpicsMotor, 'O}Mtr')
    xgap = Cpt(EpicsMotor, 'XGap}Mtr')
    xctr = Cpt(EpicsMotor, 'XCtr}Mtr')
    ygap = Cpt(EpicsMotor, 'YGap}Mtr')
    yctr = Cpt(EpicsMotor, 'YCtr}Mtr')

pbslits = PBSlits('XF:17BMA-OP{Slt:PB-Ax:', name='pbslits')

#Real and virtual XFP ADC Slit axes in a single class.
class ADCSlits(Device):
    top = Cpt(EpicsMotor, 'T}Mtr')
    bot = Cpt(EpicsMotor, 'B}Mtr')
    inb = Cpt(EpicsMotor, 'I}Mtr')
    outb = Cpt(EpicsMotor, 'O}Mtr')
    xgap = Cpt(EpicsMotor, 'XGap}Mtr')
    xctr = Cpt(EpicsMotor, 'XCtr}Mtr')
    ygap = Cpt(EpicsMotor, 'YGap}Mtr')
    yctr = Cpt(EpicsMotor, 'YCtr}Mtr')

adcslits = ADCSlits('XF:17BMA-OP{Slt:ADC-Ax:', name='adcslits')


