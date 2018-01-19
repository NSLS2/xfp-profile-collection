from bluesky.callbacks.mpl_plotting import plot_peak_stats
from bluesky.callbacks.fitting import PeakStats


HT_X_START = 8.72
HT_Y_START = -89.72
HT_COORDS_FILE = str(PROFILE_STARTUP_PATH / 'ht_coords.csv')


def align_ht(x_start=HT_X_START, y_start=HT_Y_START, md=None):
    """Align high-throughput sample holder.

        x_start : horizontal start position
        y_start : vertical start position
        md : optional metadata information
    """

    yield from bps.mv(ht.x, x_start)
    yield from bps.mv(ht.y, y_start)

    # Find uid and peak stats for horizontal calibration:
    global PS_X, PS_Y, HT_COORDS

    uid, PS_X = yield from _align_ht('horizontal', ht.x,
                                   -3, 3, 61,
                                   md=md)
    '''
    if uid is not None:
        print('slot {} h shift by {}'.format(
                j, ps.com-h_pos[j]))
        h_pos[j] = ps.com
    '''

    # Move hor. position to COM before we scan vertical one:
    yield from bps.mv(ht.x, PS_X.com)
    
    uid, PS_Y = yield from _align_ht('vertical', ht.y,
                                   -3, 3, 61,
                                   md=md)
    '''
    if uid is not None:
        print('slot {} v shift by {}'.format(
             j, ps.com - v_pos[j]))
        v_pos[j] = ps.com
    '''
    HT_COORDS = default_coords(x_start=PS_X.com, y_start=PS_Y.com)
    HT_COORDS.to_csv(HT_COORDS_FILE, float_format='%.2f')


def default_coords(x_start=HT_X_START, y_start=HT_Y_START, 
                   x_init_slot=2, y_init_slot=0,
                   n_cols=8, n_rows=12,
                   x_spacing=9.0, y_spacing=9.0):
    """Default coordinates for the HT sample holder.

        x_start : horizontal start position
        y_start : vertical start position
        x_init_slot : horizontal slot number to align
        y_init_slot : vertical slot number to align
        n_cols : number of columns
        n_rows : number of rows
        x_spacing : distance between slots in horizontal direction
        y_spacing : distance between slots in vertical direction

    """
    ht_coords = []
    for i in range(n_rows):
        ht_coords.append([])
        for j in range(n_cols):
            ht_coords[-1].append([
                x_start + (j - x_init_slot) * x_spacing,
                y_start + (i - y_init_slot) * y_spacing,
            ])
    ht_coords = np.array(ht_coords)
    ht_coords = np.reshape(ht_coords, (n_cols*n_rows, 2))
    return pd.DataFrame(ht_coords, columns=['x', 'y'])


def _align_ht(dir_name, mtr,
              start, stop, num_points, *,
              md=None):
    fig = plt.figure('align {}'.format(mtr.name))
    lp = LivePlot('tcm1_val', mtr.name, ax=fig.gca())
    ps = PeakStats(mtr.name, 'tcm1_val')
    
    _md = {'purpose': 'table alignment',
           'plan_name': '_align_ht',
           'dir_name': dir_name,
           'ps': {k: v for k, v in ps.__dict__.items() if not k.startswith('_')}}
    _md.update(md or {})
    yield from bps.mv(shutter, 'Open')
    
    r = yield from bpp.subs_wrapper(
            bp.relative_scan([tcm1, ht.y, ht.x],
                             mtr,
                             start, stop, num_points,
                             md=_md),
                             [lp, ps])
    print({k: v for k, v in ps.__dict__.items() if not k.startswith('_')})
    yield from bps.mv(shutter, 'Close')
    return (r, ps)

