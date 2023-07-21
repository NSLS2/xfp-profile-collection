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

    pinhole_dict = {"2mm": [-1, -13],
                    "1.5mm": [-1, -3],
                    "1mm": [-1, 7],
                    "100um": [11, -3]}   
    
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
