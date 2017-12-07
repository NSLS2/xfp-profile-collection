import bluesky.plans as bp
from  bluesky.callbacks.scientific import plot_peak_stats

def _align(dir_name, mtr,
           start, stop, num_points, *,
           md=None):
    fig = plt.figure('align {}'.format(mtr.name))
    lp = LivePlot('quad_ch3', mtr.name, ax=fig.gca())
    ps = PeakStats(mtr.name, 'quad_ch3')
    
    _md = {'purpose': 'table height alignment',
           'plan_name': '_align',
           'dir_name': dir_name}
    _md.update(md or {})
    yield from bp.mv(shutter, 'Open')
    
    r = yield from bp.subs_wrapper(
            bp.relative_scan([quad, mshlift, msh],
                             mtr,
                             start, stop, num_points,
                             md=_md),
        [lp, ps])
    yield from bp.mv(shutter, 'Close')
    
    return (r, ps)

def align_msh(h_pos, v_pos, *, md=None):
    print(f'{h_pos}\n{v_pos}')
    return
    for j in range(4):
        if j == 10:
            continue
        _md = {'slot': j}
        _md.update(md or {})

        yield from bp.mv(msh, h_pos[j])
        yield from bp.mv(mshlift, v_pos[j])
        
        uid, ps = yield from _align('horizontal',
                                    msh,
                                    -3, 3, 50,
                                    md=_md)
        if uid is not None:
            print('slot {} h shift by {}'.format(
                j,ps.com-h_pos[j]))
            h_pos[j] = ps.com

        yield from bp.mv(msh, h_pos[j])
        
        uid, ps = yield from _align('vertical',
                                    mshlift,
                                    -3, 3, 50,
                                    md=_md)
        if uid is not None:
            print('slot {} v shift by {}'.format(
                j, ps.com - v_pos[j]))
            v_pos[j] = ps.com


def _align_ht(*args, **kwargs):
    ...

def align_ht(h_start=-2.10100000e+02, v_start=8.6,
             h_init_slot=2, v_init_slot=0,
             n_cols=8, n_rows=12,
             h_spacing=9.0, v_spacing=9.0):
    """Align high-throughput sample holder.

        h_start : horizontal start position
        v_start : vertical start position
        h_init_slot : horizontal slot number to align
        v_init_slot : vertical slot number to align
        n_cols : number of columns
        n_rows : number of rows
        h_spacing : distance between slots in horizontal direction
        v_spacing : distance between slots in vertical direction
    """
    coords = []

    for i in range(n_rows):
        coords.append([])
        for j in range(n_cols):
            coords[-1].append([(j-h_init_slot)*h_spacing, (i-v_init_slot)*v_spacing])

    coords = np.array(coords)

    return coords

    '''
    # Find uid and peak stats for horizontal calibration:
    uid, ps = yield from _align_ht('horizontal',
                                msh,
                                -3, 3, 50,
                                md=_md)

    if uid is not None:
        print('slot {} h shift by {}'.format(
                j, ps.com-h_pos[j]))
        h_pos[j] = ps.com

    # yield from bp.mv(msh, h_pos[j])
    
    uid, ps = yield from _align_('vertical',
                                mshlift,
                                -3, 3, 50,
                                md=_md)
    if uid is not None:
        print('slot {} v shift by {}'.format(
             j, ps.com - v_pos[j]))
        v_pos[j] = ps.com
    '''


















