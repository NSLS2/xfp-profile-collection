def pump_plan(volume, rate):
    yield from bps.abs_set(pump.volume, volume, group='pump')
    yield from bps.abs_set(pump.infusion_rate, rate, group='pump')
    yield from bps.wait(group='pump')
    yield from bps.sleep(15)

def run_the_pump(pmp, **kwargs):
    yield from bps.configure(pmp, kwargs)
    yield from bps.abs_set(shutter, 'open', wait=True)
    yield from bps.kickoff(pmp, group='pump_started')
    yield from bps.wait(group='pump_started')
    yield from bps.complete(pmp, group='pump_done')
    yield from bps.wait(group='pump_done')
    yield from bps.abs_set(shutter, 'close', wait=True)


def simple_pump(pump):

    @bpp.run_decorator(md={'plan_name': 'simple_pump'})
    def inner_plan():
        yield from bps.clear_checkpoint()
        yield from bps.abs_set(shutter, 'Open', wait=True)

        yield from bps.kickoff(pump, group='pump_started')
        print('waiting for pump to start')

        yield from bps.wait('pump_started')
        print('pump started')
        st = yield from bps.complete(pump, group='pump_done', wait=False)
        print('waiting for pump to finish')

        yield from bps.trigger_and_read([pump])

        while st is not None and not st.done:
            yield from bps.trigger_and_read([pump])
            yield from bps.sleep(.5)

        yield from bps.sleep(.1)
        yield from bps.trigger_and_read([pump])

        yield from bps.wait('pump_done')
        print('pump finished')

        yield from bps.abs_set(shutter, 'Close', wait=True)
        print('closed shutter')

    def clean_up():
        yield from bps.abs_set(shutter, 'Close', wait=True)


    yield from bpp.finalize_wrapper(inner_plan(), clean_up())


def in_vivo(food_pump, sample_pump, fraction_collector, shutter):
    # waiting times in seconds
    pre_flow_time = 5
    exposure_time = 5
    growth_time = 5
    post_growth_exposure_time = 5
    dets = [shutter, sample_pump, fraction_collector]
    # TODO add monitor on shutter status instead of TaR
    # TODO add monitor for pumps?
    # TODO add monitoring for fraction collector
    @bpp.run_decorator(md={'plan_name': 'in_vivo'})
    def inner_plan():
        # prevent pausing
        yield from bps.clear_checkpoint()

        #start the fraction collector spinning
        yield from bps.kickoff(fraction_collector)
        # flow some sample through
        yield from bps.kickoff(sample_pump, wait=True)
        yield from bps.trigger_and_read(dets)

        yield from bps.sleep(pre_flow_time)

        #open the shutter
        yield from bps.abs_set(shutter, 'Open', wait=True)
        yield from bps.trigger_and_read(dets)

        # collect some sample with beam
        yield from bps.sleep(exposure_time)

        # close the shutter and stop flowing the sample
        yield from bps.abs_set(shutter, 'Close', wait=True)
        yield from bps.complete(sample_pump, wait=True)
        yield from bps.complete(fraction_collector, wait=True)

        yield from bps.trigger_and_read(dets)

        # feed the cells
        yield from bps.kickoff(food_pump, wait=True)
        yield from bps.complete(food_pump, wait=True)

        # let them grow
        yield from bps.sleep(growth_time)

        #open the shutter
        yield from bps.abs_set(shutter, 'Open', wait=True)
        #start the fraction collector spinning and flow some sample through
        yield from bps.kickoff(fraction_collector, wait=True)
        yield from bps.kickoff(sample_pump, wait=True)
        yield from bps.trigger_and_read(dets)

        # collect some sample with beam
        yield from bps.sleep(post_growth_exposure_time)

        # close the shutter and stop flowing the sample
        yield from bps.abs_set(shutter, 'Close', wait=True)
        yield from bps.complete(sample_pump, wait=True)
        yield from bps.complete(fraction_collector, wait=True)

        yield from bps.trigger_and_read(dets)

    def clean_up():
        yield from bps.abs_set(shutter, 'Close', wait=True)
        yield from bps.complete(sample_pump, wait=True)
        yield from bps.complete(fraction_collector, wait=True)

    yield from bpp.finalize_wrapper(inner_plan(), clean_up())
