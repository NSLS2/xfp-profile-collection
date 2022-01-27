from collections import ChainMap
import datetime


def invivo_dr_fc(flow_rate, pre_vol, exp_vol, frac_vol, *, md=None):
    '''Run dose-response experiment

    Parameters
    ----------
    flow_rate : float
        Flow rate in mL/min

    pre_vol : float
        volume to collect without exposure in mL

    exp_vol : float
        volume to collect with exposure in mL

    frac_vol : float
        volume to collect per tube in mL
    '''
    flow_rate_ulps = (flow_rate / 60) * 1000

    pre_exp_time = (pre_vol / flow_rate) *60
    exp_time = (exp_vol / flow_rate) *60
    frac_time = (frac_vol / (flow_rate / 60))
    dets = [shutter, sample_pump]
    # set parameters that will remain static during most runs
    r1_last = 60
    r2_last = 60
    #pattern 1 = standard s-pattern; pattern 2 = left to right
    pattern = 1
    # ftype 1 = time, ftype 2 = drops, ftype 3 = external counts
    ftype = 1

    # TODO add monitor on shutter status instead of TaR
    # TODO add monitor for pumps?
    # TODO add monitoring for fraction collector

    if md is None:
        md = {}

    md['flow_rate'] = flow_rate
    md['pre_exp_vol'] = pre_vol
    md['exp_vol'] = exp_vol
    md['frac_vol'] = frac_vol

    @bpp.run_decorator(md=ChainMap(md, {'plan_name': 'invivo_dr'}))
    def inner_plan():
        # prevent pausing
        yield from bps.clear_checkpoint()
        print("== ({}) set for {} mL/m ({:.2f} uL/s)".format(datetime.datetime.now().strftime(_time_fmtstr), flow_rate, flow_rate_ulps))
        yield from bps.abs_set(sample_pump.vel, flow_rate_ulps, wait=True)

        yield from bps.trigger_and_read(dets)

        # set fraction collector parameters
        #yield from bps.mv(fc.r1last, r1_last)
        #yield from bps.mv(fc.r2last, r2_last)
        #yield from bps.mv(fc.pattern, pattern)

        yield from bps.mv(fc.ftime, frac_time)
        yield from bps.sleep(2)
        print("== ({}) each {:.2f} mL fraction will take {:.2f} s".format(datetime.datetime.now().strftime(_time_fmtstr), frac_vol, frac_time))
        #start fraction collector
        # move to where we want to start to save time
        yield from bps.mv(fc.tube, 1001)
        print("== Fraction Collector Started")

        # flow some sample through
        yield from bps.kickoff(sample_pump, wait=True)
        # as soon as the pump reports that it is started, 
        # start the fraction collector
        yield from bps.mv(fc.run, 1)
        print("== ({}) started the pump".format(datetime.datetime.now().strftime(_time_fmtstr)))

        yield from bps.trigger_and_read(dets)

        print("== ({}) flowing pre-exposure sample for {}mL ({:.1f}s)".format(datetime.datetime.now().strftime(_time_fmtstr),
                                                                            pre_vol, pre_exp_time))


        yield from bps.sleep(pre_exp_time)
        print("== ({}) Done flowing pre-exposure sample".format(datetime.datetime.now().strftime(_time_fmtstr)))

        yield from bps.trigger_and_read(dets)

        #open the shutter
        yield from bps.abs_set(shutter, 'Open', wait=True)
        print("== ({}) Shutter open".format(datetime.datetime.now().strftime(_time_fmtstr)))

        yield from bps.trigger_and_read(dets)

        print("== ({}) flowing exposure sample for {}ml ({:.1f}s)".format(datetime.datetime.now().strftime(_time_fmtstr),
                                                                     exp_vol, exp_time))
        # collect some sample with beam
        yield from bps.sleep(exp_time)

        yield from bps.trigger_and_read(dets)

        # close the shutter, stop the fc and stop flowing the sample
        yield from bps.complete(sample_pump, wait=True)
        yield from bps.abs_set(shutter, 'Close', wait=True)
        yield from bps.mv(fc.end, 1)
        

        yield from bps.trigger_and_read(dets)

        print("== ({}) done!".format(datetime.datetime.now().strftime(_time_fmtstr)))


    def clean_up():
        yield from bps.complete(sample_pump, wait=True)
        yield from bps.abs_set(shutter, 'Close', wait=True)
        yield from bps.mv(fc.valve, 0)
        yield from bps.mv(fc.end, 1)
        yield from bps.mv(fc.hm, 1)
        

    yield from bpp.finalize_wrapper(inner_plan(), clean_up())

