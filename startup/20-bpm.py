cha = EpicsSignalRO('XF:17BM-BI{EM:BPM0}Ampl:ACurrAvg-I', name='cha')
chb = EpicsSignalRO('XF:17BM-BI{EM:BPM0}Ampl:BCurrAvg-I', name='chb')
chc = EpicsSignalRO('XF:17BM-BI{EM:BPM0}Ampl:CCurrAvg-I', name='chc')
chd = EpicsSignalRO('XF:17BM-BI{EM:BPM0}Ampl:DCurrAvg-I', name='chd')

bpm_x = EpicsMotor('XF:17BMA-OP{Bpm:1-Ax:X}Mtr', name='bpm_x')
bpm_y = EpicsMotor('XF:17BMA-OP{Bpm:1-Ax:Y}Mtr', name='bpm_y')

