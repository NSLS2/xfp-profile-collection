#Capillary destructive testing (pre-shutter only)

import datetime

def timed_shutter_pre(exp_time, *, md=None):
    '''Opens the pre-shutter for a defined exposure time.
    Prerequisites: FE photon shutter and any downstream shutters are open

    Parameter
    ---------
    exp_time: float
        Exposure time in seconds
    '''
    dets = [shutter]

    if md is None:
        md = {}

    md['exp_time'] = exp_time

    @bpp.run_decorator(md={'plan_name': 'timed_shutter_pre'})
    def inner_plan():
        yield from bps.clear_checkpoint()
        
        #check state of FE shutter
        if pps_shutter.status.get() == 'Not Open' and EpicsSignalRO(pps_shutter.enabled_status.pvname).get() == 1:
            raise Exception("The photon shutter is not open. Open it first!")

        # open the shutter
        yield from bps.abs_set(shutter, 'Open', wait=True)
        yield from bps.trigger_and_read(dets)

        print('Pre-shutter opened')
        print("({}) Exposing for {:.2f} s".format(datetime.datetime.now().strftime(_time_fmtstr), exp_time))

       # wait
        yield from bps.sleep(exp_time)

        # close the shutter
        yield from bps.abs_set(shutter, 'Close', wait=True)
        print('closed pre-shutter')
        yield from bps.trigger_and_read(dets)

    def clean_up():
        yield from bps.abs_set(shutter, 'Close', wait=True)


    yield from bpp.finalize_wrapper(inner_plan(), clean_up())

def timed_shutter(exp_time, *, md=None):
    '''Opens the PPS shutter and pre-shutter for a defined exposure time.
    Prerequisites: Any other downstream shutters are open

    Parameter
    ---------
    exp_time: float
        Exposure time in seconds
    '''
    dets = [pps_shutter, shutter]

    if md is None:
        md = {}

    md['exp_time'] = exp_time

    @bpp.run_decorator(md={'plan_name': 'timed_shutter'})
    def inner_plan():
        yield from bps.clear_checkpoint()
        
        # open the PPS and preshutters
        if EpicsSignalRO(pps_shutter.enabled_status.pvname).get() == 0:
            raise Exception("Can't open FE shutter! Check that the hutch is interlocked and the shutter is enabled.")
        
        yield from bps.abs_set(pps_shutter, 'Open', wait=True)
        print('FE shutter opened')
        
        yield from bps.abs_set(shutter, 'Open', wait=True)
        yield from bps.trigger_and_read(dets)

        print('Pre-shutter opened')
        print("({}) Exposing for {:.2f} s".format(datetime.datetime.now().strftime(_time_fmtstr), exp_time))

       # wait
        yield from bps.sleep(exp_time)

        # close the shutters
        yield from bps.abs_set(shutter, 'Close', wait=True)
        print('closed pre-shutter')
        yield from bps.abs_set(pps_shutter, 'Close', wait=True)
        print('closed FE shutter')
        yield from bps.trigger_and_read(dets)

    def clean_up():
        yield from bps.abs_set(shutter, 'Close', wait=True)
        yield from bps.abs_set(pps_shutter, 'Close', wait=True)

    yield from bpp.finalize_wrapper(inner_plan(), clean_up())

#TODO: fix up functions below to capture into databroker.
#Functions to actuate Uniblitz fast shutter

def timed_uniblitz(fire_time):
    '''Opens the Uniblitz shutter for a defined exposure time.
    Prerequisites: FE photon shutter and pre-shutter are open

    Parameter
    ---------
    fire_time: float
        Exposure time in seconds
    '''
    yield from bps.mv(dg, fire_time)        #set Uniblitz opening time
    yield from bps.mv(dg.fire, 1)           #fire Uniblitz
    yield from bps.sleep(fire_time*1.1)     #wait for shutter to finish
    if fire_time <= 1:
        print(f"Fired Uniblitz shutter for {fire_time*1000} millseconds.")
    else:
        print(f"Fired Uniblitz shutter for {fire_time} seconds.")

def timed_uniblitz_pre(fire_time):
    '''Opens the pre-shutter, then Uniblitz shutter for a defined exposure time.
    Prerequisites: FE photon shutter is open

    Parameter
    ---------
    fire_time: float
        Exposure time in seconds
    '''
    yield from bps.mv(shutter, 'Open')      #open pre-shutter
    print("Opened pre-shutter.")
    if fire_time <= 0.5:                    #add a pre-shutter sleep for short exposure times
        yield from bps.sleep(0.5)
    yield from timed_uniblitz(fire_time)    #fire Uniblitz for specified duration
    if fire_time <= 0.5:
        yield from bps.sleep(0.5)
    yield from bps.mv(shutter, 'Close')     #close pre-shutter
    print("Closed pre-shutter.")

def timed_uniblitz_ss(fire_time):
    '''Opens the sample shutter, then Uniblitz shutter for a defined exposure time.
    Prerequisites: FE photon shutter and pre-shutter are open

    Parameter
    ---------
    fire_time: float
        Exposure time in seconds
    '''
    yield from bps.mv(diode_shutter, 'Open')
    print("Opened DIODE sample shutter.")
    if fire_time <= 0.5:                            #sample-shutter sleep for short exposure times   
        yield from bps.sleep(0.5)               
    yield from timed_uniblitz(fire_time)
    if fire_time <= 0.5:
        yield from bps.sleep(0.5)
    yield from bps.mv(diode_shutter, 'Close')
    print("Closed DIODE sample shutter.")

#Functions to actuate sample shutter in BIFS

def timed_sam_shutter(ss_exp_time):
    '''Opens the sample shutter for a defined exposure time.
    Prerequisites: FE photon shutter and pre-shutter are open

    Parameter
    ---------
    ss_exp_time_time: float
        Exposure time in seconds
    '''
    yield from bps.mv(diode_shutter, 'Open')
    print("Opened DIODE sample shutter.")
    yield from bps.sleep(ss_exp_time)
    yield from bps.mv(diode_shutter, 'Close')
    print(f"Closed DIODE sample shutter after a {ss_exp_time} second(s) exposure.")

def timed_sam_shutter_pre(ss_exp_time):
    '''Opens the pre-shutter, then sample shutter for a defined exposure time.
    Prerequisites: FE photon shutter is open

    Parameter
    ---------
    ss_exp_time_time: float
        Exposure time in seconds
    '''
    yield from bps.mv(shutter, 'Open')
    print("Opened pre-shutter.")
    yield from timed_sam_shutter(ss_exp_time)
    yield from bps.mv(shutter, 'Close')
    print("Closed pre-shutter.")
