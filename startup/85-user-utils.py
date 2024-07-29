#Various useful funcs for non-std users

#read-in yaml file motor positions
MTR_POS_CONFIG_FILE_PATH = str(PROFILE_STARTUP_PATH / 'yaml-files/position_lookup.yaml')
mtr_pos_config = load_yamlfile_config(MTR_POS_CONFIG_FILE_PATH)

#read in specific dicts from yaml file
PINHOLE_DICT = mtr_pos_config.get('pinhole_dict', {})
ATTEN_DICT = mtr_pos_config.get('attenuator_positions', {})
MICRO_PINHOLE_DICT = mtr_pos_config.get('micropinhole_dict', {})

def choose_pinhole(pinhole, *, md=None):
    '''
    Function to select pinhole using cvd_x/y stages.
    Currently 150um, 300um, 500um, 1mm, 1.5mm, and 2mm pinholes are available.
    Stage positions are listed in position_lookup.yaml.

    Parameters
    ----------
    pinhole: string
        Pinhole to use.
        Must be one of '150um', '300um', '500um', '1mm', '1.5mm' or '2mm'
    
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
    
def position_micro_pinhole(position, *, md=None):
    '''
    Function to position micro-pinhole mounted on mod34_x/y stages.
    Choose from in or out as positions
    Stage positions are listed in position_lookup.yaml.

    Parameters
    ----------
    position: string
        Position of micropinhole.
        Must be either 'in' or 'out'
    
    md: optional user specified metadata
        By default, the pinhole size is written as metadata for each successful run.
    
    '''
 
    _md = {'plan_name': 'position_micro_pinhole',
           'micro_pinhole_pos': position}
    _md.update(md or {})

    @bpp.run_decorator(md=_md)
    def inner_plan():
        if position in MICRO_PINHOLE_DICT:
            pinhole_x = MICRO_PINHOLE_DICT[position][0]
            pinhole_y = MICRO_PINHOLE_DICT[position][1]
        
            mod34_x_pos_orig = round(mod34.x.user_readback.value, 3)
            mod34_y_pos_orig = round(mod34.y.user_readback.value, 3)
        
            print(f"Currently at mod34_x = {mod34_x_pos_orig} and mod34_y = {mod34_y_pos_orig}.")
            if position == 'in':
                print(f"Moving micro-pinhole in, to mod34_x = {pinhole_x} and mod34_y = {pinhole_y}.")
                yield from bps.mv(mod34.y, pinhole_y, mod34.x, pinhole_x)
                mod34_x_pos_new = round(mod34.x.user_readback.value, 3)
                mod34_y_pos_new = round(mod34.y.user_readback.value, 3)
                print(f"Inserted micro-pinhole. Now at mod34_x = {mod34_x_pos_new} and mod34_y = {mod34_y_pos_new}.")

            if position == 'out':
                print(f"Moving micro-pinhole out, to mod34_x = {pinhole_x} and mod34_y = {pinhole_y}.")
                yield from bps.mv(mod34.y, pinhole_y, mod34.x, pinhole_x)
                mod34_x_pos_new = round(mod34.x.user_readback.value, 3)
                mod34_y_pos_new = round(mod34.y.user_readback.value, 3)
                print(f"Removed micro-pinhole. Now at mod34_x = {mod34_x_pos_new} and mod34_y = {mod34_y_pos_new}.")
       
        else:
            pinhole_keys = ", ".join(MICRO_PINHOLE_DICT.keys())
            print(f"You entered {position}. You must choose one of: {pinhole_keys}")
        
    return (yield from inner_plan())
