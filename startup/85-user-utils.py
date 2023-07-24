#Various useful funcs for non-std users

def choose_pinhole(pinhole, *, md=None):
    '''
    Function to select pinhole using cvd_x/y stages.
    Currently 100um, 1mm, 1.5mm, and 2mm pinholes are available.
    Stage positions are listed internally in the function.

    Parameters
    ----------
    pinhole: string
        Pinhole to use.
        Must be one of '100um', '1mm', '1.5mm' or '2mm'
    
    md: optional user specified metadata
        By default, the pinhole size is written as metadata for each successful run.
    
    '''

    pinhole_dict = {"2mm": [-1.2, -13.2],
                    "1.5mm": [-1.1, -3.4],
                    "1mm": [-1.1, 6.6],
                    "100um": [10.9, -3.6]}   
    
    _md = {'plan_name': 'choose_pinhole',
           'pinhole_size': pinhole}
    _md.update(md or {})

    @bpp.run_decorator(md=_md)
    def inner_plan():
        if pinhole in pinhole_dict:
            pinhole_x = pinhole_dict[pinhole][0]
            pinhole_y = pinhole_dict[pinhole][1]
        
            cvd_x_pos_orig = round(cvd.x.user_readback.value, 3)
            cvd_y_pos_orig = round(cvd.y.user_readback.value, 3)
        
            print(f"Currently at cvd_x = {cvd_x_pos_orig} and cvd_y = {cvd_y_pos_orig}.")
            print(f"Moving to cvd_x = {pinhole_x} and cvd_y = {pinhole_y}.")
            yield from bps.mv(cvd.y, pinhole_y, cvd.x, pinhole_x)

            cvd_x_pos_new = round(cvd.x.user_readback.value, 3)
            cvd_y_pos_new = round(cvd.y.user_readback.value, 3)
        
            print(f"Now at cvd_x = {cvd_x_pos_new} and cvd_y = {cvd_y_pos_new} for the {pinhole} pinhole.")
        
        else:
            pinhole_keys = ", ".join(pinhole_dict.keys())
            print(f"You entered {pinhole}. You must choose one of: {pinhole_keys}")
        
    return (yield from inner_plan())

def choose_atten(atten_thick, *, md=None):
    '''
    Function to select attenuator using cfsam_z stage.
    Currently 0 - 9mm Al attenuators (in 1mm steps) are available.
    Stage positions are listed internally in the function.

    Parameters
    ----------
    atten_thick: string
        Attenuator to use.
        Must be one of '0mm', '1mm' ... '9mm'
    
    md: optional user specified metadata
        By default, the attenuator thickness is written as metadata.
    
    '''

    atten_dict = {"0mm": 90.0,
                  "1mm": 0.0,
                  "2mm": 10.0,
                  "3mm": 20.0,
                  "4mm": 30.0,
                  "5mm": 40.0,
                  "6mm": 50.0,
                  "7mm": 60.0,
                  "8mm": 70.0,
                  "9mm": 80.0}   
    
    _md = {'plan_name': 'choose_attenuator',
           'attenuator_thickness': atten_thick}
    _md.update(md or {})

    @bpp.run_decorator(md=_md)
    def inner_plan():
        if atten_thick in atten_dict:
            atten_x = atten_dict[atten_thick]
                    
            cfsam_z_pos_orig = round(cfsam.z.user_readback.value, 3)
        
            print(f"Currently at cfsam_z = {cfsam_z_pos_orig}.")
            print(f"Moving to cfsam_z = {atten_x}.")
            yield from bps.mv(cfsam.z, atten_x)

            cfsam_z_pos_new = round(cfsam.z.user_readback.value, 3)
        
            print(f"Now at cfsam_z = {cfsam_z_pos_new} for the {atten_thick} Al attenuator.")
        
        else:
            atten_keys = ", ".join(atten_dict.keys())
            print(f"You entered {atten_thick}. You must choose one of: {atten_keys}")
        
    return (yield from inner_plan())    
    

