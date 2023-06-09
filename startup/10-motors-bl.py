#Defines classes for beamline / endstation motors
#Includes: all components in XFP PDS, ES:1, and ES:3.

#This stuff should be imported by 10-fp-devices.py
import time
import datetime
from ophyd import (EpicsMotor, Device,
                   Component as Cpt, EpicsSignal,
                   EpicsSignalRO, DeviceStatus)

#CF stage, 100mm travel
class ModXY_CF(Device):
    x = Cpt(EpicsMotor, 'X}Mtr', labels=('FP ES:1',))
    y = Cpt(EpicsMotor, 'Y}Mtr', labels=('FP ES:1',))

cf = ModXY_CF('XF:17BMA-ES:1{Stg:5-Ax:', name='cf')
#modx = EpicsMotor('XF:17BMA-ES:1{Stg:5-Ax:X}Mtr', name = 'modx')

#Beampipe manipulator, not usually connected
class BeamPipeStage(Device):
    x = Cpt(EpicsMotor, 'X}Mtr', labels=('FP PDS',))
    y = Cpt(EpicsMotor, 'Y}Mtr', labels=('FP PDS',))

pipe = BeamPipeStage('XF:17BMA-OP{Stg:2-Ax:', name='pipe')

#ES:1 3-axis table
class Table1(Device):
    x = Cpt(EpicsMotor, 'X}Mtr', labels=('FP ES:1',))
    y = Cpt(EpicsMotor, 'Y}Mtr', labels=('FP ES:1',))
    z = Cpt(EpicsMotor, 'Z}Mtr', labels=('FP ES:1',))

tbl1 = Table1('XF:17BMA-ES:1{Tbl:1-Ax:', name='tbl1')

#HT stage (200mm travel)
class HT(Device):
    x = Cpt(EpicsMotor, 'X}Mtr', labels=('FP ES:2',))
    y = Cpt(EpicsMotor, 'Y}Mtr', labels=('FP ES:2',))

ht = HT('XF:17BMA-ES:2{Stg:7-Ax:', name='ht')

#HTFly XY stages (shutterless HT)
class HTFly(Device):
    x = Cpt(EpicsMotor, 'X}Mtr', labels=('FP ES:2',))
    y = Cpt(EpicsMotor, 'Y}Mtr', labels=('FP ES:2',))

htfly = HT('XF:17BMA-ES:2{HTFly:1-Ax:', name='htfly')

#Amazon 50mm-100mm slides, not usually connected
class CVDViewer(Device):
    x = Cpt(EpicsMotor, 'X}Mtr', labels=('FP ES:1',))
    y = Cpt(EpicsMotor, 'Y}Mtr', labels=('FP ES:1',))

cvd = CVDViewer('XF:17BMA-ES:1{CVD:1-Ax:', name='cvd')

#CF sample collector (Amaazon slide), not usually connected
class CFSample(Device):
    z = Cpt(EpicsMotor, 'Z}Mtr', labels=('FP ES:1',))

cfsam = CFSample('XF:17BMA-ES:1{Sam:1-Ax:', name='cfsam')

#Real and virtual XFP PB Slit axes in a single class.
class PBSlits(Device):
    top = Cpt(EpicsMotor, 'T}Mtr', labels=('FP PDS',))
    bot = Cpt(EpicsMotor, 'B}Mtr', labels=('FP PDS',))
    inb = Cpt(EpicsMotor, 'I}Mtr', labels=('FP PDS',))
    outb = Cpt(EpicsMotor, 'O}Mtr', labels=('FP PDS',))
    xgap = Cpt(EpicsMotor, 'XGap}Mtr', labels=('FP PDS',))
    xctr = Cpt(EpicsMotor, 'XCtr}Mtr', labels=('FP PDS',))
    ygap = Cpt(EpicsMotor, 'YGap}Mtr', labels=('FP PDS',))
    yctr = Cpt(EpicsMotor, 'YCtr}Mtr', labels=('FP PDS',))

pbslits = PBSlits('XF:17BMA-OP{Slt:PB-Ax:', name='pbslits')

#Real and virtual XFP ADC Slit axes in a single class.
class ADCSlits(Device):
    top = Cpt(EpicsMotor, 'T}Mtr', labels=('FP ES:2','monochromatic ES',))
    bot = Cpt(EpicsMotor, 'B}Mtr', labels=('FP ES:2','monochromatic ES',))
    inb = Cpt(EpicsMotor, 'I}Mtr', labels=('FP ES:2','monochromatic ES',))
    outb = Cpt(EpicsMotor, 'O}Mtr', labels=('FP ES:2','monochromatic ES',))
    xgap = Cpt(EpicsMotor, 'XGap}Mtr', labels=('FP ES:2','monochromatic ES',))
    xctr = Cpt(EpicsMotor, 'XCtr}Mtr', labels=('FP ES:2','monochromatic ES',))
    ygap = Cpt(EpicsMotor, 'YGap}Mtr', labels=('FP ES:2','monochromatic ES',))
    yctr = Cpt(EpicsMotor, 'YCtr}Mtr', labels=('FP ES:2','monochromatic ES',))

adcslits = ADCSlits('XF:17BMA-OP{Slt:ADC-Ax:', name='adcslits')

#XAS components at ES:3. 
#Includes: monochromator, cryo stage, premono slits, and table
#Excludes: picomotor and PB_Diag_Y

#XAS monochromator in keV energy and theta units in a single class.
#Units on xasmono.en are in keV.
class XASMono(Device):
    en = Cpt(EpicsMotor, 'En}Mtr', settle_time=0.5, labels=('monochromatic ES',))
    theta = Cpt(EpicsMotor, 'Theta}Mtr', settle_time=0.5, labels=('monochromatic ES',))

xasmono = XASMono('XF:17BMA-OP{Mono:1-Ax:', name='xasmono')

#Sample cryostat motion stages, three axes:
class Sample_Cryo(Device):
    x = Cpt(EpicsMotor, 'X}Mtr', labels=('monochromatic ES',))
    y = Cpt(EpicsMotor, 'Y}Mtr', labels=('monochromatic ES',))
    z = Cpt(EpicsMotor, 'Z}Mtr', labels=('monochromatic ES',))

sample_cryo = Sample_Cryo('XF:17BMA-ES:3{Stg:9-Ax:', name='sample_cryo')

#Real and virtual PreMono Slit axes in a single class.
#Functionally identical to the XFP PB slits
class PreMonoSlits(Device):
    top = Cpt(EpicsMotor, 'T}Mtr', labels=('monochromatic ES',))
    bot = Cpt(EpicsMotor, 'B}Mtr', labels=('monochromatic ES',))
    inb = Cpt(EpicsMotor, 'I}Mtr', labels=('monochromatic ES',))
    outb = Cpt(EpicsMotor, 'O}Mtr', labels=('monochromatic ES',))
    xgap = Cpt(EpicsMotor, 'XGap}Mtr', labels=('monochromatic ES',))
    xctr = Cpt(EpicsMotor, 'XCtr}Mtr', labels=('monochromatic ES',))
    ygap = Cpt(EpicsMotor, 'YGap}Mtr', labels=('monochromatic ES',))
    yctr = Cpt(EpicsMotor, 'YCtr}Mtr', labels=('monochromatic ES',))

premono_slits = PreMonoSlits('XF:17BMA-OP{Slt:PB-Ax:', name='premono_slits')

#ES:3 vertical lift table
class Table3(Device):
    y = Cpt(EpicsMotor, 'Y}Mtr', labels=('monochromatic ES',))

tbl3 = Table3('XF:17BMA-ES:3{Tbl:3-Ax:', name='tbl3')
