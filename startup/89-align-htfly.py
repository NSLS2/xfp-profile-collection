#Alignment positions for D3 hole on HTFly
HTFLY_X_START = 1.8
HTFLY_Y_START = -3.2

#Define vertical position of row 3
ROW3_Y_VERT = -3.0

def _htfly_align(fig=None, ax_hor=None, ax_ver=None):
    '''
    Alignment of htfly in both x and y axes. Assumes both pre-shutter and Uniblitz shutter are open.
    Updates the global ROW3_Y_VERT value if alignment succeeds.
    If alignment is not run prior to htfly exposure plans, bluesky uses ROW3_Y_VERT value in startup.
    '''    
    def inner_align(mtr, ax=None):
        peaks = PeakStats(mtr.name, qem1.current3.mean_value.name)
        lp = LivePlot(qem1.current3.mean_value.name, mtr.name, ax=ax)
        uid = yield from bpp.subs_wrapper(bp.rel_scan([qem1], mtr, -4, 4, 41), [lp, peaks])
        print(f'Found {mtr.name} at COM = {round(peaks.com, 3)} mm, FWHM = {round(peaks.fwhm, 3)} mm.')

        ax.set_title(f'COM: {peaks.com:.2f} mm  FWHM: {peaks.fwhm:.2f} mm')
        ax.figure.canvas.draw_idle()

        if uid is not None:
            if peaks['com'] is not None:
                yield from bps.mv(mtr, peaks.com)
                print(f'Moved {mtr.name} to {round(peaks.com, 3)}.')
            else:
                print("Returned None")
        return(peaks)

    global ROW3_Y_VERT
    print("Aligning HTFly apparatus in y, then x.")
    yield from bps.mv(htfly.y, HTFLY_Y_START, htfly.x, HTFLY_X_START)
    start_htflyx_vel = htfly.x.velocity.get()
    yield from bps.mv(htfly.x.velocity, 5)  #Slow x velocity for alignment purposes

    #Ensure ADC slit x_gap is open (>= 6.0mm).
    old_xgap = round(adcslits.xgap.user_readback.get(), 3)
    if old_xgap < 6.0:
        print(f'ADC slit horizontal size is {old_xgap} mm. Opening to 6.0 mm.')
        yield from bps.mv(adcslits.xgap, 6.000)
    else:
        pass

    if EpicsSignalRO(pps_shutter.enabled_status.pvname).get() == 0:
        raise Exception("Can't open photon shutter! Check that the hutch is interlocked and the shutter is enabled.")
        
    if pps_shutter.status.get() == 'Not Open':
        print("The photon shutter was closed and is now being opened.")
        pps_shutter.set('Open')
        yield from bps.sleep(3)   #Allow some wait time for the shutter opening to finish
    
    yield from bps.mv(diode_shutter, 'Open')

    peaks_y = yield from inner_align(htfly.y, ax=ax_ver)
    ROW3_Y_VERT = round(peaks_y.com, 3)
    yield from inner_align(htfly.x, ax=ax_hor)

    yield from bps.mv(diode_shutter, 'Close')
    pps_shutter.set('Close')
    yield from bps.sleep(3)
    yield from bps.mv(htfly.x.velocity, start_htflyx_vel)
    yield from htfly_move_to_load()
    print(f"Completed HTFly alignment, with row 3 center now set to {ROW3_Y_VERT} mm.")

def htfly_align(*, md=None):
    # Copied nearly verbatim from HT alignment routine
    fig = plt.figure('HTFly Vertical and Horizontal Alignment', figsize=(16, 5))
    axes_d = {ax.get_label(): ax for ax in fig.axes}
    if 'horizontal' not in axes_d:
        ax_ver = fig.add_subplot(121, label='horizontal')
        ax_hor = fig.add_subplot(122, label='vertical')
    else:
        ax_ver = axes_d['horizontal']
        ax_hor = axes_d['vertical']
    kwargs = {}
    kwargs['fig'] = fig
    kwargs['ax_hor'] = ax_hor
    kwargs['ax_ver'] = ax_ver
    RE(_htfly_align(**kwargs))
    return([])  #Necessary to avoid a NoneType error

