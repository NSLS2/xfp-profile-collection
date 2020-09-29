#Channel names specific to this device from NSLS2_EM
sydor_cha = EpicsSignalRO('XF:17BM-BI{EM:BPM1}Current1:MeanValue_RBV', name='sydor_cha')
sydor_chb = EpicsSignalRO('XF:17BM-BI{EM:BPM1}Current2:MeanValue_RBV', name='sydor_chb')
sydor_chc = EpicsSignalRO('XF:17BM-BI{EM:BPM1}Current3:MeanValue_RBV', name='sydor_chc')
sydor_chd = EpicsSignalRO('XF:17BM-BI{EM:BPM1}Current4:MeanValue_RBV', name='sydor_chd')

#def motor motions as a class
class BPM(Device):
    x = Cpt(EpicsMotor, 'X}Mtr')
    y = Cpt(EpicsMotor, 'Y}Mtr')

bpm1 = BPM('XF:17BMA-OP{Bpm:1-Ax:', name='bpm1')
