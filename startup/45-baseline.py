#Capture a baseline of the beamline state before/after each run event.
#Scope comprises the FE components, PDS, ES:1, and ES:2
#Currently excludes ES:3

sd.baseline =[
    beam_ring_current,
    fe_wb_slits,
    xfp_fe_mirror,
    pbslits, dbpm, pipe,
    cf, 
    tbl1,
    filter_wheel,
    adcslits,
    ht,
    htfly,
    tcm1    
]
