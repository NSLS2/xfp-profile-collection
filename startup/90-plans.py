from collections import ChainMap
import datetime


def invivo_dr(flow_rate, pre_vol, exp_vol, *, md=None):
    '''Run dose-response experiment

    Parameters
    ----------
    flow_rate : float
        Flow rate in mL/min

    pre_vol : float
        volume to collect without exposure in mL

    exp_vol : float
        volume to collect with exposure in mL
    '''
    flow_rate_ulps = (flow_rate / 60) * 1000

    pre_exp_time = (pre_vol / flow_rate) *60
    exp_time = (exp_vol / flow_rate) *60
    dets = [shutter, sample_pump]
    # TODO add monitor on shutter status instead of TaR
    # TODO add monitor for pumps?
    # TODO add monitoring for fraction collector

    if md is None:
        md = {}

    md['flow_rate'] = flow_rate
    md['pre_exp_vol'] = pre_vol
    md['exp_vol'] = exp_vol

    @bp.run_decorator(md=ChainMap(md, {'plan_name': 'invivo_dr'}))
  # @bp.run_decorator(md={'plan_name': 'invivo_dr'})
    def inner_plan():
        # prevent pausing
        yield from bp.clear_checkpoint()
        print("== ({}) flowing at {} mL/m ({:.2f} uL/s)".format(datetime.datetime.now().strftime(_time_fmtstr), flow_rate, flow_rate_ulps))
        yield from bp.abs_set(sample_pump.vel, flow_rate_ulps, wait=True)

        yield from bps.trigger_and_read(dets)

        # flow some sample through
        yield from bp.kickoff(sample_pump, wait=True)
        print("== ({}) started the flow pump".format(datetime.datetime.now().strftime(_time_fmtstr)))

        yield from bps.trigger_and_read(dets)

        print("== ({}) flowing pre-exposure sample for {}mL ({:.1f}s)".format(datetime.datetime.now().strftime(_time_fmtstr),
                                                                            pre_vol, pre_exp_time))
        yield from bp.sleep(pre_exp_time)
        print("== ({}) Done flowing pre-exposure sample".format(datetime.datetime.now().strftime(_time_fmtstr)))

        yield from bps.trigger_and_read(dets)

        #open the shutter
        yield from bp.abs_set(shutter, 'Open', wait=True)
        print("== ({}) Shutter open".format(datetime.datetime.now().strftime(_time_fmtstr)))

        yield from bps.trigger_and_read(dets)

        print("== ({}) flowing exposure sample for {}ml ({:.1f}s)".format(datetime.datetime.now().strftime(_time_fmtstr),
                                                                     exp_vol, exp_time))
        # collect some sample with beam
        yield from bp.sleep(exp_time)

        yield from bps.trigger_and_read(dets)

        # close the shutter and stop flowing the sample
        yield from bp.complete(sample_pump, wait=True)
        yield from bp.abs_set(shutter, 'Close', wait=True)
        

        yield from bps.trigger_and_read(dets)

        print("== ({}) done!".format(datetime.datetime.now().strftime(_time_fmtstr)))


    def clean_up():
        yield from bp.complete(sample_pump, wait=True)
        yield from bp.abs_set(shutter, 'Close', wait=True)
        

    yield from bp.finalize_wrapper(inner_plan(), clean_up())
