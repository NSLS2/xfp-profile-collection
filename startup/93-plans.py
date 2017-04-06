#syringe pump capillary flow experiment

import datetime

def flow(diameter, rate, tgt_vol, *, md=None):

    dets = [shutter, spump]

    if md is None:
        md = {}

    md['diameter'] = diameter
    md['rate'] = rate
    md['tgt_vol'] = tgt_vol

    @bp.run_decorator(md={'plan_name': 'flow'})
    def inner_plan():
        yield from bp.clear_checkpoint()

        # set pump parameters
        yield from bp.abs_set(spump.diameter, diameter, wait=True)
        yield from bp.abs_set(spump.infusion_rate, rate, wait=True)
        yield from bp.abs_set(spump.infusion_volume, tgt_vol, wait=True)

        # open the shutter
        yield from bp.abs_set(shutter, 'Open', wait=True)
        yield from bp.trigger_and_read(dets)

        print('Shutter opened')
 
        # push sample
        print('waiting for pump to start')
        #yield from bp.kickoff(spump, wait=True)
        #for rate test yield from bp.sleep(10)
        yield from bp.kickoff(spump, group='pump_started')
        yield from bp.wait('pump_started')
        print("({}) Exposing {:.2f} mL at {:.2f} mL/min".format(datetime.datetime.now().strftime(_time_fmtstr), tgt_vol, rate))
        print('waiting for pump to finish')
        st = yield from bp.complete(spump, group='pump_done', wait=False)
        #st = yield from bp.complete(spump, wait=True)
        #print('pump finished')
        yield from bp.trigger_and_read(dets)

        while st is not None and not st.done:
            yield from bp.trigger_and_read(dets)
            yield from bp.sleep(.5)

        yield from bp.sleep(.1)
        yield from bp.trigger_and_read(dets)

        yield from bp.wait('pump_done')
        print('pump finished')
        
       # close the shutter
        yield from bp.abs_set(shutter, 'Close', wait=True)
        print('closed shutter')
        yield from bp.trigger_and_read(dets)

    def clean_up():
        yield from bp.abs_set(shutter, 'Close', wait=True)

    yield from bp.finalize_wrapper(inner_plan(), clean_up())

