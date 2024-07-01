#Alignment positions for D3 hole on HTFly
HTFLY_X_START = -6.4
HTFLY_Y_START = -3.2

#Define vertical position of row 3
ROW3_Y_VERT = -3.0

def _htfly_align(mtr):
    '''
    Internal function to align single axis of htfly, producing liveplots and
    returning peak statistics. Takes motor name + axis as input and assumes
    use of qem1 channel3 as the alignment detector. Not called by users.
    '''
    
    peaks = PeakStats(mtr.name, qem1.current3.mean_value.name)
    lp = LivePlot(qem1.current3.mean_value.name, mtr.name)
    uid = yield from bpp.subs_wrapper(bp.rel_scan([qem1], mtr, -4, 4, 41), [lp, peaks])
    print(f'Found center for {mtr.name} at COM = {round(peaks.com, 3)} mm, FWHM = {round(peaks.fwhm, 3)} mm.')
    
    if uid is not None:
        if peaks['com'] is not None:
            yield from bps.mv(mtr, peaks.com)
            print(f'Moved {mtr.name} to {round(peaks.com, 3)}.')
        else:
            print("Returned None")
    return(peaks)

def htfly_align():
    '''
    Alignment of htfly in both x and y axes. No variable input.
    Assumes both pre-shutter and Uniblitz shutter are open.
    Updates the ROW3_Y_VERT value if alignment succeeds.
    If alignment is not run, uses ROW3_Y_VERT value set in startup.
    '''
    
    global ROW3_Y_VERT

    yield from bps.mv(htfly.y, HTFLY_Y_START, htfly.x, HTFLY_X_START)
    start_htflyx_vel = htfly.x.velocity.get()
    yield from bps.mv(htfly.x.velocity, 5)  #Slow x velocity for alignment purposes

    if EpicsSignalRO(pps_shutter.enabled_status.pvname).get() == 0:
        raise Exception("Can't open photon shutter! Check that the hutch is interlocked and the shutter is enabled.")
        
    if pps_shutter.status.get() == 'Not Open':
        print("The photon shutter was closed and is now being opened.")
        pps_shutter.set('Open')
        yield from bps.sleep(3)   #Allow some wait time for the shutter opening to finish
    
    yield from bps.mv(diode_shutter, 'Open')

    peaks_y = yield from _htfly_align(htfly.y)
    ROW3_Y_VERT = round(peaks_y.com, 3)
    yield from _htfly_align(htfly.x)

    yield from bps.mv(diode_shutter, 'Close')
    pps_shutter.set('Close')
    yield from bps.sleep(3)
    yield from bps.mv(htfly.x.velocity, start_htflyx_vel)
    yield from htfly_move_to_load()



