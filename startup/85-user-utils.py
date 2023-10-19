#Various useful funcs for non-std users

#read in from yaml file (def'd in 01-utils.py)
PINHOLE_DICT = mtr_pos_config.get('pinhole_dict', {})
ATTEN_DICT = mtr_pos_config.get('attenuator_positions', {})

def choose_pinhole(pinhole, *, md=None):
    '''
    Function to select pinhole using cvd_x/y stages.
    Currently 100um, 1mm, 1.5mm, and 2mm pinholes are available.
    Stage positions are listed in position_lookup.yaml.

    Parameters
    ----------
    pinhole: string
        Pinhole to use.
        Must be one of '100um', '1mm', '1.5mm' or '2mm'
    
    md: optional user specified metadata
        By default, the pinhole size is written as metadata for each successful run.
    
    '''
 
    _md = {'plan_name': 'choose_pinhole',
           'pinhole_size': pinhole}
    _md.update(md or {})

    @bpp.run_decorator(md=_md)
    def inner_plan():
        if pinhole in PINHOLE_DICT:
            pinhole_x = PINHOLE_DICT[pinhole][0]
            pinhole_y = PINHOLE_DICT[pinhole][1]
        
            cvd_x_pos_orig = round(cvd.x.user_readback.value, 3)
            cvd_y_pos_orig = round(cvd.y.user_readback.value, 3)
        
            print(f"Currently at cvd_x = {cvd_x_pos_orig} and cvd_y = {cvd_y_pos_orig}.")
            print(f"Moving to cvd_x = {pinhole_x} and cvd_y = {pinhole_y}.")
            yield from bps.mv(cvd.y, pinhole_y, cvd.x, pinhole_x)

            cvd_x_pos_new = round(cvd.x.user_readback.value, 3)
            cvd_y_pos_new = round(cvd.y.user_readback.value, 3)
        
            print(f"Now at cvd_x = {cvd_x_pos_new} and cvd_y = {cvd_y_pos_new} for the {pinhole} pinhole.")
        
        else:
            pinhole_keys = ", ".join(PINHOLE_DICT.keys())
            print(f"You entered {pinhole}. You must choose one of: {pinhole_keys}")
        
    return (yield from inner_plan())

def choose_atten(atten_thick, *, md=None):
    '''
    Function to select attenuator using cfsam_z stage.
    Currently 0 - 9mm Al attenuators (in 1mm steps) are available.
    Stage positions are listed in position_lookup.yaml.

    Parameters
    ----------
    atten_thick: string
        Attenuator to use.
        Must be one of '0mm', '1mm' ... '9mm'
    
    md: optional user specified metadata
        By default, the attenuator thickness is written as metadata.
    
    '''
    
    _md = {'plan_name': 'choose_attenuator',
           'attenuator_thickness': atten_thick}
    _md.update(md or {})

    @bpp.run_decorator(md=_md)
    def inner_plan():
        if atten_thick in ATTEN_DICT:
            atten_x = ATTEN_DICT[atten_thick]
                    
            cfsam_z_pos_orig = round(cfsam.z.user_readback.value, 3)
        
            print(f"Currently at cfsam_z = {cfsam_z_pos_orig}.")
            print(f"Moving to cfsam_z = {atten_x}.")
            yield from bps.mv(cfsam.z, atten_x)

            cfsam_z_pos_new = round(cfsam.z.user_readback.value, 3)
        
            print(f"Now at cfsam_z = {cfsam_z_pos_new} for the {atten_thick} Al attenuator.")
        
        else:
            atten_keys = ", ".join(ATTEN_DICT.keys())
            print(f"You entered {atten_thick}. You must choose one of: {atten_keys}")
        
    return (yield from inner_plan())    
    

