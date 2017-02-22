#NEEDS WORK - NOT FINISHED!!!!!

import datetime

def tr_pump(mix_flow_rate, mix_vol, mixing_time, exp_flow_rate, exp_vol, *, md=None):
    '''Run time-resolved experiment

    Parameters
    ----------
    mix_flow_rate : float
        flow rate in mL/min for mixing

    mix_vol : float
        volume to push for mixing without exposure in mL

    mixing_time : float
        time in seconds for mixing prior to exposure

    exp_flow_rate : float
        flow rate in mL/min for exposure and collection

    exp_vol : float
        volume to collect with exposure in mL
    ''' 
    
    dets = [shutter, spump]

    if md is None:
        md = {}

    md['mix_flow_rate'] = mix_flow_rate
    md['mix_vol'] = mix_vol
    md['mixing_time'] = mixing_time
    md['exp_flow_rate'] = exp_flow_rate
    md['exp_vol'] = exp_vol

    @bp.run_decorator(md={'plan_name': 'tr_pump'})
    def inner_plan():
        yield from bp.clear_checkpoint()

        # set pump diameter - MUST BE DONE ONCE IN THIS PROGRAM***
        yield from bp.abs_set(spump.diameter, 14.57, wait=True)

        # set pump parameters for mixing push
        yield from bp.abs_set(spump.infusion_rate, mix_flow_rate, wait=True)
        yield from bp.abs_set(spump.infusion_volume, mix_vol, wait=True)
        
        # start the pump for mixing
        yield from bp.kickoff(spump)

        print("== ({}) flowing at {} mL/m".format(datetime.datetime.now().strftime(_time_fmtstr), mix_flow_rate))
        yield from bp.complete(spump, wait=True)
        finish_time = time.time()
        yield from bp.trigger_and_read(dets)
        print("({}) first push complete, mixing for {:.2f} s".format(datetime.datetime.now().strftime(_time_fmtstr), mixing_time))
        
        # set pump parameters for exposure push
        yield from bp.abs_set(spump.infusion_rate, exp_flow_rate, wait=True)
        yield from bp.abs_set(spump.infusion_volume, exp_vol, wait=True)

        # mix
        delay = time.time() - finish_time
        #print('delay': delay)
        yield from bp.sleep(max(0, (mixing_time - (delay))))

        # open the shutter
        yield from bp.abs_set(shutter, 'Open', wait=True)
        yield from bp.trigger_and_read(dets)

        # start the pump for exposure and collection
        yield from bp.kickoff(spump, wait=True)

        print("== ({}) exposing sample at {} mL/m".format(datetime.datetime.now().strftime(_time_fmtstr), exp_flow_rate))
        print('waiting for pump to finish')
        yield from bp.complete(spump, wait=True)
        
        # close the shutter
        yield from bp.abs_set(shutter, 'Close', wait=True)
        print('closed shutter')
        print("== ({}) ***Exposure Complete!***".format(datetime.datetime.now().strftime(_time_fmtstr)))

    def clean_up():
        yield from bp.abs_set(shutter, 'Close', wait=True)

    yield from bp.finalize_wrapper(inner_plan(), clean_up())

