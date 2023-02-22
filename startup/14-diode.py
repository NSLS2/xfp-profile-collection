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

def clear_diodepdm():
    '''
    Function to clear DIODE PDM arrays and reset next index to 0 and next
    array to 1. The function takes no input.
    '''

    yield from bps.abs_set(diode_pdm.value_index_set, 0)
    yield from bps.abs_set(diode_pdm.array_index_set, 1)
    yield from bps.abs_set(diode_pdm.clear_arrays, 1)
    print("Reset to index 0 of array 1 and cleared all DIODE PDM arrays.")

def set_pos_diodepdm(val_num, array_num):
    '''
    Function to set next index and array positions for DIODE PDM.

    Parameters
    ----------
    val_num: integer
        Next index to write. Must be in the range 0 - 31.

    array_num: integer
        Next array to write. Must be in range 1 - 5.
    '''

    if val_num < 0 or val_num > 31:
        raise ValueError(f"You entered index {val_num}. It needs to be between 0 and 31, inclusive.")
    if array_num < 1 or array_num > 5:
        raise ValueError(f"You entered array {array_num}. It needs to be between 1 and 5, inclusive.")
    yield from bps.abs_set(diode_pdm.value_index_set, val_num)
    yield from bps.abs_set(diode_pdm.array_index_set, array_num)
    print(f"Set next DIODE PDM write to index {val_num} of array {array_num}.")
