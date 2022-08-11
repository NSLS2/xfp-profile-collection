#Plans for operation of the HTfly device.

#Define parameters for future alignment routine, for D3 hole
#HTFLY_X_START = 0.50
#HTFLY_Y_START = -2.9

LOAD_HTFLY_POS_X = -285
EXPOSED_HTFLY_POS_X = 285

#Define vertical positions
row3_y_vert = -2.9

def htfly_exp_row(row_num, htfly_vel, hslit_size):
    '''Function to expose a single row on the HTFly device.
    Prerequisites: FE photon shutter and pre-shutter must be open

    Parameters
    ----------
    row_num: integer
        Row number on HTFly exposure cell, must be in the range 1 - 6

    htfly_vel: float
        HTFly X stage velocity in mm/sec, must be between 1 - 500 mm/sec

    hslit_size: float
        ADC horizontal slit size in mm, must be > 0.
    
    '''

    #Calculate exposure time in milliseconds
    htfly_exp_time = (hslit_size / htfly_vel) * 1000
    
    #Set HTFly velocity.
    if htfly_vel <= 0:
        raise ValueError("Enter a velocity greater than 0 mm/sec!")
    if htfly_vel > 500:
        raise ValueError("Enter a velocity less than or equal to 500 mm/sec!")
    else:
        print("Setting htfly_x stage velocity to " + str(htfly_vel) + " mm/sec.")
        yield from bps.mv(htfly.x.velocity, htfly_vel)
        
    #Set ADC slit size, trap exception if a negative number is entered or value > 6 is entered
    if hslit_size <= 0:
        raise ValueError("Enter a positive horizontal slit size!")
    elif hslit_size > 6:
        raise ValueError("Enter a horizontal slit size smaller than 6 mm!")
    else:        
        print("Moving the ADC horizontal slit size to " + str(hslit_size) + " mm.")
        yield from bps.mv(adcslits.xgap, hslit_size)
            
    #Move to desired row number, throw exception if row /= 1-6
    if row_num == 1:
        print("moving to row1")
        yield from bps.mv(htfly.y, row3_y_vert-18)
    elif row_num == 2:
        print("moving to row 2")
        yield from bps.mv(htfly.y, row3_y_vert-9)
    elif row_num == 3:
        print("moving to row 3")
        yield from bps.mv(htfly.y, row3_y_vert)
    elif row_num == 4:
        print("moving to row 4")
        yield from bps.mv(htfly.y, row3_y_vert+9)
    elif row_num == 5:
        print("moving to row 5")
        yield from bps.mv(htfly.y, row3_y_vert+18)
    elif row_num == 6:
        print("moving to row 6")
        yield from bps.mv(htfly.y, row3_y_vert+27)
    else:
        raise ValueError("Row value must be in the range 1-6!")
        
    if htfly.x.position != LOAD_HTFLY_POS_X:
        print("Moving to load position")
        yield from bps.mv(htfly.x, LOAD_HTFLY_POS_X)

    #For now, add logic to catch shutters being closed and abort run.

    if pps_shutter.status.get() == 'Not Open':
        raise Exception("The photon shutter is not open. Open the photon shutter first.")
        
    if pre_shutter.status.get() == 'Not Open':
        raise Exception("The pre-shutter is not open! Open the pre-shutter first.")

    print("Pre-shutter and PPS shutter are open. Opening the sample shutter.")
  
    yield from bps.mv(diode_shutter, 'open')
    
    #Open Uniblitz shutter silently
    yield from bps.mv(dg, 30)               #set Uniblitz opening time
    yield from bps.mv(dg.fire, 1)           #fire Uniblitz
    
    print("Row " + str(row_num) + " being exposed at " + str(htfly_vel) + " mm/sec and a " + str(hslit_size) + " mm slit size.")
    print("This corresponds to an exposure time of " + str(htfly_exp_time) + " milliseconds.")
    yield from bps.mv(htfly.x, EXPOSED_HTFLY_POS_X)
    
    #Cleanup: close shutters, return to load position.
    print("Closing sample shutter and returning to load position")
    yield from bps.mv(diode_shutter, 'close')
    yield from bps.mv(dg, 0)    #Close Uniblitz shutter after exposure
    yield from bps.sleep(1)
    yield from bps.mv(htfly.x, LOAD_HTFLY_POS_X)
    print("All done, ready for another row!")
