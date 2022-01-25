#Define a class for SydorBPM Channel names specific to this device from NSLS2_EM
class SydorBPM(Device):
    chan_a = Cpt(EpicsSignalRO, 'Current1:MeanValue_RBV')
    chan_b = Cpt(EpicsSignalRO, 'Current2:MeanValue_RBV')
    chan_c = Cpt(EpicsSignalRO, 'Current3:MeanValue_RBV')
    chan_d = Cpt(EpicsSignalRO, 'Current4:MeanValue_RBV')
    pos_X = Cpt(EpicsSignalRO, 'PosX:MeanValue_RBV')
    pos_Y = Cpt(EpicsSignalRO, 'PosY:MeanValue_RBV')
    sum_curr = Cpt(EpicsSignalRO, 'SumAll:MeanValue_RBV')

sydor_bpm = SydorBPM('XF:17BM-BI{EM:BPM1}', name='sydor_bpm')

#sydor_cha = EpicsSignalRO('XF:17BM-BI{EM:BPM1}Current1:MeanValue_RBV', name='sydor_cha')
#sydor_chb = EpicsSignalRO('XF:17BM-BI{EM:BPM1}Current2:MeanValue_RBV', name='sydor_chb')
#sydor_chc = EpicsSignalRO('XF:17BM-BI{EM:BPM1}Current3:MeanValue_RBV', name='sydor_chc')
#sydor_chd = EpicsSignalRO('XF:17BM-BI{EM:BPM1}Current4:MeanValue_RBV', name='sydor_chd')

#def motor motions as a class
class BPM(Device):
    x = Cpt(EpicsMotor, 'X}Mtr')
    y = Cpt(EpicsMotor, 'Y}Mtr')

bpm1 = BPM('XF:17BMA-OP{Bpm:1-Ax:', name='bpm1')

class SydorPBG(Device):
    temp_w = Cpt(EpicsSignalRO, 'ThermocoupleW')
    temp_x = Cpt(EpicsSignalRO, 'ThermocoupleX')
    temp_y = Cpt(EpicsSignalRO, 'ThermocoupleY')
    temp_z = Cpt(EpicsSignalRO, 'ThermocoupleZ')
    amp = Cpt(EpicsSignal, 'Amplitude', kind='config')
    mode = Cpt(EpicsSignal, 'Mode', kind='config')
    polarity = Cpt(EpicsSignal, 'Polarity', kind='config')

sydor_pbg = SydorPBG('XF:17BM-ES{PBG:1}', name='sydor_pbg')

