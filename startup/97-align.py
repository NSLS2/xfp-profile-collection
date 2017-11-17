import bluesky.plans as bp
from  bluesky.callbacks.mpl_plotting import plot_peak_stats

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
    
    for j in range(24):
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
