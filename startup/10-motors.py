#Defines classes for beamline / endstation motors
#Includes: all components in XFP PDS, ES:1, and ES:3.
#ES:3 XAS components are defined in a separate section at bottom
#Excludes: front end slits and front end mirror

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

#XAS components at ES:3. 
#Includes: monochromator, cryo stage, premono slits, and table
#Excludes: picomotor and PB_Diag_Y

#XAS monochromator in keV energy and theta units in a single class.
#Units on xasmono.en are in keV.
class XASMono(Device):
    en = Cpt(EpicsMotor, 'En}Mtr', settle_time=0.5)
    theta = Cpt(EpicsMotor, 'Theta}Mtr', settle_time=0.5)

xasmono = XASMono('XF:17BMA-OP{Mono:1-Ax:', name='xasmono')

#Sample cryostat motion stages, three axes:
class Sample_Cryo(Device):
    x = Cpt(EpicsMotor, 'X}Mtr')
    y = Cpt(EpicsMotor, 'Y}Mtr')
    z = Cpt(EpicsMotor, 'Z}Mtr')

sample_cryo = Sample_Cryo('XF:17BMA-ES:3{Stg:9-Ax:', name='sample_cryo')

#Real and virtual PreMono Slit axes in a single class.
#Functionally identical to the XFP PB slits
class PreMonoSlits(Device):
    top = Cpt(EpicsMotor, 'T}Mtr')
    bot = Cpt(EpicsMotor, 'B}Mtr')
    inb = Cpt(EpicsMotor, 'I}Mtr')
    outb = Cpt(EpicsMotor, 'O}Mtr')
    xgap = Cpt(EpicsMotor, 'XGap}Mtr')
    xctr = Cpt(EpicsMotor, 'XCtr}Mtr')
    ygap = Cpt(EpicsMotor, 'YGap}Mtr')
    yctr = Cpt(EpicsMotor, 'YCtr}Mtr')

premono_slits = PreMonoSlits('XF:17BMA-OP{Slt:PB-Ax:', name='premono_slits')

#ES:3 vertical lift table
class Table3(Device):
    y = Cpt(EpicsMotor, 'Y}Mtr')

tbl3 = Table3('XF:17BMA-ES:3{Tb3:1-Ax:', name='tbl3')


#Define front-end motors for baseline purposes
#FE slits limited to the physical X/Y positions for now

class FE_WhiteBeam_Slits(Device):
    top = Cpt(EpicsMotor, '1-Ax:T}Mtr')
    bot = Cpt(EpicsMotor, '2-Ax:B}Mtr')
    inb = Cpt(EpicsMotor, '2-Ax:I}Mtr')
    outb = Cpt(EpicsMotor, '1-Ax:O}Mtr')

fe_wb_slits = FE_WhiteBeam_Slits('FE:C17B-OP{Slt:', name='fe_wb_slits')

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

