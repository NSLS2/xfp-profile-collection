#Capillary destructive testing (pre-shutter only)

import datetime

def timed_shutter(exp_time, *, md=None):

    dets = [shutter]

    if md is None:
        md = {}

    md['exp_time'] = exp_time

    @bpp.run_decorator(md={'plan_name': 'timed_shutter'})
    def inner_plan():
        yield from bps.clear_checkpoint()
        
        # open the shutter
        yield from bps.abs_set(shutter, 'Open', wait=True)
        yield from bps.trigger_and_read(dets)

        print('Shutter opened')
        print("({}) Exposing for {:.2f} s".format(datetime.datetime.now().strftime(_time_fmtstr), exp_time))

       # wait
        yield from bps.sleep(exp_time)

        # close the shutter
        yield from bps.abs_set(shutter, 'Close', wait=True)
        print('closed shutter')
        yield from bps.trigger_and_read(dets)

    def clean_up():
        yield from bps.abs_set(shutter, 'Close', wait=True)


    yield from bpp.finalize_wrapper(inner_plan(), clean_up())

#Functions to actuate Uniblitz fast shutter

def timed_uniblitz(fire_time):
    yield from bps.mv(dg, fire_time)      #set Uniblitz opening time
    yield from bps.mv(dg.fire, 1)         #fire Uniblitz
    yield from bps.sleep(fire_time*1.1)   #wait for shutter to finish
    fire_time_str = str(fire_time)
    print("Fired Uniblitz shutter for " + fire_time_str + "seconds")

def timed_uniblitz_pre(fire_time):
    yield from bps.mv(shutter, 'Open')    #open pre-shutter
    print("Opened pre-shutter")
    yield from bps.mv(dg, fire_time)      #set Uniblitz opening time
    yield from bps.mv(dg.fire, 1)         #fire Uniblitz
    yield from bps.sleep(fire_time*1.2)   #wait for shutter to finish
    fire_time_str = str(fire_time)
    print("Fired Uniblitz shutter for " + fire_time_str + "seconds")
    yield from bps.mv(shutter, 'Close')   #close pre-shutter
    print("Closed pre-shutter")


