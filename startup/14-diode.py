'''Purpose: define ophyd objects for DIODE features.
Currently limited to the PDM.
The sample shutter is defined in 11-shutters.py
'''

class DIODE_PDM(Device):
    array1 = Cpt(EpicsSignalRO, 'ValuesArray:1-Wf')
    array2 = Cpt(EpicsSignalRO, 'ValuesArray:2-Wf')
    array3 = Cpt(EpicsSignalRO, 'ValuesArray:3-Wf')
    array4 = Cpt(EpicsSignalRO, 'ValuesArray:4-Wf')
    array5 = Cpt(EpicsSignalRO, 'ValuesArray:5-Wf')
    value_index_curr = Cpt(EpicsSignalRO, 'ValuesArray:NextIndex-I')
    value_index_last = Cpt(EpicsSignalRO, 'ValuesArray:LastIndex-I')
    array_index_curr = Cpt(EpicsSignalRO, 'StorageArray:NextIndex-I')
    array_index_last = Cpt(EpicsSignalRO, 'StorageArray:LastIndex-I')
    value_index_set = Cpt(EpicsSignal, 'ValuesArray:NextIndex-Sel', kind='config')
    array_index_set = Cpt(EpicsSignal, 'StorageArray:NextIndex-Sel', kind='config')
    clear_arrays = Cpt(EpicsSignal, 'StorageArray:Reset-Cmd')

diode_pdm = DIODE_PDM('XF:17BMA-CT{DIODE-PDM:1}', name='diode_pdm')