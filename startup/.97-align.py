from bluesky.callbacks.mpl_plotting import plot_peak_stats
from bluesky.callbacks.fitting import PeakStats


def _align(dir_name, mtr,
           start, stop, num_points, *,
           md=None):
    fig = plt.figure('align {}'.format(mtr.name))
    lp = LivePlot('tcm1', mtr.name, ax=fig.gca())
    ps = PeakStats(mtr.name, 'tcm1')
    
    _md = {'purpose': 'table height alignment',
           'plan_name': '_align',
           'dir_name': dir_name}
    _md.update(md or {})
    yield from bps.mv(shutter, 'Open')
    
    r = yield from bpp.subs_wrapper(
            bp.relative_scan([quad, mshlift, msh],
                             mtr,
                             start, stop, num_points,
                             md=_md),
                             [lp, ps])
    yield from bps.mv(shutter, 'Close')
    
    return (r, ps)

def align_msh(h_pos, v_pos, *, md=None):
    print(f'{h_pos}\n{v_pos}')
    return
    for j in range(4):
        if j == 10:
            continue
        _md = {'slot': j}
        _md.update(md or {})

        yield from bps.mv(msh, h_pos[j])
        yield from bps.mv(mshlift, v_pos[j])
        
        uid, ps = yield from _align('horizontal',
                                    msh,
                                    -3, 3, 50,
                                    md=_md)
        if uid is not None:
            print('slot {} h shift by {}'.format(
                j,ps.com-h_pos[j]))
            h_pos[j] = ps.com

        yield from bps.mv(msh, h_pos[j])
        

