cha = EpicsSignalRO('XF:17BM-BI{EM:BPM1}Current1:MeanValue_RBV', name='cha')
chb = EpicsSignalRO('XF:17BM-BI{EM:BPM1}Current2:MeanValue_RBV', name='chb')
chc = EpicsSignalRO('XF:17BM-BI{EM:BPM1}Current3:MeanValue_RBV', name='chc')
chd = EpicsSignalRO('XF:17BM-BI{EM:BPM1}Current4:MeanValue_RBV', name='chd')

bpm_x = EpicsMotor('XF:17BMA-OP{Bpm:1-Ax:X}Mtr', name='bpm_x')
bpm_y = EpicsMotor('XF:17BMA-OP{Bpm:1-Ax:Y}Mtr', name='bpm_y')

