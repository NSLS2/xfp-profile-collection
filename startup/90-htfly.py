#Plans for operation of the HTfly device.

#Define parameters for future alignment routine, for D3 hole
#HTFLY_X_START = 0.50
#HTFLY_Y_START = -2.9

LOAD_HTFLY_POS_X = -285
EXPOSED_HTFLY_POS_X = 285

#Define vertical position of row 3
row3_y_vert = -2.9

def htfly_move_to_load():
    if htfly.x.position != LOAD_HTFLY_POS_X:
        print("Moving to load position")
        yield from bps.mv(htfly.x, LOAD_HTFLY_POS_X)
    else:
        print("Already there!")


def htfly_exp_row(row_num, htfly_vel, hslit_size, al_thickness, *, md=None):
    '''
    Function to expose a single row on the HTFly device, specifying velocity, 
    slit size, and attenuation. Moves device back to load position after exposure.
    Leaves FE shutter and pre-shutter open after run.

    Parameters
    ----------
    row_num: integer
        Row number on HTFly exposure cell. 
        Must be in the range 1 - 6

    htfly_vel: float
        HTFly fast x stage velocity in mm/sec.
        Must be between 1 - 500 mm/sec

    hslit_size: float
        BIFS ADC horizontal slit size in mm.
        Must be > 0.

    al_thickness: integer
        Aluminum attenuator thickness in um.
        Must be an entry in the list [762, 508, 305, 203, 152, 76, 25, 0]

    md: optional user specified metadata
        By default, the plan name, exposure time, row number, stage velocity, 
        slit size, and attenuator are written as metadata for each successful run.
     
    '''

    #Calculate exposure time in milliseconds, rounded to 3 decimal places.
    #Trap velocity = 0 mistakes here.
    if htfly_vel == 0:
        raise ValueError(f"You entered {htfly_vel} mm/s. The stage won't move!")
    else:
        htfly_exp_time = round((hslit_size / htfly_vel) * 1000, 3)
    
    _md = {'plan_name': 'htfly_exp_row',
           'exposure': htfly_exp_time,
           'row_number': row_num,
           'htfly_velocity': htfly_vel,
           'slit_size': hslit_size,
           'attenuator': al_thickness}
    _md.update(md or {})

    def htfly_exp_setup():
        #Set HTFly velocity, trap velocities that are negative or > 500
        if htfly_vel < 0:
            raise ValueError(f"You entered {htfly_vel} mm/s. Enter a velocity greater than 0 mm/sec!")
        if htfly_vel > 500:
            raise ValueError(f"You entered {htfly_vel} mm/s. Enter a velocity less than or equal to 500 mm/sec!")
        else:
            print(f"Setting htfly_x stage velocity to {htfly_vel} mm/sec.")
            yield from bps.mv(htfly.x.velocity, htfly_vel)
        
        #Set ADC slit size, trap exception if a negative number is entered or value > 6 is entered
        if hslit_size <= 0:
            raise ValueError(f"You asked for a {hslit_size} mm slit. Enter a positive horizontal slit size!")
        elif hslit_size > 6:
            raise ValueError(f"You asked for a {hslit_size} mm slit. Enter a horizontal slit size smaller than 6 mm!")
        else:        
            print(f"Moving the ADC horizontal slit size to {hslit_size} mm.")
            yield from bps.mv(adcslits.xgap, hslit_size)
            
        #Move to desired row number, throw exception if row /= 1-6

        htfly_row_vert = [row3_y_vert - 18, row3_y_vert - 9, row3_y_vert, row3_y_vert + 9, row3_y_vert +18, row3_y_vert + 27]

        if (row_num < 1) or (row_num > 6):
            raise ValueError(f"You entered row {row_num}. Row value must be in the range 1 - 6!")
        else:
            print(f"moving to row {row_num} at htfly_y = {htfly_row_vert[row_num-1]}")
            yield from bps.mv(htfly.y, htfly_row_vert[row_num-1])
        
        #if row_num == 1:
        #    print(f"moving to row 1 at htfly_y = {row3_y_vert-18}")
        #    yield from bps.mv(htfly.y, row3_y_vert-18)
        #elif row_num == 2:
        #    print(f"moving to row 2 at htfly_y = {row3_y_vert-9}")
        #    yield from bps.mv(htfly.y, row3_y_vert-9)
        #elif row_num == 3:
        #    print(f"moving to row 3 at htfly_y = {row3_y_vert}")
        #    yield from bps.mv(htfly.y, row3_y_vert)
        #elif row_num == 4:
        #    print(f"moving to row 4 at htfly_y = {row3_y_vert+9}")
        #    yield from bps.mv(htfly.y, row3_y_vert+9)
        #elif row_num == 5:
        #    print(f"moving to row 5 at htfly_y = {row3_y_vert+18}")
        #    yield from bps.mv(htfly.y, row3_y_vert+18)
        #elif row_num == 6:
        #    print(f"moving to row 6 at htfly_y = {row3_y_vert+27}")
        #    yield from bps.mv(htfly.y, row3_y_vert+27)
        #else:
        #    raise ValueError(f"You entered row {row_num}. Row value must be in the range 1 - 6!")
    
        #Check the attenuator thickness is in the filter wheel list dictionary.
        if not any(d['thickness'] == al_thickness for d in filter_wheel.wheel_positions):
            raise ValueError(f"{al_thickness} is not an available attenuator. Choose from: 762, 508, 305, 203, 152, 76, 25, or 0")
        else:
            print(f"Moving filter wheel to {al_thickness} um Al attenuation.")
            yield from bps.mv(filter_wheel.thickness, al_thickness)

        #Check that HTFly is at load position and move it there before opening shutters.
        if htfly.x.position != LOAD_HTFLY_POS_X:
            print("Moving to load position.")
            yield from bps.mv(htfly.x, LOAD_HTFLY_POS_X)
    
        #Check state of pps_shutter and pre_shutter and open if needed and enabled.
        #If the pps_shutter is disabled, exit and inform the user.
        #This nomenclature allows the shutters to remain open after RE completes.
        if EpicsSignalRO(pps_shutter.enabled_status.pvname).get() == 0:
            raise Exception("Can't open photon shutter! Check that the hutch is interlocked and the shutter is enabled.")
    
        if pps_shutter.status.get() == 'Not Open':
            print("The photon shutter was closed and is now being opened.")
            pps_shutter.set('Open')
            yield from bps.sleep(3)   #Allow some wait time for the shutter opening to finish
        
        if pre_shutter.status.get() == 'Not Open':
            print("The pre-shutter was closed and is now being opened.")
            pre_shutter.set('Open')
            yield from bps.sleep(3)   #Allow some wait time for the shutter opening to finish
   
    @bpp.run_decorator(md=_md)
    def inner_htfly_exp():
        
        #Run the setup plan
        yield from htfly_exp_setup()

        #Open sample shutter and do the exposure.
        print("Pre-shutter and PPS shutter are open. Opening the sample shutter.")
  
        yield from bps.mv(diode_shutter, 'open')
        #Comment out Uniblitz actuation.
        #yield from bps.mv(dg, 30)               #set Uniblitz opening time
        #yield from bps.mv(dg.fire, 1)           #fire Uniblitz
    
        print(f"\nExposing row {row_num} at {htfly_vel}mm/sec with a {hslit_size}mm horizontal slit and {al_thickness}um Al attenuation.")
        print(f"This corresponds to an exposure time of {htfly_exp_time} milliseconds.\n")
        yield from bps.mv(htfly.x, EXPOSED_HTFLY_POS_X)
    
        #Cleanup: close shutters, return to load position.
        print("Closing sample shutter and returning to load position")
        yield from bps.mv(diode_shutter, 'close')
        #yield from bps.mv(dg, 0)    #Close Uniblitz shutter after exposure
        yield from bps.sleep(1)
        yield from bps.mv(htfly.x, LOAD_HTFLY_POS_X)
        print("All done, ready for another row!")

    return (yield from inner_htfly_exp())
