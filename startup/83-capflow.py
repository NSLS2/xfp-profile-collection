#syringe pump capillary flow experiment

import datetime

def flow(diameter, rate, tgt_vol, *, md=None):
    '''Run syringe-pump capillary flow experiment

    Parameters
    ----------
    diameter : float
        syringe diameter in mm

    rate : float
        rate of flow in mL / min

    tgt_vol : float
        volume to collect with exposure in mL
    '''
    dets = [shutter, spump]

    if md is None:
        md = {}

    md['diameter'] = diameter
    md['rate'] = rate
    md['tgt_vol'] = tgt_vol

    @bpp.run_decorator(md={'plan_name': 'flow'})
    def inner_plan():
        yield from bps.clear_checkpoint()

        # set pump parameters
        yield from bps.abs_set(spump.diameter, diameter, wait=True)
        yield from bps.abs_set(spump.infusion_rate, rate, wait=True)
        yield from bps.abs_set(spump.infusion_volume, tgt_vol, wait=True)

        # open the shutter
        yield from bps.abs_set(shutter, 'Open', wait=True)
        yield from bps.trigger_and_read(dets)

        print('Shutter opened')
 
        # push sample
        print('waiting for pump to start')
        #yield from bps.kickoff(spump, wait=True)
        #for rate test yield from bps.sleep(10)
        yield from bps.kickoff(spump, group='pump_started')
        yield from bps.wait('pump_started')
        print("({}) Exposing {:.2f} mL at {:.2f} mL/min".format(datetime.datetime.now().strftime(_time_fmtstr), tgt_vol, rate))
        print('waiting for pump to finish')
        st = yield from bps.complete(spump, group='pump_done', wait=False)
        #st = yield from bps.complete(spump, wait=True)
        #print('pump finished')
        yield from bps.trigger_and_read(dets)

        while st is not None and not st.done:
            yield from bps.trigger_and_read(dets)
            yield from bps.sleep(.5)

        yield from bps.sleep(.1)
        yield from bps.trigger_and_read(dets)

        yield from bps.wait('pump_done')
        print('pump finished')
        
       # close the shutter
        yield from bps.abs_set(shutter, 'Close', wait=True)
        print('closed shutter')
        yield from bps.trigger_and_read(dets)

    def clean_up():
        yield from bps.abs_set(shutter, 'Close', wait=True)

    yield from bpp.finalize_wrapper(inner_plan(), clean_up())

