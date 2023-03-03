'''Purpose: define ophyd objects for:
1. Sydor BPM
    a. electrometer readout (via modified NSLS2_EM)
    b. EpicsMotor motions for bpm alignment
2. Sydor PBG bias control and thermocouple readout
'''

class SydorBPM(Device):
    chan_a = Cpt(EpicsSignalRO, 'Current1:MeanValue_RBV')
    chan_b = Cpt(EpicsSignalRO, 'Current2:MeanValue_RBV')
    chan_c = Cpt(EpicsSignalRO, 'Current3:MeanValue_RBV')
    chan_d = Cpt(EpicsSignalRO, 'Current4:MeanValue_RBV')
    pos_X = Cpt(EpicsSignalRO, 'PosX:MeanValue_RBV')
    pos_Y = Cpt(EpicsSignalRO, 'PosY:MeanValue_RBV')
    sum_curr = Cpt(EpicsSignalRO, 'SumAll:MeanValue_RBV')

sydor_bpm = SydorBPM('XF:17BM-BI{EM:BPM1}', name='sydor_bpm')

class DBPM(Device):
    x = Cpt(EpicsMotor, 'X}Mtr', labels=('FP PDS',))
    y = Cpt(EpicsMotor, 'Y}Mtr', labels=('FP PDS',))

dbpm = DBPM('XF:17BMA-OP{Bpm:1-Ax:', name='dbpm')

class SydorPBG(Device):
    temp_w = Cpt(EpicsSignalRO, 'ThermocoupleW')
    temp_x = Cpt(EpicsSignalRO, 'ThermocoupleX')
    temp_y = Cpt(EpicsSignalRO, 'ThermocoupleY')
    temp_z = Cpt(EpicsSignalRO, 'ThermocoupleZ')
    amp = Cpt(EpicsSignal, 'Amplitude', kind='config')
    mode = Cpt(EpicsSignal, 'Mode', kind='config')
    polarity = Cpt(EpicsSignal, 'Polarity', kind='config')

sydor_pbg = SydorPBG('XF:17BM-ES{PBG:1}', name='sydor_pbg')
