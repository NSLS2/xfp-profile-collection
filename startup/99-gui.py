from matplotlib.backends.qt_compat import QtWidgets
import bluesky.plans as bp
import pandas as pd

class ColumnWidget:
    def __init__(self, j):
        self._position = j
        cb = self.cb = QtWidgets.QGroupBox('Position {}'.format(j))
        cb.setCheckable(True)
        sb = self.sb = QtWidgets.QDoubleSpinBox()
        sb.setValue(10)
        sb.setMinimum(10)
        sb.setMaximum(20000)
        le = self.le = QtWidgets.QLineEdit('sample {}'.format(j))
        notes = self.notes = QtWidgets.QTextEdit(''.format(j))
        cb.toggled.connect(sb.setEnabled)
        cb.toggled.connect(le.setEnabled)
        cb.setChecked(True)

        f_layout = QtWidgets.QFormLayout()
        f_layout.addRow('name', le)
        f_layout.addRow('exposure[ms]', sb)
        f_layout.addRow('notes', notes)
              
        cb.setLayout(f_layout)

    @property
    def enabled(self):
        return self.cb.isChecked()

    @property
    def md(self):
        return {'name': self.le.displayText(),
                'notes': self.notes.toPlainText()}

    @property
    def position(self):
        return self._position

    @property
    def exposure(self):
        return self.sb.value()

class XFPSampleSelector:
    def __init__(self, h_pos, v_pos):
        self.window = window = QtWidgets.QMainWindow()
        window.setWindowTitle('XFP Mult-Sample Holder Samples')
        mw = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()

        self.controls = []
        
        for j in range(24):
            if j == 10:
                continue
            r, c = np.unravel_index(j, (4, 6))
            cw = ColumnWidget(j)
            layout.addWidget(cw.cb, r, c)
            self.controls.append(cw)

        mw.setLayout(layout)
        window.setCentralWidget(mw)

        self.h_pos = h_pos
        self.v_pos = v_pos

    def walk_values(self):
        return [{'exposure': d.exposure,
                 'position': d.position,
                 **d.md} for d in self.controls
                if d.enabled]

    def show(self):
        return self.window.show()

    def uncheck(self):
        MSHgui.controls
        for column in MSHgui.controls:                                          
            column.cb.setChecked(False)
        for column in MSHgui.controls:
            column.cb.setChecked(False)

    def plan(self, file_name=None):
        uid_list = []
        for d in self.walk_values():
            yield from bp.abs_set(msh,
                                  self.h_pos[d['position']],
                                  group='msh')
            yield from bp.abs_set(mshlift,
                                  self.v_pos[d['position']],
                                  group='msh')
            # awlays want to wait at least 3 seconds
            yield from bp.sleep(3)	    
            yield from bp.wait('msh')
  
            uid = (yield from xfp_plan_fast_shutter(d))
            #uid = (yield from bp.count([msh, mshlift], md=d))
            
            if uid is not None:
                uid_list.append(uid)
                
        if uid_list:
            columns = ('uid', 'name', 'exposure', 'notes')
            tbl = pd.DataFrame([[h.start[c] for c in columns]
                                for h in db[uid_list]], columns=columns)
            self.last_table = tbl
            if file_name is not None:
                tbl.to_csv(file_name, index=False)

        yield from bp.mv(msh, -275)
            
def xfp_plan_fast_shutter(d):
    exp_time = d['exposure']/1000

    yield from bp.mv(dg, exp_time)
    #open the protective shutter
    yield from bp.abs_set(shutter, 'Open', wait=True)
  
    #fire the fast shutter and wait for it to close again

    yield from bp.mv(dg.fire, 1)
    yield from bp.sleep(exp_time*1.1)

    #close the protective shutter
    yield from bp.abs_set(shutter, 'Close', wait=True)
    
    return (yield from bp.count([msh, mshlift, pin_diode], md=d))

v_pos = np.array(
       [-0.04748597, -0.14456723, -0.13177728, -0.11648054, -0.06279284,
       -0.07053911, -0.08911035, -0.10780352, -0.09622153, -0.09031389,
            np.nan, -0.10261846, -0.08914209, -0.0290418 , -0.03097136,
       -0.02468776,  0.12187718,  0.08942056,  0.11222398,  0.13697166,
        0.16229399,  0.16175469,  0.20066004,  0.23661985])

h_pos = np.array(
      [ -2.10322903e+02,  -1.95427769e+02,  -1.80438639e+02,
        -1.65447505e+02,  -1.50475229e+02,  -1.35526951e+02,
        -1.20521777e+02,  -1.05551707e+02,  -9.05237852e+01,
        -7.54414645e+01,  -6.05000000e+01,  -4.52726477e+01,
        -3.02192623e+01,  -1.52115641e+01,  -1.21439727e-01,
         1.49150754e+01,   2.99701310e+01,   4.48912847e+01,
         5.99197880e+01,   7.45000000e+01,   8.95000000e+01,
         1.04500000e+02,   1.19500000e+02,   1.34500000e+02])
  
MSHgui = XFPSampleSelector(h_pos, v_pos)
#MSHgui.show()


#Need to add in an obvious go button to gui
#Good to have a pause/unpause (with shutter closings as fail-safe)
